"""English for episode 12 (keys are the Chinese strings in ep12_addressing.py)."""

EN = {
    # ---- end card
    "寻址方式：基址 + 偏移、PC 相对、绝对":
        "The three addressing modes are base plus displacement, PC-relative, and absolute",
    "偏移 = 目标地址 − 当前指令地址，搬家不变":
        "An offset is the target address minus this instruction's address, so moving the code "
        "doesn't change it",
    "分支太远：条件取反，跳过一条 j（±1 MiB）":
        "When a branch is too far, negate it and hop over a j, which reaches about one "
        "mebibyte either way",
    "任意地址：lui 或 auipc 配合 jalr":
        "To reach any address, use lui or auipc together with jalr",
    "拆常数：低 12 位的最高位是 1，高 20 位先加 1":
        "To split a constant, if bit eleven of the low part is one, add one to the upper "
        "twenty bits",

    # ---- addressing modes
    "三种寻址方式": "Three Addressing Modes",
    "基址 + 偏移": "Base + displacement",
    "PC 相对": "PC-relative",
    "直接给出完整地址": "Full address, given directly",
    "绝对": "Absolute",
    "其余指令：PC + 4": "Everything else: PC + 4",

    # ---- labels -> offsets
    "从标签到偏移": "From Labels to Offsets",
    "写死“跳到 0x1C”？搬家后 End 在 0x101C，跳错了！":
        "Hard-code \"jump to 0x1C\"? End has moved to 0x101C!",

    # ---- encode beq and j
    "手工汇编：beq 与 j": "Hand-Assembling beq and j",

    # ---- S vs B
    "S 型与 B 型：只差两位": "S vs. B: Just Two Bits Apart",

    # ---- branching far
    "分支够不着怎么办？": "When a Branch Can't Reach",
    "示意图，未按比例": "Not to scale",
    "B 型：±4 KiB（": "B-type: ±4 KiB (",
    "条指令）": "instructions)",
    "够不着！": "Out of range!",
    "J 型：±1 MiB（": "J-type: ±1 MiB (",

    # ---- jumping anywhere
    "跳到任意地址": "Jumping Anywhere",
    "绝对：lui + jalr": "Absolute: lui + jalr",
    "PC 相对：auipc + jalr": "PC-relative: auipc + jalr",
    "jalr  x0, lo(t1)     # PC = t1 + lo，不保存返回地址":
        "jalr  x0, lo(t1)     # PC = t1 + lo; no return address",

    # ---- li
    "高 20 位 → lui": "upper 20 bits → lui",
    "低 12 位 → addi": "lower 12 bits → addi",
    "练习：li 与大常数": "Practice: li with Big Constants",
    "高 20 位少了 1！": "Upper 20 bits are 1 short!",
    "正确！": "Correct!",
    "低 12 位的最高位（第 11 位）是 1 → 高 20 位加 1":
        "Top bit of the lower 12 (bit 11) is 1 → add 1 to the upper 20",
    "2 × 32 = 64 位": "2 × 32 = 64 bits",

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
    "（无）": "(none)",

    # ---- spoken beats and cue phrases (see references/narration-writing.md)
    "6 种指令格式已经凑齐。这一集换个角度：指令要访问的地址、要跳去的目标，是怎么算出来的？这些计算规则叫寻址方式（addressing mode）。RISC-V 主要用到三种。":
        "All six instruction formats are now in place. This episode takes a different view, "
        "asking how the address an instruction accesses, or the target it jumps to, is worked "
        "out. These calculation rules are called addressing modes, and RISC-V mainly uses "
        "three.",
    "这些计算规则叫寻址方式": "These calculation rules",
    "第一种：基址 + 偏移（base/displacement），地址 = 寄存器 + 立即数。lw 和 sw 就是这样找到数据的。jalr 也属于这一类：跳到 rs1 + 立即数。新 PC 只取决于寄存器，与 jalr 自己在哪儿无关。":
        "The first is base plus displacement, where the address is a register plus an "
        "immediate. That is how lw, together with sw, finds its data. The jalr instruction "
        "belongs here too, jumping to rs1 plus the immediate, so the new PC depends only on a "
        "register, not on where the jalr itself is.",
    "jalr 也属于这一类": "The jalr instruction belongs here too",
    "第二种：PC 相对寻址，以 PC 为基准加上偏移。条件分支、jal 和 auipc 都用它。第三种：绝对寻址，直接给出完整地址。比如 lui 装入地址的高 20 位，jalr 补上低 12 位并跳过去。":
        "The second is PC-relative addressing, which adds an offset to the PC. Conditional "
        "branches, jal, and auipc all use it. The third is absolute addressing, which gives "
        "the complete address directly. For example, lui loads the upper twenty bits of an "
        "address, and jalr adds the lower twelve and jumps.",
    "第三种：绝对寻址": "The third is absolute addressing",
    "其实几乎每条指令都以 PC 相对的方式更新 PC：普通指令 PC + 4，分支和 jal 是 PC + 偏移。只有 jalr 例外。伪指令也各有归属：j 是 jal x0 的简写，属于 PC 相对；jr 和 ret 则是 jalr 的简写。":
        "In fact, almost every instruction updates the PC in a PC-relative way. An ordinary "
        "instruction adds four, and branches and jal add an offset. Only jalr is the "
        "exception. Pseudo-instructions have their homes too, where j is shorthand for jal x0 "
        "and is PC-relative, while jr and ret are shorthand for jalr.",
    "伪指令也各有归属": "Pseudo-instructions have their homes too",
    "只有 jalr 例外": "Only jalr is the exception",
    "来算几个具体的偏移。这是课程笔记里的循环，每条指令都标了示例地址：beq 在 0x0C。标签不是指令，机器码里根本没有 Loop 和 End。汇编器得把它们换算成相对 PC 的偏移。":
        "Let's work out some concrete offsets. This is the loop from the course notes, with "
        "an example address on every instruction, and beq is at 0x0C. A label isn't an "
        "instruction, so there is no Loop or End in the machine code, and the assembler has "
        "to convert them into offsets relative to the PC.",
    "标签不是指令": "A label isn't an instruction",
    "情况一：beq 不跳。PC 走到下一条，偏移是 +4。情况二：beq 跳到 End。0x1C − 0x0C = 0x10，偏移 +16，也就是往后 4 条指令。情况三：j Loop 从 0x18 跳回 0x0C。0x0C − 0x18 = −12，往回 3 条指令：偏移可以是负数。":
        "In case one, beq doesn't branch, and the PC just moves to the next instruction, so "
        "the offset is plus four. In case two, beq jumps to End, where 0x1C minus 0x0C is "
        "0x10, so the offset is plus sixteen, four instructions ahead. In case three, j Loop "
        "jumps from 0x18 back to 0x0C, which is minus twelve, three instructions back, so an "
        "offset can be negative.",
    "情况二": "In case two",
    "情况三": "In case three",
    "上一集提过位置无关代码。把整个循环搬到 0x100C：地址全变了，+16 和 −12 却一个都不用改。反过来，要是指令里写死“跳到 0x1C”，一搬家就跳错了：绝对地址经不起代码搬家。":
        "Remember position-independent code from the last episode. Move the whole loop to "
        "0x100C, and every address changes, but plus sixteen and minus twelve don't need to "
        "change at all. Conversely, if an instruction had a jump to 0x1C hard-wired into it, "
        "moving house would send it to the wrong place, because an absolute address can't "
        "survive a move.",
    "反过来": "Conversely",
    "一个都不用改": "don't need to change at all",
    "现在编成机器码。先是 beq x19, x10, End，偏移 +16：上一集算过，快速过一遍。接着填上 rs2 = x10、rs1 = x19、funct3 = 000、opcode = 1100011，得到 0x00A98863。":
        "Now let's encode them. First comes beq x19, x10, End, with an offset of plus "
        "sixteen, which we worked out last episode, so let's go through it quickly. Then we "
        "fill in rs2 as x10, rs1 as x19, funct3 as zero zero zero, and the opcode as one one "
        "zero zero zero one one, which gives 0x00A98863.",
    "再编码 j Loop。j 是伪指令，实际是 jal x0, Loop：返回地址写进 x0，也就是直接丢掉。J 型的偏移有 21 位。−12 是负数，写成 21 位补码：高 17 位全是 1，最后 4 位是 0100。":
        "Next we encode j Loop. The j is a pseudo-instruction, really jal x0, Loop, which "
        "writes the return address into x0, so it is simply thrown away. The offset in the J "
        "format is twenty-one bits. Minus twelve is negative, so as a twenty-one bit two's "
        "complement number, its upper seventeen bits are all ones, and its last four bits are "
        "zero one zero zero.",
    "J 型的偏移有 21 位": "The offset in the J format",
    "最低位照例不存，其余各位按 imm[20|10:1|11|19:12] 的顺序对号入座。rd = x0，写成 00000；jal 的 opcode 是 1101111。结果是 0xFF5FF06F。开头的 FF 和中间的 FF，都来自负偏移高位的那一串 1。":
        "As usual the lowest bit isn't stored, and the other bits go into their places in the "
        "order imm[20|10:1|11|19:12]. Then rd is x0, which is five zeros, and the opcode of "
        "jal is one one zero one one one one. The result is 0xFF5FF06F, where the FF at the "
        "start and the FF in the middle both come from the long run of ones in the upper bits "
        "of the negative offset.",
    "把 S 型和 B 型上下对齐：两者的立即数都分成两段，占着同样的位置。inst[30:25] 在两者中都是 imm[10:5]，inst[11:8] 都是 imm[4:1]：含义完全相同。":
        "Line up the S format and the B format, one above the other. In both, the immediate "
        "is split into two pieces in the same places. In both, inst[30:25] is imm[10:5], and "
        "inst[11:8] is imm[4:1], so they mean exactly the same thing.",
    "inst[30:25] 在两者中": "In both, inst[30:25]",
    "真正换了含义的只有两位。inst[31] 在 S 型是 imm[11]，在 B 型是 imm[12]，但始终是符号位；inst[7] 在 S 型是 imm[0]，在 B 型是 imm[11]。硬件拼立即数时，只有这两位要分情况处理。":
        "Only two bits really change meaning. The bit inst[31] is imm[11] in the S format and "
        "imm[12] in the B format, but it is always the sign bit. And inst[7] is imm[0] in S "
        "and imm[11] in B. When the hardware assembles the immediate, only these two bits "
        "need special handling.",
    "inst[7] 在 S 型": "And inst[7]",
    "小测验：如果程序里只有 32 位指令，B 型指令的 inst[8] 是不是一定为 0？是的。这时偏移都是 4 的倍数，imm[1] 恒为 0，而它正好存在 inst[8]。偏移以 2 字节为单位，分支不可能只挪 1 个字节；而只有 32 位指令时，能编码的目标里还有一半用不上。":
        "A quick quiz. If a program contains only thirty-two bit instructions, is inst[8] of "
        "a B-type instruction always zero? Yes. The offsets are then all multiples of four, "
        "so imm[1] is always zero, and it happens to be stored at inst[8]. Offsets count in "
        "units of two bytes, so a branch can't move by just one byte, but with only thirty- "
        "two bit instructions, half of the encodable targets go unused.",
    "是的": "Yes",
    "上一集算过：B 型偏移的范围是 −4096 到 +4094 字节，约 ±4 KiB，也就是前后各 2 的 10 次方条指令。if 和循环通常很短，这个范围绰绰有余。可要是目标 far 远在 4 KiB 之外，beq x10, x0, far 就够不着了。":
        "Last episode we worked out that the range of a B-type offset is minus 4096 to plus "
        "4094 bytes, about four kibibytes either way, or roughly a thousand instructions each "
        "way. Ifs and loops are usually short, so this range is more than enough. But if the "
        "target, far, is beyond four kibibytes, then beq x10, x0, far can't reach it.",
    "if 和循环通常很短": "Ifs and loops are usually short",
    "beq x10, x0, far 就够不着了": "then beq x10, x0, far can't reach it",
    "办法：把条件取反，让分支只负责跳过一条 j。x10 等于 0 时，bne 不跳，执行 j far，跳到远处。x10 不等于 0 时，bne 跳过 j，直接到 next 继续。效果和原来的 beq 完全一样。":
        "The fix is to invert the condition, so that the branch only has to hop over a j. "
        "When x10 equals zero, the bne doesn't jump, and executes the j far, which goes to "
        "the distant target. When x10 isn't zero, the bne skips over the j and carries on at "
        "next, and the effect is exactly the same as the original beq.",
    "x10 等于 0 时": "When x10 equals zero",
    "x10 不等于 0 时": "When x10 isn't zero",
    "执行 j far": "and executes the j far",
    "跳到远处": "which goes to the distant target",
    "直接到 next 继续": "and carries on at next",
    "j 是 J 型，偏移有 21 位，能到约 ±1 MiB，即前后各 2 的 18 次方条指令。这也是无条件跳转用 j、不用 beq x0, x0 的原因：J 型没有 rs1、rs2 和 funct3，省下的位让偏移多出 8 位，范围大 256 倍。":
        "The j is a J format, with a twenty-one bit offset, reaching about one mebibyte "
        "either way, or roughly two to the eighteenth instructions each way. That is also why "
        "an unconditional jump uses j rather than beq x0, x0. The J format has no rs1, rs2, "
        "or funct3, and the bits saved give the offset eight more bits, making the range two "
        "hundred fifty-six times bigger.",
    "这也是无条件跳转": "That is also why",
    "上一集说过，auipc 配 jalr 能跳到 32 位地址空间的任何位置。其实还有一种组合：lui 配 jalr。先看绝对版本：lui 装入目标地址的高 20 位，jalr 加上低 12 位并跳过去。目标是一个固定的地址。":
        "As we said last episode, auipc with jalr can reach anywhere in the thirty-two bit "
        "address space. There is another combination too, lui with jalr. Let's look at the "
        "absolute version first. There, lui loads the upper twenty bits of the target "
        "address, and jalr adds the lower twelve and jumps, so the target is a fixed address.",
    "先看绝对版本": "Let's look at the absolute version",
    "jalr 用旧的 ra 算目标，同时把 PC + 4 写进 ra：同一个 ra 既当基址，又存返回地址。auipc 版本则是 PC 相对的：ra = PC + (hi << 12)。目标跟着代码一起走，整段搬家也照样正确。":
        "The jalr uses the old ra to work out its target, and writes PC plus four into ra at "
        "the same time. So one ra is both the base and the place the return address goes. The "
        "auipc version is PC-relative, with ra equal to PC plus hi shifted left by twelve, so "
        "the target travels with the code, and stays correct even if the whole block moves.",
    "auipc 版本则是 PC 相对的": "The auipc version",
    "伪指令 call 展开的正是这一对。只想跳走、不必返回时，jalr 的 rd 改成 x0；中转寄存器也换成 t1，免得冲掉 ra 里的返回地址。注意：jalr 的 12 位立即数也会符号扩展。hi 和 lo 该怎么拆？这和 li 是同一个问题。":
        "The pseudo-instruction call expands into exactly this pair. If we only want to jump "
        "away and never come back, the rd of jalr becomes x0. The middle register also "
        "changes to t1, so we don't wipe out the return address in ra. Note that the twelve- "
        "bit immediate of jalr is also sign-extended, so how do we split hi and lo? That is "
        "the same problem as li.",
    "只想跳走": "If we only want to jump away",
    "注意：jalr": "Note that the twelve-bit immediate",
    "用笔记里的两道题，练练上一集的 lui + addi。先交代一句：常数在 −2048 到 2047 之间时，li 只需一条 addi。练习一：li x10, 0x87654321。高 20 位 0x87654 交给 lui，低 12 位 0x321 交给 addi。":
        "Let's practice last episode's lui plus addi with two problems from the notes. First, "
        "when the constant is between minus two thousand forty-eight and two thousand forty- "
        "seven, li needs only one addi. Exercise one is li x10, 0x87654321. The upper twenty "
        "bits, 0x87654, go to lui, and the lower twelve bits, 0x321, go to addi.",
    "练习一": "Exercise one",
    "lui 先得到 0x87654000。0x321 的最高位是 0，符号扩展后不变，一加正好是 0x87654321。顺手汇编成机器码：lui 是 U 型，opcode 为 0110111（auipc 是 0010111），得到 0x87654537；addi 则是 0x32150513。":
        "The lui first gives 0x87654000. The top bit of 0x321 is zero, so sign extension "
        "changes nothing, and adding it gives exactly 0x87654321. For the machine code, lui "
        "is a U format with opcode zero one one zero one one one, while auipc is zero zero "
        "one zero one one one. That gives 0x87654537, and the addi is 0x32150513.",
    "顺手汇编成机器码": "For the machine code",
    "练习二：li x10, 0xB0BACAFE。照葫芦画瓢，写成 lui x10, 0xB0BAC 和 addi x10, x10, 0xAFE？问题出在 0xAFE：它的最高位是 1，作为 12 位补码是负数，会被符号扩展成 0xFFFFFAFE。0xB0BAC000 + 0xFFFFFAFE = 0xB0BABAFE：高 20 位少了 1！":
        "Exercise two is li x10, 0xB0BACAFE. Following the same pattern, we would write lui "
        "x10, 0xB0BAC and addi x10, x10, 0xAFE. But there is a problem with 0xAFE. Its top "
        "bit is a one, so as a twelve-bit two's complement number it is negative, and gets "
        "sign-extended to 0xFFFFFAFE. So adding it gives 0xB0BABAFE, and the upper twenty "
        "bits are short by one!",
    "问题出在 0xAFE": "But there is a problem with 0xAFE",
    "0xB0BAC000 + 0xFFFFFAFE": "So adding it",
    "因为 0xFFFFFAFE 等于 0xAFE − 0x1000：加上它，就是加 0xAFE 再减 0x1000，正好从高 20 位扣掉 1。所以要预先给高 20 位加 1：lui x10, 0xB0BAD。0xB0BAD000 + 0xFFFFFAFE = 0xB0BACAFE，对了。":
        "That is because 0xFFFFFAFE is 0xAFE minus 0x1000, so adding it means adding 0xAFE "
        "and then subtracting 0x1000, which takes exactly one off the upper twenty bits. So "
        "we must add one to the upper twenty bits beforehand, with lui x10, 0xB0BAD, and now "
        "the sum comes out as 0xB0BACAFE, which is right.",
    "所以要预先给高 20 位加 1": "So we must add one",
    "对了": "which is right",
    "规则：低 12 位的最高位（第 11 位）是 1，高 20 位就先加 1。写成公式：hi = (x + 0x800) >> 12。上一节 lui 或 auipc 配 jalr，也照这条规则拆 hi 和 lo；用 auipc 时，x 是目标地址与 PC 之差。":
        "The rule is that if the top bit of the low twelve bits, which is bit eleven, is one, "
        "we add one to the upper twenty bits first. As a formula, hi equals x plus 0x800, "
        "shifted right by twelve. Splitting hi and lo for lui or auipc with jalr in the last "
        "section follows the same rule, and with auipc, x is the difference between the "
        "target address and the PC.",
    "上一节 lui 或 auipc 配 jalr": "Splitting hi and lo",
    "小测验：li x5, 0x44331416 编码后占多少位？答案是 64 位：li 是伪指令，这里要展开成 lui 和 addi 两条指令。":
        "A quick quiz. How many bits does li x5, 0x44331416 take once encoded? The answer is "
        "sixty-four bits, because li is a pseudo-instruction, and here it expands into two "
        "instructions, lui and addi.",
    "答案是 64 位": "The answer is sixty-four bits",
    "最后把汇编与机器码的互译整理成两份清单。先看汇编 → 二进制；其中的 I* 就是第 10 集讲的移位格式。第 ③ 步转寄存器时，先把 ABI 名换成编号：s0 是 x8，写作 01000；t4 是 x29，写作 11101。":
        "Finally, let's sum up translating between assembly and machine code in two "
        "checklists. First, assembly to binary, where the I-star is the shift format from "
        "episode ten. In step three, when converting registers, first change the ABI name "
        "into a number. So s0 is x8, written zero one zero zero zero, and t4 is x29, written "
        "one one one zero one.",
    "第 ③ 步转寄存器时": "In step three",
    "反方向就是第 10 集的反汇编，四步列在右边。手边备一张 61C 参考卡最方便。":
        "The reverse direction is the disassembly from episode ten, with its four steps "
        "listed on the right. It is handy to keep a 61C reference card nearby.",
    "拿 J 型练一次：把 0xFF5FF06F 翻译回来。opcode 是 1101111，这是 jal。按 J 型切开：rd 是 00000，即 x0；立即数按 imm[20|10:1|11|19:12] 拼回去，补上最低位的 0，得 −12。拼起来就是 jal x0, −12：正是前面编码的 j Loop。":
        "Let's practice once with the J format, translating 0xFF5FF06F back. The opcode is "
        "one one zero one one one one, so this is jal. Cutting it as a J format, rd is five "
        "zeros, which is x0. Putting the immediate back together in the order "
        "imm[20|10:1|11|19:12], and adding the lowest bit, a zero, gives minus twelve. Put "
        "together, it is jal x0, minus twelve, which is exactly the j Loop we encoded "
        "earlier.",
    "按 J 型切开": "Cutting it as a J format",
    "拼起来就是": "Put together",
    "opcode 是 1101111": "The opcode is",
    "rd 是 00000": "rd is five zeros",
    "立即数按": "Putting the immediate back",
    "得 −12": "gives minus twelve",
    "笔记里还有一份整文件的对照。标签 main 没有对应的机器码；伪指令 mv a0, a5 其实是 addi a0, a5, 0。最后一行 call printf 只编成了一条 jal：目标够近时，工具链会把 auipc + jalr 缩成一条 jal。":
        "The notes also have a whole-file comparison. The label main has no corresponding "
        "machine code, and the pseudo-instruction mv a0, a5 is really addi a0, a5, 0. The "
        "last line, call printf, compiled into just one jal. When the target is near enough, "
        "the toolchain shrinks the auipc plus jalr pair into one jal.",
    "最后一行 call printf": "The last line",
    "标签 main 没有对应的机器码": "The label main",
    "伪指令 mv a0, a5": "and the pseudo-instruction mv",
    "接着填上": "Then we fill in",
    "rd = x0，写成": "Then rd is x0",
    "结果是 0xFF5FF06F": "The result is",
}
