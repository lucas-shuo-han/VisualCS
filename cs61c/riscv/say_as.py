"""Pronunciations for the CS61C RISC-V series (voice-over). Used by tts.py.

Start from the skill's assets/say_as_asm.py; the extras below came from
listening to earlier renders. Check the result with
`python <skill>/scripts/captions.py cs61c/riscv N --spoken`.
"""

import re

try:
    LETTER_A
except NameError:   # run outside tts.py
    LETTER_A = "A"


def _reg(m):
    # LETTER_A is provided by tts.py: "eigh" for Kokoro, which would read a bare "A 1" as "uh one"
    letter = LETTER_A if m[1] in "aA" else m[1].upper()
    return f"{letter} {m[2]}"


def _offset(lang):
    word = {"en": ("plus", "minus"), "zh": ("加", "减")}[lang]

    def f(m):
        n, r = m[1].replace("−", "-"), m[2]
        if len(r) <= 3 and r[-1].isdigit() and r[0] in "xatsXATS":
            r = _reg(re.match(r"(\D+)(\d+)", r))
        return f"{r} {word[n.startswith('-')]} {n.lstrip('-')}"
    return f


def _bits(lang):
    word = {"en": ("immediate bits {b}", "instruction bits {b}", " to ", ", "),
            "zh": ("立即数第 {b} 位", "指令第 {b} 位", "到", "、")}[lang]

    def f(m):
        b = m[2].replace(":", word[2]).replace("|", word[3])
        return (word[0] if m[1] == "imm" else word[1]).format(b=b)
    return f


REWRITES = [
    # a lone backslash-zero (the C string terminator)
    (r"\\0", {"en": " backslash zero", "zh": " 反斜杠零"}),
    # imm[20|10:1|11|19:12], inst[30:25]
    (r"\b(imm|inst)\[([0-9:|]+)\]", {"en": _bits("en"), "zh": _bits("zh")}),
    # 8(sp), -4(sp), 0(x5)
    (r"([−-]?\d+)\((\w+)\)", {"en": _offset("en"), "zh": _offset("zh")}),
    # registers x5, t0, a1, s11
    (r"\b([xatsXATS])(\d{1,2})\b", {"en": _reg, "zh": _reg}),
]

SAY_AS = {
    "addi": "add immediate", "subi": "sub immediate", "andi": "and immediate",
    "ori": "or immediate", "xori": "ex-or immediate",
    "xor": "ex-or", "mv": "move", "ret": "return", "nop": "no-op", "ecall": "E call",
    "ebreak": "E break", "printf": "print F", "funct3": "funct 3", "funct7": "funct 7",
    "opcode": "op code", "RISC-V": "risk five", "RISC": "risk", "ARM": "arm",
    "RV32I": "R V 32 I", "RV32": "R V 32", "CS61C": "C S 61 C", "CS": "C S", "61C": "61 C",
    "ASCII": "ask ee", "F5": "F 5",
    "XOR": "ex or", "AND": "and", "DRAM": "dee ram", "CISC": "sisk", "MIPS": "mips",
    "Neumann": "Noyman", "Cocke": "Coke", "Krste": "Kerstay", "Asanovic": "Ah sah no vich",
    "KiB": {"en": "kibibytes", "zh": "KB"}, "MiB": {"en": "mebibytes", "zh": "MB"},
    # spelled out, "jal ra" sounds like "jalr a"
    "jal": "jump and link", "jalr": "jump and link register",
}

SPELL = """lw sw lb lbu lh lhu lwu sb sh sbu beq bne blt bge bltu bgeu bgt ble sll srl sra
    slli srli srai slt slti sltu sltiu jr lui auipc li la ISA ABI PC pc sp ra fp gp tp
    rd rs rs1 rs2 lt CPU ALU DDR HBM IBM UC""".split()
