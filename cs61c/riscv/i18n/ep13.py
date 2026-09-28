"""English for episode 13 (keys are the Chinese strings in ep13_call.py)."""

EN = {
    # ---- end card
    "编译器：C → 汇编（可以含伪指令）": "Compiler: C → assembly (may use pseudo-instructions)",
    "汇编器：展开伪指令，两遍扫描解决向前引用": "Assembler: expands pseudo-instructions; two passes resolve labels",
    "目标文件 = 机器码 + 符号表 + 重定位表": "Object file = machine code + symbol table + relocation table",
    "链接器：拼接各段，按重定位表补全地址": "Linker: joins segments, fills in addresses from the relocation table",
    "加载器：建立地址空间，复制代码和数据，经启动例程进入 main":
        "Loader: new address space, copy code & data, start-up calls main",

    # ---- overview
    "编译器": "Compiler",
    "汇编器": "Assembler",
    "链接器": "Linker",
    "加载器": "Loader",
    "运行": "Run",
    "从一个 C 文件到一个正在运行的程序，要经过四个步骤。":
        "Getting from a C file to a running program takes four steps.",
    "编译器 Compiler、汇编器 Assembler、链接器 Linker、加载器 Loader——首字母连起来，就是 CALL。":
        "Compiler, Assembler, Linker, Loader: put their first letters together and you get CALL.",
    "编译器把 C 翻译成汇编——前面几集，我们一直在手工做这件事。":
        "The compiler translates C into assembly: exactly what we've been doing by hand in earlier episodes.",
    "编译器输出的汇编里可以有伪指令，比如 mv、li、j，展开的活儿留给汇编器。":
        "The compiler's output may use pseudo-instructions such as mv, li and j; the assembler expands them.",

    # ---- assembler
    "汇编器 Assembler": "Assembler",
    "汇编器读入汇编代码，产出目标文件（object file）。里面除了机器码，还有链接和调试要用的信息。":
        "The assembler reads assembly code and produces an object file. Besides machine code, "
        "it holds information for linking and debugging.",
    "第一件事：把伪指令展开成真实的指令。": "Job one: expand pseudo-instructions into real instructions.",
    "第二件事：把标签换算成偏移。但这里有个麻烦：向前引用（forward reference）。":
        "Job two: turn labels into offsets. But there's a snag: forward references.",
    "汇编器读到 bne 时，还没见过 Skip 的定义，不知道该跳多远。":
        "When the assembler reaches bne, it hasn't seen Skip defined yet, so it can't tell how far to jump.",
    "符号表": "Symbol table",
    "解决办法：扫描两遍。第一遍不生成机器码，只把每个标签的地址记进符号表（symbol table）。":
        "The fix: two passes. The first pass generates no machine code; "
        "it just records each label's address in the symbol table.",
    "第二遍再生成机器码。这时 Skip 的地址已知：偏移 = 0x08 − 0x00 = 8。":
        "The second pass generates the machine code, now knowing where Skip is: offset = 0x08 − 0x00 = 8.",
    "jal  ra, printf     # printf 在别的文件里": "jal  ra, printf     # in another file",
    "la   t0, A          # 静态数据 A 的地址": "la   t0, A          # A: static data",
    "但有些地址，扫多少遍都算不出来：调用另一个文件里的 printf，或者取静态数据 A 的地址。":
        "But some addresses can't be worked out in any number of passes: "
        "calling printf in another file, or taking the address of static data A.",
    "重定位表": "Relocation table",
    "它们的最终地址要等链接时才知道。汇编器把这些“待补的洞”记进重定位表（relocation table），留给链接器。":
        "Their final addresses aren't known until link time, so the assembler lists these holes "
        "in the relocation table: a to-do list for the linker.",
    "文件头 header": "Header",
    "代码段 .text": "Text segment (.text)",
    "数据段 .data": "Data segment (.data)",
    "重定位表 relocation": "Relocation table",
    "符号表 symbol table": "Symbol table",
    "调试信息 debug": "Debugging info",
    "所以一个目标文件包含：文件头、代码段、数据段、重定位表、符号表，还有调试信息。":
        "So an object file holds a header, a text segment, a data segment, a relocation table, "
        "a symbol table and debugging information.",

    # ---- linker
    "链接器 Linker": "Linker",
    "链接器把多个目标文件拼成一个可执行文件。": "The linker combines several object files into one executable.",
    "foo 代码": "foo text",
    "foo 数据": "foo data",
    "lib 代码": "lib text",
    "lib 数据": "lib data",
    "第一步：把各文件的代码段首尾相接，再把数据段接在后面。":
        "Step 1: concatenate the text segments, then append the data segments.",
    "第二步：各段位置一旦排定（代码从 0x10000 开始），每个符号的最终地址也就定了，比如 printf 在 0x10180。":
        "Step 2: with the segments laid out from 0x10000 up, every symbol has its final address. "
        "printf is at 0x10180.",
    "第三步：按重定位表逐个补洞。foo 里 0x10040 处的 jal 要跳到 printf……":
        "Step 3: fill every hole in the relocation table. The jal at 0x10040 in foo must reach printf…",
    "……jal 用 PC 相对偏移，所以填进去的是 0x10180 − 0x10040 = 0x140。":
        "…and since jal is PC-relative, the offset filled in is 0x10180 − 0x10040 = 0x140.",
    "而文件内部的分支完全不用改：PC 相对偏移，整块挪动后依然正确。这正是第 11 集说的“位置无关”。":
        "Branches inside a file need no changes: PC-relative offsets stay correct when the whole block moves. "
        "That's the position independence from Episode 11.",
    "顺便一提：现代系统还常用“动态链接”，库要等程序加载时才链接进来。这里讲的是静态链接。":
        "By the way, modern systems often use dynamic linking, where libraries are linked in only "
        "when the program is loaded. What we've shown is static linking.",

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
    "最后，操作系统中的加载器负责把可执行文件真正运行起来。":
        "Finally, the operating system's loader actually gets the executable running.",
    "它先读文件头，得知代码段和数据段有多大，再为程序创建一个新的地址空间……":
        "It reads the header to learn how big the text and data segments are, "
        "then creates a new address space…",
    "代码": "Text",
    "数据": "Data",
    "……然后把代码和数据复制进内存……": "…copies the code and data into memory…",
    "……把命令行参数放到栈上，初始化寄存器，让 sp 指向栈顶……":
        "…puts the command-line arguments on the stack, initializes the registers, "
        "and points sp at the top of the stack…",
    "……最后跳到启动例程，由它调用 main。程序开始运行！":
        "…and finally jumps to a start-up routine, which calls main. The program is running!",

    # ---- wrap up
    "在内存中运行": "Running in memory",
    "到这里，我们走完了一整条路：C 代码，到汇编，到机器码，再到内存里运行的程序。":
        "We've now traveled the whole road: from C code to assembly, to machine code, "
        "to a program running in memory.",
    "①② 机器结构与算术": "①② Machines & arithmetic",
    "③④ 内存": "③④ Memory",
    "⑤⑥ 分支与循环": "⑤⑥ Branches & loops",
    "⑦⑧ 函数与栈": "⑦⑧ Functions & the stack",
    "⑨–⑫ 指令编码": "⑨–⑫ Instruction encoding",
    "寄存器、内存、分支、函数调用、指令编码、编译链接——这就是 CS61C 中 RISC-V 部分的全貌。":
        "Registers, memory, branches, function calls, instruction encoding, compiling and linking: "
        "that's the big picture of RISC-V in CS61C.",
}
