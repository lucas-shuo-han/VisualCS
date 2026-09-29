"""English for episode 14 (keys are the Chinese strings in ep14_hello_world.py)."""

EN = {
    # ---- end card
    "汇编指示不产生指令，只告诉汇编器如何组织目标文件":
        "Directives produce no instructions; they tell the assembler how to lay out the object file",
    "hello.o 里未知的地址先填 0，并记进重定位表":
        "Unknown addresses in hello.o are left as 0 and listed in the relocation table",
    "文件内的 PC 相对跳转不用重定位，静态数据和外部函数则需要":
        "PC-relative jumps within a file need no relocation; static data and external functions do",
    "链接器排好各段、算出符号地址，再逐项补洞":
        "The linker lays out the segments, computes symbol addresses, then fills each hole",
    "静态链接自给自足；动态链接更省空间、更易升级":
        "Static linking is self-contained; dynamic linking saves space and eases upgrades",

    # ---- intro and quick check
    "小测验": "Quick check",
    "哪一步之后，这两条指令的机器码才完全确定？":
        "After which step are all the machine code bits of these two instructions known?",
    "编译": "Compile",
    "汇编": "Assemble",
    "链接": "Link",
    "加载": "Load",
    "上一集讲了 CALL 的四个步骤。这一集，我们跟着一个真实的程序走完全程。":
        "Last time we met the four steps of CALL. This time, let's follow one real program all the way through.",
    "先来个小测验：下面两条指令的机器码，要到哪一步之后才完全确定？":
        "First, a quick check: after which step are all the machine code bits of these two instructions known?",

    # ---- compiler, directives
    "编译器": "Compiler",
    "第一步，编译器把 C 代码翻译成汇编，得到 hello.s。":
        "Step one: the compiler translates the C code into assembly, hello.s.",
    "注意 la、call、li、ret 都是伪指令，要留给汇编器展开。":
        "Note that la, call, li and ret are pseudo-instructions, left for the assembler to expand.",
    "以点开头的是汇编指示（directive）：不产生机器指令，只告诉汇编器怎样组织目标文件。":
        "Lines starting with a dot are directives: they produce no machine instructions, "
        "they tell the assembler how to lay out the object file.",
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
        ".text says what follows goes in the text segment; .align 2 aligns it to 2² = 4 bytes.",
    ".global（也写作 .globl）把 main 声明为全局符号，别的文件也能引用它。":
        ".global (also spelled .globl) makes main a global symbol that other files can refer to.",
    "接着切换到只读数据段 .rodata，同样按 4 字节对齐。":
        "Then we switch to the read-only data section, .rodata, again aligned to 4 bytes.",
    ".string 存入以 0 结尾的字符串，标签 str1、str2 标出它们的起点。":
        ".string stores a null-terminated string; the labels str1 and str2 mark where each one starts.",
    "另外两个常用指示这里没用到：.data 进入数据段，.word 依次存放 32 位的字。":
        "Two other common directives aren't used here: .data switches to the data segment, "
        "and .word stores 32-bit words one after another.",

    # ---- assembler: hello.o
    "第二步，汇编器生成目标文件 hello.o。它是二进制的，直接看只是一串十六进制数。":
        "Step two: the assembler produces the object file hello.o. It's binary: "
        "looked at directly, it's just a run of hex numbers.",
    "地址": "Address",
    "机器码": "Machine code",
    "指令": "Instruction",
    "把 main 反汇编出来：左列是模块内的地址，中间是机器码，右列是指令。":
        "Disassembling main: addresses within the module on the left, machine code in the middle, "
        "instructions on the right.",
    "注：la 也可能展开成 auipc + addi；call 通常是 auipc + jalr（第 12 集）":
        "Note: la may also become auipc + addi; call is usually auipc + jalr (Episode 12)",
    "伪指令都展开了。注意这份清单做了简化：call 只变成了一条 jalr。":
        "The pseudo-instructions are expanded. This listing is simplified: call became a single jalr.",
    "但这五条的立即数都是 0，只是占位符：数据和 printf 在哪，汇编器还不知道。":
        "But these five have immediates of 0, just placeholders: "
        "the assembler doesn't yet know where the data or printf will be.",
    "其余指令不涉及地址，汇编完，机器码就定了。":
        "The other instructions involve no addresses, so their machine code is final after assembly.",
    "符号表": "Symbol table",
    "标签": "Label",
    "段内地址": "Offset in segment",
    "类型": "Type",
    "符号表记下本文件的标签，以及它们在各自段内的地址；调试器 gdb 也要用它。":
        "The symbol table lists this file's labels and their offsets within their segments; "
        "the debugger gdb uses it too.",
    "main 在代码段偏移 0 处，类型是 global，这正是 .global 的作用。":
        "main sits at offset 0 of the text segment and is global: that's what .global did.",
    "数据段（.rodata）": "Data segment (.rodata)",
    "两个字符串是局部数据。第一个连同结尾的 0 共 12 字节，所以第二个从 0xc 开始。":
        "Both strings are local data. The first is 12 bytes including its terminating 0, "
        "so the second starts at 0xc.",
    "重定位表": "Relocation table",
    "依赖": "Depends on",
    "重定位表是留给链接器的“待办清单”，每一项对应一个占位符。":
        "The relocation table is the linker's to-do list: one entry per placeholder.",
    "前两项：0x8 处的 lui 等着 str1 地址的高 20 位，0xc 处的 addi 等着低 12 位。":
        "The first two: the lui at 0x8 waits for the upper 20 bits of str1's address, "
        "the addi at 0xc for the lower 12.",
    "str2 的两项同理；最后一项在 0x18，jalr 等着 printf 的地址。":
        "Same for str2; the last entry, at 0x18, is the jalr waiting for printf's address.",

    # ---- three kinds of addresses
    "哪些地址需要重定位？": "Which addresses need relocating?",
    "① 文件内的 PC 相对跳转": "① PC-relative, within the file",
    "② 静态数据的绝对地址": "② Absolute address of static data",
    "③ 外部函数": "③ External function",
    "汇编器直接算好": "Assembler resolves it",
    "B 型分支从不用改": "B-type never needs editing",
    "进重定位表": "→ relocation table",
    "为什么有的地址汇编器就能定，有的却要等链接器？因为地址分三种。":
        "Why can the assembler settle some addresses but not others? Because there are three kinds.",
    "一、文件内的 PC 相对跳转，比如 beq，或 jal 到本文件的标签：代码整体挪到哪儿，距离都不变。":
        "One: PC-relative jumps within the file, like beq, or jal to a local label. "
        "Wherever the code moves, the distance stays the same.",
    "二、静态数据的地址，比如 la 要装入的 str1、lw 要读的全局变量：要等所有文件拼好才知道。":
        "Two: addresses of static data, like str1 for la, or a global that lw reads. "
        "They're known only once all the files are put together.",
    "三、外部函数，比如 printf：它在别的文件里，汇编器连它有多远都不知道。":
        "Three: external functions like printf. It lives in another file, "
        "so the assembler can't even tell how far away it is.",
    "后两种要记进重定位表。所以 jal 有时要改，而 B 型分支只在模块内跳，从来不用改。":
        "The last two go into the relocation table. So jal sometimes needs editing, "
        "but B-type branches stay within the module and never do.",

    # ---- linker
    "链接：hello.o → a.out": "Linking: hello.o → a.out",
    "启动例程": "Start-up code",
    "第三步，链接器把 hello.o、启动例程和库里的 printf 拼成可执行文件 a.out。":
        "Step three: the linker combines hello.o, the start-up code and printf from the library "
        "into the executable a.out.",
    "一包 .o 文件": "a bundle of .o files",
    "printf 在哪？链接器先查用户的 .o 文件，找不到再查库。库文件 .a 其实就是一包 .o 文件。":
        "Where's printf? The linker searches the user's .o files first, then the libraries. "
        "A .a library is just a bundle of .o files.",
    "重新编译": "recompile",
    "不用重新编译": "no recompiling",
    "链接也让分开编译成为可能：改了 hello.c 只需重新编译它自己，庞大的 C 库不用跟着重编。":
        "Linking also makes separate compilation possible: change hello.c and only it gets recompiled, "
        "not the huge C library.",
    "先把各代码段从 0x10000 起首尾相接：启动例程在最前，接着是 main，再往后是 printf。":
        "First the text segments are laid end to end from 0x10000: start-up code first, "
        "then main, and further on, printf.",
    "数据段接在代码之后：str1 在 0x20A10，str2 比它晚 12 字节。":
        "The data segment follows the code: str1 lands at 0x20A10, str2 12 bytes later.",
    "符号表（链接后）": "Symbol table (linked)",
    "符号": "Symbol",
    "所有符号的最终地址都定了，链接器据此更新符号表。":
        "Every symbol now has its final address, and the linker updates the symbol table.",
    "然后按重定位表逐项补洞。先换上每条指令的最终地址。":
        "Then it works through the relocation table, filling each hole. "
        "First, every instruction gets its final address.",
    "从 str1 = 0x20A10 开始：低 12 位 0xA10 的最高位是 1，addi 会把它当成负数 −1520。":
        "Start with str1 = 0x20A10. The low 12 bits, 0xA10, have their top bit set, "
        "so addi reads them as the negative number -1520.",
    "所以高 20 位要多加 1，写成 0x21。这正是第 12 集里 li 的拆法。":
        "So the upper 20 bits get an extra 1: 0x21. It's the same split li uses, from Episode 12.",
    "把 0x21 填进 lui 的立即数字段：占位的 0 变成了真正的地址位。":
        "0x21 goes into lui's immediate field: the placeholder zeros become real address bits.",
    "addi 填入 −1520，这两条指令就补全了。": "addi gets -1520, and both instructions are complete.",
    "str2 同理：lui 也填 0x21，addi 填 −1508。": "Likewise for str2: lui gets 0x21 again, addi gets -1508.",
    "最后是 printf：它在 0x10450，离这条调用 0x288 字节。":
        "Finally, printf: it's at 0x10450, 0x288 bytes from the call.",
    "链接器旧称“链接编辑器”，\n因为它改写的正是这些“链接”":
        "The linker's old name, \"link editor\",\ncomes from editing these links",
    "jal 能跳 ±1 MiB，足够了：链接器把这里直接改写成一条 jal。":
        "jal reaches ±1 MiB, which is plenty, so the linker rewrites this as a single jal.",
    "文件头": "Header",
    "调试信息": "Debugging info",
    "其余指令一位没动。再加上文件头和调试信息，a.out 就完成了：每一位都已确定。":
        "The other instructions are untouched. Add a header and debugging info, "
        "and a.out is done: every bit is now fixed.",

    # ---- quick check, answered
    "回到小测验：add 不涉及任何地址，汇编之后就确定了。":
        "Back to the quick check: add involves no addresses, so it's settled after assembly.",
    "汇编之后": "After assembly",
    "链接之后": "After linking",
    "而 jal 跳向 stdio 库里的外部函数 fprintf，要到链接之后才确定。":
        "But jal targets fprintf, an external function in the stdio library, "
        "so it's settled only after linking.",

    # ---- static vs dynamic linking
    "静态链接": "Static linking",
    "动态链接": "Dynamic linking",
    "代码": "code",
    "libc 副本": "libc copy",
    "程序 A": "Program A",
    "程序 B": "Program B",
    "每个程序都很大": "Every program is big",
    "刚才这种叫静态链接：库代码直接拷进 a.out，程序自给自足，但文件很大。":
        "What we just did is static linking: the library code is copied into a.out. "
        "The program is self-contained, but large.",
    "漏洞": "bug",
    "库一旦修了 bug 或安全漏洞，每个程序都得重新链接、重新发布。":
        "When the library fixes a bug or a security hole, every program must be relinked and shipped again.",
    "逐个重新链接、重新发布": "Relink and reship each one",
    "加载时链接": "linked at load time",
    "动态链接则把库单独存成文件，比如 libc.so，等程序加载时才链接进来。":
        "Dynamic linking keeps the library in its own file, such as libc.so, "
        "and links it in when the program is loaded.",
    "libc.so（新）": "libc.so (new)",
    "一份库，大家共享": "One library, shared",
    "程序文件更小，多个程序还能共享内存里的同一份库；换掉 libc.so，大家一起升级。":
        "Programs get smaller, and they can share one copy of the library in memory. "
        "Replace libc.so and they all upgrade.",
    "运行时有链接开销": "Linking cost at run time",
    "光有 a.out 不够，还要库文件": "a.out alone isn't enough",
    "代价是运行时的链接开销，而且光有 a.out 已经跑不起来。总体上仍是利大于弊。":
        "The cost: linking overhead at run time, and a.out alone no longer runs. "
        "On balance, it's still worth it.",

    # ---- bonus: interpretation vs translation
    "番外：解释与翻译": "Bonus: interpretation vs. translation",
    "（不考）": "(not tested)",
    "解释器逐句执行": "interpreted",
    "字节码 + 解释执行": "bytecode, interpreted",
    "编译成机器码": "compiled",
    "硬件直接执行": "run by hardware",
    "← 更好写": "← easier to write",
    "更快 →": "faster →",
    "番外（不考）：程序也可以不翻译，而是交给解释器（另一个程序）直接执行。":
        "A bonus, not tested: instead of translating a program, we can hand it to an interpreter, "
        "another program that runs it directly.",
    "Python 全靠解释，最好写也最慢；Java 先编译成字节码再解释，所以到处都能跑。":
        "Python is fully interpreted: easiest to write, slowest to run. "
        "Java compiles to bytecode, which is then interpreted, so it runs anywhere.",
    "C 编译成机器码，快得多。机器码最难手写，却最好“解释”：硬件直接就能执行。":
        "C compiles to machine code and is much faster. Machine code is the hardest to write, "
        "yet the easiest to \"interpret\": the hardware runs it directly.",
    "Venus：用软件逐条执行 RISC-V": "Venus: runs RISC-V in software",
    "Rosetta：让 Intel 程序跑在 Apple 芯片上": "Rosetta: runs Intel apps on Apple chips",
    "机器码也能用软件来解释：Venus 逐条模拟 RISC-V，方便单步调试。":
        "Machine code can be interpreted in software too: Venus simulates RISC-V one instruction "
        "at a time, so you can step through it.",
    "Apple 几次更换 ISA，都靠软件来运行旧 ISA 的程序，最近的一次就是 Rosetta。":
        "Each time Apple switched ISAs, software ran the programs built for the old one. "
        "The latest is Rosetta.",
    "解释的长处": "Interpretation",
    "更容易实现": "Easier to write",
    "报错、调试更友好": "Better errors and debugging",
    "代码更小，不依赖具体 ISA": "Smaller code, ISA-independent",
    "翻译的长处": "Translation",
    "通常快 10 倍以上": "Usually 10× faster or more",
    "不必公开源代码": "Hides the source code",
    "程序自己分不清跑在解释器上还是硬件上": "A program can't tell an interpreter from hardware",
    "解释器好写、好调试、可移植；翻译后的程序通常快 10 倍以上，还不必公开源代码。":
        "Interpreters are easier to write, debug and port; translated programs usually run "
        "10 times faster or more, and keep the source private.",

    # ---- finale
    "串起来看：编译成汇编，汇编成带占位符的机器码，链接时补上地址，最后加载运行。":
        "Putting it together: compile to assembly, assemble to machine code with placeholders, "
        "fill in the addresses when linking, then load and run.",
    "加载器把 a.out 读进内存，经启动例程调用 main，屏幕上就出现了 Hello, world!":
        "The loader reads a.out into memory, the start-up code calls main, and Hello, world! appears.",
    "这也是整个系列的缩影：从寄存器、内存、分支、函数，到指令编码和 CALL。":
        "It's the whole series in miniature: registers, memory, branches, functions, "
        "instruction encoding, and CALL.",
    "从一行 printf 到一串确定的比特，这就是程序运行前走过的路。":
        "From one line of printf to a string of settled bits: that's the road a program travels before it runs.",
}
