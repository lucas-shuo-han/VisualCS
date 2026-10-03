"""English for episode 2 (keys are the Chinese strings in ep02_isa_registers.py).

Narration beats are written in English for the ear, not translated line by line
(see the skill's references/narration-writing.md). Cue phrases in the episode,
L(zh, en), are substrings of these English beats.
"""

EN = {
    # end card
    "ISA 是软件与硬件之间的契约": "The ISA is the contract between software and hardware",
    "RV32I 有 32 个 32 位寄存器，x0 恒为 0":
        "RV32I has thirty-two registers of thirty-two bits each, and x0 is always zero",
    "算术指令：add / sub rd, rs1, rs2":
        "The add and sub instructions take a destination register and two source registers",
    "addi 带 12 位立即数；mv、li、nop 是伪指令":
        "addi takes a twelve-bit immediate, and mv, li, and nop are pseudo-instructions",

    # ---- labels
    "编译器 Compiler": "Compiler",
    "汇编器 Assembler": "Assembler",
    "软件：C、Python、操作系统……": "Software: C, Python, the OS...",
    "指令集架构  ISA": "Instruction Set Architecture (ISA)",
    "硬件：CPU 电路": "Hardware: CPU circuits",
    "RISC = Reduced Instruction Set Computer  精简指令集": "RISC = Reduced Instruction Set Computer",
    "寄存器 Registers": "Registers",
    "32 位 = 4 字节 = 1 个字（word）": "32 bits = 4 bytes = 1 word",
    "寄存器：32 × 4 B = 128 字节": "Registers: 32 × 4 B = 128 bytes",
    "内存：数十亿字节": "Memory: billions of bytes",
    "算术指令": "Arithmetic Instructions",
    "操作名": "opname",
    "目标": "dest",
    "源 1": "src 1",
    "源 2": "src 2",
    "立即数 Immediate": "Immediates",
    "立即数：直接写在指令里的常数": "Immediate: a constant written right into the instruction",
    "立即数只有 12 位：范围 −2048 ~ 2047（原因见第 9 集）":
        "Only 12 bits: −2048 to 2047 (why: see Episode 9)",
    "复制：加 0": "copy: add 0",
    "装入常数：从 x0 加": "load a constant: add it to x0",
    "什么也不做": "do nothing",

    # ---- hook
    "我们写下一行 C 代码：a = b + c; 但 CPU 并不认识 C。它只会执行一串串的 0 和 1。":
        "Here is one line of C. It adds the variables b and c and stores the sum in the "
        "variable a. But a CPU can't run C at all, because all it understands is long "
        "strings of zeros and ones.",
    "中间隔着两步翻译：编译器先把 C 变成汇编语言，汇编器再把每条汇编指令变成一条 32 位的机器指令。"
    "汇编和机器码几乎一一对应：汇编就是机器指令的“文字版”。":
        "Between the two there are two translation steps. First the compiler turns the C "
        "into assembly language, and then the assembler turns each assembly instruction "
        "into one thirty-two bit machine instruction. Because the two match almost one to "
        "one, you can think of assembly as machine code written out as text.",

    # ---- ISA
    "一台 CPU 支持哪些指令、有哪些寄存器，这套规定叫做指令集架构（ISA）。"
    "它是软件和硬件之间的契约：软件只使用这些指令，硬件保证正确执行它们。":
        "Every CPU comes with a rulebook that says which instructions it supports and "
        "which registers it has. That rulebook is called the instruction set architecture, "
        "ISA for short. It works like a contract, because software promises to use only those "
        "instructions, and the hardware promises to carry them out correctly.",
    "x86、ARM、RISC-V 都是 ISA。CS61C 用的是 RISC-V：开源、简洁、规整。"
    "RISC 是“精简指令集”：指令少而规整，硬件就能做得简单、快速。"
    "RV32I 基础指令集只有大约 40 条指令，这个系列会讲到其中的大部分。":
        "x86, ARM and RISC-V are all instruction set architectures, and this course uses "
        "RISC-V because it's open, simple and very regular. The R in RISC stands for "
        "reduced, which means the instructions are few and uniform, so the hardware can be "
        "simple and fast. The base version, called RV32I, has only about forty "
        "instructions, and this series covers most of them.",

    # ---- registers
    "RISC-V 的算术指令只能操作寄存器：CPU 内部极少量、极快的存储单元。"
    "RV32I 一共有 32 个整数寄存器：x0 到 x31。"
    "每个寄存器 32 位宽。32 位，也就是 4 个字节，称为一个“字”。":
        "In RISC-V, arithmetic instructions work only on registers, which are a small "
        "number of very fast storage cells inside the CPU. The base instruction set has "
        "thirty-two integer registers, named x0 through x31. Each one is thirty-two bits "
        "wide, and thirty-two bits, or four bytes, is what we call a word.",
    "为什么只有 32 个？因为越小越快。寄存器在一个时钟周期内就能读写，而访问内存往往要慢上百倍。":
        "So why only thirty-two? Because a smaller register file is faster, and a register "
        "can be read or written within a single clock cycle. Memory holds billions of "
        "bytes, but reaching into it can take a hundred times longer.",
    "其中 x0 很特别：它的值永远是 0。往 x0 里写任何值，都会被悄悄丢弃。"
    "听起来有点浪费？稍后你就会看到它有多好用。":
        "Register x0 is special, because its value is always zero. If you try to write "
        "anything into it, the value is simply thrown away. That might sound wasteful, but "
        "you'll soon see how useful a register that is always zero can be.",
    "在汇编里，我们通常用寄存器的“别名”，也就是 ABI 名字。"
    "t 开头的是临时寄存器（temporary），s 开头的是保存寄存器（saved），"
    "a 开头的用来传递参数（argument）和返回值。":
        "In assembly we usually don't write x0 through x31. Instead we use friendlier "
        "names, called the ABI names. The registers t0 through t6 are temporaries, s0 "
        "through s11 are saved registers, and a0 through a7 hold arguments and return "
        "values.",
    "ra、sp 等有专门用途。这些寄存器的使用规则，第 7 集讲函数调用时再细说。":
        "A few others, like ra and sp, have special jobs. The rules for using them come "
        "with function calls in episode seven.",

    # ---- add / sub
    "算术指令的格式是固定的：操作名、目标寄存器，然后是两个源寄存器。"
    "add rd, rs1, rs2 的意思就是：rd = rs1 + rs2。":
        "Arithmetic instructions all share one fixed format. First comes the name of the "
        "operation, then the destination register, and then two source registers. So an "
        "add simply puts the sum of the two source registers into the destination "
        "register.",
    "举个例子：s1 里是 7，s2 里是 5。执行 add s0, s1, s2：两个值被送进加法器，得到 12，写回 s0。":
        "Here's an example. Say s1 holds seven and s2 holds five. When we run add s0, s1, "
        "s2, both values flow into the adder, and out comes twelve, which is written back "
        "into s0.",
    "sub 也一样：rd = rs1 − rs2。注意顺序，被减数是 rs1，减数是 rs2。":
        "Subtraction works the same way, but now the order matters. The first source "
        "register is the number we subtract from, and the second is the number being "
        "subtracted, so seven minus five leaves two.",

    # ---- a = b + c - d
    "来编译一个稍复杂的表达式：a = b + c - d。"
    "假设编译器已经把 a、b、c、d 分别放在 s0、s1、s2、s3 中。":
        "Let's compile a slightly bigger expression, one that adds b and c and then "
        "subtracts d. We'll assume the compiler has already put the variables a, b, c and "
        "d into registers s0, s1, s2 and s3.",
    "每条指令只能做一次运算，所以要拆成两步，中间结果放在临时寄存器 t0。":
        "Each instruction can do only one operation, so we split this into two steps, and "
        "keep the middle result in the temporary register t0.",
    "设 b = 10，c = 20，d = 5。第一步：t0 = 10 + 20 = 30。"
    "第二步：s0 = t0 − d = 30 − 5 = 25。完成！":
        "Let's say b is ten, c is twenty and d is five. The first instruction adds b and "
        "c, so t0 becomes thirty. The second one subtracts d from t0, which leaves "
        "twenty-five in s0, and we're done.",

    # ---- immediates
    "如果要加的是一个常数呢？比如 a = b + 5。"
    "用 addi。i 表示 immediate，立即数：这个常数直接编码在指令里。":
        "What if the thing we want to add is a constant, like five? For that there's the "
        "instruction addi, where the i stands for immediate, because the constant is "
        "stored right inside the instruction itself.",
    "RISC-V 没有 subi：减一个常数，就是加一个负数。"
    "addi 的立即数只有 12 位，范围是 −2048 到 2047。为什么是 12 位？第 9 集揭晓。":
        "There's no subi in RISC-V, because subtracting a constant is the same as adding "
        "a negative one. The constant in addi is only twelve bits wide, so it can only "
        "hold values from about minus two thousand to about plus two thousand. Why twelve "
        "bits? We'll find out in episode nine.",
    "现在看 x0 的妙用。汇编器提供了一些“伪指令”，它们会被替换成真实指令。"
    "mv 是加 0；li 是从 x0 出发加一个常数，nop 则把结果写进 x0：什么都不会改变。":
        "Now we can see what x0 is good for. The assembler offers a few "
        "pseudo-instructions, and it replaces each one with a real instruction. The mv "
        "instruction is just an add of zero, li starts from x0 and adds a constant, and "
        "nop writes its result into x0, so nothing changes at all.",
    "只用一个恒为 0 的寄存器，就省掉了好几条专用指令。这就是 RISC 的思路。":
        "With just one register that is always zero, we avoid needing several "
        "special-purpose instructions, and that is exactly the RISC way of thinking.",

    # ---- cue phrases (Chinese phrase -> the words in the English beat)
    "：操作名": "the name of the operation",
    "但 CPU 并不认识 C": "But a CPU can't run C",
    "编译器先把 C 变成汇编语言": "First the compiler",
    "汇编器再把每条汇编指令": "and then the assembler",
    "一条 32 位的机器指令": "one thirty-two bit machine instruction",
    "汇编和机器码几乎一一对应": "Because the two match",
    "这套规定叫做指令集架构": "That rulebook is called",
    "它是软件和硬件之间的契约": "It works like a contract",
    "CS61C 用的是 RISC-V": "this course uses RISC-V",
    "RISC 是“精简指令集”": "The R in RISC",
    "x0 到 x31": "named x0 through x31",
    "每个寄存器 32 位宽": "Each one is thirty-two bits wide",
    "寄存器在一个时钟周期内就能读写": "a register can be read or written",
    "而访问内存往往要慢上百倍": "Memory holds billions of bytes",
    "往 x0 里写任何值": "If you try to write anything",
    "t 开头的是临时寄存器": "t0 through t6 are temporaries",
    "s 开头的是保存寄存器": "s0 through s11 are saved registers",
    "a 开头的用来传递参数": "a0 through a7 hold arguments",
    "目标寄存器": "the destination register",
    "两个源寄存器": "two source registers",
    "add rd, rs1, rs2 的意思": "So an add simply",
    "执行 add s0, s1, s2": "When we run add",
    "两个值被送进加法器": "both values flow into the adder",
    "写回 s0": "which is written back",
    "被减数是 rs1": "The first source register",
    "假设编译器已经把": "We'll assume the compiler",
    "第一步": "The first instruction",
    "第二步": "The second one",
    "用 addi": "For that there's the instruction addi",
    "这个常数直接编码在指令里": "because the constant is stored",
    "addi 的立即数只有 12 位": "The constant in addi is only twelve bits",
    "mv 是加 0": "The mv instruction",
    "nop 则把结果写进 x0": "and nop writes",

    # ---- cue phrases (Chinese phrase -> the words in the English beat)
    "我们通常用寄存器的“别名”": "Instead we use friendlier names",
}
