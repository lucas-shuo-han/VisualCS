"""Pronunciations for an assembly / computer-architecture course (from the
CS61C RISC-V series). Copy next to tts.py as say_as.py and adapt: add the
course's jargon, drop what doesn't apply. Check the result with
`captions.py SRC N --spoken`.
"""

import re


def _reg(m):
    return f"{m[1].upper()} {m[2]}"


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
    # imm[20|10:1|11|19:12], inst[30:25]
    (r"\b(imm|inst)\[([0-9:|]+)\]", {"en": _bits("en"), "zh": _bits("zh")}),
    # 8(sp), -4(sp), 0(x5)
    (r"([−-]?\d+)\((\w+)\)", {"en": _offset("en"), "zh": _offset("zh")}),
    # registers x5, t0, a1, s11
    (r"\b([xatsXATS])(\d{1,2})\b", {"en": _reg, "zh": _reg}),
]

SAY_AS = {
    "addi": "add I", "subi": "sub I", "andi": "and I", "ori": "or I", "xori": "X or I",
    "xor": "X or", "mv": "move", "ret": "return", "nop": "no-op", "ecall": "E call",
    "ebreak": "E break", "printf": "print F", "funct3": "funct 3", "funct7": "funct 7",
    "opcode": "op code", "RISC-V": "risk five", "RISC": "risk", "RV32I": "R V 32 I",
    "CS61C": "CS 61 C",
    # spelled out, "jal ra" sounds like "jalr a"
    "jal": "jump and link", "jalr": "jump and link register",
}

SPELL = """lw sw lb lbu lh lhu sb sh beq bne blt bge bltu bgeu bgt ble sll srl sra
    slli srli srai slt slti sltu sltiu jr lui auipc li la ISA ABI PC pc sp ra fp gp tp
    rd rs rs1 rs2""".split()
