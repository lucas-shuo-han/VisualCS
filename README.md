# VisualCS

用 3Blue1Brown 风格的动画讲计算机课程。第一个系列：**CS61C · RISC-V**（伯克利 CS61C 中 RISC-V 指令集部分）。

动画用 [Manim Community](https://www.manim.community/) 制作：深色背景、按字段着色的指令编码、一步步执行的寄存器和内存。
每集都有烧录在画面里的中文字幕，另附同步的 `.srt` 字幕文件（可以直接拿来配音或做 TTS）。

## CS61C RISC-V 系列

| 集 | 标题 | 内容 |
|---|---|---|
| 1 | 从 C 到汇编 | ISA 是软硬件的契约；32 个寄存器与 ABI 名字；x0；`add` / `sub` / `addi`；伪指令 `mv` `li` `nop` |
| 2 | 内存 | 字节寻址、字与对齐、小端序；`lw` / `sw` 与 `偏移(基址)`；`A[i]` 的偏移是 `4×i`；`lb` / `lbu` 的符号扩展与零扩展 |
| 3 | 决策与循环 | PC；六条条件分支；if-else 的“条件取反”；`and/or/xor` 与 `sll/srl/sra`；逐步执行一个数组求和循环 |
| 4 | 函数调用与栈 | 调用函数的六个步骤；`jal` / `jr ra`；调用者保存与被调用者保存；栈与压栈出栈；`sumSquare` 的序言与尾声 |
| 5 | 指令格式（上） | 存储程序；R / I / S 型逐位编码（`add`、`addi`、`lw`、`sw`）；为什么 S 型要把立即数拆开 |
| 6 | 指令格式（下） | PC 相对寻址；B 型的“打乱”位序与 `beq` 编码；`lui` + `addi` 的符号扩展陷阱；J 型与 `auipc`+`jalr`；六种格式总览 |
| 7 | CALL | 编译、汇编（伪指令展开、两遍扫描、符号表与重定位表）、链接、加载 |

成片在 [`videos/cs61c-riscv/`](videos/cs61c-riscv/)（1080p30，每集约 3.5–4 分钟），全部旁白文字见 [`cs61c/riscv/SCRIPT.md`](cs61c/riscv/SCRIPT.md)。

## 目录结构

```
cs61c/riscv/common.py      共享组件：带字幕计时的 NarratedScene、代码高亮、寄存器、内存、指令位字段……
cs61c/riscv/epXX_*.py      每集一个 Scene
tools/render.py            渲染全部（或指定）剧集，并把 mp4 + srt 收集到 videos/
tools/contact_sheet.py     按字幕时间点截帧、拼成联系表，用来快速检查排版
tools/srt_to_script.py     从字幕生成旁白脚本 SCRIPT.md
```

## 自己渲染

系统依赖：`ffmpeg`、`libcairo2-dev`、`libpango1.0-dev`、`pkg-config`，以及中文字体 Noto Sans CJK（Ubuntu 上是 `fonts-noto-cjk`）。

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python tools/render.py --manim .venv/bin/manim            # 全部剧集，1080p30
.venv/bin/python tools/render.py --manim .venv/bin/manim --preview 3  # 第 3 集 480p 快速预览
```

## 说明

- 目前没有配音，旁白以字幕形式呈现；字幕停留时长按阅读速度自动计算。
- 内容按 CS61C 中 RISC-V 部分的知识点和 RISC-V 规范整理；各集示例里的机器码都在代码里用断言核对过。
