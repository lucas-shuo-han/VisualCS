"""English for episode 4 (keys are the Chinese strings in ep04_memory_practice.py)."""

EN = {
    # code with a Chinese comment (the notes' own wording)
    'char b[] = "string";  // 数组会存放在栈上': 'char b[] = "string";  // Array will get stored on stack',

    # end card
    "寄存器没有类型：指令决定怎样解读比特":
        "Registers have no types, and the instruction decides how to read the bits",
    "一行一条指令；表达式要拆开，可借用临时寄存器":
        "A line holds one instruction, so expressions are broken up using temporary registers",
    "从内存 load，往内存 store；运算只在寄存器上做":
        "Data is loaded from memory and stored back to it, and computing happens only on "
        "registers",
    "元素地址 = 基地址 + 下标 × 大小；变量下标要在寄存器里算":
        "An element's address is the base plus index times size, and a variable index is "
        "computed in a register",
    "load 要填满 32 位（lb 符号扩展），store 无需扩展":
        "Loads fill all thirty-two bits, with lb sign-extending, while stores never extend",

    # hook

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
    "有符号：−1": "signed: −1",
    "无符号：4294967295": "unsigned: 4294967295",
    "指针运算": "pointer arithmetic",
    "乘法": "multiply",
    "整数加法": "integer add",
    "解引用": "dereference",
    "≈ 6 条指令": "≈ 6 instructions",

    # warm-up: (g + h) - (i + j)
    "写法 A": "Approach A",
    "写法 B": "Approach B",

    # load / store
    "访问内存：load 与 store": "Memory access: load and store",
    "处理器": "Processor",
    "内存": "Memory",
    "地址": "address",
    "① load 进寄存器": "① load into registers",
    "② 在寄存器上运算": "② compute on registers",
    "③ store 回内存（如需要）": "③ store back (if needed)",
    "x86（CISC）": "x86 (CISC)",
    "一条指令：读内存 + 相加": "one instruction: memory read + add",
    "偏移量 12 字节": "offset: 12 bytes",
    "s0 = A 的基地址": "s0 = base address of A",
    "s0 = p，成员 y 的偏移量是 4": "s0 = p; member y is at offset 4",

    # the stack-array example
    "大例子：栈上的数组": "Big example: arrays on the stack",
    "sp = x2：栈指针": "sp = x2: stack pointer",
    "13 条指令": "13 instructions",
    "li → lui + addi（第 12 集）": "li → lui + addi (Episode 12)",
    "（不需要指令）": "(no instructions)",

    # notes, Example 1
    "练习 1：lb 读到了什么？": "Practice 1: what does lb read?",

    # notes, Example 2
    "练习 2：*x = *y": "Practice 2: *x = *y",
    "空闲": "free",

    # no sbu, alignment
    "两个细节": "Two details",
    "寄存器": "Register",
    "只取最低字节，原样存入": "takes the low byte, as is",
    "小端（CS61C）": "little-endian (CS61C)",
    "大端": "big-endian",

    # ---- spoken beats and cue phrases (see references/narration-writing.md)
    "这一集是练习课：亲手把 C 代码翻译成 RISC-V 汇编。":
        "This episode is a practice session, where we translate C code into RISC-V assembly "
        "by hand.",
    "先对比汇编和 C。第一，C 的变量有类型；寄存器没有类型，只是 32 个比特。第二，C 由类型决定运算；汇编反过来，由指令决定怎样解读这些比特。比如 t0 全是 1：当成有符号数是 −1，当成无符号数就是 4294967295，全看指令怎么用。":
        "Let's start by comparing assembly with C. A C variable has a type, but a register "
        "has no type, only thirty-two bits. In C the type decides the operation, while in "
        "assembly the instruction decides how the bits are read. So if t0 is all ones, a "
        "signed instruction sees minus one, and an unsigned one sees over four billion.",
    "第二": "In C the type decides",
    "比如 t0 全是 1": "So if t0 is all ones",
    "第三，C 的运算符有多种含义：第 2 行的 + 是指针运算，第 4 行的 + 是整数加法，两个 * 是乘法和解引用。汇编里指令名和运算一一对应，字节数得自己算：p + 2 前进 8 字节，就写 addi 加 8。":
        "Third, a C operator can mean several things. On line two the plus is pointer "
        "arithmetic, on line four it's integer addition, and the two stars are a "
        "multiplication and a dereference. In assembly each instruction name matches exactly "
        "one operation, but you count the bytes yourself, so p plus two moves forward eight "
        "bytes, and we write addi with eight.",
    "汇编里指令名和运算一一对应": "In assembly each instruction name",
    "第 2 行的 + 是指针运算": "On line two",
    "第 4 行的 + 是整数加法": "on line four",
    "就写 addi 加 8": "and we write addi",
    "第四，C 的一条语句可以有多个运算，汇编一行只有一条指令。这一行大约要六条。":
        "Fourth, one C statement can contain several operations, but a line of assembly holds "
        "exactly one instruction. This statement would take about six.",
    "这一行大约要六条": "This statement would take",
    "汇编里也没有变量名，所以注释很重要：# 到行尾都是注释，没有多行注释。":
        "Assembly has no variable names either, so comments matter a lot. Everything from a "
        "hash mark to the end of the line is a comment, and there are no multi-line comments.",
    "# 到行尾都是注释": "Everything from a hash mark",
    "先热身：f = (g + h) - (i + j)，g 到 j 在 x20 到 x23 里，f 放进 x19。":
        "Let's warm up with f equals the sum of g and h, minus the sum of i and j. The four "
        "inputs live in registers x20 through x23, and f goes into x19.",
    "写法 A 照着 C 的顺序，把两个括号先算进临时寄存器 x5 和 x6，再相减得 23。但它们原来的值被覆盖了。":
        "Version A follows the order of the C code. It computes g plus h into x5, then i plus "
        "j into x6, and then subtracts them to get twenty-three. But that overwrites the "
        "values those two registers held before.",
    "先算进临时寄存器 x5": "It computes g plus h",
    "和 x6": "then i plus j",
    "再相减得 23": "and then subtracts",
    "但它们原来的值被覆盖了": "But that overwrites",
    "写法 B 从同样的初值出发，利用代数：先算 g + h，再依次减去 i 和 j。同样得 23，且没动 x5、x6。代价是要做代数变形，式子复杂了（比如展开乘法）就得靠更聪明的编译器。":
        "Version B starts from the same values and uses a little algebra. It computes g plus "
        "h first, then subtracts i, and then subtracts j. That also gives twenty-three, and "
        "it leaves x5 and x6 untouched, but the price is some algebra, and a more complicated "
        "expression, such as one with a multiplication, needs a smarter compiler.",
    "同样得 23": "That also gives twenty-three",
    "先算 g + h": "It computes g plus h first",
    "再依次减去 i": "then subtracts i",
    "和 j": "and then subtracts j",
    "寄存器只有 32 个，变量再多也不怕：放不下的就“溢出”（spill）到内存里。":
        "There are only thirty-two registers, but that doesn't limit the number of variables, "
        "because whatever doesn't fit gets spilled out to memory.",
    "放不下的就": "whatever doesn't fit",
    "（spill）到内存里": "gets spilled out",
    "处理器靠地址访问内存。方向以处理器为准：读进来叫 load from，写出去叫 store to。":
        "The processor reaches memory through addresses, and the direction is always from the "
        "processor's point of view. Reading data in is called a load, and writing it out is "
        "called a store.",
    "读进来叫 load from": "Reading data in is called",
    "RISC-V 是“加载-存储”架构，只在寄存器上运算：内存里的数先 load，算完需要时再 store 回去。x86 则允许一个操作数直接来自内存，一条 add 就够了；RISC-V 得拆成 lw 和 add 两条。":
        "RISC-V is a load-store architecture, so it computes only on registers. A number in "
        "memory is loaded first, and after the calculation it is stored back if needed. The "
        "x86 architecture is different, because an add can take one operand straight from "
        "memory, while RISC-V has to split that into two instructions, an lw and an add.",
    "x86 则允许一个操作数直接来自内存": "The x86 architecture is different",
    "“基地址 + 偏移量”是照着数组和结构体设计的：基地址指向开头，偏移量是固定的字节距离，汇编时确定。":
        "Base plus offset was designed to match arrays and structures. The base address "
        "points at the beginning, and the offset is a fixed distance in bytes that is known "
        "when the code is assembled.",
    "偏移量是固定的字节距离": "the offset is a fixed distance",
    "汇编时确定": "known when the code",
    "今天的大例子：四个局部变量，两个是数组。规定只能用 t0、t1、t2 和栈指针 sp，内存随便用。":
        "Today's big example has four local variables, and two of them are arrays. We may use "
        "only t0, t1, t2, and the stack pointer sp, though memory is free to use.",
    "规定只能用": "We may use only",
    "sp 就是 x2，指向存放局部变量的栈。这是约定：谁拿 x2 当临时寄存器，靠 sp 的访存就全乱了。":
        "The stack pointer sp is just x2, and it points to the stack that holds the local "
        "variables. That is a convention, and if anyone used x2 as a temporary, every memory "
        "access through sp would break.",
    "谁拿 x2 当临时寄存器": "and if anyone used x2",
    "变量放哪儿由我们这个“人肉编译器”决定，前后一致就行。左边是相对 sp 的偏移量。":
        "Where each variable goes is up to us, the human compiler, as long as we stay "
        "consistent. The numbers on the left are offsets from sp.",
    "a 放在 0(sp)；b 是 \"string\" 加结尾的 \\0，共 7 字节，从 4(sp) 开始。c 是 10 个 int，共 40 字节，占 12(sp) 到 51(sp)；d 只有 1 字节，放在 52(sp)。c 从 12(sp) 而不是 11(sp) 开始，这样每个 int 都对齐到 4 的倍数。":
        "The integer a goes at offset zero from sp. The array b holds the string plus its "
        "terminating null, seven bytes in all, and starts at four from sp. The array c is ten "
        "ints, so forty bytes, covering twelve through fifty-one from sp, and d is a single "
        "byte at fifty-two. Notice that c starts at twelve instead of eleven, so that every "
        "int is aligned to a multiple of four.",
    "c 是 10 个 int": "The array c is ten ints",
    "c 从 12(sp) 而不是 11(sp) ": "Notice that c starts",
    "第一行 a = 5：sw 只能存寄存器的值，所以先用 li 把 5 装进 t0，再存到 0(sp)。":
        "The first line sets a to five. Since sw can store only a register's value, we first "
        "load five into t0 with li, and then store it at zero from sp.",
    "先用 li 把 5 装进 t0": "we first load five",
    "再存到 0(sp)": "and then store it",
    "第二行存 \"string\"：查 ASCII 表得到这 7 个字节。最直接的办法是逐个 li 再 sb，\\0 用 x0 存，共 13 条指令。":
        "The second line stores the string, and a lookup in the ASCII table gives us its "
        "seven bytes. The most direct way is an li and an sb for each byte, with x0 supplying "
        "the null byte, which comes to thirteen instructions.",
    "最直接的办法": "The most direct way",
    "共 13 条指令": "which comes to thirteen",
    "更聪明的办法：4 个字符拼成一个字，一条 sw 存下。按小端序，第一个字符要放在最低字节，所以 \"stri\" 写成 0x69727473。sw 存到 4(sp) 后，从低地址往高地址看，正好是 s、t、r、i。":
        "There's a cleverer way, which is to pack four characters into one word and store it "
        "with a single sw. Because of little-endian order, the first character goes in the "
        "lowest byte, so the letters s, t, r, and i are written as 0x69727473. After the "
        "store at four from sp, reading from the low address upward gives exactly s, t, r, i.",
    "sw 存到 4(sp) 后": "After the store at four from sp",
    "4 个字符拼成一个字": "pack four characters",
    "第一个字符要放在最低字节": "the first character goes",
    "写成 0x69727473": "are written as",
    "正好是 s、t、r、i": "gives exactly",
    "剩下 n、g、\\0 再补一个 0 字节，凑成 0x0000676E，存到 8(sp)。总共只要 4 条指令。常数这么大，addi 的 12 位立即数装不下，li 会展开成 lui + addi 两条，第 12 集细讲。":
        "The remaining n, g, and null get padded with one more zero byte, to make 0x0000676E, "
        "which is stored at eight from sp. That's only four instructions in all. And because "
        "such a big constant doesn't fit in the twelve-bit immediate of addi, li expands into "
        "a lui and an addi, which we'll cover in episode twelve.",
    "常数这么大": "And because such a big constant",
    "凑成 0x0000676E": "to make",
    "存到 8(sp)": "which is stored",
    "第三行 int c[10] 没有初值，不需要指令；布局本身也不产生指令。":
        "The third line, int c of ten, has no initial value, so it needs no instructions, and "
        "the layout itself doesn't generate any either.",
    "第四行 d = b[3]：b 从 4(sp) 开始，b[3] 再往后 3 字节，就是 7(sp)。lb 读出 0x69，即 'i'；最高位是 0，符号扩展补的也是 0。再用 sb 存进 52(sp)，这就是 d。":
        "The fourth line is d equals b of three. Since b starts at four from sp, b of three "
        "is three bytes further on, at seven from sp. The lb instruction reads 0x69, which is "
        "the letter i, and since its top bit is zero, sign extension fills with zeros too. "
        "Then sb stores it at fifty-two from sp, and that is d.",
    "lb 读出 0x69": "The lb instruction reads",
    "再用 sb 存进": "Then sb stores",
    "第五行 c[4] = a+d：两个数都要先 load 进来。a 是 int，用 lw；d 是无符号的 uint8_t，用 lbu。5 + 105 = 110。c 从 12(sp) 开始，c[4] 再往后 4 × 4 字节，所以存到 28(sp)。":
        "The fifth line is c of four equals a plus d, and both values have to be loaded "
        "first. The variable a is an int, so we use lw, and d is an unsigned byte, so we use "
        "lbu. Five plus one hundred five is one hundred ten. Since c starts at twelve from "
        "sp, c of four is four times four bytes further on, so we store it at twenty-eight "
        "from sp.",
    "5 + 105 = 110": "Five plus one hundred five",
    "d 是无符号的": "and d is an unsigned byte",
    "用 lbu": "so we use lbu",
    "= 110": "is one hundred ten",
    "c[4] 再往后": "c of four is four times",
    "最后一行 c[a] = 20 最难：能像 c[4] 那样，写一个固定的偏移量吗？不行：a 是变量，运行时才知道是 5，而偏移量得在汇编时确定。地址只能在寄存器里算。":
        "The last line, c of a equals twenty, is the hardest. Can we write a fixed offset, as "
        "we did for c of four? No, because a is a variable that we know to be five only at "
        "run time. An offset has to be fixed when the code is assembled, so the address has "
        "to be computed in a register.",
    "不行": "No, because",
    "c[a] 的地址是 sp + 12 + 4 × a。先把 20 放进 t0，再把 a 读进 t1。乘 4 就是左移 2 位：slli 把 0b101 变成 0b10100，也就是 20。移位第 5 集细讲。":
        "The address of c of a is sp plus twelve plus four times a. First we put twenty into "
        "t0, and then load a into t1. Multiplying by four is a left shift by two, so slli "
        "turns binary one zero one into one zero one zero zero, which is twenty, and we'll "
        "cover shifts in episode five.",
    "乘 4 就是左移 2 位": "Multiplying by four",
    "先把 20 放进 t0": "First we put twenty",
    "再把 a 读进 t1": "and then load a",
    "加上 c 的偏移量 12 得 32，即 0x20；再加上 sp 的 0x1000，得到完整地址 0x1020。地址已经完整，所以偏移量写 0：sw t0, 0(t1) 把 20 写进 c[5]。":
        "Adding the offset of c, which is twelve, gives thirty-two, or 0x20, and adding the "
        "value of sp, 0x1000, gives the complete address, 0x1020. Since the address is now "
        "complete, the offset is just zero, and sw with zero from t1 writes twenty into c of "
        "five.",
    "地址已经完整": "Since the address is now complete",
    "得 32": "gives thirty-two",
    "再加上 sp 的 0x1000": "and adding the value of sp",
    "得到完整地址": "gives the complete address",
    "小测验：此刻 t1 里是什么？不是 c[a] 的值，而是它的地址 &c[a]。":
        "A quick quiz. What is in t1 right now? It isn't the value of c of a, but its "
        "address.",
    "再做两道短练习。第一道：x5 = 0x100，执行这三条指令后，x12 里是什么？li 把 x11 设成 0x000093F5；sw 按小端序把它存进 0x100：F5 93 00 00。":
        "Now for two short exercises. In the first, x5 holds 0x100, and the question is what "
        "x12 contains after these three instructions. The li sets x11 to 0x000093F5, and sw "
        "stores it at 0x100 in little-endian order, so the four bytes are F5, 93, and then "
        "two zero bytes.",
    "li 把 x11 设成 0x000093F5": "The li sets",
    "sw 按小端序": "and sw stores it",
    "F5 93 00 00": "so the four bytes are",
    "lb x12, 1(x5) 读的是 0x101 处的字节：0x93，而不是 0xF5。":
        "The lb instruction, with an offset of one from x5, reads the byte at 0x101, which is "
        "0x93 and not 0xF5.",
    "0x93 是 1001 0011，最高位是 1。lb 做符号扩展，高 24 位全填 1。所以 x12 = 0xFFFFFF93。两个坑：小端序让 1(x5) 读到 0x93，lb 又把它扩展成了负数。":
        "In binary, 0x93 is one zero zero one zero zero one one, so its top bit is a one. The "
        "lb instruction does sign extension, which fills the upper twenty-four bits with "
        "ones, so x12 becomes 0xFFFFFF93. That's two traps in one, because little-endian "
        "order made the offset of one read 0x93, and then lb extended it into a negative "
        "number.",
    "所以 x12 = 0xFFFFFF93": "so x12 becomes",
    "0x93 是 1001 0011": "In binary",
    "最高位是 1": "so its top bit",
    "高 24 位全填 1": "which fills the upper",
    "第二道：x、y 是 int 指针，分别在 x3 和 x5 里。*x = *y 该选哪几条？1 和 2 复制的是指针本身；3 和 4 用 lw 覆盖了指针寄存器。都不对。":
        "In the second exercise, x and y are int pointers, kept in x3 and x5, and the "
        "question is which instructions implement star x equals star y. Options one and two "
        "copy the pointers themselves, and options three and four use lw to overwrite the "
        "pointer registers, so none of those is right.",
    "1 和 2 复制的是指针本身": "Options one and two",
    "答案是 5 → 6：lw 把 *y 读进空闲的 x8，sw 再写到 x 指向的地址。内存到内存，必须经过寄存器。顺序不能反：6 → 5 会先存 x8 的旧值；7、8 把 x8 当成了地址，也不对。":
        "The answer is five followed by six. The lw instruction reads star y into the free "
        "register x8, and then sw writes that value to the address that x points to. Copying "
        "from memory to memory has to go through a register. The order matters too. Six then "
        "five would store the old value of x8 first, and seven and eight treat x8 as an "
        "address, so they are wrong as well.",
    "顺序不能反": "The order matters too",
    "lw 把 *y 读进": "The lw instruction reads",
    "sw 再写到": "and then sw writes",
    "最后两个细节。第一个：有 lbu，为什么没有“sbu”？看看 store 做了什么。sb 只取最低字节，原样放进内存，无需扩展。load 却必须写满寄存器的 32 位。":
        "Two last details. The first one is, why is there an lbu but no sbu? To see why, look "
        "at what a store does. It takes just the lowest byte and puts it into memory as it "
        "is, with no extension needed, whereas a load must fill all thirty-two bits of the "
        "register.",
    "load 却必须写满": "whereas a load must fill",
    "看看 store 做了什么": "look at what a store does",
    "sb 只取最低字节": "It takes just the lowest byte",
    "原样放进内存": "as it is",
    "寄存器只是比特，后续指令怎么用它说不准，所以高位得明确：符号扩展，还是补 0。":
        "A register is just bits, and we can't tell how later instructions will use it, so "
        "the upper bits have to be spelled out, either sign extended or filled with zeros.",
    "第二个是对齐：地址是访问大小整数倍的 load 和 store，规范保证绝不触发不对齐异常。不对齐的访问由具体实现决定：可能很慢，也可能报错。所以把“应该对齐”当成“必须对齐”。":
        "The second detail is alignment. A load or store whose address is a multiple of its "
        "access size is guaranteed never to raise a misaligned exception. What happens with a "
        "misaligned access is left to the implementation, since it might be very slow or it "
        "might trap, so treat should be aligned as must be aligned.",
    "不对齐的访问由具体实现决定": "What happens with a misaligned access",
    "另外，规范允许小端和大端两种实现，CS61C 按小端讲。":
        "One more thing. The spec allows both little-endian and big-endian implementations, "
        "and CS61C teaches little-endian.",
    "CS61C 按小端讲": "and CS61C teaches",
}
