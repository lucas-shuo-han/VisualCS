"""The episode list: order, titles and output names, in both languages.


Episode numbers, title cards, "next episode" lines and video file names all
come from here, so reordering the series is a one-line change. The episodes
are written in Chinese (SOURCE_LANG); English comes from i18n/epNN.py."""

SOURCE_LANG = "zh"
LANGS = ["zh", "en"]

SERIES_NAME = {"zh": "CS61C · RISC-V", "en": "CS61C · RISC-V"}

EPISODES = [
    {"file": 'ep01_intro.py', "scene": 'Ep01Intro',
     "title": {"zh": '机器结构与 RISC-V', "en": 'Machine Structures & RISC-V'},
     "sub": {"zh": '抽象层次 · 冯·诺依曼结构 · RISC 的故事', "en": 'Abstraction · von Neumann · the RISC story'},
     "slug": {"zh": '机器结构与RISC-V', "en": 'machine-structures-and-risc-v'}},
    {"file": 'ep02_isa_registers.py', "scene": 'Ep02ISARegisters',
     "title": {"zh": '从 C 到汇编', "en": 'From C to Assembly'},
     "sub": {"zh": '指令集架构 · 寄存器 · 算术指令', "en": 'ISA · registers · arithmetic'},
     "slug": {"zh": '从C到汇编-ISA与寄存器', "en": 'from-c-to-assembly'}},
    {"file": 'ep03_memory.py', "scene": 'Ep03Memory',
     "title": {"zh": '内存', "en": 'Memory'},
     "sub": {"zh": '字节寻址 · 小端序 · lw / sw', "en": 'Byte addressing · little-endian · lw / sw'},
     "slug": {"zh": '内存-字节寻址与lw-sw', "en": 'memory-lw-sw'}},
    {"file": 'ep04_memory_practice.py', "scene": 'Ep04MemoryPractice',
     "title": {"zh": '汇编实战：表达式与数组', "en": 'Assembly in Practice'},
     "sub": {"zh": '无类型的寄存器 · 栈上的数组 · 字节与符号', "en": 'Untyped registers · arrays on the stack · bytes & signs'},
     "slug": {"zh": '汇编实战-表达式与数组', "en": 'assembly-in-practice'}},
    {"file": 'ep05_branches_loops.py', "scene": 'Ep05BranchesLoops',
     "title": {"zh": '决策与循环', "en": 'Decisions & Loops'},
     "sub": {"zh": 'PC · 条件分支 · 位运算 · 循环', "en": 'PC · branches · bitwise ops · loops'},
     "slug": {"zh": '决策与循环', "en": 'decisions-and-loops'}},
    {"file": 'ep06_control_patterns.py', "scene": 'Ep06ControlPatterns',
     "title": {"zh": '控制流进阶', "en": 'Control Flow Patterns'},
     "sub": {"zh": '取指执行 · 比较指令 · 循环的套路', "en": 'Fetch-execute · set-less-than · loop recipes'},
     "slug": {"zh": '控制流进阶', "en": 'control-flow-patterns'}},
    {"file": 'ep07_procedures.py', "scene": 'Ep07Procedures',
     "title": {"zh": '函数调用', "en": 'Function Calls'},
     "sub": {"zh": 'jal · 调用约定 · 栈', "en": 'jal · calling convention · the stack'},
     "slug": {"zh": '函数调用与栈', "en": 'function-calls'}},
    {"file": 'ep08_recursion.py', "scene": 'Ep08Recursion',
     "title": {"zh": '递归与栈帧', "en": 'Recursion & Stack Frames'},
     "sub": {"zh": 'jal / jalr · 阶乘 · 叶子函数', "en": 'jal / jalr · factorial · leaf functions'},
     "slug": {"zh": '递归与栈帧', "en": 'recursion-and-stack-frames'}},
    {"file": 'ep09_formats_ris.py', "scene": 'Ep09FormatsRIS',
     "title": {"zh": '指令格式（上）', "en": 'Instruction Formats, Part 1'},
     "sub": {"zh": '存储程序 · R / I / S 型', "en": 'Stored program · R / I / S types'},
     "slug": {"zh": '指令格式上-R-I-S', "en": 'formats-r-i-s'}},
    {"file": 'ep10_decoding.py', "scene": 'Ep10Decoding',
     "title": {"zh": '读懂机器码', "en": 'Reading Machine Code'},
     "sub": {"zh": '反汇编 · 字段复用 · I 型全家', "en": 'Disassembly · shared fields · the I-type family'},
     "slug": {"zh": '读懂机器码', "en": 'reading-machine-code'}},
    {"file": 'ep11_formats_buj.py', "scene": 'Ep11FormatsBUJ',
     "title": {"zh": '指令格式（下）', "en": 'Instruction Formats, Part 2'},
     "sub": {"zh": 'PC 相对寻址 · B / U / J 型', "en": 'PC-relative addressing · B / U / J types'},
     "slug": {"zh": '指令格式下-B-U-J', "en": 'formats-b-u-j'}},
    {"file": 'ep12_addressing.py', "scene": 'Ep12Addressing',
     "title": {"zh": '寻址方式与大常数', "en": 'Addressing & Big Constants'},
     "sub": {"zh": '远跳转 · li 的展开 · 手工汇编', "en": 'Far jumps · expanding li · hand assembly'},
     "slug": {"zh": '寻址方式与大常数', "en": 'addressing-and-big-constants'}},
    {"file": 'ep13_call.py', "scene": 'Ep13CALL',
     "title": {"zh": 'CALL', "en": 'CALL'},
     "sub": {"zh": '编译 · 汇编 · 链接 · 加载', "en": 'Compile · Assemble · Link · Load'},
     "slug": {"zh": 'CALL-编译汇编链接加载', "en": 'call-compile-assemble-link-load'}},
    {"file": 'ep14_hello_world.py', "scene": 'Ep14HelloWorld',
     "title": {"zh": 'Hello World 的一生', "en": 'The Life of Hello World'},
     "sub": {"zh": '目标文件 · 符号表 · 重定位 · 动态链接', "en": 'Object files · symbols · relocation · dynamic linking'},
     "slug": {"zh": 'HelloWorld的一生', "en": 'life-of-hello-world'}},
]
