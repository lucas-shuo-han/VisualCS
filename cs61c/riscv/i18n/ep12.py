"""English for episode 12 (keys are the Chinese strings in ep12_addressing.py)."""

EN = {
    # ---- end card
    "寻址方式：基址 + 偏移、PC 相对、绝对":
        "Addressing modes: base + displacement, PC-relative, absolute",
    "偏移 = 目标地址 − 当前指令地址，搬家不变":
        "Offset = target − this instruction's address: moving code keeps it",
    "分支太远：条件取反，跳过一条 j（±1 MiB）":
        "Branch too far: negate it and hop over a j (±1 MiB)",
    "任意地址：lui 或 auipc 配合 jalr":
        "Any address: lui or auipc, plus jalr",
    "拆常数：低 12 位的最高位是 1，高 20 位先加 1":
        "Splitting constants: if bit 11 is 1, add 1 to the upper 20 bits",

    # ---- addressing modes
    "三种寻址方式": "Three Addressing Modes",
    "6 种指令格式已经凑齐。这一集换个角度：指令要访问的地址、要跳去的目标，是怎么算出来的？":
        "We now have all six instruction formats. This time, a different angle: how does an "
        "instruction compute the address it accesses, or the target it jumps to?",
    "基址 + 偏移": "Base + displacement",
    "PC 相对": "PC-relative",
    "直接给出完整地址": "Full address, given directly",
    "绝对": "Absolute",
    "这些计算规则叫寻址方式（addressing mode）。RISC-V 主要用到三种。":
        "These rules are called addressing modes. RISC-V mainly uses three.",
    "第一种：基址 + 偏移（base/displacement），地址 = 寄存器 + 立即数。lw 和 sw 就是这样找到数据的。":
        "First, base/displacement: address = register + immediate. "
        "That's how lw and sw find their data.",
    "jalr 也属于这一类：跳到 rs1 + 立即数。新 PC 只取决于寄存器，与 jalr 自己在哪儿无关。":
        "jalr belongs here too: it jumps to rs1 + immediate. The new PC depends only on a register, "
        "not on where the jalr itself sits.",
    "第二种：PC 相对寻址，以 PC 为基准加上偏移。条件分支、jal 和 auipc 都用它。":
        "Second, PC-relative addressing: an offset added to the PC. "
        "Conditional branches, jal and auipc all use it.",
    "第三种：绝对寻址，直接给出完整地址。比如 lui 装入地址的高 20 位，jalr 补上低 12 位并跳过去。":
        "Third, absolute addressing: the full address is given directly. For example, lui loads "
        "the address's upper 20 bits, and jalr adds the lower 12 and jumps.",
    "其余指令：PC + 4": "Everything else: PC + 4",
    "其实几乎每条指令都以 PC 相对的方式更新 PC：普通指令 PC + 4，分支和 jal 是 PC + 偏移。只有 jalr 例外。":
        "In fact, almost every instruction sets the new PC relative to the current one: PC + 4 for most, "
        "PC + offset for branches and jal. Only jalr is different.",
    "伪指令也各有归属：j 是 jal x0 的简写，属于 PC 相对；jr 和 ret 则是 jalr 的简写。":
        "The pseudo-instructions fit this map too: j is shorthand for jal x0, so it's PC-relative; "
        "jr and ret are shorthand for jalr.",

    # ---- labels -> offsets
    "从标签到偏移": "From Labels to Offsets",
    "来算几个具体的偏移。这是课程笔记里的循环，每条指令都标了示例地址：beq 在 0x0C。":
        "Let's compute some real offsets. Here is the loop from the course notes, "
        "with a sample address on each instruction: beq is at 0x0C.",
    "标签不是指令，机器码里根本没有 Loop 和 End。汇编器得把它们换算成相对 PC 的偏移。":
        "Labels aren't instructions: Loop and End don't exist in machine code at all. "
        "The assembler must turn them into PC-relative offsets.",
    "情况一：beq 不跳。PC 走到下一条，偏移是 +4。":
        "Case 1: the beq isn't taken. The PC moves to the next instruction: offset +4.",
    "情况二：beq 跳到 End。0x1C − 0x0C = 0x10，偏移 +16，也就是往后 4 条指令。":
        "Case 2: the beq is taken and jumps to End. 0x1C − 0x0C = 0x10: offset +16, "
        "four instructions ahead.",
    "情况三：j Loop 从 0x18 跳回 0x0C。0x0C − 0x18 = −12，往回 3 条指令：偏移可以是负数。":
        "Case 3: j Loop goes from 0x18 back to 0x0C. 0x0C − 0x18 = −12, three instructions back: "
        "offsets can be negative.",
    "上一集提过位置无关代码。把整个循环搬到 0x100C：地址全变了，+16 和 −12 却一个都不用改。":
        "Last episode mentioned position-independent code. Move the whole loop to 0x100C: "
        "every address changes, yet +16 and −12 stay exactly the same.",
    "写死“跳到 0x1C”？搬家后 End 在 0x101C，跳错了！":
        "Hard-code \"jump to 0x1C\"? End has moved to 0x101C!",
    "反过来，要是指令里写死“跳到 0x1C”，一搬家就跳错了：绝对地址经不起代码搬家。":
        "Had the instruction said \"jump to 0x1C\", the move would break it. "
        "Absolute addresses break when code moves.",

    # ---- encode beq and j
    "手工汇编：beq 与 j": "Hand-Assembling beq and j",
    "现在编成机器码。先是 beq x19, x10, End，偏移 +16：上一集算过，快速过一遍。":
        "Now to machine code. First beq x19, x10, End with offset +16: "
        "we did this last episode, so here's a quick replay.",
    "接着填上 rs2 = x10、rs1 = x19、funct3 = 000、opcode = 1100011，得到 0x00A98863。":
        "Then fill in rs2 = x10, rs1 = x19, funct3 = 000 and opcode = 1100011, and we get 0x00A98863.",
    "再编码 j Loop。j 是伪指令，实际是 jal x0, Loop：返回地址写进 x0，也就是直接丢掉。":
        "Next, j Loop. j is a pseudo-instruction for jal x0, Loop: the return address goes to x0, "
        "which simply discards it.",
    "J 型的偏移有 21 位。−12 是负数，写成 21 位补码：高 17 位全是 1，最后 4 位是 0100。":
        "A J-type offset has 21 bits. −12 is negative, so in 21-bit two's complement "
        "the top 17 bits are all 1s and the last 4 bits are 0100.",
    "最低位照例不存，其余各位按 imm[20|10:1|11|19:12] 的顺序对号入座。":
        "As usual bit 0 isn't stored; the rest go to their slots in the order imm[20|10:1|11|19:12].",
    "rd = x0，写成 00000；jal 的 opcode 是 1101111。":
        "rd = x0 is 00000, and jal's opcode is 1101111.",
    "结果是 0xFF5FF06F。开头的 FF 和中间的 FF，都来自负偏移高位的那一串 1。":
        "The result is 0xFF5FF06F. The FF at the front and the FF in the middle both come "
        "from the negative offset's run of high 1s.",

    # ---- S vs B
    "S 型与 B 型：只差两位": "S vs. B: Just Two Bits Apart",
    "把 S 型和 B 型上下对齐：两者的立即数都分成两段，占着同样的位置。":
        "Line up S-type and B-type: both split the immediate into two pieces "
        "in the same places.",
    "inst[30:25] 在两者中都是 imm[10:5]，inst[11:8] 都是 imm[4:1]：含义完全相同。":
        "inst[30:25] is imm[10:5] in both, and inst[11:8] is imm[4:1] in both: identical meaning.",
    "真正换了含义的只有两位。inst[31] 在 S 型是 imm[11]，在 B 型是 imm[12]，但始终是符号位；":
        "Only two bits change meaning. inst[31] is imm[11] in S-type but imm[12] in B-type, "
        "though it's always the sign bit;",
    "inst[7] 在 S 型是 imm[0]，在 B 型是 imm[11]。硬件拼立即数时，只有这两位要分情况处理。":
        "inst[7] is imm[0] in S-type but imm[11] in B-type. When hardware builds the immediate, "
        "only these two bits need special handling.",
    "小测验：如果程序里只有 32 位指令，B 型指令的 inst[8] 是不是一定为 0？":
        "Quick check: if a program has only 32-bit instructions, is inst[8] of every B-type "
        "instruction always 0?",
    "是的。这时偏移都是 4 的倍数，imm[1] 恒为 0，而它正好存在 inst[8]。":
        "Yes. Every offset is then a multiple of 4, so imm[1] is always 0, "
        "and imm[1] is exactly what inst[8] holds.",
    "偏移以 2 字节为单位，分支不可能只挪 1 个字节；而只有 32 位指令时，能编码的目标里还有一半用不上。":
        "Offsets are in 2-byte units, so a branch can never move the PC by one byte. And with "
        "only 32-bit instructions, half of the encodable targets are unusable.",

    # ---- branching far
    "分支够不着怎么办？": "When a Branch Can't Reach",
    "示意图，未按比例": "Not to scale",
    "B 型：±4 KiB（": "B-type: ±4 KiB (",
    "条指令）": "instructions)",
    "上一集算过：B 型偏移的范围是 −4096 到 +4094 字节，约 ±4 KiB，也就是前后各 2 的 10 次方条指令。":
        "As we worked out last time, a B-type offset spans −4096 to +4094 bytes: "
        "about ±4 KiB, or 2^10 instructions either way.",
    "够不着！": "Out of range!",
    "if 和循环通常很短，这个范围绰绰有余。可要是目标 far 远在 4 KiB 之外，beq x10, x0, far 就够不着了。":
        "If statements and loops are usually short, so that's plenty. But if far is more than 4 KiB away, "
        "beq x10, x0, far can't reach it.",
    "办法：把条件取反，让分支只负责跳过一条 j。":
        "The fix: negate the condition, and let the branch just hop over a j.",
    "x10 等于 0 时，bne 不跳，执行 j far，跳到远处。":
        "If x10 is 0, the bne isn't taken; j far runs and jumps far away.",
    "x10 不等于 0 时，bne 跳过 j，直接到 next 继续。效果和原来的 beq 完全一样。":
        "If x10 isn't 0, the bne skips the j and carries on at next. "
        "Exactly what the original beq did.",
    "J 型：±1 MiB（": "J-type: ±1 MiB (",
    "j 是 J 型，偏移有 21 位，能到约 ±1 MiB，即前后各 2 的 18 次方条指令。":
        "j is J-type with a 21-bit offset: about ±1 MiB, or 2^18 instructions either way.",
    "这也是无条件跳转用 j、不用 beq x0, x0 的原因：J 型没有 rs1、rs2 和 funct3，省下的位让偏移多出 8 位，范围大 256 倍。":
        "That's also why unconditional jumps use j rather than beq x0, x0: J-type drops rs1, rs2 "
        "and funct3, so its offset gets 8 more bits: 256 times the range.",

    # ---- jumping anywhere
    "跳到任意地址": "Jumping Anywhere",
    "绝对：lui + jalr": "Absolute: lui + jalr",
    "PC 相对：auipc + jalr": "PC-relative: auipc + jalr",
    "上一集说过，auipc 配 jalr 能跳到 32 位地址空间的任何位置。其实还有一种组合：lui 配 jalr。":
        "Last episode we saw that auipc plus jalr can reach anywhere in the 32-bit address space. "
        "There's another pair too: lui plus jalr.",
    "先看绝对版本：lui 装入目标地址的高 20 位，jalr 加上低 12 位并跳过去。目标是一个固定的地址。":
        "The absolute version first: lui loads the target's upper 20 bits, and jalr adds the lower 12 "
        "and jumps. The target is one fixed address.",
    "jalr 用旧的 ra 算目标，同时把 PC + 4 写进 ra：同一个 ra 既当基址，又存返回地址。":
        "jalr computes the target from the old ra while writing PC + 4 into ra, so one register "
        "serves as both the base and the return address.",
    "auipc 版本则是 PC 相对的：ra = PC + (hi << 12)。目标跟着代码一起走，整段搬家也照样正确。":
        "The auipc version is PC-relative: ra = PC + (hi << 12). The target moves with the code, "
        "so it still works when the whole block moves.",
    "jalr  x0, lo(t1)     # PC = t1 + lo，不保存返回地址":
        "jalr  x0, lo(t1)     # PC = t1 + lo; no return address",
    "伪指令 call 展开的正是这一对。":
        "This pair is exactly what the pseudo-instruction call expands to.",
    "只想跳走、不必返回时，jalr 的 rd 改成 x0；中转寄存器也换成 t1，免得冲掉 ra 里的返回地址。":
        "To jump without returning, set jalr's rd to x0, and hold the upper part in t1 "
        "so the return address in ra survives.",
    "注意：jalr 的 12 位立即数也会符号扩展。hi 和 lo 该怎么拆？这和 li 是同一个问题。":
        "Careful: jalr's 12-bit immediate is sign-extended too. So how do we split hi and lo? "
        "It's the same question as for li.",

    # ---- li
    "高 20 位 → lui": "upper 20 bits → lui",
    "低 12 位 → addi": "lower 12 bits → addi",
    "练习：li 与大常数": "Practice: li with Big Constants",
    "用笔记里的两道题，练练上一集的 lui + addi。先交代一句：常数在 −2048 到 2047 之间时，li 只需一条 addi。":
        "Let's practice last episode's lui + addi on two examples from the notes. "
        "One thing first: for a constant between −2048 and 2047, li needs just one addi.",
    "练习一：li x10, 0x87654321。高 20 位 0x87654 交给 lui，低 12 位 0x321 交给 addi。":
        "Example 1: li x10, 0x87654321. The upper 20 bits, 0x87654, go to lui; "
        "the lower 12 bits, 0x321, go to addi.",
    "lui 先得到 0x87654000。0x321 的最高位是 0，符号扩展后不变，一加正好是 0x87654321。":
        "lui gives 0x87654000. The top bit of 0x321 is 0, so sign extension leaves it alone, "
        "and the sum is exactly 0x87654321.",
    "顺手汇编成机器码：lui 是 U 型，opcode 为 0110111（auipc 是 0010111），得到 0x87654537；addi 则是 0x32150513。":
        "While we're here, the machine code: lui is U-type with opcode 0110111 (auipc's is 0010111), "
        "giving 0x87654537; the addi is 0x32150513.",
    "练习二：li x10, 0xB0BACAFE。照葫芦画瓢，写成 lui x10, 0xB0BAC 和 addi x10, x10, 0xAFE？":
        "Example 2: li x10, 0xB0BACAFE. Same recipe: lui x10, 0xB0BAC, "
        "then addi x10, x10, 0xAFE?",
    "问题出在 0xAFE：它的最高位是 1，作为 12 位补码是负数，会被符号扩展成 0xFFFFFAFE。":
        "The trouble is 0xAFE: its top bit is 1, so as a 12-bit two's complement number it's negative, "
        "and it's sign-extended to 0xFFFFFAFE.",
    "高 20 位少了 1！": "Upper 20 bits are 1 short!",
    "0xB0BAC000 + 0xFFFFFAFE = 0xB0BABAFE：高 20 位少了 1！":
        "0xB0BAC000 + 0xFFFFFAFE = 0xB0BABAFE: the upper 20 bits come out 1 short!",
    "因为 0xFFFFFAFE 等于 0xAFE − 0x1000：加上它，就是加 0xAFE 再减 0x1000，正好从高 20 位扣掉 1。":
        "Because 0xFFFFFAFE equals 0xAFE − 0x1000. Adding it adds 0xAFE and subtracts 0x1000, "
        "which takes exactly 1 off the upper 20 bits.",
    "正确！": "Correct!",
    "所以要预先给高 20 位加 1：lui x10, 0xB0BAD。0xB0BAD000 + 0xFFFFFAFE = 0xB0BACAFE，对了。":
        "So add 1 to the upper 20 bits in advance: lui x10, 0xB0BAD. "
        "0xB0BAD000 + 0xFFFFFAFE = 0xB0BACAFE. Correct.",
    "低 12 位的最高位（第 11 位）是 1 → 高 20 位加 1":
        "Top bit of the lower 12 (bit 11) is 1 → add 1 to the upper 20",
    "规则：低 12 位的最高位（第 11 位）是 1，高 20 位就先加 1。写成公式：hi = (x + 0x800) >> 12。":
        "The rule: if the top bit of the lower 12 (bit 11) is 1, add 1 to the upper 20 bits. "
        "As a formula: hi = (x + 0x800) >> 12.",
    "上一节 lui 或 auipc 配 jalr，也照这条规则拆 hi 和 lo；用 auipc 时，x 是目标地址与 PC 之差。":
        "The same rule splits hi and lo for the previous section's lui or auipc plus jalr. "
        "With auipc, x is the distance from the PC to the target.",
    "2 × 32 = 64 位": "2 × 32 = 64 bits",
    "小测验：li x5, 0x44331416 编码后占多少位？":
        "Quick check: how many bits does li x5, 0x44331416 take once encoded?",
    "答案是 64 位：li 是伪指令，这里要展开成 lui 和 addi 两条指令。":
        "64 bits: li is a pseudo-instruction, and here it expands into two instructions, lui and addi.",

    # ---- recipe
    "汇编 → 二进制": "Assembly → binary",
    "① 确定指令类型：R、I、I*、S、B、U、J": "1. Identify the type: R, I, I*, S, B, U, J",
    "② 找到对应的指令格式": "2. Find that type's format",
    "③ 把寄存器和立即数转成二进制": "3. Convert registers and immediate to binary",
    "④ 按格式摆放，填上 opcode 和 funct": "4. Arrange the bits, add opcode and funct",
    "二进制 → 汇编": "Binary → assembly",
    "① 看 opcode（和 funct3/7）认出指令": "1. Identify it by opcode (and funct3/7)",
    "② 按格式把 32 位切成字段": "2. Split the 32 bits into fields",
    "③ 翻译寄存器和立即数": "3. Translate registers and immediate",
    "④ 拼出完整的汇编指令": "4. Assemble the final instruction",
    "最后把汇编与机器码的互译整理成两份清单。先看汇编 → 二进制；其中的 I* 就是第 10 集讲的移位格式。":
        "Finally, two checklists for translating between assembly and machine code. First, "
        "assembly → binary; I* is the shift format from Episode 10.",
    "第 ③ 步转寄存器时，先把 ABI 名换成编号：s0 是 x8，写作 01000；t4 是 x29，写作 11101。":
        "In step 3, first turn ABI names into register numbers: s0 is x8, written 01000; "
        "t4 is x29, written 11101.",
    "反方向就是第 10 集的反汇编，四步列在右边。手边备一张 61C 参考卡最方便。":
        "The reverse is Episode 10's disassembly, with its four steps on the right. "
        "Keep the 61C reference card handy.",
    "拿 J 型练一次：把 0xFF5FF06F 翻译回来。opcode 是 1101111，这是 jal。":
        "Let's try it on a J-type: translate 0xFF5FF06F back. The opcode is 1101111: that's jal.",
    "按 J 型切开：rd 是 00000，即 x0；立即数按 imm[20|10:1|11|19:12] 拼回去，补上最低位的 0，得 −12。":
        "Split it as J-type: rd is 00000, so x0. Reassemble the immediate as imm[20|10:1|11|19:12], "
        "append the implicit 0, and get −12.",
    "拼起来就是 jal x0, −12：正是前面编码的 j Loop。":
        "Put together: jal x0, −12. That's the j Loop we encoded earlier.",
    "（无）": "(none)",
    "笔记里还有一份整文件的对照。标签 main 没有对应的机器码；伪指令 mv a0, a5 其实是 addi a0, a5, 0。":
        "The notes also translate a whole file. The label main has no machine code, "
        "and the pseudo-instruction mv a0, a5 is really addi a0, a5, 0.",
    "最后一行 call printf 只编成了一条 jal：目标够近时，工具链会把 auipc + jalr 缩成一条 jal。":
        "The last line, call printf, became a single jal: when the target is close enough, "
        "the toolchain shrinks auipc + jalr into one jal.",
}
