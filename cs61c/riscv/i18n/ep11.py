"""English for episode 11 (keys are the Chinese strings in ep11_formats_buj.py)."""

EN = {
    # ---- end card
    "分支用 PC 相对寻址：目标 = PC + 偏移":
        "Branches use PC-relative addressing: target = PC + offset",
    "B 型偏移以 2 字节为单位，范围约 ±4 KiB":
        "B-type offsets count 2-byte units: range about ±4 KiB",
    "打乱的位序让各格式尽量共用同一组连线":
        "Scrambled bit orders let the formats share wiring",
    "U 型：lui / auipc 提供高 20 位":
        "U-type: lui / auipc supply the upper 20 bits",
    "J 型：jal，范围约 ±1 MiB；jalr 是 I 型":
        "J-type: jal, range about ±1 MiB; jalr is I-type",

    # ---- PC-relative addressing
    "分支的目标地址怎么编码？": "How Do We Encode a Branch Target?",
    "条件分支要比较两个寄存器 rs1、rs2，还要一个跳转目标；它不写寄存器，所以没有 rd。":
        "A conditional branch compares two registers, rs1 and rs2, and needs a target. "
        "It writes no register, so there's no rd.",
    "可目标地址本身就有 32 位，根本塞不进一条 32 位的指令。怎么办？":
        "But the target address alone is 32 bits; it can't possibly fit "
        "inside a 32-bit instruction. What now?",
    "观察：分支通常跳得很近——if 和循环体一般只有几条到几十条指令。":
        "Observation: branches rarely go far. An if or a loop body is usually "
        "a few to a few dozen instructions.",
    "目标地址 = PC + 偏移量": "target = PC + offset",
    "所以只编码“相对当前 PC 的偏移量”。这叫 PC 相对寻址（PC-relative addressing）。":
        "So we encode only the offset from the current PC. "
        "This is called PC-relative addressing.",
    "偏移总是 2 的倍数 → 最低位恒为 0，不必存储":
        "Offsets are always even → bit 0 is always 0, not stored",
    "RISC-V 为 16 位的压缩指令留了余地，指令地址总是 2 的倍数，所以偏移的最低位恒为 0，不用存。":
        "RISC-V leaves room for 16-bit compressed instructions, so instruction addresses "
        "are always even: an offset's lowest bit is always 0 and isn't stored.",
    "于是 12 个比特能表示 13 位的偏移：范围约 ±4 KiB，也就是前后各约 1024 条指令。":
        "So 12 bits encode a 13-bit offset: about ±4 KiB, "
        "or roughly 1024 instructions in either direction.",
    "还有个好处：整段代码搬到内存别处，分支的偏移完全不用改。这叫位置无关代码（position-independent code）。":
        "A bonus: move the whole block of code elsewhere in memory and not one branch offset "
        "changes. That's position-independent code.",

    # ---- B-type
    "B 型：条件分支": "B-Type: Conditional Branches",
    "B 型的布局和 S 型几乎一样：rs1、rs2、funct3、opcode 都在老位置，立即数也分成两段。":
        "B-type is laid out almost like S-type: rs1, rs2, funct3 and opcode stay put, "
        "and the immediate is split in two again.",
    "黄色都是立即数；上方标注它存的是偏移量的哪几位":
        "Yellow = immediate; labels show which offset bits each holds",
    "但立即数的位序被“打乱”了：第 12 位放在指令最高位，第 11 位挪到了右边那段的末尾。":
        "But the immediate's bits are \"scrambled\": bit 12 goes in the instruction's top bit, "
        "and bit 11 moves to the end of the right-hand piece.",
    "这是为了复用 S 型的连线：第 10:5 位和第 4:1 位与 S 型完全同位，符号位也永远在第 31 位。":
        "That reuses S-type's wiring: bits 10:5 and 4:1 sit exactly where they do in S-type, "
        "and the sign bit is still bit 31.",
    "编码 beq x19, x10, End。End 在 4 条指令之后，偏移是 16 字节。":
        "Encode beq x19, x10, End. End is 4 instructions ahead, so the offset is 16 bytes.",
    "16 的 13 位二进制是 0 0000 0001 0000。最低位不存，其余各位按规定的位置“对号入座”。":
        "16 in 13-bit binary is 0 0000 0001 0000. Bit 0 is dropped; "
        "every other bit goes to its assigned seat.",
    "寄存器照旧：rs2 = x10，rs1 = x19；beq 的 funct3 是 000，分支的 opcode 是 1100011。":
        "Registers as usual: rs2 = x10, rs1 = x19. beq's funct3 is 000, "
        "and the branch opcode is 1100011.",
    "最终的机器码是 0x00A98863。": "The final machine code is 0x00A98863.",

    # ---- U-type
    "U 型：长立即数": "U-Type: Wide Immediates",
    "12 位立即数只装得下小常数。想把 0xDEADBEEF 这样的 32 位常数放进寄存器，怎么办？":
        "A 12-bit immediate only holds small constants. How do we get a 32-bit constant "
        "like 0xDEADBEEF into a register?",
    "U 型只有 rd 和一个 20 位的立即数。lui（load upper immediate）就用这个格式。":
        "U-type has just rd and a 20-bit immediate. lui (load upper immediate) uses this format.",
    "低 12 位清零": "lower 12 bits zeroed",
    "来自立即数的高 20 位": "upper 20 bits, from the immediate",
    "lui t0, 0xDEADB：把 20 位立即数放进 t0 的高 20 位，低 12 位全部清零。":
        "lui t0, 0xDEADB puts the 20-bit immediate into t0's upper 20 bits "
        "and clears the lower 12.",
    "addi t0, t0, -273    # 低 12 位 0xEEF = -273":
        "addi t0, t0, -273    # low 12 bits: 0xEEF = -273",
    "再用 addi 补上低 12 位 0xEEF 就行？小心：addi 的立即数是有符号的。":
        "Then just addi the low 12 bits, 0xEEF? Careful: addi's immediate is signed.",
    "0xEEF 的最高位是 1，按 12 位补码它表示 −273，会被符号扩展成 0xFFFFFEEF。":
        "0xEEF has its top bit set, so as 12-bit two's complement it means −273, "
        "and it gets sign-extended to 0xFFFFFEEF.",
    "高位被借走了 1！": "The upper bits lost 1!",
    "相加的结果是 0xDEADAEEF：高 20 位被“借”走了 1。":
        "The sum is 0xDEADAEEF: a 1 was \"borrowed\" from the upper 20 bits.",
    "lui  t0, 0xDEADC     # 先给高位加 1":
        "lui  t0, 0xDEADC     # upper 20 bits + 1",
    "正确！": "Correct!",
    "解决办法：低 12 位的最高位是 1 时，先把高 20 位加 1，写成 lui t0, 0xDEADC。":
        "The fix: when the top bit of the low 12 is set, add 1 to the upper 20 bits first: "
        "lui t0, 0xDEADC.",
    "li t0, 0xDEADBEEF   # 伪指令，汇编器自动展开":
        "li t0, 0xDEADBEEF   # pseudo-instruction",
    "好在不用手算：伪指令 li t0, 0xDEADBEEF 会由汇编器自动展开成这两条。":
        "Luckily there's no need to do this by hand: the assembler expands "
        "the pseudo-instruction li t0, 0xDEADBEEF into these two.",
    "另一条 U 型指令 auipc：把立即数左移 12 位后加到 PC 上，用来算出离当前位置很远的地址。":
        "The other U-type instruction, auipc, shifts its immediate left by 12 and adds it "
        "to the PC, to reach addresses far from the current one.",

    # ---- J-type
    "J 型：jal": "J-Type: jal",
    "jal 只需要 rd 和一个偏移量。于是 J 型把剩下的 20 位全都给了立即数。":
        "jal needs only rd and an offset, so J-type gives all 20 remaining bits "
        "to the immediate.",
    "偏移以 2 字节为单位：范围约 ±1 MiB": "Offset in 2-byte units: range about ±1 MiB",
    "同样以 2 字节为单位、最低位不存：21 位的偏移，范围约 ±1 MiB，足够覆盖绝大多数函数调用。":
        "Again in 2-byte units with bit 0 not stored: a 21-bit offset, about ±1 MiB. "
        "That covers the vast majority of function calls.",
    "位序同样是打乱的：让尽量多的位和 I 型、U 型同位，符号位依旧待在第 31 位。":
        "The bits are scrambled too, lining up as many as possible with I-type and U-type; "
        "the sign bit stays at bit 31.",
    "jalr  ra, 0x678(ra)     # 跳到 ra + 0x678，返回地址存进 ra":
        "jalr  ra, 0x678(ra)     # jump to ra + 0x678; ra = PC + 4",
    "更远怎么办？jalr 是 I 型：跳到 rs1 + 立即数，并把 PC + 4 存进 rd。":
        "Need to go farther? jalr is I-type: it jumps to rs1 + immediate "
        "and saves PC + 4 in rd.",
    "配合 auipc 先算出高 20 位，就能跳到 32 位地址空间的任何位置。伪指令 call 就是这么展开的。":
        "Pair it with auipc for the upper 20 bits and you can reach any 32-bit address. "
        "That's how the pseudo-instruction call expands.",

    # ---- overview
    "把 RV32I 的全部 6 种格式放在一起看。": "Here are all six RV32I formats together.",
    "rs1、rs2、rd 和 opcode 的位置始终固定；变化的只是立即数的摆法。":
        "rs1, rs2, rd and opcode never move; the only thing that changes "
        "is how the immediate is laid out.",
    "而立即数的符号位，永远是第 31 位：硬件可以在知道指令类型之前就开始做符号扩展。":
        "And the immediate's sign bit is always bit 31, so sign extension can start "
        "before the instruction type is even known.",
}
