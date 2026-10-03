"""English for episode 11 (keys are the Chinese strings in ep11_formats_buj.py)."""

EN = {
    # ---- end card
    "分支用 PC 相对寻址：目标 = PC + 偏移":
        "Branches use PC-relative addressing, so the target is the PC plus an offset",
    "B 型偏移以 2 字节为单位，范围约 ±4 KiB":
        "B-type offsets count in units of two bytes, with a range of about four kibibytes "
        "either way",
    "打乱的位序让各格式尽量共用同一组连线":
        "Scrambled bit orders let the formats share the same wiring",
    "U 型：lui / auipc 提供高 20 位":
        "The U format has lui and auipc, which supply the upper twenty bits",
    "J 型：jal，范围约 ±1 MiB；jalr 是 I 型":
        "The J format is jal, with a range of about one mebibyte either way, and jalr is an I "
        "format",

    # ---- PC-relative addressing
    "分支的目标地址怎么编码？": "How Do We Encode a Branch Target?",
    "目标地址 = PC + 偏移量": "target = PC + offset",
    "偏移总是 2 的倍数 → 最低位恒为 0，不必存储":
        "Offsets are always even → bit 0 is always 0, not stored",

    # ---- B-type
    "B 型：条件分支": "B-Type: Conditional Branches",
    "黄色都是立即数；上方标注它存的是偏移量的哪几位":
        "Yellow = immediate; labels show which offset bits each holds",

    # ---- U-type
    "U 型：长立即数": "U-Type: Wide Immediates",
    "低 12 位清零": "lower 12 bits zeroed",
    "来自立即数的高 20 位": "upper 20 bits, from the immediate",
    "addi t0, t0, -273    # 低 12 位 0xEEF = -273":
        "addi t0, t0, -273    # low 12 bits: 0xEEF = -273",
    "高位被借走了 1！": "The upper bits lost 1!",
    "lui  t0, 0xDEADC     # 先给高位加 1":
        "lui  t0, 0xDEADC     # upper 20 bits + 1",
    "正确！": "Correct!",
    "li t0, 0xDEADBEEF   # 伪指令，汇编器自动展开":
        "li t0, 0xDEADBEEF   # pseudo-instruction",

    # ---- J-type
    "J 型：jal": "J-Type: jal",
    "偏移以 2 字节为单位：范围约 ±1 MiB": "Offset in 2-byte units: range about ±1 MiB",
    "jalr  ra, 0x678(ra)     # 跳到 ra + 0x678，返回地址存进 ra":
        "jalr  ra, 0x678(ra)     # jump to ra + 0x678; ra = PC + 4",

    # ---- overview

    # ---- spoken beats and cue phrases (see references/narration-writing.md)
    "条件分支要比较两个寄存器 rs1、rs2，还要一个跳转目标；它不写寄存器，所以没有 rd。可目标地址本身就有 32 位，根本塞不进一条 32 位的指令。怎么办？":
        "A conditional branch compares two registers, rs1 and rs2, and also needs a jump "
        "target, and since it writes no register, it has no rd. But the target address itself "
        "is thirty-two bits, which can't possibly fit inside a thirty-two bit instruction. So "
        "what do we do?",
    "可目标地址本身就有 32 位": "But the target address itself",
    "观察：分支通常跳得很近——if 和循环体一般只有几条到几十条指令。所以只编码“相对当前 PC 的偏移量”。这叫 PC 相对寻址（PC-relative addressing）。":
        "Notice that branches usually jump only a short way, since an if or a loop body is "
        "typically a few to a few dozen instructions. So we encode only the offset relative "
        "to the current PC, which is called PC-relative addressing.",
    "所以只编码": "So we encode only the offset",
    "RISC-V 为 16 位的压缩指令留了余地，指令地址总是 2 的倍数，所以偏移的最低位恒为 0，不用存。于是 12 个比特能表示 13 位的偏移：范围约 ±4 KiB，也就是前后各约 1024 条指令。还有个好处：整段代码搬到内存别处，分支的偏移完全不用改。这叫位置无关代码（position-independent code）。":
        "RISC-V leaves room for sixteen-bit compressed instructions, so instruction addresses "
        "are always multiples of two, and the lowest bit of the offset is always zero, which "
        "we don't need to store. So twelve bits can represent a thirteen-bit offset, with a "
        "range of about four kibibytes either way, or roughly a thousand instructions each "
        "way. There is another benefit, which is that if the whole block of code moves "
        "elsewhere in memory, the branch offsets need no change at all. This is called "
        "position-independent code.",
    "还有个好处": "There is another benefit",
    "B 型的布局和 S 型几乎一样：rs1、rs2、funct3、opcode 都在老位置，立即数也分成两段。但立即数的位序被“打乱”了：第 12 位放在指令最高位，第 11 位挪到了右边那段的末尾。这是为了复用 S 型的连线：第 10:5 位和第 4:1 位与 S 型完全同位，符号位也永远在第 31 位。":
        "The B format is laid out almost like the S format. The fields rs1, rs2, funct3, and "
        "opcode are in their old places, and the immediate is split into two pieces. But the "
        "order of the immediate's bits is scrambled, with bit twelve at the very top of the "
        "instruction, and bit eleven moved to the end of the right-hand piece. This is to "
        "reuse the wiring of the S format. Bits ten to five and bits four to one are in "
        "exactly the same places as in S, and the sign bit is always bit thirty-one.",
    "但立即数的位序被": "But the order of the immediate's bits",
    "这是为了复用": "This is to reuse",
    "立即数也分成两段": "and the immediate is split",
    "编码 beq x19, x10, End。End 在 4 条指令之后，偏移是 16 字节。16 的 13 位二进制是 0 0000 0001 0000。最低位不存，其余各位按规定的位置“对号入座”。":
        "Let's encode beq x19, x10, End. End is four instructions ahead, so the offset is "
        "sixteen bytes. Sixteen as a thirteen-bit binary number is zero, zero zero zero zero, "
        "zero zero zero one, zero zero zero zero. The lowest bit isn't stored, and the other "
        "bits go into their prescribed places.",
    "16 的 13 位二进制": "Sixteen as a thirteen-bit",
    "最低位不存": "The lowest bit isn't stored",
    "寄存器照旧：rs2 = x10，rs1 = x19；beq 的 funct3 是 000，分支的 opcode 是 1100011。最终的机器码是 0x00A98863。":
        "The registers are as usual, rs2 is x10 and rs1 is x19, the funct3 of beq is zero "
        "zero zero, and the branch opcode is one one zero zero zero one one. So the final "
        "machine code is 0x00A98863.",
    "12 位立即数只装得下小常数。想把 0xDEADBEEF 这样的 32 位常数放进寄存器，怎么办？U 型只有 rd 和一个 20 位的立即数。lui（load upper immediate）就用这个格式。":
        "A twelve-bit immediate holds only small constants. So how do we get a thirty-two bit "
        "constant, like 0xDEADBEEF, into a register? The U format has just rd and a twenty-bit immediate, and the lui instruction, short for load upper immediate, uses this "
        "format.",
    "U 型只有 rd": "The U format has just",
    "lui t0, 0xDEADB：把 20 位立即数放进 t0 的高 20 位，低 12 位全部清零。":
        "The instruction lui t0, 0xDEADB puts the twenty-bit immediate into the upper twenty "
        "bits of t0, and clears the lower twelve bits to zero.",
    "把 20 位立即数放进 t0 的高 20 位": "puts the twenty-bit immediate",
    "低 12 位全部清零": "and clears the lower",
    "再用 addi 补上低 12 位 0xEEF 就行？小心：addi 的立即数是有符号的。0xEEF 的最高位是 1，按 12 位补码它表示 −273，会被符号扩展成 0xFFFFFEEF。":
        "Can we then add the low twelve bits, 0xEEF, with an addi? Careful, because the "
        "immediate of addi is signed. The top bit of 0xEEF is a one, so as a twelve-bit two's "
        "complement number it means minus two hundred seventy-three, and it gets sign-extended to 0xFFFFFEEF.",
    "0xEEF 的最高位是 1": "The top bit of 0xEEF",
    "相加的结果是 0xDEADAEEF：高 20 位被“借”走了 1。解决办法：低 12 位的最高位是 1 时，先把高 20 位加 1，写成 lui t0, 0xDEADC。":
        "The sum comes out as 0xDEADAEEF, so one has been borrowed from the upper twenty "
        "bits. The fix is, when the top bit of the low twelve bits is one, to add one to the "
        "upper twenty bits first, and write lui t0, 0xDEADC.",
    "解决办法": "The fix is",
    "好在不用手算：伪指令 li t0, 0xDEADBEEF 会由汇编器自动展开成这两条。另一条 U 型指令 auipc：把立即数左移 12 位后加到 PC 上，用来算出离当前位置很远的地址。":
        "Luckily we don't need to work this out by hand, because the pseudo-instruction li "
        "t0, 0xDEADBEEF is expanded by the assembler into these two instructions. Another "
        "U-format instruction is auipc, which shifts the immediate left by twelve bits and "
        "adds it to the PC, to work out an address far from the current position.",
    "另一条 U 型指令": "Another U-format instruction",
    "jal 只需要 rd 和一个偏移量。于是 J 型把剩下的 20 位全都给了立即数。同样以 2 字节为单位、最低位不存：21 位的偏移，范围约 ±1 MiB，足够覆盖绝大多数函数调用。位序同样是打乱的：让尽量多的位和 I 型、U 型同位，符号位依旧待在第 31 位。":
        "The jal instruction needs only rd and an offset, so the J format gives all the "
        "remaining twenty bits to the immediate. As before, the unit is two bytes and the "
        "lowest bit isn't stored. So the offset is twenty-one bits, with a range of about one "
        "mebibyte either way, enough to cover most function calls. The bit order is scrambled "
        "again, so that as many bits as possible line up with the I format and the U format, "
        "and the sign bit still stays at bit thirty-one.",
    "同样以 2 字节为单位": "As before, the unit is two bytes",
    "位序同样是打乱的": "The bit order is scrambled again",
    "更远怎么办？jalr 是 I 型：跳到 rs1 + 立即数，并把 PC + 4 存进 rd。配合 auipc 先算出高 20 位，就能跳到 32 位地址空间的任何位置。伪指令 call 就是这么展开的。":
        "What if the target is farther away? The jalr instruction is an I format, which jumps "
        "to rs1 plus the immediate, and stores PC plus four into rd. Together with auipc "
        "computing the upper twenty bits first, we can jump anywhere in the thirty-two bit "
        "address space, and that is how the pseudo-instruction call is expanded.",
    "配合 auipc": "Together with auipc",
    "把 RV32I 的全部 6 种格式放在一起看。rs1、rs2、rd 和 opcode 的位置始终固定；变化的只是立即数的摆法。而立即数的符号位，永远是第 31 位：硬件可以在知道指令类型之前就开始做符号扩展。":
        "Now let's put all six RV32I formats together. The positions of rs1, rs2, rd, and the "
        "opcode never change, and only the arrangement of the immediate varies. And the sign "
        "bit of the immediate is always bit thirty-one, so the hardware can start sign "
        "extension before it even knows the instruction type.",
    "rs1、rs2、rd 和 opcode 的位置": "The positions of rs1",
    "而立即数的符号位": "And the sign bit",
    "最终的机器码": "So the final machine code",
}
