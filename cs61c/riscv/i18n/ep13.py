"""English for episode 13 (keys are the Chinese strings in ep13_call.py)."""

EN = {
    # ---- end card
    "编译器：C → 汇编（可以含伪指令）":
        "The compiler turns C into assembly, which may use pseudo-instructions",
    "汇编器：展开伪指令，两遍扫描解决向前引用":
        "The assembler expands pseudo-instructions, and two passes resolve forward references",
    "目标文件 = 机器码 + 符号表 + 重定位表":
        "An object file holds machine code, a symbol table, and a relocation table",
    "链接器：拼接各段，按重定位表补全地址":
        "The linker joins the segments, and fills in addresses from the relocation table",
    "加载器：建立地址空间，复制代码和数据，经启动例程进入 main":
        "The loader builds an address space, copies the code and data, and enters main "
        "through the startup routine",

    # ---- overview
    "编译器": "Compiler",
    "汇编器": "Assembler",
    "链接器": "Linker",
    "加载器": "Loader",
    "运行": "Run",

    # ---- assembler
    "汇编器 Assembler": "Assembler",
    "符号表": "Symbol table",
    "jal  ra, printf     # printf 在别的文件里": "jal  ra, printf     # in another file",
    "la   t0, A          # 静态数据 A 的地址": "la   t0, A          # A: static data",
    "重定位表": "Relocation table",
    "文件头 header": "Header",
    "代码段 .text": "Text segment (.text)",
    "数据段 .data": "Data segment (.data)",
    "重定位表 relocation": "Relocation table",
    "符号表 symbol table": "Symbol table",
    "调试信息 debug": "Debugging info",

    # ---- linker
    "链接器 Linker": "Linker",
    "foo 代码": "foo text",
    "foo 数据": "foo data",
    "lib 代码": "lib text",
    "lib 数据": "lib data",

    # ---- loader
    "加载器 Loader": "Loader",
    "栈 Stack": "Stack",
    "堆 Heap": "Heap",
    "静态数据": "Static data",
    "代码 Text": "Text",
    "新的地址空间": "New address space",
    "1. 读文件头，得知各段大小": "1. Read the header: segment sizes",
    "2. 创建新的地址空间": "2. Create a new address space",
    "3. 把代码和数据复制进内存": "3. Copy code and data into memory",
    "4. 把命令行参数放到栈上": "4. Put command-line args on the stack",
    "5. 初始化寄存器，sp 指向栈顶": "5. Initialize registers; sp → stack top",
    "6. 跳到启动例程，再由它调用 main": "6. Jump to start-up code, which calls main",
    "代码": "Text",
    "数据": "Data",

    # ---- wrap up
    "在内存中运行": "Running in memory",
    "①② 机器结构与算术": "①② Machines & arithmetic",
    "③④ 内存": "③④ Memory",
    "⑤⑥ 分支与循环": "⑤⑥ Branches & loops",
    "⑦⑧ 函数与栈": "⑦⑧ Functions & the stack",
    "⑨–⑫ 指令编码": "⑨–⑫ Instruction encoding",

    # ---- spoken beats and cue phrases (see references/narration-writing.md)
    "从一个 C 文件到一个正在运行的程序，要经过四个步骤。编译器 Compiler、汇编器 Assembler、链接器 Linker、加载器 Loader——首字母连起来，就是 CALL。":
        "Going from a C file to a running program takes four steps. They are the Compiler, "
        "the Assembler, the Linker, and the Loader, and their initials spell CALL.",
    "编译器 Compiler": "They are the Compiler",
    "编译器把 C 翻译成汇编——前面几集，我们一直在手工做这件事。编译器输出的汇编里可以有伪指令，比如 mv、li、j，展开的活儿留给汇编器。":
        "The compiler translates C into assembly, which is what we have been doing by hand in "
        "the last few episodes. The assembly a compiler outputs can contain pseudo-instructions, such as mv, li, and j, leaving the work of expanding them to the "
        "assembler.",
    "汇编器读入汇编代码，产出目标文件（object file）。里面除了机器码，还有链接和调试要用的信息。第一件事：把伪指令展开成真实的指令。":
        "The assembler reads assembly code and produces an object file, which holds the "
        "machine code plus information needed for linking and debugging. Its first job is to "
        "expand pseudo-instructions into real instructions.",
    "第一件事": "Its first job",
    "第二件事：把标签换算成偏移。但这里有个麻烦：向前引用（forward reference）。汇编器读到 bne 时，还没见过 Skip 的定义，不知道该跳多远。":
        "The second job is converting labels into offsets, but there is a catch, the forward "
        "reference. When the assembler reads the bne, it hasn't seen the definition of Skip "
        "yet, so it doesn't know how far to jump.",
    "汇编器读到 bne 时": "When the assembler reads the bne",
    "解决办法：扫描两遍。第一遍不生成机器码，只把每个标签的地址记进符号表（symbol table）。第二遍再生成机器码。这时 Skip 的地址已知：偏移 = 0x08 − 0x00 = 8。":
        "The fix is to scan twice. The first pass generates no machine code, and only records "
        "each label's address in the symbol table. On the second pass we generate the machine "
        "code, and now the address of Skip is known, so the offset is 0x08 minus 0x00, which "
        "is eight.",
    "第二遍再生成机器码": "On the second pass",
    "第一遍不生成机器码": "The first pass",
    "记进符号表": "in the symbol table",
    "偏移 = 0x08": "so the offset is",
    "但有些地址，扫多少遍都算不出来：调用另一个文件里的 printf，或者取静态数据 A 的地址。它们的最终地址要等链接时才知道。汇编器把这些“待补的洞”记进重定位表（relocation table），留给链接器。":
        "But some addresses can't be worked out however many times we scan, such as calling "
        "printf in another file, or taking the address of static data A. Their final "
        "addresses aren't known until link time, so the assembler records these holes to be "
        "filled in the relocation table, and leaves them to the linker.",
    "它们的最终地址": "Their final addresses",
    "所以一个目标文件包含：文件头、代码段、数据段、重定位表、符号表，还有调试信息。":
        "So an object file contains a header, the code segment, the data segment, the "
        "relocation table, the symbol table, and debugging information.",
    "链接器把多个目标文件拼成一个可执行文件。第一步：把各文件的代码段首尾相接，再把数据段接在后面。":
        "The linker puts several object files together into one executable. Step one is to "
        "join the code segments of the files end to end, and then put the data segments after "
        "them.",
    "第一步": "Step one",
    "代码段首尾相接": "join the code segments",
    "再把数据段接在后面": "and then put the data",
    "第二步：各段位置一旦排定（代码从 0x10000 开始），每个符号的最终地址也就定了，比如 printf 在 0x10180。":
        "Step two. Once the positions of the segments are fixed, with the code starting at "
        "0x10000, the final address of every symbol is fixed too, for example printf at "
        "0x10180.",
    "比如 printf 在": "for example printf",
    "第三步：按重定位表逐个补洞。foo 里 0x10040 处的 jal 要跳到 printf，jal 用 PC 相对偏移，所以填进去的是 0x10180 − 0x10040 = 0x140。":
        "Step three is to fill in the holes one by one, using the relocation table. The jal "
        "at 0x10040 in foo has to jump to printf. Since jal uses a PC-relative offset, what "
        "goes in is 0x10180 minus 0x10040, which is 0x140.",
    "jal 用 PC 相对偏移": "Since jal uses a PC-relative offset",
    "而文件内部的分支完全不用改：PC 相对偏移，整块挪动后依然正确。这正是第 11 集说的“位置无关”。顺便一提：现代系统还常用“动态链接”，库要等程序加载时才链接进来。这里讲的是静态链接。":
        "Branches inside a file need no change at all, because PC-relative offsets stay "
        "correct when the whole block moves, which is exactly the position independence from "
        "episode eleven. By the way, modern systems often use dynamic linking, where "
        "libraries are linked in only when the program is loaded, but what we describe here "
        "is static linking.",
    "最后，操作系统中的加载器负责把可执行文件真正运行起来。它先读文件头，得知代码段和数据段有多大，再为程序创建一个新的地址空间……":
        "Finally, the loader in the operating system actually gets the executable running. It "
        "first reads the header, to learn how big the code and data segments are, and creates "
        "a new address space for the program.",
    "它先读文件头": "It first reads the header",
    "……然后把代码和数据复制进内存，把命令行参数放到栈上，初始化寄存器，让 sp 指向栈顶，最后跳到启动例程，由它调用 main。程序开始运行！":
        "Then it copies the code and data into memory, puts the command-line arguments on the "
        "stack, initializes the registers, and points sp at the top of the stack. Finally it "
        "jumps to the startup routine, which calls main, and the program starts running!",
    "把命令行参数放到栈上": "puts the command-line arguments",
    "最后跳到启动例程": "Finally it jumps to",
    "到这里，我们走完了一整条路：C 代码，到汇编，到机器码，再到内存里运行的程序。寄存器、内存、分支、函数调用、指令编码、编译链接——这就是 CS61C 中 RISC-V 部分的全貌。":
        "That completes the whole journey, from C code to assembly, to machine code, and then "
        "to a program running in memory. Registers, memory, branches, function calls, "
        "instruction encoding, compiling and linking, this is the whole picture of the RISC-V "
        "part of CS61C.",
    "寄存器、内存、分支": "Registers, memory, branches",
}
