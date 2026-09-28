"""English for episode 2 (keys are the Chinese strings in ep02_isa_registers.py)."""

EN = {
    # end card
    "ISA 是软件与硬件之间的契约": "The ISA is the contract between software and hardware",
    "RV32I 有 32 个 32 位寄存器，x0 恒为 0": "RV32I has 32 registers of 32 bits; x0 is always 0",
    "算术指令：add / sub rd, rs1, rs2": "Arithmetic: add / sub rd, rs1, rs2",
    "addi 带 12 位立即数；mv、li、nop 是伪指令": "addi: 12-bit immediate; mv, li, nop are pseudoinstructions",

    # hook
    "我们写下一行 C 代码：a = b + c;": "Let's write one line of C: a = b + c;",
    "但 CPU 并不认识 C。它只会执行一串串的 0 和 1。":
        "But a CPU doesn't understand C. All it can run is strings of 0s and 1s.",
    "编译器 Compiler": "Compiler",
    "汇编器 Assembler": "Assembler",
    "中间隔着两步翻译：编译器先把 C 变成汇编语言……":
        "Two translation steps sit in between. First the compiler turns C into assembly language...",
    "……汇编器再把每条汇编指令变成一条 32 位的机器指令。":
        "...then the assembler turns each assembly instruction into a 32-bit machine instruction.",
    "汇编和机器码几乎一一对应：汇编就是机器指令的“文字版”。":
        "Assembly maps almost one-to-one onto machine code: it's machine instructions written out as text.",

    # ISA
    "软件：C、Python、操作系统……": "Software: C, Python, the OS...",
    "指令集架构  ISA": "Instruction Set Architecture (ISA)",
    "硬件：CPU 电路": "Hardware: CPU circuits",
    "一台 CPU 支持哪些指令、有哪些寄存器，这套规定叫做指令集架构（ISA）。":
        "The specification of which instructions a CPU supports and which registers it has "
        "is called its instruction set architecture (ISA).",
    "它是软件和硬件之间的契约：软件只使用这些指令，硬件保证正确执行它们。":
        "It's a contract between software and hardware: software uses only these instructions, "
        "and hardware guarantees to execute them correctly.",
    "x86、ARM、RISC-V 都是 ISA。CS61C 用的是 RISC-V：开源、简洁、规整。":
        "x86, ARM and RISC-V are all ISAs. CS61C uses RISC-V: open-source, simple and regular.",
    "RISC = Reduced Instruction Set Computer  精简指令集": "RISC = Reduced Instruction Set Computer",
    "RISC 是“精简指令集”：指令少而规整，硬件就能做得简单、快速。":
        "RISC means a reduced instruction set: few, regular instructions, "
        "so the hardware can be simple and fast.",
    "RV32I 基础指令集只有大约 40 条指令，这个系列会讲到其中的大部分。":
        "The RV32I base instruction set has only about 40 instructions, and this series covers most of them.",

    # registers
    "寄存器 Registers": "Registers",
    "RISC-V 的算术指令只能操作寄存器：CPU 内部极少量、极快的存储单元。":
        "RISC-V arithmetic works only on registers: a tiny amount of very fast storage inside the CPU.",
    "RV32I 一共有 32 个整数寄存器：x0 到 x31。": "RV32I has 32 integer registers: x0 through x31.",
    "32 位 = 4 字节 = 1 个字（word）": "32 bits = 4 bytes = 1 word",
    "每个寄存器 32 位宽。32 位，也就是 4 个字节，称为一个“字”。":
        "Each register is 32 bits wide. 32 bits, or 4 bytes, is called a word.",
    "寄存器：32 × 4 B = 128 字节": "Registers: 32 × 4 B = 128 bytes",
    "内存：数十亿字节": "Memory: billions of bytes",
    "为什么只有 32 个？因为越小越快。": "Why only 32? Because smaller is faster.",
    "寄存器在一个时钟周期内就能读写，而访问内存往往要慢上百倍。":
        "A register can be read or written within one clock cycle; "
        "a memory access is often 100 times slower or more.",
    "其中 x0 很特别：它的值永远是 0。": "One of them, x0, is special: its value is always 0.",
    "往 x0 里写任何值，都会被悄悄丢弃。": "Anything written to x0 is silently thrown away.",
    "听起来有点浪费？稍后你就会看到它有多好用。": "Sounds wasteful? You'll soon see how handy it is.",
    "在汇编里，我们通常用寄存器的“别名”，也就是 ABI 名字。":
        "In assembly we usually call registers by their other names, the ABI names.",
    "t 开头的是临时寄存器（temporary）……": "Names starting with t are temporary registers...",
    "s 开头的是保存寄存器（saved）……": "those starting with s are saved registers...",
    "a 开头的用来传递参数（argument）和返回值。": "and the a registers pass arguments and return values.",
    "ra、sp 等有专门用途。这些寄存器的使用规则，第 7 集讲函数调用时再细说。":
        "ra, sp and a few others have special jobs. "
        "We'll cover the rules for all these registers with function calls in Episode 7.",

    # add / sub
    "算术指令": "Arithmetic Instructions",
    "操作名": "opname",
    "目标": "dest",
    "源 1": "src 1",
    "源 2": "src 2",
    "算术指令的格式是固定的：操作名、目标寄存器，然后是两个源寄存器。":
        "Arithmetic instructions have a rigid format: operation name, destination register, "
        "then two source registers.",
    "add rd, rs1, rs2 的意思就是：rd = rs1 + rs2。": "add rd, rs1, rs2 simply means rd = rs1 + rs2.",
    "举个例子：s1 里是 7，s2 里是 5。": "For example, say s1 holds 7 and s2 holds 5.",
    "执行 add s0, s1, s2：两个值被送进加法器……": "Run add s0, s1, s2: both values go into the adder...",
    "……得到 12，写回 s0。": "...and the result, 12, is written to s0.",
    "sub 也一样：rd = rs1 − rs2。注意顺序，被减数是 rs1，减数是 rs2。":
        "sub works the same way: rd = rs1 − rs2. Order matters: rs2 is subtracted from rs1.",

    # a = b + c - d
    "来编译一个稍复杂的表达式：a = b + c - d。": "Now let's compile something a bit bigger: a = b + c - d.",
    "假设编译器已经把 a、b、c、d 分别放在 s0、s1、s2、s3 中。":
        "Suppose the compiler has put a, b, c and d in s0, s1, s2 and s3.",
    "每条指令只能做一次运算，所以要拆成两步，中间结果放在临时寄存器 t0。":
        "Each instruction does only one operation, so this takes two steps, "
        "with the intermediate result in the temporary register t0.",
    "设 b = 10，c = 20，d = 5。第一步：t0 = 10 + 20 = 30。":
        "Let b = 10, c = 20, d = 5. Step one: t0 = 10 + 20 = 30.",
    "第二步：s0 = t0 − d = 30 − 5 = 25。完成！": "Step two: s0 = t0 − d = 30 − 5 = 25. Done!",

    # immediates
    "立即数 Immediate": "Immediates",
    "如果要加的是一个常数呢？比如 a = b + 5。": "What if we're adding a constant, as in a = b + 5?",
    "立即数：直接写在指令里的常数": "Immediate: a constant written right into the instruction",
    "用 addi。i 表示 immediate，立即数：这个常数直接编码在指令里。":
        "Use addi. The i stands for immediate: the constant is encoded right in the instruction.",
    "RISC-V 没有 subi：减一个常数，就是加一个负数。":
        "RISC-V has no subi: subtracting a constant is just adding a negative one.",
    "立即数只有 12 位：范围 −2048 ~ 2047（原因见第 9 集）":
        "Only 12 bits: −2048 to 2047 (why: see Episode 9)",
    "addi 的立即数只有 12 位，范围是 −2048 到 2047。为什么是 12 位？第 9 集揭晓。":
        "addi's immediate is only 12 bits, so it ranges from −2048 to 2047. "
        "Why 12 bits? Episode 9 explains.",
    "复制：加 0": "copy: add 0",
    "装入常数：从 x0 加": "load a constant: add it to x0",
    "什么也不做": "do nothing",
    "现在看 x0 的妙用。汇编器提供了一些“伪指令”，它们会被替换成真实指令。":
        "Now for x0's trick. The assembler offers pseudoinstructions, "
        "which it replaces with real instructions.",
    "mv 是加 0；li 是从 x0 出发加一个常数……": "mv adds 0; li starts from x0 and adds a constant...",
    "……nop 则把结果写进 x0：什么都不会改变。": "...and nop writes its result to x0, so nothing changes.",
    "只用一个恒为 0 的寄存器，就省掉了好几条专用指令。这就是 RISC 的思路。":
        "One register that's always 0 saves several dedicated instructions. That's RISC thinking.",
}
