"""The episode list: order, titles and output names, in both languages.

Episode numbers, title cards, "next episode" lines and video file names all
come from here, so reordering the series is a one-line change."""

from typing import NamedTuple


class Episode(NamedTuple):
    file: str
    scene: str
    zh_title: str
    zh_sub: str
    en_title: str
    en_sub: str
    zh_slug: str
    en_slug: str


SERIES = [
    Episode("ep01_intro.py", "Ep01Intro",
            "机器结构与 RISC-V", "抽象层次 · 冯·诺依曼结构 · RISC 的故事",
            "Machine Structures & RISC-V", "Abstraction · von Neumann · the RISC story",
            "机器结构与RISC-V", "machine-structures-and-risc-v"),
    Episode("ep02_isa_registers.py", "Ep02ISARegisters",
            "从 C 到汇编", "指令集架构 · 寄存器 · 算术指令",
            "From C to Assembly", "ISA · registers · arithmetic",
            "从C到汇编-ISA与寄存器", "from-c-to-assembly"),
    Episode("ep03_memory.py", "Ep03Memory",
            "内存", "字节寻址 · 小端序 · lw / sw",
            "Memory", "Byte addressing · little-endian · lw / sw",
            "内存-字节寻址与lw-sw", "memory-lw-sw"),
    Episode("ep04_memory_practice.py", "Ep04MemoryPractice",
            "汇编实战：表达式与数组", "无类型的寄存器 · 栈上的数组 · 字节与符号",
            "Assembly in Practice", "Untyped registers · arrays on the stack · bytes & signs",
            "汇编实战-表达式与数组", "assembly-in-practice"),
    Episode("ep05_branches_loops.py", "Ep05BranchesLoops",
            "决策与循环", "PC · 条件分支 · 位运算 · 循环",
            "Decisions & Loops", "PC · branches · bitwise ops · loops",
            "决策与循环", "decisions-and-loops"),
    Episode("ep06_control_patterns.py", "Ep06ControlPatterns",
            "控制流进阶", "取指执行 · 比较指令 · 循环的套路",
            "Control Flow Patterns", "Fetch-execute · set-less-than · loop recipes",
            "控制流进阶", "control-flow-patterns"),
    Episode("ep07_procedures.py", "Ep07Procedures",
            "函数调用", "jal · 调用约定 · 栈",
            "Function Calls", "jal · calling convention · the stack",
            "函数调用与栈", "function-calls"),
    Episode("ep08_recursion.py", "Ep08Recursion",
            "递归与栈帧", "jal / jalr · 阶乘 · 叶子函数",
            "Recursion & Stack Frames", "jal / jalr · factorial · leaf functions",
            "递归与栈帧", "recursion-and-stack-frames"),
    Episode("ep09_formats_ris.py", "Ep09FormatsRIS",
            "指令格式（上）", "存储程序 · R / I / S 型",
            "Instruction Formats, Part 1", "Stored program · R / I / S types",
            "指令格式上-R-I-S", "formats-r-i-s"),
    Episode("ep10_decoding.py", "Ep10Decoding",
            "读懂机器码", "反汇编 · 字段复用 · I 型全家",
            "Reading Machine Code", "Disassembly · shared fields · the I-type family",
            "读懂机器码", "reading-machine-code"),
    Episode("ep11_formats_buj.py", "Ep11FormatsBUJ",
            "指令格式（下）", "PC 相对寻址 · B / U / J 型",
            "Instruction Formats, Part 2", "PC-relative addressing · B / U / J types",
            "指令格式下-B-U-J", "formats-b-u-j"),
    Episode("ep12_addressing.py", "Ep12Addressing",
            "寻址方式与大常数", "远跳转 · li 的展开 · 手工汇编",
            "Addressing & Big Constants", "Far jumps · expanding li · hand assembly",
            "寻址方式与大常数", "addressing-and-big-constants"),
    Episode("ep13_call.py", "Ep13CALL",
            "CALL", "编译 · 汇编 · 链接 · 加载",
            "CALL", "Compile · Assemble · Link · Load",
            "CALL-编译汇编链接加载", "call-compile-assemble-link-load"),
    Episode("ep14_hello_world.py", "Ep14HelloWorld",
            "Hello World 的一生", "目标文件 · 符号表 · 重定位 · 动态链接",
            "The Life of Hello World", "Object files · symbols · relocation · dynamic linking",
            "HelloWorld的一生", "life-of-hello-world"),
]

BY_SCENE = {e.scene: (i + 1, e) for i, e in enumerate(SERIES)}


def number(scene: str) -> int:
    return BY_SCENE[scene][0]


def title(ep: Episode, lang: str) -> str:
    return ep.en_title if lang == "en" else ep.zh_title


def subtitle(ep: Episode, lang: str) -> str:
    return ep.en_sub if lang == "en" else ep.zh_sub


def slug(n: int, lang: str) -> str:
    ep = SERIES[n - 1]
    return f"{n:02d}-" + (ep.en_slug if lang == "en" else ep.zh_slug)
