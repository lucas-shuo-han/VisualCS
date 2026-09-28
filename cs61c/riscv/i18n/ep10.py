"""English for episode 10 (keys are the Chinese strings in ep10_decoding.py)."""

EN = {
    # ---- end card
    "反汇编：先看 opcode 定格式，再切字段、定操作、译寄存器":
        "Disassembly: opcode → format, then fields, operation, registers",
    "第 30 位是开关：add/sub、srl/sra、srli/srai": "Bit 30 is a flag: add/sub, srl/sra, srli/srai",
    "I 型有 4 个 opcode：立即数运算、load、jalr、ecall/ebreak":
        "I-type has 4 opcodes: immediate arithmetic, loads, jalr, ecall/ebreak",
    "funct3 成对复用：addi 与 add，lw 与 sw（没有 subi）":
        "Shared funct3 codes: addi with add, lw with sw (no subi)",

    # ---- binaries are ISA-bound
    "本课程": "this course",
    "多数手机": "most phones",
    "多数电脑": "most PCs",
    "4 字节": "4 bytes",
    "2 字节": "2 bytes",
    "第 2 集说过，x86、ARM、RISC-V 是三种不同的指令集。同一行 C 代码，交给三种编译器……":
        "As Episode 2 showed, x86, ARM and RISC-V are three different ISAs. Hand the same line of C to three compilers…",
    "……得到的机器码完全不同。手机里多是 ARM 芯片，电脑里多是 x86。":
        "…and the machine code comes out completely different. Most phones run ARM chips; most PCs run x86.",
    "连长度都不一样：x86 的指令有长有短，这一条只有 2 个字节。":
        "Even the lengths differ: x86 instructions vary in size, and this one is just 2 bytes.",
    "RISC-V 的指令则一律 32 位，和数据字一样宽：取指令和读数据能共用同一套内存硬件。":
        "RISC-V instructions are always 32 bits, as wide as a data word, so instructions and data can share memory hardware.",
    "1981 年": "1981",
    "x86 电脑": "x86 PC",
    "所以程序的二进制文件和指令集是绑定的：RISC-V 的可执行文件，在 Intel 的 x86 电脑上根本跑不起来。":
        "So a program binary is tied to its ISA: a RISC-V executable simply won't run on an Intel x86 machine.",
    "不过，同一个指令集常常向后兼容：今天的 x86 处理器，仍能运行 1981 年为 Intel 8088 写的程序。":
        "ISAs are often backward compatible, though: today's x86 processors still run programs "
        "written for the Intel 8088 in 1981.",

    # ---- disassembly
    "反汇编：从机器码到汇编": "Disassembly: machine code → assembly",
    "上一集把汇编翻译成机器码；这一集反过来：拿到机器码，怎么读回汇编？这叫反汇编（disassembly）。":
        "Last episode, assembly became machine code. Now the reverse: how do we read machine code back as assembly? That's disassembly.",
    "拿这个字练手：0x01B342B3。": "Let's practice on this word: 0x01B342B3.",
    "第一步：换成二进制。每个十六进制数字，正好展开成 4 位。":
        "Step one: convert to binary. Each hex digit expands to exactly 4 bits.",
    "接着找 opcode：不管哪种格式，它永远占最低的 7 位。":
        "Next, find the opcode: whatever the format, it always sits in the lowest 7 bits.",
    "R 型": "R-type",
    "I 型": "I-type",
    "S 型": "S-type",
    "寄存器之间运算": "register–register ops",
    "立即数运算": "immediate ops",
    "每种格式都有自己专属的一组 opcode。查表：0110011，是 R 型。":
        "Each format has its own set of opcodes. Look it up: 0110011 means R-type.",
    "第二步：知道了格式，才知道其余 25 位怎么切。按 R 型切开：funct7、rs2、rs1、funct3、rd。":
        "Step two: only the format tells us how to cut the other 25 bits. "
        "For R-type: funct7, rs2, rs1, funct3, rd.",
    "第三步：funct3 = 100，funct7 = 0000000。查 R 型的表：这是 xor。":
        "Step three: funct3 = 100 and funct7 = 0000000. Look them up in the R-type table: it's xor.",
    "注意：助记符（mnemonic）xor 不存放在任何一个字段里，而是由 opcode、funct3、funct7 共同决定。":
        "Note that the mnemonic xor isn't stored in any single field: opcode, funct3 and funct7 "
        "decide it together.",
    "第四步：寄存器字段是 5 位无符号数：rd = 00101 = 5，rs1 = 00110 = 6，rs2 = 11011 = 27。":
        "Step four: each register field is a 5-bit unsigned number. rd = 00101 = 5, rs1 = 00110 = 6, "
        "rs2 = 11011 = 27.",
    "再换成寄存器名：x5 是 t0，x6 是 t1，x27 是 s11。":
        "Then convert to register names: x5 is t0, x6 is t1, x27 is s11.",
    "拼起来：xor t0, t1, s11。": "Put it together: xor t0, t1, s11.",
    "小心顺序：汇编里写 rd, rs1, rs2，而字段从左到右是 rs2, rs1, rd，正好相反。":
        "Watch the order: assembly lists rd, rs1, rs2, but the fields run rs2, rs1, rd "
        "from left to right, exactly reversed.",
    "转成二进制，看 opcode 定格式": "Binary, then opcode → format",
    "按格式切分字段": "Split into fields",
    "由 funct3、funct7 定操作": "funct3, funct7 → operation",
    "寄存器编号换成名字": "Register numbers → names",
    "所有格式通用": "same for all formats",
    "因格式而异": "format-specific",
    "反汇编的四个步骤": "Disassembly in four steps",
    "反汇编就这四步。前两步对任何格式都一样，后两步因格式而异。":
        "That's all four steps. The first two work the same for every format; the last two depend on it.",

    # ---- bit 30
    "第 30 位：一个开关": "Bit 30: a flag",
    "回头看完整的 R 型表：10 条指令共用一个 opcode，funct3 却只有 8 种。":
        "Back to the full R-type table: all 10 instructions share one opcode, "
        "but there are only 8 funct3 values.",
    "funct3 相同的有两对：add 和 sub 都是 000，srl 和 sra 都是 101。":
        "Two pairs share a funct3: add and sub are both 000; srl and sra are both 101.",
    "区分它们靠 funct7。funct7 也只有两种取值，而且只差一位：第 30 位。":
        "It's funct7 that tells them apart. It takes only two values, and they differ in a single bit: bit 30.",
    "opcode 7 位 + funct3 3 位 + funct7 7 位 = 17 位":
        "opcode 7 bits + funct3 3 bits + funct7 7 bits = 17 bits",
    "光为区分运算就动用了 17 位，明显有富余。但让字段位置对齐，比省下几位更重要。":
        "That's 17 bits just to pick the operation, far more than needed. "
        "But keeping the fields aligned matters more than saving bits.",
    "第 30 位": "bit 30",
    "以 add t0, t1, s11 为例：把第 30 位从 0 翻成 1，它就变成了 sub t0, t1, s11。":
        "Take add t0, t1, s11: flip bit 30 from 0 to 1 and it becomes sub t0, t1, s11.",
    "add 和 sub 共用一个加法器。第 30 位就是个开关（flag）：为 1 时先把 rs2 取负（按位取反再加 1），再相加。":
        "add and sub share one adder, and bit 30 is a flag: when it's 1, rs2 is negated "
        "(invert the bits, add one) before the addition.",
    "以 8 位为例，右移 2 位：": "8-bit example, shifted right by 2:",
    "funct3 换成 101 就是右移。第 30 位为 0 是 srl：逻辑右移，空出的高位补 0。":
        "With funct3 = 101 it's a right shift. Bit 30 = 0 gives srl, a logical shift: "
        "the vacated top bits fill with 0s.",
    "第 30 位为 1 就成了 sra：算术右移，高位补的是符号位。这回，这个开关管的是符号扩展。":
        "Bit 30 = 1 gives sra, an arithmetic shift that fills with the sign bit. "
        "This time the flag controls sign extension.",
    "移位立即数用的是 I 型的一个变体，CS61C 叫它 I* 型：移位量最多 31，只占立即数的低 5 位。":
        "Immediate shifts use a variant CS61C calls I*-type: shifts go up to 31, so only the low 5 immediate bits are used.",
    "立即数的高 7 位不当数值用，而是像 funct7 一样当开关：srai 的这 7 位是 0100000，开关依旧是第 30 位。":
        "The upper 7 bits aren't part of the number; they act like funct7. For srai they're 0100000, "
        "and the flag is bit 30 once again.",
    "关掉第 30 位就是 srli。左移只有逻辑移位一种，所以 slli 的这一位永远是 0。":
        "Clear bit 30 and you get srli. Left shifts are always logical, so slli always has a 0 there.",

    # ---- the I-type family
    "I 型全家": "The I-type family",
    "I 型不只有 addi。把立即数运算和 R 型并排：funct3 一一对应，addi 对 add，xori 对 xor，slti 对 slt……":
        "I-type is more than addi. Next to R-type, the funct3 codes match: addi and add, xori and xor, slti and slt…",
    "唯独没有 subi：要减一个常数，addi 一个负数就行。":
        "The one gap is subi: to subtract a constant, just addi a negative number.",
    "3 位的 funct3 只有 8 种编码，这里已经全部用光，srli 和 srai 还得靠第 30 位来区分。":
        "A 3-bit funct3 has only 8 codes, and they're all used up here; srli and srai even need "
        "bit 30 to tell them apart.",
    "间接跳转": "indirect jump",
    "系统": "system",
    "5 种 load 也要靠 funct3 区分，只好另开一个 opcode。算下来，I 型一共有 4 个 opcode。":
        "The five loads need funct3 codes too, so they get an opcode of their own. "
        "All told, I-type has 4 opcodes.",
    "操作系统": "operating system",
    "调试器": "debugger",
    "ecall（environment call，环境调用）向操作系统请求服务，比如输出文字、结束程序。":
        "ecall (environment call) asks the operating system for a service, such as printing text "
        "or ending the program.",
    "ebreak 则把控制权交给调试器：调试器里的断点，就是靠它实现的。":
        "ebreak hands control to the debugger; it's how debuggers implement breakpoints.",
    "这两条都没有操作数：ecall 除了 opcode 全是 0；ebreak 只是在立即数的最低位多了一个 1。":
        "Neither takes operands: ecall is all 0s apart from the opcode, and ebreak just adds a 1 "
        "in the lowest bit of the immediate.",
    "字节": "byte",
    "半字": "halfword",
    "字": "word",
    "字节，无符号": "byte, unsigned",
    "半字，无符号": "halfword, unsigned",
    "load 和 store 的 funct3 也是配套的：lb 和 sb 是 000，lh 和 sh 是 001，lw 和 sw 是 010。":
        "Loads and stores share funct3 codes too: lb and sb are 000, lh and sh are 001, lw and sw are 010.",
    "RV32 也没有 lwu：一个字正好填满 32 位的寄存器":
        "RV32 has no lwu either: a word exactly fills a 32-bit register",
    "lbu、lhu 没有对应的 store：store 只写入指定的字节，不涉及扩展。同理，RV32 也没有 lwu。":
        "lbu and lhu have no store versions: a store writes just the bytes it targets, with nothing to extend. RV32 has no lwu either.",
    "lw   t0, 8(t1)     # 地址 = t1 + 8": "lw   t0, 8(t1)     # address = t1 + 8",
    "jalr ra, t1, 8     # 跳到 t1 + 8": "jalr ra, t1, 8     # jump to t1 + 8",
    "都要算 rs1 + imm：复用同一个加法器": "All compute rs1 + imm, so they share one adder",
    "load 和 jalr 为什么也用 I 型？它们都要先算 rs1 + 立即数：一个算地址，一个算跳转目标，正好复用同一个加法器。":
        "Why are loads and jalr I-type? Both compute rs1 + immediate, an address or a jump target, so they reuse the same adder.",

    # ---- jalr and ret
    "jalr 与函数返回": "jalr and returning",
    "jalr rd, rs1, imm（也写作 jalr rd, imm(rs1)）：先把 PC + 4 存进 rd，再跳到 rs1 + imm。":
        "jalr rd, rs1, imm (also written jalr rd, imm(rs1)) saves PC + 4 in rd, then jumps to rs1 + imm.",
    "第 7 集的 ret 和 jr ra 都是伪指令，没有自己的 opcode：汇编器把它们都翻译成 jalr x0, ra, 0。":
        "The ret and jr ra from Episode 7 are pseudo-instructions with no opcode of their own: "
        "the assembler turns both into jalr x0, ra, 0.",
    "rd 取 x0，是因为返回时不需要再留下返回地址：写进 x0 的值会被直接丢掉。":
        "rd is x0 because a return doesn't need to save a return address: anything written to x0 is discarded.",
    "编码：立即数 0，rs1 = ra = x1，rd = x0。jalr 只有一条，funct3 其实用不上，按格式填 000。":
        "Encoding: immediate 0, rs1 = ra = x1, rd = x0. There's only one jalr, so funct3 selects nothing; it's just 000.",
    "opcode 是 1100111。合起来就是 0x00008067：在反汇编结果里见到它，就知道函数要返回了。":
        "The opcode is 1100111, giving 0x00008067. Spot this word in a disassembly and you know "
        "a function is returning.",

    # ---- S-type example
    "S 型：拆开的立即数": "S-type: a split immediate",
    "再来一个 S 型的例子：sw x14, 36(x2)。": "One more example, this time S-type: sw x14, 36(x2).",
    "36 的 12 位二进制是 0000 0010 0100。高 7 位 0000001 放进 imm[11:5]，低 5 位 00100 放进 imm[4:0]。":
        "36 in 12 bits is 0000 0010 0100. The top 7 bits, 0000001, go in imm[11:5]; "
        "the low 5 bits, 00100, go in imm[4:0].",
    "为什么要拆？只用 funct7 的 7 位，只能表示 128 个值；store 没有 rd，正好借用 rd 的 5 位，凑满 12 位。":
        "Why split it? The funct7 slot alone has 7 bits, only 128 values. With no rd, a store borrows rd's 5 bits to make 12.",
    "其余照旧：rs2 = x14，rs1 = x2，funct3 = 010 表示 sw，opcode 是 0100011。":
        "The rest is routine: rs2 = x14, rs1 = x2, funct3 = 010 for sw, and opcode 0100011.",
    "结果是 0x02E12223。反汇编时就反过来：把两段拼回去，0000001 00100 就是 36。":
        "The result is 0x02E12223. Disassembling reverses this: glue the two pieces back together, "
        "and 0000001 00100 is 36.",

    # ---- quiz
    "小测验": "Quick check",
    "最后留两道题：把这两个字翻译成汇编。先暂停视频，自己试试。":
        "To finish, two for you: translate these words into assembly. Pause the video and try them yourself.",
    "第 1 题：opcode 是 0110011，R 型；funct3 和 funct7 全是 0，所以是 add。":
        "Question 1: opcode 0110011 means R-type; funct3 and funct7 are all 0s, so it's add.",
    "rd = 1，rs1 = 2，rs2 = 3：答案是 add x1, x2, x3，也就是 add ra, sp, gp。":
        "rd = 1, rs1 = 2, rs2 = 3: the answer is add x1, x2, x3, that is, add ra, sp, gp.",
    "第 2 题：opcode 0000011 是 load，funct3 = 010 是 lw；rd = 10 是 a0，rs1 = 2 是 sp。":
        "Question 2: opcode 0000011 is a load, and funct3 = 010 makes it lw; rd = 10 is a0, and rs1 = 2 is sp.",
    "立即数 1111 1111 1100 的最高位是 1，按补码是 −4。答案：lw a0, -4(sp)。":
        "The immediate 1111 1111 1100 has its top bit set, so in two's complement it's −4. "
        "Answer: lw a0, -4(sp).",
}
