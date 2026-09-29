"""English for episode 4 (keys are the Chinese strings in ep04_memory_practice.py)."""

EN = {
    # code with a Chinese comment (the notes' own wording)
    'char b[] = "string";  // 数组会存放在栈上': 'char b[] = "string";  // Array will get stored on stack',

    # end card
    "寄存器没有类型：指令决定怎样解读比特": "Registers have no types: the instruction decides how to read the bits",
    "一行一条指令；表达式要拆开，可借用临时寄存器":
        "One instruction per line: break expressions up, using temporary registers",
    "从内存 load，往内存 store；运算只在寄存器上做": "Load from memory, store to memory; compute only on registers",
    "元素地址 = 基地址 + 下标 × 大小；变量下标要在寄存器里算":
        "Element address = base + index × size; a variable index must be computed in a register",
    "load 要填满 32 位（lb 符号扩展），store 无需扩展": "Loads fill all 32 bits (lb sign-extends); stores never extend",

    # hook
    "这一集是练习课：亲手把 C 代码翻译成 RISC-V 汇编。":
        "This episode is practice: we'll translate real C code into RISC-V assembly by hand.",

    # assembly vs. C
    "汇编 vs. C": "Assembly vs. C",
    "RISC-V 汇编": "RISC-V assembly",
    "变量要声明，有类型": "Variables are declared and typed",
    "寄存器没有类型，只有比特": "Registers hold just bits",
    "类型决定运算": "Types determine operations",
    "指令决定怎样解读比特": "Instructions decide how bits are read",
    "一个运算符，多种运算": "One operator, many operations",
    "指令名与运算一一对应": "One op name, one operation",
    "一条语句，多个运算": "One statement, many operations",
    "一行只有一条指令": "One instruction per line",
    "先对比汇编和 C。第一，C 的变量有类型；寄存器没有类型，只是 32 个比特。":
        "First, assembly vs. C. One: C variables have types; registers don't. They just hold 32 bits.",
    "第二，C 由类型决定运算；汇编反过来，由指令决定怎样解读这些比特。":
        "Two: in C, the type decides the operation. Assembly flips this: the instruction decides how to read the bits.",
    "有符号：−1": "signed: −1",
    "无符号：4294967295": "unsigned: 4294967295",
    "比如 t0 全是 1：当成有符号数是 −1，当成无符号数就是 4294967295，全看指令怎么用。":
        "Say t0 is all ones: as a signed number it's −1, as unsigned it's 4294967295. "
        "It depends on the instruction.",
    "指针运算": "pointer arithmetic",
    "乘法": "multiply",
    "整数加法": "integer add",
    "解引用": "dereference",
    "第三，C 的运算符有多种含义：第 2 行的 + 是指针运算，第 4 行的 + 是整数加法，两个 * 是乘法和解引用。":
        "Three: C operators have several meanings. On line 2, + is pointer arithmetic; on line 4 it's "
        "integer addition, and the two *s are multiplication and dereference.",
    "汇编里指令名和运算一一对应，字节数得自己算：p + 2 前进 8 字节，就写 addi 加 8。":
        "In assembly, each op name means exactly one operation, and you count the bytes yourself: "
        "p + 2 moves 8 bytes, so addi adds 8.",
    "≈ 6 条指令": "≈ 6 instructions",
    "第四，C 的一条语句可以有多个运算，汇编一行只有一条指令。这一行大约要六条。":
        "Four: a C statement can hold many operations, but each assembly line is one instruction. "
        "This line takes about six.",
    "汇编里也没有变量名，所以注释很重要：# 到行尾都是注释，没有多行注释。":
        "Assembly has no variable names either, so comments matter: everything from # to the end of "
        "the line is a comment. There are no multi-line comments.",

    # warm-up: (g + h) - (i + j)
    "先热身：f = (g + h) - (i + j)，g 到 j 在 x20 到 x23 里，f 放进 x19。":
        "Warm-up: f = (g + h) - (i + j), with g through j in x20 through x23, and f in x19.",
    "写法 A": "Approach A",
    "写法 B": "Approach B",
    "写法 A 照着 C 的顺序，把两个括号先算进临时寄存器 x5 和 x6，再相减得 23。但它们原来的值被覆盖了。":
        "Approach A follows C: sum each parenthesis into a temporary, x5 or x6, "
        "then subtract to get 23. But their old values are lost.",
    "写法 B 从同样的初值出发，利用代数：先算 g + h，再依次减去 i 和 j。":
        "Approach B starts from the same values and uses algebra: compute g + h, then subtract i and j in turn.",
    "同样得 23，且没动 x5、x6。代价是要做代数变形，式子复杂了（比如展开乘法）就得靠更聪明的编译器。":
        "Also 23, and x5 and x6 are untouched. The price is algebraic rewriting: harder expressions "
        "(say, distributing a multiply) need a smarter compiler.",

    # load / store
    "访问内存：load 与 store": "Memory access: load and store",
    "处理器": "Processor",
    "内存": "Memory",
    "地址": "address",
    "寄存器只有 32 个，变量再多也不怕：放不下的就“溢出”（spill）到内存里。":
        "There are only 32 registers, but that doesn't limit your variables: whatever doesn't fit "
        "spills over to memory.",
    "处理器靠地址访问内存。方向以处理器为准：读进来叫 load from，写出去叫 store to。":
        "The processor reaches memory through addresses. Directions are processor-centric: "
        "reading in is load from, writing out is store to.",
    "① load 进寄存器": "① load into registers",
    "② 在寄存器上运算": "② compute on registers",
    "③ store 回内存（如需要）": "③ store back (if needed)",
    "RISC-V 是“加载-存储”架构，只在寄存器上运算：内存里的数先 load，算完需要时再 store 回去。":
        "RISC-V is a load-store architecture that computes only on registers: data in memory is "
        "loaded first, and stored back afterward if needed.",
    "x86（CISC）": "x86 (CISC)",
    "一条指令：读内存 + 相加": "one instruction: memory read + add",
    "x86 则允许一个操作数直接来自内存，一条 add 就够了；RISC-V 得拆成 lw 和 add 两条。":
        "x86 lets one operand come straight from memory, so a single add does it; "
        "RISC-V splits it into lw and add.",
    "偏移量 12 字节": "offset: 12 bytes",
    "s0 = A 的基地址": "s0 = base address of A",
    "s0 = p，成员 y 的偏移量是 4": "s0 = p; member y is at offset 4",
    "“基地址 + 偏移量”是照着数组和结构体设计的：基地址指向开头，偏移量是固定的字节距离，汇编时确定。":
        "Base + offset is modeled on arrays and structs: the base points to the start, and the offset "
        "is a fixed byte distance, known at assembly time.",

    # the stack-array example
    "大例子：栈上的数组": "Big example: arrays on the stack",
    "今天的大例子：四个局部变量，两个是数组。规定只能用 t0、t1、t2 和栈指针 sp，内存随便用。":
        "Today's big example: four local variables, two of them arrays. We may use only t0, t1, t2 "
        "and the stack pointer sp, plus any memory.",
    "sp = x2：栈指针": "sp = x2: stack pointer",
    "sp 就是 x2，指向存放局部变量的栈。这是约定：谁拿 x2 当临时寄存器，靠 sp 的访存就全乱了。":
        "sp is x2, which by convention points to the stack of locals. "
        "Use x2 as a temporary, and every sp-based access breaks.",
    "变量放哪儿由我们这个“人肉编译器”决定，前后一致就行。左边是相对 sp 的偏移量。":
        "We, the human compiler, decide where variables go; we just have to be consistent. "
        "On the left: offsets from sp.",
    'a 放在 0(sp)；b 是 "string" 加结尾的 \\0，共 7 字节，从 4(sp) 开始。':
        'a goes at 0(sp); b is "string" plus its terminating \\0, 7 bytes starting at 4(sp).',
    "c 是 10 个 int，共 40 字节，占 12(sp) 到 51(sp)；d 只有 1 字节，放在 52(sp)。":
        "c is 10 ints, 40 bytes, from 12(sp) to 51(sp); d is a single byte at 52(sp).",
    "c 从 12(sp) 而不是 11(sp) 开始，这样每个 int 都对齐到 4 的倍数。":
        "c starts at 12(sp), not 11(sp), so every int is aligned to a multiple of 4.",
    "第一行 a = 5：sw 只能存寄存器的值，所以先用 li 把 5 装进 t0，再存到 0(sp)。":
        "Line 1, a = 5: sw can only store a register, so li first puts 5 into t0, then we store it at 0(sp).",
    '第二行存 "string"：查 ASCII 表得到这 7 个字节。最直接的办法是逐个 li 再 sb，\\0 用 x0 存，共 13 条指令。':
        'Line 2 stores "string"; ASCII gives these 7 bytes. Simplest is li and sb per byte, '
        'with \\0 straight from x0: 13 instructions.',
    "13 条指令": "13 instructions",
    '更聪明的办法：4 个字符拼成一个字，一条 sw 存下。按小端序，第一个字符要放在最低字节，所以 "stri" 写成 0x69727473。':
        'Smarter: pack 4 characters into a word and store it with one sw. In little-endian the first '
        'character must be the lowest byte, so "stri" becomes 0x69727473.',
    "sw 存到 4(sp) 后，从低地址往高地址看，正好是 s、t、r、i。":
        "After sw to 4(sp), reading from low to high addresses gives s, t, r, i.",
    '剩下 n、g、\\0 再补一个 0 字节，凑成 0x0000676E，存到 8(sp)。总共只要 4 条指令。':
        'The remaining n, g, \\0 plus one zero byte make 0x0000676E, stored at 8(sp). '
        'Just 4 instructions in total.',
    "li → lui + addi（第 12 集）": "li → lui + addi (Episode 12)",
    "常数这么大，addi 的 12 位立即数装不下，li 会展开成 lui + addi 两条，第 12 集细讲。":
        "A constant this big won't fit addi's 12-bit immediate, so li expands into lui + addi. "
        "More in Episode 12.",
    "（不需要指令）": "(no instructions)",
    "第三行 int c[10] 没有初值，不需要指令；布局本身也不产生指令。":
        "Line 3, int c[10], has no initializer, so no instructions. The layout itself generates none either.",
    "第四行 d = b[3]：b 从 4(sp) 开始，b[3] 再往后 3 字节，就是 7(sp)。":
        "Line 4, d = b[3]: b starts at 4(sp), and b[3] is 3 bytes further, at 7(sp).",
    "lb 读出 0x69，即 'i'；最高位是 0，符号扩展补的也是 0。再用 sb 存进 52(sp)，这就是 d。":
        "lb reads 0x69, which is 'i'. Its top bit is 0, so sign extension fills in 0s. "
        "Then sb stores it at 52(sp): that's d.",
    "第五行 c[4] = a+d：两个数都要先 load 进来。a 是 int，用 lw；d 是无符号的 uint8_t，用 lbu。":
        "Line 5, c[4] = a+d: both values must be loaded first. a is an int, so lw; "
        "d is an unsigned uint8_t, so lbu.",
    "5 + 105 = 110。c 从 12(sp) 开始，c[4] 再往后 4 × 4 字节，所以存到 28(sp)。":
        "5 + 105 = 110. c starts at 12(sp) and c[4] is 4 × 4 bytes further, so we store at 28(sp).",
    "最后一行 c[a] = 20 最难：能像 c[4] 那样，写一个固定的偏移量吗？":
        "The last line, c[a] = 20, is the hardest. Can we use a fixed offset, as for c[4]?",
    "不行：a 是变量，运行时才知道是 5，而偏移量得在汇编时确定。地址只能在寄存器里算。":
        "No: a is a variable, only known to be 5 at runtime, but the offset is fixed at assembly time. "
        "The address must be computed in a register.",
    "c[a] 的地址是 sp + 12 + 4 × a。先把 20 放进 t0，再把 a 读进 t1。":
        "The address of c[a] is sp + 12 + 4 × a. First put 20 in t0, then load a into t1.",
    "乘 4 就是左移 2 位：slli 把 0b101 变成 0b10100，也就是 20。移位第 5 集细讲。":
        "Multiplying by 4 is a left shift by 2: slli turns 0b101 into 0b10100, which is 20. "
        "Shifts are covered in Episode 5.",
    "加上 c 的偏移量 12 得 32，即 0x20；再加上 sp 的 0x1000，得到完整地址 0x1020。":
        "Adding c's offset, 12, gives 32, or 0x20; adding sp's 0x1000 gives the full address 0x1020.",
    "地址已经完整，所以偏移量写 0：sw t0, 0(t1) 把 20 写进 c[5]。":
        "The address is complete, so the offset is 0: sw t0, 0(t1) writes 20 into c[5].",
    "小测验：此刻 t1 里是什么？不是 c[a] 的值，而是它的地址 &c[a]。":
        "Quick check: what's in t1 now? Not the value of c[a], but its address, &c[a].",

    # notes, Example 1
    "练习 1：lb 读到了什么？": "Practice 1: what does lb read?",
    "再做两道短练习。第一道：x5 = 0x100，执行这三条指令后，x12 里是什么？":
        "Two short exercises. First: x5 = 0x100. After these three instructions, what's in x12?",
    "li 把 x11 设成 0x000093F5；sw 按小端序把它存进 0x100：F5 93 00 00。":
        "li sets x11 to 0x000093F5; sw stores it at 0x100 in little-endian order: F5 93 00 00.",
    "lb x12, 1(x5) 读的是 0x101 处的字节：0x93，而不是 0xF5。":
        "lb x12, 1(x5) reads the byte at 0x101: 0x93, not 0xF5.",
    "0x93 是 1001 0011，最高位是 1。lb 做符号扩展，高 24 位全填 1。":
        "0x93 is 1001 0011, so its top bit is 1. lb sign-extends, filling the upper 24 bits with 1s.",
    "所以 x12 = 0xFFFFFF93。两个坑：小端序让 1(x5) 读到 0x93，lb 又把它扩展成了负数。":
        "So x12 = 0xFFFFFF93. Two traps: little-endian puts 0x93 at 1(x5), "
        "and lb extends it into a negative number.",

    # notes, Example 2
    "练习 2：*x = *y": "Practice 2: *x = *y",
    "空闲": "free",
    "第二道：x、y 是 int 指针，分别在 x3 和 x5 里。*x = *y 该选哪几条？":
        "Second: x and y are int pointers, held in x3 and x5. Which instructions implement *x = *y?",
    "1 和 2 复制的是指针本身；3 和 4 用 lw 覆盖了指针寄存器。都不对。":
        "1 and 2 copy the pointers themselves; 3 and 4 use lw to overwrite a pointer register. "
        "None of them work.",
    "答案是 5 → 6：lw 把 *y 读进空闲的 x8，sw 再写到 x 指向的地址。内存到内存，必须经过寄存器。":
        "The answer is 5 → 6: lw loads *y into the free x8, then sw writes it where x points. "
        "Memory to memory must go through a register.",
    "顺序不能反：6 → 5 会先存 x8 的旧值；7、8 把 x8 当成了地址，也不对。":
        "Order matters: 6 → 5 would store x8's old value first. 7 and 8 treat x8 as an address, also wrong.",

    # no sbu, alignment
    "两个细节": "Two details",
    "寄存器": "Register",
    "最后两个细节。第一个：有 lbu，为什么没有“sbu”？看看 store 做了什么。":
        'Two last details. First: there is lbu, so why no "sbu"? Look at what a store does.',
    "只取最低字节，原样存入": "takes the low byte, as is",
    "sb 只取最低字节，原样放进内存，无需扩展。load 却必须写满寄存器的 32 位。":
        "sb takes only the lowest byte and puts it in memory as is; nothing to extend. "
        "A load, though, must fill all 32 bits of the register.",
    "寄存器只是比特，后续指令怎么用它说不准，所以高位得明确：符号扩展，还是补 0。":
        "A register is just bits, and there's no telling how later instructions will use it, "
        "so the upper bits must be defined: sign-extend or fill with 0s.",
    "第二个是对齐：地址是访问大小整数倍的 load 和 store，规范保证绝不触发不对齐异常。":
        "Second, alignment: the spec guarantees that loads and stores at a multiple of the access size "
        "never raise a misaligned exception.",
    "不对齐的访问由具体实现决定：可能很慢，也可能报错。所以把“应该对齐”当成“必须对齐”。":
        'Misaligned access is up to the implementation: it may be slow, or fail. '
        'So treat "should be aligned" as "must be aligned".',
    "小端（CS61C）": "little-endian (CS61C)",
    "大端": "big-endian",
    "另外，规范允许小端和大端两种实现，CS61C 按小端讲。":
        "Also, the spec allows both little-endian and big-endian implementations; CS61C uses little-endian.",
}
