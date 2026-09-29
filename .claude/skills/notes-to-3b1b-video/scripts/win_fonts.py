"""Install the fonts the videos use (Noto Sans CJK SC, DejaVu Sans Mono) for the
current Windows user, and load them into the running session so Pango sees
them without a re-login.

Usage (once per Windows login, from the venv; setup_env.ps1 runs it):
    python win_fonts.py
"""

import ctypes
import io
import os
import sys
import urllib.request
import winreg
import zipfile

FONT_DIR = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts")
NOTO = "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-{}.otf"
DEJAVU = "https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip"
REG = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"


def fetch():
    os.makedirs(FONT_DIR, exist_ok=True)
    for w in ("Regular", "Bold"):
        dst = os.path.join(FONT_DIR, f"NotoSansCJKsc-{w}.otf")
        if not os.path.exists(dst):
            print("downloading", os.path.basename(dst))
            urllib.request.urlretrieve(NOTO.format(w), dst)
    if not os.path.exists(os.path.join(FONT_DIR, "DejaVuSansMono.ttf")):
        print("downloading DejaVu")
        with zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(DEJAVU).read())) as z:
            for n in z.namelist():
                base = os.path.basename(n)
                if base.startswith("DejaVuSans") and base.endswith(".ttf"):
                    with open(os.path.join(FONT_DIR, base), "wb") as fh:
                        fh.write(z.read(n))


def install():
    gdi = ctypes.windll.gdi32
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG) as key:
        for f in sorted(os.listdir(FONT_DIR)):
            if not f.startswith(("NotoSansCJK", "DejaVuSans")):
                continue
            path = os.path.join(FONT_DIR, f)
            kind = "OpenType" if f.endswith(".otf") else "TrueType"
            winreg.SetValueEx(key, f"{os.path.splitext(f)[0]} ({kind})", 0, winreg.REG_SZ, path)
            gdi.AddFontResourceW(path)
    ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001D, 0, 0, 0x2, 1000, None)


if __name__ == "__main__":
    if sys.platform != "win32":
        sys.exit("Windows only; on Linux/macOS install fonts-noto-cjk and DejaVu via the package manager.")
    fetch()
    install()
    import manimpango

    have = [f for f in manimpango.list_fonts() if f in ("Noto Sans CJK SC", "DejaVu Sans Mono")]
    print("Pango sees:", have)
