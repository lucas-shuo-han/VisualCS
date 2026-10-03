"""English for episode 3 (keys are the Chinese strings in ep03_memory.py)."""

EN = {
    # end card
    "内存按字节寻址；一个字 = 4 字节": "Memory is addressed by the byte, and one word is four bytes",
    "小端序：低位字节放在低地址": "Little-endian puts the least significant byte at the lowest address",
    "lw / sw  寄存器, 偏移(基址)：地址 = 基址 + 偏移": "A load or a store adds an offset to a base register to form the address",
    "A[i] 的字节偏移是 4 × i": "Element i of an array is at byte offset four times i",
    "lb 符号扩展，lbu 零扩展": "lb sign-extends, and lbu zero-extends",

    # why memory
    "内存 Memory": "Memory",
    "寄存器 × 32": "32 registers",
    "内存：数组、结构体……": "Memory:\narrays, structs...",
    "load 加载": "load",
    "store 存储": "store",

    # byte addressing
    "字地址通常是 4 的倍数\n这叫“对齐”": "Word addresses are\nusually multiples of 4:\nthey're aligned",
    "高位": "high byte",
    "低位": "low byte",

    # lw / sw
    "偏移是 12，不是 3！": "The offset is 12, not 3!",
    "注意：sw 的源寄存器写在前面": "Note: sw lists the source register first",

    # bytes, sign extension
    "字节读写：lb / lbu / sb": "Bytes: lb / lbu / sb",
    "内存中的一个字节": "a byte in memory",
    "扩展出来的 24 位": "24 extended bits",
    "读入的字节": "loaded byte",
    "sb：只把寄存器最低的 8 位写入内存，其余 24 位被忽略":
        "sb: stores only the lowest 8 bits; the upper 24 are ignored",
    "写入": "Store",
    "宽度": "Width",
    "无符号": "Unsigned",
    "有符号": "Signed",
    "字节 8 位": "Byte (8 bits)",
    "半字 16 位": "Half-word (16 bits)",
    "字 32 位": "Word (32 bits)",

    # ---- spoken beats and cue phrases (see references/narration-writing.md)
    "寄存器只有 32 个，可程序里有数组、结构体，成千上万个变量。寄存器放不下的，就放在内存里。":
        "A processor has only thirty-two registers, but a real program has arrays, structures "
        "and thousands upon thousands of variables. Whatever doesn't fit in the registers has "
        "to live in memory.",
    "RISC-V 是“加载-存储”架构：算术指令只能操作寄存器，访问内存必须用专门的指令。load 把数据从内存搬进寄存器，store 把寄存器的值写回内存。":
        "RISC-V is what we call a load-store architecture, which means arithmetic "
        "instructions work only on registers, and reaching memory takes special instructions. "
        "A load copies data from memory into a register, and a store writes a register's "
        "value back out to memory.",
    "load 把数据从内存搬进寄存器": "A load copies data",
    "可以把内存想象成一个巨大的字节数组：每个字节都有自己的编号，也就是地址。为了看得清楚，每行画 4 个字节：第一行是 0x100 到 0x103，下一行从 0x104 开始。":
        "You can picture memory as one enormous array of bytes, where every byte has its own "
        "number, called its address. To keep the picture readable we draw four bytes per row, "
        "so the first row runs from 0x100 to 0x103, and the next row starts at 0x104.",
    "为了看得清楚": "we draw four bytes per row",
    "每个字节都有自己的编号": "every byte has its own number",
    "一个字占 4 个字节，所以相邻两个字的地址相差 4，而不是 1。字的地址通常是 4 的倍数，叫做“对齐”。不对齐的访问可能更慢，甚至直接出错。":
        "A word takes four bytes, so the addresses of neighboring words differ by four, not "
        "by one. Word addresses are normally multiples of four, which is called alignment, "
        "and a misaligned access can be slower or even fail outright.",
    "字的地址通常是 4 的倍数": "Word addresses are normally",
    "相邻两个字的地址相差 4": "differ by four",
    "一个 32 位的数，怎么放进 4 个字节？比如 0x12345678。RISC-V 通常采用小端序（little-endian）：最低位的字节放在最小的地址。":
        "How do we fit a thirty-two bit number, such as 0x12345678, into four bytes? RISC-V "
        "uses what's called little-endian order, which puts the least significant byte at the "
        "smallest address.",
    "RISC-V 通常采用小端序": "RISC-V uses what's called little-endian order",
    "所以从 0x100 往后看，依次是 78、56、34、12，像是“倒着”存的。好在按字读写时，硬件会自动拼回原来的数，大多数时候你不用操心字节顺序。":
        "So reading upward from 0x100, the bytes are seven eight, five six, three four and "
        "one two, which looks like the number was stored backwards. The good news is that "
        "loading or storing a whole word reassembles the number for you, so you rarely need "
        "to think about byte order.",
    "现在假设内存里有一个 int 数组 A：从地址 0x100 开始，每个元素占一个字。数组的起始地址，也叫基地址，放在 s0 里。":
        "Now suppose memory holds the integer array A, which starts at address 0x100 and uses "
        "one word per element. The address where the array begins is called the base address, "
        "and we'll keep it in the register s0.",
    "数组的起始地址": "The address where the array begins",
    "lw 是 load word。lw t0, 8(s0)：从地址 s0 + 8 读一个字，放进 t0。偏移量 8 加上基地址，得到 0x108，正是 A[2] 所在的位置。":
        "The instruction lw stands for load word. Take lw t0, 8(s0), which reads one word "
        "from the address s0 plus 8 and puts it into t0. The offset, 8, plus the base address "
        "gives 0x108, and that is exactly where A[2] lives.",
    "偏移量 8 加上基地址": "The offset, 8, plus the base address",
    "从地址 s0 + 8": "the address s0 plus 8",
    "正是 A[2] 所在的位置": "that is exactly where",
    "所以 C 里的 A[i]，对应的字节偏移是 4 × i。比如 A[3] 的偏移是 12，而不是 3。这是写汇编时最常见的错误之一。":
        "So in C, the element A[i] sits at a byte offset of four times i. For example, A[3] "
        "is at offset 12, not 3, and mixing those two up is one of the most common mistakes "
        "in assembly.",
    "比如 A[3] 的偏移是 12": "For example",
    "sw 是 store word，方向相反：把寄存器的值写进内存。来看一个完整的例子。A[3] = h + A[1]，其中 h 在 s1 里。先把 A[1] 读进来……":
        "The store instruction sw goes the other way and writes a register's value into "
        "memory. Let's work through a complete example, where element three of the array A is "
        "set to h plus element one, and h is kept in s1. First we load element one into a "
        "register.",
    "A[3] = h + A[1]": "Let's work through a complete example",
    "先把 A[1] 读进来": "First we load element one",
    "……再加上 h：t0 = 10 + 12 = 22，最后用 sw 写回 A[3]。注意 sw 把源寄存器写在前面，内存地址写在后面。":
        "Next we add h, so t0 becomes ten plus twelve, which is twenty-two. Finally sw writes "
        "that value back to element three, and notice that sw lists the source register first "
        "and the memory address second.",
    "最后用 sw 写回 A[3]": "Finally sw writes",
    "22 的十六进制是 0x16，按小端序存进 0x10C：16 00 00 00。":
        "In hexadecimal, twenty-two is 0x16, so with little-endian order the lowest address, "
        "0x10C, holds the byte 0x16, and the three bytes after it hold zero.",
    "除了整个字，也可以只读写一个字节：lb、lbu 和 sb。lb 把这个字节读进 32 位的寄存器。那多出来的 24 位，要填什么？":
        "Besides whole words, RISC-V can also read and write a single byte, using the "
        "instructions lb, lbu, and sb. When lb loads a byte into a thirty-two bit register, "
        "twenty-four extra bits are left over, so what should they be filled with?",
    "lb 把这个字节读进 32 位的寄存器": "When lb loads a byte",
    "lb 做“符号扩展”：把最高位（符号位）复制到所有高位。0xF3 的最高位是 1，于是高 24 位全是 1，得到 0xFFFFFFF3。0xF3 当作有符号数是 −13，扩展后仍是 −13。":
        "The answer is sign extension, which copies the top bit, the sign bit, into all the "
        "higher bits. The top bit of 0xF3 is a one, so all twenty-four upper bits become "
        "ones, giving 0xFFFFFFF3. As a signed number, 0xF3 is minus thirteen, and after "
        "extension it is still minus thirteen.",
    "得到 0xFFFFFFF3": "giving 0xFFFFFFF3",
    "于是高 24 位全是 1": "so all twenty-four upper bits",
    "lbu 是无符号版本：高位一律填 0，结果是 243。sb 则只把寄存器最低的 8 位写进内存，高 24 位直接忽略。":
        "The unsigned version, lbu, always fills the upper bits with zeros, so the result is "
        "243. And sb goes the other way, writing only the lowest eight bits of a register to "
        "memory and ignoring the other twenty-four.",
    "sb 则只把寄存器最低的 8 位写进内存": "And sb goes the other way",
    "半字（16 位）也是同样的规则：lh、lhu、sh。在 RV32 里，lw 已经读满 32 位，不需要扩展，所以没有 lwu。":
        "Halfwords, which are sixteen bits, follow the same rules with lh, lhu, and sh. And "
        "since lw already reads a full thirty-two bits, it needs no extension, which is why "
        "RV32 has no lwu.",
    "在 RV32 里": "And since lw already reads",
}
