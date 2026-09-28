"""English for episode 3 (keys are the Chinese strings in ep03_memory.py)."""

EN = {
    # end card
    "内存按字节寻址；一个字 = 4 字节": "Memory is byte-addressed; 1 word = 4 bytes",
    "小端序：低位字节放在低地址": "Little-endian: least significant byte at the lowest address",
    "lw / sw  寄存器, 偏移(基址)：地址 = 基址 + 偏移": "lw / sw  reg, offset(base): address = base + offset",
    "A[i] 的字节偏移是 4 × i": "A[i] is at byte offset 4 × i",
    "lb 符号扩展，lbu 零扩展": "lb sign-extends, lbu zero-extends",

    # why memory
    "内存 Memory": "Memory",
    "寄存器 × 32": "32 registers",
    "内存：数组、结构体……": "Memory:\narrays, structs...",
    "寄存器只有 32 个，可程序里有数组、结构体，成千上万个变量。寄存器放不下的，就放在内存里。":
        "There are only 32 registers, but programs have arrays, structs, thousands of variables. "
        "Whatever doesn't fit in registers goes in memory.",
    "load 加载": "load",
    "store 存储": "store",
    "RISC-V 是“加载-存储”架构：算术指令只能操作寄存器，访问内存必须用专门的指令。":
        "RISC-V is a load-store architecture: arithmetic works only on registers, "
        "and memory is accessed only through dedicated instructions.",
    "load 把数据从内存搬进寄存器，store 把寄存器的值写回内存。":
        "A load copies data from memory into a register; a store writes a register's value to memory.",

    # byte addressing
    "可以把内存想象成一个巨大的字节数组：每个字节都有自己的编号，也就是地址。":
        "Think of memory as one huge array of bytes: every byte has its own number, its address.",
    "为了看得清楚，每行画 4 个字节：第一行是 0x100 到 0x103，下一行从 0x104 开始。":
        "To keep it readable we draw 4 bytes per row: the first row is 0x100 to 0x103, "
        "and the next starts at 0x104.",
    "一个字占 4 个字节，所以相邻两个字的地址相差 4，而不是 1。":
        "A word takes 4 bytes, so the addresses of neighboring words differ by 4, not 1.",
    "字地址通常是 4 的倍数\n这叫“对齐”": "Word addresses are\nusually multiples of 4:\nthey're aligned",
    "字的地址通常是 4 的倍数，叫做“对齐”。不对齐的访问可能更慢，甚至直接出错。":
        "Word addresses are usually multiples of 4; we say they're aligned. "
        "A misaligned access may be slower, or even fail outright.",
    "一个 32 位的数，怎么放进 4 个字节？比如 0x12345678。":
        "How does a 32-bit number fit into 4 bytes? Take 0x12345678.",
    "高位": "high byte",
    "低位": "low byte",
    "RISC-V 通常采用小端序（little-endian）：最低位的字节放在最小的地址。":
        "RISC-V is normally little-endian: the least significant byte goes at the lowest address.",
    "所以从 0x100 往后看，依次是 78、56、34、12，像是“倒着”存的。":
        "So reading up from 0x100, the bytes are 78, 56, 34, 12, as if stored backwards.",
    "好在按字读写时，硬件会自动拼回原来的数，大多数时候你不用操心字节顺序。":
        "Luckily, when you load or store a whole word, the hardware puts the number back together, "
        "so most of the time you needn't worry about byte order.",

    # lw / sw
    "现在假设内存里有一个 int 数组 A：从地址 0x100 开始，每个元素占一个字。":
        "Now suppose memory holds an int array A, starting at address 0x100, one word per element.",
    "数组的起始地址，也叫基地址，放在 s0 里。": "The array's starting address, its base address, is in s0.",
    "lw 是 load word。lw t0, 8(s0)：从地址 s0 + 8 读一个字，放进 t0。":
        "lw means load word. lw t0, 8(s0) loads the word at address s0 + 8 into t0.",
    "偏移量 8 加上基地址，得到 0x108，正是 A[2] 所在的位置。":
        "The offset 8 plus the base address gives 0x108: exactly where A[2] lives.",
    "所以 C 里的 A[i]，对应的字节偏移是 4 × i。": "So A[i] in C is at byte offset 4 × i.",
    "偏移是 12，不是 3！": "The offset is 12, not 3!",
    "比如 A[3] 的偏移是 12，而不是 3。这是写汇编时最常见的错误之一。":
        "For A[3] the offset is 12, not 3. This is one of the most common mistakes in assembly.",
    "sw 是 store word，方向相反：把寄存器的值写进内存。来看一个完整的例子。":
        "sw means store word and goes the other way: it writes a register's value to memory. "
        "Let's work through a full example.",
    "A[3] = h + A[1]，其中 h 在 s1 里。先把 A[1] 读进来……":
        "A[3] = h + A[1], with h in s1. First, load A[1]...",
    "……再加上 h：t0 = 10 + 12 = 22……": "...then add h: t0 = 10 + 12 = 22...",
    "注意：sw 的源寄存器写在前面": "Note: sw lists the source register first",
    "……最后用 sw 写回 A[3]。注意 sw 把源寄存器写在前面，内存地址写在后面。":
        "...and finally sw stores it to A[3]. Note that sw puts the source register first "
        "and the memory address second.",
    "22 的十六进制是 0x16，按小端序存进 0x10C：16 00 00 00。":
        "22 is 0x16 in hex; stored little-endian at 0x10C, that's 16 00 00 00.",

    # bytes, sign extension
    "字节读写：lb / lbu / sb": "Bytes: lb / lbu / sb",
    "除了整个字，也可以只读写一个字节：lb、lbu 和 sb。":
        "Besides whole words, you can also load or store a single byte: lb, lbu and sb.",
    "内存中的一个字节": "a byte in memory",
    "扩展出来的 24 位": "24 extended bits",
    "读入的字节": "loaded byte",
    "lb 把这个字节读进 32 位的寄存器。那多出来的 24 位，要填什么？":
        "lb loads this byte into a 32-bit register. So what goes in the other 24 bits?",
    "lb 做“符号扩展”：把最高位（符号位）复制到所有高位。0xF3 的最高位是 1……":
        "lb sign-extends: it copies the top bit, the sign bit, into all the upper bits. "
        "The top bit of 0xF3 is 1...",
    "……于是高 24 位全是 1，得到 0xFFFFFFF3。0xF3 当作有符号数是 −13，扩展后仍是 −13。":
        "...so the upper 24 bits are all 1s, giving 0xFFFFFFF3. "
        "As a signed byte, 0xF3 is −13, and after extension it's still −13.",
    "lbu 是无符号版本：高位一律填 0，结果是 243。":
        "lbu is the unsigned version: it always fills the upper bits with 0, giving 243.",
    "sb：只把寄存器最低的 8 位写入内存，其余 24 位被忽略":
        "sb: stores only the lowest 8 bits; the upper 24 are ignored",
    "sb 则只把寄存器最低的 8 位写进内存，高 24 位直接忽略。":
        "sb stores just the register's lowest 8 bits to memory; the upper 24 bits are simply ignored.",
    "写入": "Store",
    "宽度": "Width",
    "无符号": "Unsigned",
    "有符号": "Signed",
    "字节 8 位": "Byte (8 bits)",
    "半字 16 位": "Half-word (16 bits)",
    "字 32 位": "Word (32 bits)",
    "半字（16 位）也是同样的规则：lh、lhu、sh。": "Half-words (16 bits) follow the same rules: lh, lhu, sh.",
    "在 RV32 里，lw 已经读满 32 位，不需要扩展，所以没有 lwu。":
        "In RV32, lw already fills all 32 bits, so there's nothing to extend, and no lwu.",
}
