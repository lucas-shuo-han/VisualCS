"""English for episode 9 (keys are the Chinese strings in ep09_formats_ris.py)."""

EN = {
    # ---- end card
    "存储程序：指令就是存放在内存里的 32 位数":
        "Stored program: instructions are 32-bit numbers in memory",
    "R 型：funct7 | rs2 | rs1 | funct3 | rd | opcode":
        "R-type: funct7 | rs2 | rs1 | funct3 | rd | opcode",
    "I 型：12 位立即数取代 funct7 和 rs2":
        "I-type: a 12-bit immediate replaces funct7 and rs2",
    "S 型：立即数拆成两段，rs1、rs2 位置不变":
        "S-type: the immediate is split in two; rs1, rs2 stay put",
    "字段位置固定，硬件译码更简单":
        "Fixed field positions keep decoding simple",

    # ---- stored program
    "内存": "Memory",
    "前几集我们一直在写汇编。可硬件真正执行的，是一个个 32 位的二进制数。":
        "So far we've been writing assembly. But what the hardware actually runs "
        "is a sequence of 32-bit binary numbers.",
    "指令本身也是数据，和普通数据一样存在内存里：这就是“存储程序”（stored program）的思想。":
        "Instructions are data too, kept in memory just like any other data: "
        "that's the stored-program idea.",
    "PC 里存的，是当前指令在内存中的地址。":
        "The PC holds the memory address of the current instruction.",
    "那么，一条汇编指令究竟是怎样变成 32 个比特的？":
        "So how exactly does a line of assembly become 32 bits?",

    # ---- R-type
    "R 型：寄存器之间的运算": "R-Type: Register-Register Arithmetic",
    "32 位被切成几段，每段叫一个字段（field）。add、sub 这类操作数全是寄存器的指令，用 R 型格式。":
        "The 32 bits are cut into pieces called fields. Instructions whose operands "
        "are all registers, like add and sub, use the R-type format.",
    "rd、rs1、rs2 各占 5 位：2 的 5 次方是 32，刚好够给 32 个寄存器编号。":
        "rd, rs1 and rs2 get 5 bits each: 2 to the 5th is 32, just enough "
        "to number all 32 registers.",
    "opcode 占最低 7 位，说明这是哪一类指令；funct3 和 funct7 再进一步区分具体的运算。":
        "The opcode, in the lowest 7 bits, says what kind of instruction this is; "
        "funct3 and funct7 pin down the exact operation.",
    "来编码 add x18, x19, x10。": "Let's encode add x18, x19, x10.",
    "rd = 18，写成 5 位二进制是 10010；rs1 = 19 是 10011；rs2 = 10 是 01010。":
        "rd = 18 is 10010 in 5-bit binary; rs1 = 19 is 10011; rs2 = 10 is 01010.",
    "add 的 funct3 和 funct7 都是 0，R 型算术指令的 opcode 是 0110011。":
        "For add, funct3 and funct7 are both 0, and the opcode for R-type arithmetic is 0110011.",
    "R 型": "R-type",
    "每 4 位合成一个十六进制数字：整条指令就是 0x00A98933。":
        "Every 4 bits make one hex digit: the whole instruction is 0x00A98933.",
    "换成 sub 呢？只有 funct7 变了：0100000。硬件看到第 30 位的这个 1，就让加法器改做减法。":
        "What about sub? Only funct7 changes, to 0100000. That 1 in bit 30 "
        "tells the hardware to make the adder subtract.",
    "所有 R 型运算共用一个 opcode，靠 funct3 和 funct7 的组合来区分。":
        "All R-type operations share one opcode; the combination of funct3 and funct7 "
        "tells them apart.",

    # ---- I-type
    "I 型：带立即数的指令": "I-Type: Instructions with an Immediate",
    "addi 只有两个寄存器，外加一个常数。常数放在哪儿？":
        "addi has only two registers, plus a constant. Where does the constant go?",
    "I 型把 R 型里 funct7 和 rs2 的位置合并成一个 12 位的立即数，其余字段纹丝不动。":
        "I-type merges R-type's funct7 and rs2 slots into one 12-bit immediate; "
        "every other field stays exactly where it was.",
    "12 位补码：−2048 ~ 2047": "12-bit two's complement: −2048 to 2047",
    "第 2 集的问题有了答案：立即数只分到这 12 位，而 12 位补码的范围正是 −2048 到 2047。":
        "That answers the question from Episode 2: the immediate only gets these 12 bits, "
        "and 12-bit two's complement spans exactly −2048 to 2047.",
    "编码 addi x15, x1, -50：-50 的 12 位补码是 1111 1100 1110。":
        "Encode addi x15, x1, -50: -50 in 12-bit two's complement is 1111 1100 1110.",
    "I 型算术": "I-type arith",
    "执行时，硬件把这 12 位符号扩展成 32 位，再和 rs1 相加。编码结果是 0xFCE08793。":
        "When it runs, the hardware sign-extends these 12 bits to 32 and adds them to rs1. "
        "The encoding is 0xFCE08793.",
    "load 指令也是 I 型。lw x14, 8(x2) 里，偏移量 8 就是立即数，基址寄存器 x2 放在 rs1。":
        "Loads are I-type too. In lw x14, 8(x2), the offset 8 is the immediate "
        "and the base register x2 goes in rs1.",
    "所有 load 共用一个 opcode，由 funct3 区分宽度和有无符号：lb、lh、lw、lbu、lhu。":
        "All loads share one opcode; funct3 picks the width and signedness: "
        "lb, lh, lw, lbu, lhu.",
    "slli / srli / srai 也是 I 型：移位量只用立即数的低 5 位":
        "slli / srli / srai: I-type, shift amount = imm's low 5 bits",
    "移位 slli、srli、srai 也用 I 型，但移位量最多 31，只用到立即数的低 5 位。":
        "slli, srli and srai are I-type too, but a shift amount is at most 31, "
        "so only the immediate's low 5 bits are used.",

    # ---- S-type
    "S 型：store": "S-Type: Stores",
    "store 有两个源寄存器——数据和基址——没有目标寄存器，但还需要一个 12 位偏移。":
        "A store has two source registers, the data and the base, and no destination, "
        "but it still needs a 12-bit offset.",
    "S 型的做法：把立即数拆成两段。高 7 位放在 funct7 的老位置，低 5 位放在原来 rd 的位置。":
        "S-type's trick: split the immediate in two. The upper 7 bits go where funct7 was, "
        "the lower 5 where rd used to be.",
    "编码 sw x14, 8(x2)。偏移 8 的 12 位二进制是 0000000 01000：高 7 位全 0，低 5 位是 01000。":
        "Encode sw x14, 8(x2). The offset 8 in 12 bits is 0000000 01000: "
        "the upper 7 bits are all 0, the lower 5 are 01000.",
    "8 低位": "8, lower",
    "8 高位": "8, upper",
    "要写入的数据 x14 放在 rs2，基址 x2 放在 rs1；funct3 = 010 表示整字，opcode 是 0100011。":
        "The data to store, x14, goes in rs2 and the base x2 in rs1; "
        "funct3 = 010 means a full word, and the opcode is 0100011.",
    "拼起来，这条 sw 就是 0x00E12423。":
        "Put together, this sw is 0x00E12423.",
    "把三种格式叠起来看：为什么 S 型要拆得这么别扭？":
        "Stack the three formats: why does S-type split its immediate so awkwardly?",
    "答案：不管哪种格式，只要用到 rs1、rs2，它们就待在同一个位置。":
        "The answer: in every format that uses them, rs1 and rs2 sit in the same place.",
    "funct3 和 opcode 也一样。硬件不必先判断指令类型，就能按固定位置直接去读寄存器。":
        "The same goes for funct3 and opcode. The hardware can read the registers "
        "from fixed positions before it even knows the instruction type.",
    "读寄存器和译码可以同时进行，电路更简单，也更快。这是 RISC-V 设计中很漂亮的一笔。":
        "Register reads and decoding can happen at the same time: simpler, faster circuits. "
        "A lovely touch in RISC-V's design.",
}
