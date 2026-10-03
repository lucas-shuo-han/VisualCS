"""English for episode 14 (keys are the Chinese strings in ep14_hello_world.py)."""

EN = {
    # ---- end card
    "汇编指示不产生指令，只告诉汇编器如何组织目标文件":
        "Directives produce no instructions, and only tell the assembler how to lay out the "
        "object file",
    "hello.o 里未知的地址先填 0，并记进重定位表":
        "Unknown addresses in hello.o are left as zero, and listed in the relocation table",
    "文件内的 PC 相对跳转不用重定位，静态数据和外部函数则需要":
        "PC-relative jumps within a file need no relocation, but static data and external "
        "functions do",
    "链接器排好各段、算出符号地址，再逐项补洞":
        "The linker lays out the segments, works out the symbol addresses, and then fills in "
        "the holes",
    "静态链接自给自足；动态链接更省空间、更易升级":
        "Static linking is self-sufficient, while dynamic linking saves space and is easier "
        "to upgrade",

    # ---- intro and quick check
    "小测验": "Quick check",
    "哪一步之后，这两条指令的机器码才完全确定？":
        "After which step are all the machine code bits of these two instructions known?",
    "编译": "Compile",
    "汇编": "Assemble",
    "链接": "Link",
    "加载": "Load",

    # ---- compiler, directives
    "编译器": "Compiler",
    "汇编指示": "Directives",
    "代码段": "Text segment",
    "数据段": "Data segment",
    "全局符号": "Global symbol",
    "按 2² = 4 字节对齐": "Align to 2² = 4 bytes",
    "只读数据段": "Read-only data",
    "按 4 字节对齐": "Align to 4 bytes",
    "以 0 结尾的字符串": "Null-terminated string",
    "32 位的字": "32-bit words",
    ".text 表示接下来是代码段；.align 2 按 2² = 4 字节对齐。":
        "The .text directive says that code comes next, and .align 2 aligns to four bytes, "
        "which is two squared.",
    ".global（也写作 .globl）把 main 声明为全局符号，别的文件也能引用它。":
        "The .global directive, also written .globl, declares main as a global symbol, so "
        "other files can refer to it.",
    "接着切换到只读数据段 .rodata，同样按 4 字节对齐。":
        "Next we switch to the read-only data section, .rodata, again aligned to four bytes.",
    ".string 存入以 0 结尾的字符串，标签 str1、str2 标出它们的起点。":
        "The .string directive stores strings that end in a zero, and the labels str1 and "
        "str2 mark where they start.",

    # ---- assembler: hello.o
    "地址": "Address",
    "机器码": "Machine code",
    "指令": "Instruction",
    "注：la 也可能展开成 auipc + addi；call 通常是 auipc + jalr（第 12 集）":
        "Note: la may also become auipc + addi; call is usually auipc + jalr (Episode 12)",
    "符号表": "Symbol table",
    "标签": "Label",
    "段内地址": "Offset in segment",
    "类型": "Type",
    "数据段（.rodata）": "Data segment (.rodata)",
    "重定位表": "Relocation table",
    "依赖": "Depends on",

    # ---- three kinds of addresses
    "哪些地址需要重定位？": "Which addresses need relocating?",
    "① 文件内的 PC 相对跳转": "① PC-relative, within the file",
    "② 静态数据的绝对地址": "② Absolute address of static data",
    "③ 外部函数": "③ External function",
    "汇编器直接算好": "Assembler resolves it",
    "B 型分支从不用改": "B-type never needs editing",
    "进重定位表": "→ relocation table",

    # ---- linker
    "链接：hello.o → a.out": "Linking: hello.o → a.out",
    "启动例程": "Start-up code",
    "一包 .o 文件": "a bundle of .o files",
    "重新编译": "recompile",
    "不用重新编译": "no recompiling",
    "符号表（链接后）": "Symbol table (linked)",
    "符号": "Symbol",
    "链接器旧称“链接编辑器”，\n因为它改写的正是这些“链接”":
        "The linker's old name, \"link editor\",\ncomes from editing these links",
    "文件头": "Header",
    "调试信息": "Debugging info",

    # ---- quick check, answered
    "汇编之后": "After assembly",
    "链接之后": "After linking",

    # ---- static vs dynamic linking
    "静态链接": "Static linking",
    "动态链接": "Dynamic linking",
    "代码": "code",
    "libc 副本": "libc copy",
    "程序 A": "Program A",
    "程序 B": "Program B",
    "每个程序都很大": "Every program is big",
    "漏洞": "bug",
    "逐个重新链接、重新发布": "Relink and reship each one",
    "加载时链接": "linked at load time",
    "libc.so（新）": "libc.so (new)",
    "一份库，大家共享": "One library, shared",
    "运行时有链接开销": "Linking cost at run time",
    "光有 a.out 不够，还要库文件": "a.out alone isn't enough",

    # ---- bonus: interpretation vs translation
    "番外：解释与翻译": "Bonus: interpretation vs. translation",
    "（不考）": "(not tested)",
    "解释器逐句执行": "interpreted",
    "字节码 + 解释执行": "bytecode, interpreted",
    "编译成机器码": "compiled",
    "硬件直接执行": "run by hardware",
    "← 更好写": "← easier to write",
    "更快 →": "faster →",
    "Venus：用软件逐条执行 RISC-V": "Venus: runs RISC-V in software",
    "Rosetta：让 Intel 程序跑在 Apple 芯片上": "Rosetta: runs Intel apps on Apple chips",
    "解释的长处": "Interpretation",
    "更容易实现": "Easier to write",
    "报错、调试更友好": "Better errors and debugging",
    "代码更小，不依赖具体 ISA": "Smaller code, ISA-independent",
    "翻译的长处": "Translation",
    "通常快 10 倍以上": "Usually 10× faster or more",
    "不必公开源代码": "Hides the source code",
    "程序自己分不清跑在解释器上还是硬件上": "A program can't tell an interpreter from hardware",

    # ---- finale

    # ---- spoken beats and cue phrases (see references/narration-writing.md)
    "上一集讲了 CALL 的四个步骤。这一集，我们跟着一个真实的程序走完全程。":
        "The last episode covered the four steps of CALL. In this one, we follow a real "
        "program all the way through.",
    "先来个小测验：下面两条指令的机器码，要到哪一步之后才完全确定？":
        "First, a quick quiz. For the two instructions below, after which step is the machine "
        "code completely settled?",
    "第一步，编译器把 C 代码翻译成汇编，得到 hello.s。注意 la、call、li、ret 都是伪指令，要留给汇编器展开。":
        "In step one, the compiler translates the C code into assembly, giving hello.s. "
        "Notice that la, call, li, and ret are all pseudo-instructions, left for the "
        "assembler to expand.",
    "注意 la、call、li、ret": "Notice that la",
    "得到 hello.s": "giving hello.s",
    "以点开头的是汇编指示（directive）：不产生机器指令，只告诉汇编器怎样组织目标文件。":
        "Everything that begins with a dot is an assembler directive. It produces no machine "
        "instruction, and only tells the assembler how to organize the object file.",
    "另外两个常用指示这里没用到：.data 进入数据段，.word 依次存放 32 位的字。":
        "Two other common directives aren't used here. The .data directive enters the data "
        "segment, and .word stores thirty-two bit words one after another.",
    "第二步，汇编器生成目标文件 hello.o。它是二进制的，直接看只是一串十六进制数。":
        "In step two, the assembler produces the object file hello.o. It is binary, so looked "
        "at directly it is just a string of hexadecimal numbers.",
    "把 main 反汇编出来：左列是模块内的地址，中间是机器码，右列是指令。伪指令都展开了。注意这份清单做了简化：call 只变成了一条 jalr。":
        "Let's disassemble main. The left column holds addresses within the module, the "
        "middle holds the machine code, and the right column holds the instructions. All the "
        "pseudo-instructions have been expanded, though this listing is simplified, and call "
        "becomes only one jalr.",
    "伪指令都展开了": "All the pseudo-instructions have been expanded",
    "但这五条的立即数都是 0，只是占位符：数据和 printf 在哪，汇编器还不知道。其余指令不涉及地址，汇编完，机器码就定了。":
        "But the immediates of these five instructions are all zero. They are just "
        "placeholders, because the assembler doesn't yet know where the data and printf are. "
        "The other instructions involve no address, so once assembled, their machine code is "
        "settled.",
    "其余指令不涉及地址": "The other instructions involve no address",
    "符号表记下本文件的标签，以及它们在各自段内的地址；调试器 gdb 也要用它。main 在代码段偏移 0 处，类型是 global，这正是 .global 的作用。":
        "The symbol table records this file's labels and their addresses within their own "
        "segments, and the debugger gdb needs it too. The label main is at offset zero in the "
        "code segment, with type global, which is exactly what .global does.",
    "main 在代码段偏移 0 处": "The label main",
    "两个字符串是局部数据。第一个连同结尾的 0 共 12 字节，所以第二个从 0xc 开始。":
        "The two strings are local data. The first one, including its terminating zero, takes "
        "twelve bytes, so the second one starts at 0xc.",
    "第一个连同结尾的 0": "The first one",
    "所以第二个从 0xc 开始": "so the second one starts at",
    "重定位表是留给链接器的“待办清单”，每一项对应一个占位符。前两项：0x8 处的 lui 等着 str1 地址的高 20 位，0xc 处的 addi 等着低 12 位。str2 的两项同理；最后一项在 0x18，jalr 等着 printf 的地址。":
        "The relocation table is a to-do list for the linker, with an entry for every "
        "placeholder. The first two entries are the lui at 0x8, which is waiting for the "
        "upper twenty bits of the address of str1. The addi at 0xc is waiting for the lower "
        "twelve bits. The two entries for str2 work the same way, and the last one, at 0x18, "
        "is a jalr waiting for the address of printf.",
    "前两项": "The first two entries",
    "str2 的两项同理": "The two entries for str2",
    "为什么有的地址汇编器就能定，有的却要等链接器？因为地址分三种。一、文件内的 PC 相对跳转，比如 beq，或 jal 到本文件的标签：代码整体挪到哪儿，距离都不变。":
        "Why can the assembler settle some addresses, while others must wait for the linker? "
        "Because addresses come in three kinds. First, PC-relative jumps within the file, "
        "such as beq, or a jal to a label in this file, where the distance stays the same "
        "wherever the code as a whole moves.",
    "一、文件内的 PC 相对跳转": "First, PC-relative jumps",
    "代码整体挪到哪儿": "wherever the code as a whole moves",
    "二、静态数据的地址，比如 la 要装入的 str1、lw 要读的全局变量：要等所有文件拼好才知道。三、外部函数，比如 printf：它在别的文件里，汇编器连它有多远都不知道。后两种要记进重定位表。所以 jal 有时要改，而 B 型分支只在模块内跳，从来不用改。":
        "Second, the addresses of static data, such as the str1 that la loads, or a global "
        "variable that lw reads, can't be known until all the files are put together. Third, "
        "external functions, such as printf, are in another file, so the assembler doesn't "
        "even know how far away they are. The last two kinds go into the relocation table, "
        "which is why a jal sometimes has to be changed, while a B-type branch only jumps "
        "within the module and never needs to.",
    "三、外部函数": "Third, external functions",
    "后两种要记进重定位表": "The last two kinds",
    "第三步，链接器把 hello.o、启动例程和库里的 printf 拼成可执行文件 a.out。":
        "In step three, the linker puts hello.o, the startup routine, and the printf from the "
        "library together into the executable a.out.",
    "printf 在哪？链接器先查用户的 .o 文件，找不到再查库。库文件 .a 其实就是一包 .o 文件。链接也让分开编译成为可能：改了 hello.c 只需重新编译它自己，庞大的 C 库不用跟着重编。":
        "Where is printf? The linker looks through your own .o files first, and then through "
        "the libraries, and a .a library file is really just a bundle of .o files. Linking "
        "also makes separate compilation possible, so if you change hello.c, only that file "
        "needs recompiling, and the huge C library doesn't have to be rebuilt.",
    "链接也让分开编译成为可能": "Linking also makes separate compilation",
    "找不到再查库": "and then through the libraries",
    "库文件 .a 其实就是一包": "a .a library file is really",
    "先把各代码段从 0x10000 起首尾相接：启动例程在最前，接着是 main，再往后是 printf。数据段接在代码之后：str1 在 0x20A10，str2 比它晚 12 字节。":
        "First the code segments are joined end to end from 0x10000, with the startup routine "
        "first, then main, and then printf. The data segment follows the code, with str1 at "
        "0x20A10, and str2 twelve bytes after it.",
    "数据段接在代码之后": "The data segment follows",
    "启动例程在最前": "with the startup routine first",
    "接着是 main": "then main",
    "再往后是 printf": "and then printf",
    "所有符号的最终地址都定了，链接器据此更新符号表。":
        "With the final addresses of all the symbols settled, the linker updates the symbol "
        "table to match.",
    "据此更新符号表": "updates the symbol table",
    "然后按重定位表逐项补洞。先换上每条指令的最终地址。从 str1 = 0x20A10 开始：低 12 位 0xA10 的最高位是 1，addi 会把它当成负数 −1520。所以高 20 位要多加 1，写成 0x21。这正是第 12 集里 li 的拆法。":
        "Then, entry by entry, it fills in the holes according to the relocation table. First "
        "it puts in each instruction's final address. Starting with str1, which is 0x20A10, "
        "the lower twelve bits, 0xA10, have a top bit of one, so addi would treat them as the "
        "negative number minus one thousand five hundred twenty. So the upper twenty bits "
        "must be one higher, written 0x21, which is exactly how li was split in episode "
        "twelve.",
    "从 str1 = 0x20A10 开始": "Starting with str1",
    "所以高 20 位要多加 1": "So the upper twenty bits",
    "先换上每条指令的最终地址": "First it puts in",
    "addi 会把它当成负数": "so addi would treat them",
    "把 0x21 填进 lui 的立即数字段：占位的 0 变成了真正的地址位。addi 填入 −1520，这两条指令就补全了。":
        "Now we put 0x21 into the immediate field of the lui, so the placeholder zeros turn "
        "into real address bits. And with minus one thousand five hundred twenty filled into "
        "the addi, these two instructions are complete.",
    "addi 填入 −1520": "And with minus one thousand",
    "占位的 0 变成了真正的地址位": "so the placeholder zeros",
    "str2 同理：lui 也填 0x21，addi 填 −1508。最后是 printf：它在 0x10450，离这条调用 0x288 字节。jal 能跳 ±1 MiB，足够了：链接器把这里直接改写成一条 jal。":
        "For str2 it is the same, with the lui also filled with 0x21, and the addi with minus "
        "one thousand five hundred eight. Last is printf, which is at 0x10450, and 0x288 "
        "bytes from this call. A jal can jump about one mebibyte either way, which is plenty, "
        "so the linker rewrites this directly into a single jal.",
    "最后是 printf": "Last is printf",
    "jal 能跳": "A jal can jump",
    "lui 也填 0x21": "with the lui also filled with",
    "其余指令一位没动。再加上文件头和调试信息，a.out 就完成了：每一位都已确定。":
        "None of the other instructions changed by a single bit. With the file header and "
        "debugging information added, a.out is complete, and every bit is settled.",
    "回到小测验：add 不涉及任何地址，汇编之后就确定了。而 jal 跳向 stdio 库里的外部函数 fprintf，要到链接之后才确定。":
        "Back to the quiz. The add involves no address, so it is settled after assembly. But "
        "the jal jumps to fprintf, an external function in the stdio library, so it isn't "
        "settled until after linking.",
    "而 jal": "But the jal",
    "汇编之后就确定了": "so it is settled after assembly",
    "刚才这种叫静态链接：库代码直接拷进 a.out，程序自给自足，但文件很大。库一旦修了 bug 或安全漏洞，每个程序都得重新链接、重新发布。":
        "What we just did is called static linking. The library code is copied right into "
        "a.out, so the program is self-sufficient, but the file is large. And once the "
        "library fixes a bug or a security hole, every program has to be relinked and "
        "redistributed.",
    "库一旦修了 bug": "And once the library fixes a bug",
    "但文件很大": "but the file is large",
    "每个程序都得重新链接": "every program has to be relinked",
    "动态链接则把库单独存成文件，比如 libc.so，等程序加载时才链接进来。程序文件更小，多个程序还能共享内存里的同一份库；换掉 libc.so，大家一起升级。代价是运行时的链接开销，而且光有 a.out 已经跑不起来。总体上仍是利大于弊。":
        "Dynamic linking instead stores the library as a separate file, such as libc.so, and "
        "links it in only when the program is loaded. The program files are smaller, several "
        "programs can share the same copy of the library in memory, and replacing libc.so "
        "upgrades everyone at once. The cost is link overhead at run time, and an a.out alone "
        "can no longer run, but overall the benefits still outweigh the costs.",
    "程序文件更小": "The program files are smaller",
    "代价是运行时的链接开销": "The cost is link overhead",
    "等程序加载时才链接进来": "only when the program is loaded",
    "换掉 libc.so": "and replacing libc.so",
    "番外（不考）：程序也可以不翻译，而是交给解释器（另一个程序）直接执行。Python 全靠解释，最好写也最慢；Java 先编译成字节码再解释，所以到处都能跑。":
        "As a bonus, which isn't on the exam, a program doesn't have to be translated at all, "
        "but can be handed to an interpreter, another program, to execute directly. Python "
        "relies entirely on interpretation, which makes it the easiest to write and the "
        "slowest. Java is first compiled to bytecode and then interpreted, so it runs "
        "everywhere.",
    "Python 全靠解释": "Python relies entirely",
    "C 编译成机器码，快得多。机器码最难手写，却最好“解释”：硬件直接就能执行。":
        "C is compiled to machine code, which is much faster. Machine code is the hardest to "
        "write by hand, but the best to interpret, since the hardware can execute it "
        "directly.",
    "机器码也能用软件来解释：Venus 逐条模拟 RISC-V，方便单步调试。Apple 几次更换 ISA，都靠软件来运行旧 ISA 的程序，最近的一次就是 Rosetta。":
        "Machine code can also be interpreted by software. Venus simulates RISC-V one "
        "instruction at a time, which makes single-step debugging easy. Apple has changed its "
        "ISA several times, each time using software to run programs from the old one, and "
        "the latest was Rosetta.",
    "Apple 几次更换 ISA": "Apple has changed its ISA",
    "解释器好写、好调试、可移植；翻译后的程序通常快 10 倍以上，还不必公开源代码。":
        "Interpreters are easy to write, easy to debug, and portable, while translated "
        "programs are usually more than ten times faster, and don't have to reveal their "
        "source code.",
    "串起来看：编译成汇编，汇编成带占位符的机器码，链接时补上地址，最后加载运行。加载器把 a.out 读进内存，经启动例程调用 main，屏幕上就出现了 Hello, world!":
        "Putting it together, the program is compiled into assembly, assembled into machine "
        "code with placeholders, linked to fill in the addresses, and finally loaded and run. "
        "The loader reads a.out into memory, and through the startup routine calls main, and "
        "Hello, world! appears on the screen.",
    "加载器把 a.out 读进内存": "The loader reads a.out",
    "屏幕上就出现了": "and Hello, world! appears",
    "这也是整个系列的缩影：从寄存器、内存、分支、函数，到指令编码和 CALL。从一行 printf 到一串确定的比特，这就是程序运行前走过的路。":
        "This is also a miniature of the whole series, from registers, memory, branches, and "
        "functions, to instruction encoding and CALL. From a single line of printf to a "
        "string of settled bits, this is the road a program travels before it runs.",
    "从一行 printf": "From a single line of printf",
    "到指令编码和 CALL": "to instruction encoding",
}
