"""English for episode 10 (keys are the Chinese strings in ep10_decoding.py)."""

EN = {
    # ---- end card
    "反汇编：先看 opcode 定格式，再切字段、定操作、译寄存器":
        "To disassemble, use the opcode to find the format, then cut the fields, find the "
        "operation, and name the registers",
    "第 30 位是开关：add/sub、srl/sra、srli/srai":
        "Bit thirty is a switch that separates add from sub, srl from sra, and srli from srai",
    "I 型有 4 个 opcode：立即数运算、load、jalr、ecall/ebreak":
        "The I format has four opcodes, for immediate arithmetic, loads, jalr, and ecall with "
        "ebreak",
    "funct3 成对复用：addi 与 add，lw 与 sw（没有 subi）":
        "The funct3 codes are shared in pairs, such as addi with add, and lw with sw, and "
        "there is no subi",

    # ---- binaries are ISA-bound
    "本课程": "this course",
    "多数手机": "most phones",
    "多数电脑": "most PCs",
    "4 字节": "4 bytes",
    "2 字节": "2 bytes",
    "1981 年": "1981",
    "x86 电脑": "x86 PC",

    # ---- disassembly
    "反汇编：从机器码到汇编": "Disassembly: machine code → assembly",
    "R 型": "R-type",
    "I 型": "I-type",
    "S 型": "S-type",
    "寄存器之间运算": "register–register ops",
    "立即数运算": "immediate ops",
    "转成二进制，看 opcode 定格式": "Binary, then opcode → format",
    "按格式切分字段": "Split into fields",
    "由 funct3、funct7 定操作": "funct3, funct7 → operation",
    "寄存器编号换成名字": "Register numbers → names",
    "所有格式通用": "same for all formats",
    "因格式而异": "format-specific",
    "反汇编的四个步骤": "Disassembly in four steps",

    # ---- bit 30
    "第 30 位：一个开关": "Bit 30: a flag",
    "opcode 7 位 + funct3 3 位 + funct7 7 位 = 17 位":
        "opcode 7 bits + funct3 3 bits + funct7 7 bits = 17 bits",
    "第 30 位": "bit 30",
    "以 8 位为例，右移 2 位：": "8-bit example, shifted right by 2:",

    # ---- the I-type family
    "I 型全家": "The I-type family",
    "间接跳转": "indirect jump",
    "系统": "system",
    "操作系统": "operating system",
    "调试器": "debugger",
    "字节": "byte",
    "半字": "halfword",
    "字": "word",
    "字节，无符号": "byte, unsigned",
    "半字，无符号": "halfword, unsigned",
    "RV32 也没有 lwu：一个字正好填满 32 位的寄存器":
        "RV32 has no lwu either: a word exactly fills a 32-bit register",
    "lw   t0, 8(t1)     # 地址 = t1 + 8": "lw   t0, 8(t1)     # address = t1 + 8",
    "jalr ra, t1, 8     # 跳到 t1 + 8": "jalr ra, t1, 8     # jump to t1 + 8",
    "都要算 rs1 + imm：复用同一个加法器": "All compute rs1 + imm, so they share one adder",

    # ---- jalr and ret
    "jalr 与函数返回": "jalr and returning",

    # ---- S-type example
    "S 型：拆开的立即数": "S-type: a split immediate",

    # ---- quiz
    "小测验": "Quick check",

    # ---- spoken beats and cue phrases (see references/narration-writing.md)
    "第 2 集说过，x86、ARM、RISC-V 是三种不同的指令集。同一行 C 代码，交给三种编译器，得到的机器码完全不同。手机里多是 ARM 芯片，电脑里多是 x86。":
        "Back in episode two, we said that x86, ARM, and RISC-V are three different "
        "instruction sets. Give the same line of C to three compilers, and the machine code "
        "that comes out is completely different. Most phones use ARM chips, and most "
        "computers use x86.",
    "得到的机器码完全不同": "the machine code that comes out",
    "连长度都不一样：x86 的指令有长有短，这一条只有 2 个字节。RISC-V 的指令则一律 32 位，和数据字一样宽：取指令和读数据能共用同一套内存硬件。":
        "Even the lengths differ, since x86 instructions come in different sizes, and this "
        "one is only two bytes. RISC-V instructions are always thirty-two bits, as wide as a "
        "data word, so fetching an instruction and reading data can share one piece of memory "
        "hardware.",
    "RISC-V 的指令则一律 32 位": "RISC-V instructions are always",
    "所以程序的二进制文件和指令集是绑定的：RISC-V 的可执行文件，在 Intel 的 x86 电脑上根本跑不起来。不过，同一个指令集常常向后兼容：今天的 x86 处理器，仍能运行 1981 年为 Intel 8088 写的程序。":
        "So a program's binary is tied to its instruction set. A RISC-V executable simply "
        "cannot run on an Intel x86 computer. However, an instruction set is often backward "
        "compatible, and today's x86 processors can still run programs written in nineteen "
        "eighty-one for the Intel eight oh eight eight.",
    "不过，同一个指令集常常向后兼容": "However, an instruction set is often",
    "RISC-V 的可执行文件": "A RISC-V executable",
    "根本跑不起来": "simply cannot run",
    "今天的 x86 处理器": "today's x86 processors",
    "仍能运行": "can still run",
    "上一集把汇编翻译成机器码；这一集反过来：拿到机器码，怎么读回汇编？这叫反汇编（disassembly）。拿这个字练手：0x01B342B3。":
        "The last episode translated assembly into machine code, and this episode goes the "
        "other way. Given machine code, how do we read it back as assembly? That is called "
        "disassembly. Let's practice on this word, 0x01B342B3.",
    "拿这个字练手": "Let's practice on this word",
    "第一步：换成二进制。每个十六进制数字，正好展开成 4 位。接着找 opcode：不管哪种格式，它永远占最低的 7 位。每种格式都有自己专属的一组 opcode。查表：0110011，是 R 型。":
        "Step one is to convert to binary, where each hexadecimal digit expands into exactly "
        "four bits. Next we find the opcode, which, in every format, always occupies the "
        "lowest seven bits. Every format has its own set of opcodes, so we look it up, and "
        "zero one one zero zero one one is an R-type.",
    "接着找 opcode": "Next we find the opcode",
    "每种格式都有自己专属的一组 opcode": "Every format has its own",
    "每个十六进制数字，正好展开成": "where each hexadecimal digit",
    "查表": "so we look it up",
    "是 R 型": "is an R-type",
    "第二步：知道了格式，才知道其余 25 位怎么切。按 R 型切开：funct7、rs2、rs1、funct3、rd。":
        "Step two. Once we know the format, we know how to cut the other twenty-five bits. "
        "Cut as an R-type, they are funct7, rs2, rs1, funct3, and rd.",
    "第三步：funct3 = 100，funct7 = 0000000。查 R 型的表：这是 xor。注意：助记符（mnemonic）xor 不存放在任何一个字段里，而是由 opcode、funct3、funct7 共同决定。":
        "Step three. The funct3 is one zero zero and the funct7 is all zeros, and looking up "
        "the R-type table, this is xor. Note that the mnemonic xor isn't stored in any one "
        "field, but is decided together by the opcode, funct3, and funct7.",
    "注意：助记符": "Note that the mnemonic",
    "查 R 型的表": "and looking up the R-type table",
    "这是 xor": "this is xor",
    "第四步：寄存器字段是 5 位无符号数：rd = 00101 = 5，rs1 = 00110 = 6，rs2 = 11011 = 27。再换成寄存器名：x5 是 t0，x6 是 t1，x27 是 s11。拼起来：xor t0, t1, s11。":
        "Step four. The register fields are five-bit unsigned numbers. So rd is zero zero one "
        "zero one, which is five, rs1 is zero zero one one zero, which is six, and rs2 is one "
        "one zero one one, which is twenty-seven. Converting to register names, x5 is t0, x6 "
        "is t1, and x27 is s11. Put together, we get xor t0, t1, s11.",
    "再换成寄存器名": "Converting to register names",
    "拼起来": "Put together",
    "小心顺序：汇编里写 rd, rs1, rs2，而字段从左到右是 rs2, rs1, rd，正好相反。":
        "Be careful about the order. In assembly we write rd, rs1, rs2, but the fields run "
        "from left to right as rs2, rs1, rd, which is exactly the reverse.",
    "反汇编就这四步。前两步对任何格式都一样，后两步因格式而异。":
        "That is all there is to disassembly, just four steps. The first two are the same for "
        "every format, and the last two depend on the format.",
    "前两步对任何格式都一样": "The first two are the same",
    "回头看完整的 R 型表：10 条指令共用一个 opcode，funct3 却只有 8 种。funct3 相同的有两对：add 和 sub 都是 000，srl 和 sra 都是 101。区分它们靠 funct7。funct7 也只有两种取值，而且只差一位：第 30 位。":
        "Looking back at the full R-type table, ten instructions share one opcode, but funct3 "
        "has only eight values. Two pairs have the same funct3, add and sub are both zero "
        "zero zero, and srl and sra are both one zero one. The funct7 field tells them apart, "
        "and it also has only two values, which differ in just one bit, bit thirty.",
    "funct3 相同的有两对": "Two pairs have the same",
    "区分它们靠 funct7": "The funct7 field tells them apart",
    "光为区分运算就动用了 17 位，明显有富余。但让字段位置对齐，比省下几位更重要。":
        "Just telling the operations apart uses seventeen bits, which is clearly more than "
        "needed. But keeping the field positions aligned matters more than saving a few bits.",
    "以 add t0, t1, s11 为例：把第 30 位从 0 翻成 1，它就变成了 sub t0, t1, s11。add 和 sub 共用一个加法器。第 30 位就是个开关（flag）：为 1 时先把 rs2 取负（按位取反再加 1），再相加。":
        "Take add t0, t1, s11 as an example. Flip bit thirty from zero to one, and it becomes "
        "sub t0, t1, s11. Add and sub share one adder, and bit thirty is just a switch, a "
        "flag. When it is one, rs2 is first negated, by flipping its bits and adding one, and "
        "then the two are added.",
    "add 和 sub 共用一个加法器": "Add and sub share one adder",
    "把第 30 位从 0 翻成 1": "Flip bit thirty",
    "它就变成了": "and it becomes sub",
    "为 1 时先把 rs2 取负": "When it is one",
    "funct3 换成 101 就是右移。第 30 位为 0 是 srl：逻辑右移，空出的高位补 0。第 30 位为 1 就成了 sra：算术右移，高位补的是符号位。这回，这个开关管的是符号扩展。":
        "Change funct3 to one zero one, and it becomes a right shift. With bit thirty at zero "
        "it is srl, a logical right shift, which fills the vacated high bits with zeros. With "
        "bit thirty at one it becomes sra, an arithmetic right shift, which fills the high "
        "bits with the sign bit. This time the switch controls sign extension.",
    "第 30 位为 1 就成了 sra": "With bit thirty at one",
    "逻辑右移": "a logical right shift",
    "空出的高位补 0": "which fills the vacated",
    "高位补的是符号位": "which fills the high bits with",
    "这回，这个开关管的是符号扩展": "This time the switch",
    "移位立即数用的是 I 型的一个变体，CS61C 叫它 I* 型：移位量最多 31，只占立即数的低 5 位。":
        "Shift immediates use a variant of the I format, which CS61C calls I-star, where the "
        "shift amount is at most thirty-one and takes only the low five bits of the "
        "immediate.",
    "移位量最多 31": "where the shift amount",
    "立即数的高 7 位不当数值用，而是像 funct7 一样当开关：srai 的这 7 位是 0100000，开关依旧是第 30 位。关掉第 30 位就是 srli。左移只有逻辑移位一种，所以 slli 的这一位永远是 0。":
        "The upper seven bits of the immediate aren't used as a number, but as a switch, just "
        "like funct7. For srai those seven bits are zero one zero zero zero zero zero, and "
        "the switch is still bit thirty. Turn bit thirty off and you get srli. There is only "
        "one kind of left shift, the logical one, so for slli this bit is always zero.",
    "关掉第 30 位就是 srli": "Turn bit thirty off",
    "I 型不只有 addi。把立即数运算和 R 型并排：funct3 一一对应，addi 对 add，xori 对 xor，slti 对 slt，唯独没有 subi：要减一个常数，addi 一个负数就行。":
        "The I format is more than addi. Put the immediate operations next to the R-type, and "
        "funct3 matches one to one, so addi pairs with add, xori with xor, slti with slt, and "
        "so on. The only one missing is subi, since to subtract a constant, you just addi a "
        "negative number.",
    "唯独没有 subi": "The only one missing",
    "3 位的 funct3 只有 8 种编码，这里已经全部用光，srli 和 srai 还得靠第 30 位来区分。":
        "The three-bit funct3 has only eight encodings, and all of them are used up here, so "
        "srli, along with srai, still has to be told apart by bit thirty.",
    "5 种 load 也要靠 funct3 区分，只好另开一个 opcode。算下来，I 型一共有 4 个 opcode。":
        "The five loads also need funct3 to tell them apart, so they get an opcode of their "
        "own. All told, the I format uses four opcodes.",
    "ecall（environment call，环境调用）向操作系统请求服务，比如输出文字、结束程序。ebreak 则把控制权交给调试器：调试器里的断点，就是靠它实现的。":
        "The ecall instruction, short for environment call, asks the operating system for a "
        "service, such as printing text or ending the program. The ebreak instruction hands "
        "control to the debugger, and that is how breakpoints in a debugger are implemented.",
    "向操作系统请求服务": "asks the operating system",
    "把控制权交给调试器": "hands control to the debugger",
    "这两条都没有操作数：ecall 除了 opcode 全是 0；ebreak 只是在立即数的最低位多了一个 1。":
        "Neither of these has operands. Ecall is all zeros apart from the opcode, and ebreak "
        "just has an extra one in the lowest bit of the immediate.",
    "ecall 除了 opcode 全是 0": "Ecall is all zeros",
    "ebreak 只是在立即数的最低位": "and ebreak just has",
    "load 和 store 的 funct3 也是配套的：lb 和 sb 是 000，lh 和 sh 是 001，lw 和 sw 是 010。lbu、lhu 没有对应的 store：store 只写入指定的字节，不涉及扩展。同理，RV32 也没有 lwu。":
        "The funct3 values for loads and stores are matched too. The pair lb and sb uses zero "
        "zero zero, lh and sh uses zero zero one, and lw and sw uses zero one zero. The lbu "
        "and lhu instructions have no matching store, because a store writes only the bytes "
        "it is given and involves no extension, and for the same reason RV32 has no lwu.",
    "lbu、lhu 没有对应的 store": "The lbu and lhu instructions",
    "lb 和 sb 是 000": "The pair lb and sb",
    "load 和 jalr 为什么也用 I 型？它们都要先算 rs1 + 立即数：一个算地址，一个算跳转目标，正好复用同一个加法器。":
        "Why do loads and jalr use the I format too? Both first compute rs1 plus the "
        "immediate, one to get an address and the other to get a jump target, so they can "
        "reuse the same adder.",
    "它们都要先算": "Both first compute",
    "jalr rd, rs1, imm（也写作 jalr rd, imm(rs1)）：先把 PC + 4 存进 rd，再跳到 rs1 + imm。":
        "The jalr instruction first stores PC plus four into rd, and then jumps to rs1 plus "
        "the immediate.",
    "第 7 集的 ret 和 jr ra 都是伪指令，没有自己的 opcode：汇编器把它们都翻译成 jalr x0, ra, 0。rd 取 x0，是因为返回时不需要再留下返回地址：写进 x0 的值会被直接丢掉。":
        "In episode seven, ret and jr ra were pseudo-instructions with no opcode of their "
        "own, and the assembler turns them both into jalr x0, ra, 0. The rd is x0 because on "
        "a return we don't need to leave a return address, and whatever is written into x0 is "
        "simply thrown away.",
    "rd 取 x0": "The rd is x0",
    "编码：立即数 0，rs1 = ra = x1，rd = x0。jalr 只有一条，funct3 其实用不上，按格式填 000。opcode 是 1100111。合起来就是 0x00008067：在反汇编结果里见到它，就知道函数要返回了。":
        "For the encoding, the immediate is zero, rs1 is ra, which is x1, and rd is x0. There "
        "is only one jalr, so funct3 isn't really needed, and we fill in zero zero zero as "
        "the format requires. The opcode is one one zero zero one one one, and together this "
        "is 0x00008067. When you see it in a disassembly, you know a function is about to "
        "return.",
    "再来一个 S 型的例子：sw x14, 36(x2)。36 的 12 位二进制是 0000 0010 0100。高 7 位 0000001 放进 imm[11:5]，低 5 位 00100 放进 imm[4:0]。":
        "Here is another S-format example, sw x14, 36(x2). The number thirty-six in twelve- "
        "bit binary is zero zero zero zero, zero zero one zero, zero one zero zero. The upper "
        "seven bits, zero zero zero zero zero zero one, go into imm[11:5], and the lower five "
        "bits, zero zero one zero zero, go into imm[4:0].",
    "36 的 12 位二进制": "The number thirty-six",
    "为什么要拆？只用 funct7 的 7 位，只能表示 128 个值；store 没有 rd，正好借用 rd 的 5 位，凑满 12 位。其余照旧：rs2 = x14，rs1 = x2，funct3 = 010 表示 sw，opcode 是 0100011。":
        "Why split it? If we used only the seven bits of funct7, we could represent just a "
        "hundred twenty-eight values. A store has no rd, so it borrows the five bits of rd to "
        "make up all twelve. Everything else stays as before, rs2 is x14, rs1 is x2, funct3 "
        "is zero one zero for sw, and the opcode is zero one zero zero zero one one.",
    "结果是 0x02E12223。反汇编时就反过来：把两段拼回去，0000001 00100 就是 36。":
        "The result is 0x02E12223. Disassembling goes the other way, putting the two pieces "
        "back together, zero zero zero zero zero zero one, zero zero one zero zero, which is "
        "thirty-six.",
    "反汇编时就反过来": "Disassembling goes the other way",
    "0000001 00100 就是 36": "which is thirty-six",
    "最后留两道题：把这两个字翻译成汇编。先暂停视频，自己试试。":
        "Finally, two questions to leave you with. Translate these two words into assembly. "
        "Pause the video and try it yourself.",
    "第 1 题：opcode 是 0110011，R 型；funct3 和 funct7 全是 0，所以是 add。rd = 1，rs1 = 2，rs2 = 3：答案是 add x1, x2, x3，也就是 add ra, sp, gp。":
        "For question one, the opcode is zero one one zero zero one one, which is R-type, and "
        "funct3 and funct7 are all zero, so it is add. Here rd is one, rs1 is two, and rs2 is "
        "three, so the answer is add x1, x2, x3, which is add ra, sp, gp.",
    "rd = 1，rs1 = 2，rs2 = 3": "Here rd is one",
    "opcode 是 0110011": "the opcode is",
    "所以是 add": "so it is add",
    "第 2 题：opcode 0000011 是 load，funct3 = 010 是 lw；rd = 10 是 a0，rs1 = 2 是 sp。立即数 1111 1111 1100 的最高位是 1，按补码是 −4。答案：lw a0, -4(sp)。":
        "For question two, the opcode zero zero zero zero zero one one is a load, and funct3 "
        "equal to zero one zero means lw. Then rd is ten, which is a0, and rs1 is two, which "
        "is sp. The immediate, one one one one, one one one one, one one zero zero, has a top "
        "bit of one, so in two's complement it is minus four. So the answer is lw a0, -4(sp).",
    "立即数 1111 1111 1100": "The immediate",
    "opcode 是 1100111": "The opcode is",
    "其余照旧": "Everything else stays as before",
}
