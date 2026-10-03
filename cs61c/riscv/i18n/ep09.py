"""English for episode 9 (keys are the Chinese strings in ep09_formats_ris.py)."""

EN = {
    # ---- end card
    "存储程序：指令就是存放在内存里的 32 位数":
        "Stored program means that instructions are thirty-two bit numbers kept in memory",
    "R 型：funct7 | rs2 | rs1 | funct3 | rd | opcode":
        "The R format is funct7, rs2, rs1, funct3, rd, and opcode",
    "I 型：12 位立即数取代 funct7 和 rs2":
        "The I format replaces funct7 and rs2 with a twelve-bit immediate",
    "S 型：立即数拆成两段，rs1、rs2 位置不变":
        "The S format splits the immediate in two, and leaves rs1 and rs2 where they were",
    "字段位置固定，硬件译码更简单": "Fixed field positions make decoding simpler for the hardware",

    # ---- stored program
    "内存": "Memory",

    # ---- R-type
    "R 型：寄存器之间的运算": "R-Type: Register-Register Arithmetic",
    "R 型": "R-type",

    # ---- I-type
    "I 型：带立即数的指令": "I-Type: Instructions with an Immediate",
    "12 位补码：−2048 ~ 2047": "12-bit two's complement: −2048 to 2047",
    "I 型算术": "I-type arith",
    "slli / srli / srai 也是 I 型：移位量只用立即数的低 5 位":
        "slli / srli / srai: I-type, shift amount = imm's low 5 bits",

    # ---- S-type
    "S 型：store": "S-Type: Stores",
    "8 低位": "8, lower",
    "8 高位": "8, upper",

    # ---- spoken beats and cue phrases (see references/narration-writing.md)
    "前几集我们一直在写汇编。可硬件真正执行的，是一个个 32 位的二进制数。指令本身也是数据，和普通数据一样存在内存里：这就是“存储程序”（stored program）的思想。":
        "In the last few episodes we kept writing assembly, but what the hardware really "
        "executes is a series of thirty-two bit binary numbers. Instructions are themselves "
        "data, stored in memory just like ordinary data, and that is the stored program idea.",
    "指令本身也是数据": "Instructions are themselves data",
    "PC 里存的，是当前指令在内存中的地址。那么，一条汇编指令究竟是怎样变成 32 个比特的？":
        "The PC holds the address of the current instruction in memory. So how does an "
        "assembly instruction actually turn into thirty-two bits?",
    "32 位被切成几段，每段叫一个字段（field）。add、sub 这类操作数全是寄存器的指令，用 R 型格式。rd、rs1、rs2 各占 5 位：2 的 5 次方是 32，刚好够给 32 个寄存器编号。opcode 占最低 7 位，说明这是哪一类指令；funct3 和 funct7 再进一步区分具体的运算。":
        "The thirty-two bits are cut into pieces, and each piece is called a field. "
        "Instructions like add and sub, whose operands are all registers, use the R format. "
        "The fields rd, rs1, and rs2 take five bits each, since two to the fifth is thirty-two, just enough to number the thirty-two registers. The opcode takes the lowest "
        "seven bits and says which kind of instruction this is, while funct3 and funct7 "
        "narrow down the exact operation.",
    "rd、rs1、rs2 各占 5 位": "The fields rd, rs1, and rs2",
    "opcode 占最低 7 位": "The opcode takes",
    "来编码 add x18, x19, x10。rd = 18，写成 5 位二进制是 10010；rs1 = 19 是 10011；rs2 = 10 是 01010。":
        "Let's encode add x18, x19, x10. Here rd is eighteen, which is one zero zero one zero "
        "in five-bit binary. Then rs1 is nineteen, which is one zero zero one one, and rs2 is "
        "ten, which is zero one zero one zero.",
    "add 的 funct3 和 funct7 都是 0，R 型算术指令的 opcode 是 0110011。每 4 位合成一个十六进制数字：整条指令就是 0x00A98933。":
        "For add, funct3 and funct7 are both zero, and the opcode for R-type arithmetic is "
        "zero one one zero zero one one. Putting every four bits together as one hexadecimal "
        "digit, the whole instruction is 0x00A98933.",
    "换成 sub 呢？只有 funct7 变了：0100000。硬件看到第 30 位的这个 1，就让加法器改做减法。":
        "What about sub? Only funct7 changes, to zero one zero zero zero zero zero. When the "
        "hardware sees that one in bit thirty, it makes the adder subtract.",
    "只有 funct7 变了": "Only funct7 changes",
    "硬件看到第 30 位的这个 1": "When the hardware sees",
    "所有 R 型运算共用一个 opcode，靠 funct3 和 funct7 的组合来区分。":
        "All the R-type operations share one opcode, and are told apart by the combination of "
        "funct3 and funct7.",
    "addi 只有两个寄存器，外加一个常数。常数放在哪儿？I 型把 R 型里 funct7 和 rs2 的位置合并成一个 12 位的立即数，其余字段纹丝不动。":
        "The addi instruction has only two registers, plus a constant. Where does the "
        "constant go? The I format merges the funct7 and rs2 positions from the R format into "
        "a single twelve-bit immediate, and leaves all the other fields exactly where they "
        "were.",
    "I 型把 R 型里": "The I format merges",
    "第 2 集的问题有了答案：立即数只分到这 12 位，而 12 位补码的范围正是 −2048 到 2047。":
        "That answers the question from episode two. The immediate gets only these twelve "
        "bits, and the range of a twelve-bit two's complement number is exactly minus two "
        "thousand forty-eight to two thousand forty-seven.",
    "编码 addi x15, x1, -50：-50 的 12 位补码是 1111 1100 1110。执行时，硬件把这 12 位符号扩展成 32 位，再和 rs1 相加。编码结果是 0xFCE08793。":
        "Let's encode addi x15, x1, minus fifty. Minus fifty as a twelve-bit two's complement "
        "number is one one one one, one one zero zero, one one one zero. When it executes, "
        "the hardware sign-extends those twelve bits to thirty-two and adds them to rs1. The "
        "encoding comes out as 0xFCE08793.",
    "load 指令也是 I 型。lw x14, 8(x2) 里，偏移量 8 就是立即数，基址寄存器 x2 放在 rs1。":
        "Load instructions are also I format. In lw x14, 8(x2), the offset eight is the "
        "immediate, and the base register x2 goes in rs1.",
    "所有 load 共用一个 opcode，由 funct3 区分宽度和有无符号：lb、lh、lw、lbu、lhu。移位 slli、srli、srai 也用 I 型，但移位量最多 31，只用到立即数的低 5 位。":
        "All the loads share one opcode, and funct3 tells apart the width and the signedness, "
        "for lb, lh, lw, lbu, and lhu. The shift instructions slli, srli, and srai are I "
        "format too, but the shift amount is at most thirty-one, so only the low five bits of "
        "the immediate are used.",
    "移位 slli": "The shift instructions",
    "store 有两个源寄存器——数据和基址——没有目标寄存器，但还需要一个 12 位偏移。S 型的做法：把立即数拆成两段。高 7 位放在 funct7 的老位置，低 5 位放在原来 rd 的位置。":
        "A store has two source registers, the data and the base, and no destination "
        "register, but it still needs a twelve-bit offset. The S format splits the immediate "
        "into two pieces. The upper seven bits go in the old place of funct7, and the lower "
        "five bits go where rd used to be.",
    "S 型的做法": "The S format splits",
    "编码 sw x14, 8(x2)。偏移 8 的 12 位二进制是 0000000 01000：高 7 位全 0，低 5 位是 01000。":
        "Let's encode sw x14, 8(x2). The offset eight in twelve-bit binary is seven zeros "
        "followed by zero one zero zero zero. So the upper seven bits are all zero, and the "
        "lower five bits are zero one zero zero zero.",
    "要写入的数据 x14 放在 rs2，基址 x2 放在 rs1；funct3 = 010 表示整字，opcode 是 0100011。拼起来，这条 sw 就是 0x00E12423。":
        "The data in x14 goes into rs2 and the base x2 goes into rs1. Then funct3 is zero one "
        "zero for a whole word, and the opcode is zero one zero zero zero one one. Put "
        "together, this sw is 0x00E12423.",
    "把三种格式叠起来看：为什么 S 型要拆得这么别扭？答案：不管哪种格式，只要用到 rs1、rs2，它们就待在同一个位置。":
        "Now let's stack the three formats on top of each other. Why is the S format split so "
        "awkwardly? The answer is that whenever a format uses rs1 and rs2, they sit in the "
        "same place.",
    "答案": "The answer is that",
    "funct3 和 opcode 也一样。硬件不必先判断指令类型，就能按固定位置直接去读寄存器。读寄存器和译码可以同时进行，电路更简单，也更快。这是 RISC-V 设计中很漂亮的一笔。":
        "The same goes for funct3 and the opcode. So the hardware can read the registers "
        "straight from fixed positions, without first working out the instruction type. "
        "Reading registers and decoding can happen at the same time, which makes the circuit "
        "simpler and faster, and is a really neat touch in the design of RISC-V.",
    "rd = 18": "Here rd is eighteen",
    "每 4 位合成一个十六进制数字": "Putting every four bits together",
    "编码结果是": "The encoding comes out as",
    "拼起来": "Put together",
}
