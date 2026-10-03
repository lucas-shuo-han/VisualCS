"""English for episode 1 (keys are the Chinese strings in ep01_intro.py)."""

EN = {
    # module
    "晶体管": "Transistors",
    "机器码": "Machine code",
    "汇编语言": "Assembly language",
    "硬件架构（框图）": "Architecture (block diagrams)",
    "逻辑门": "Logic gates",
    "高级语言（C）": "High-level language (C)",
    # construct
    "抽象：高级语言 → 汇编 → 机器码 → 框图 → 逻辑门 → 晶体管":
        "Abstraction layers a system, from C through assembly, machine code, block diagrams, "
        "and gates, down to transistors",
    "ISA 是软件和硬件之间的接口": "The ISA is the interface between software and hardware",
    "五大部件：控制、数据通路、内存、输入、输出":
        "A computer has five components, which are control, datapath, memory, input, and "
        "output",
    "寄存器只有 128 字节，却比 DRAM 快 50–500 倍":
        "Registers hold a hundred twenty-eight bytes, yet are fifty to five hundred times "
        "faster than DRAM",
    "RISC：指令少而简单；RISC-V 开源、免授权费":
        "RISC uses few, simple instructions, and RISC-V is open and free of license fees",
    # abstraction
    "伟大思想 #1：抽象": "Great Idea #1: Abstraction",
    # focus
    "编译器": "compiler",
    "汇编器": "assembler",
    # half_adder
    "和": "sum",
    "进位": "carry",
    "1 位半加器": "1-bit half adder",
    # isa
    "软件": "Software",
    "硬件": "Hardware",
    "指令集架构（ISA）": "Instruction Set Architecture (ISA)",
    "ISA 规定了：": "An ISA specifies:",
    "寄存器": "Registers",
    "数据类型": "Data types",
    "机器语言：指令如何用比特表示": "Machine language: their bit encoding",
    "汇编语言：有哪些指令": "Assembly language: the instructions",
    "内存寻址方式": "Memory addressing",
    "输入输出模型": "Input/output model",
    "应用程序": "Applications",
    "操作系统": "Operating system",
    "按 ISA 编写": "Written to the ISA",
    "按 ISA 设计": "Designed to the ISA",
    # why_assembly
    "为什么要学汇编？": "Why learn assembly?",
    "C 代码": "C code",
    "汇编": "Assembly",
    "很少手写": "rarely hand-written",
    "程序员平庸还是优秀，就看懂不懂汇编": "Mediocre vs. excellent programmers: do they know assembly?",
    "懂汇编 → 懂计算机怎样执行指令": "Know assembly → know how the computer executes instructions",
    "成本更低": "Cheaper",
    "更快": "Faster",
    "更省资源": "Leaner",
    # von_neumann
    "冯·诺依曼结构": "The von Neumann Architecture",
    "处理器（CPU）": "Processor (CPU)",
    "控制单元": "Control",
    "数据通路": "Datapath",
    "内存": "Memory",
    "程序": "Program",
    "数据": "Data",
    "输入输出（I/O）": "Input/Output (I/O)",
    "输入": "Input",
    "键盘等": "keyboards…",
    "显示器等": "displays…",
    "输出": "Output",
    "使能": "enable",
    "写入数据": "write data",
    "地址": "address",
    "读出数据": "read data",
    # clock_and_light
    "寄存器与内存": "Registers and Memory",
    "4 GHz：每秒 40 亿个周期": "4 GHz: 4 billion cycles per second",
    "光速 ≈ 30 万公里/秒": "Speed of light ≈ 300,000 km/s",
    "超过一个周期": "more than one cycle",
    "好在芯片本身远小于 10 厘米": "Luckily, chips are much smaller than 10 cm",
    # chip_diagram
    "处理器": "Processor",
    "内存（DRAM）": "Memory (DRAM)",
    # two_kinds
    "极快，但空间有限": "very fast, but tiny",
    "约 100 ns ≈ 400 个周期": "≈ 100 ns ≈ 400 cycles",
    "大得多，但慢": "much bigger, but slow",
    # capacity
    "32 个寄存器 × 4 字节 = 128 字节": "32 registers × 4 bytes = 128 bytes",
    "笔记本：2–64 GB": "Laptop: 2–64 GB",
    "服务器：可达 1 TB": "Server: up to 1 TB",
    # scr
    "缩小倍数": "zoomed out",
    "64 GB 内存": "64 GB of memory",
    "128 B 寄存器": "128 B of registers",
    # band
    "DRAM 主存": "DRAM",
    "磁盘": "Disk",
    "伟大思想 #3：局部性原理 / 存储层次": "Great Idea #3: Locality / Memory Hierarchy",
    "在处理器核心里 · 约 128 字节": "In the processor core · about 128 bytes",
    "在另一块芯片上 · DDR3/4/5、HBM": "On a separate chip · DDR3/4/5, HBM",
    "几十美元就能买到好几 GB": "Many GB for a few tens of dollars",
    "更大，也更慢": "Bigger, and slower",
    "寄存器快 50–500 倍": "Registers: 50–500× faster",
    "越小，越快": "Smaller is faster",
    # jim_gray
    "伯克利": "Berkeley",
    "洛杉矶": "Los Angeles",
    "萨克拉门托": "Sacramento",
    "内存慢 100 倍：开车去萨克拉门托": "Memory, 100× slower: drive to Sacramento",
    "寄存器：1 分钟（在脑子里）": "Register: 1 minute (in your head)",
    "内存慢 500 倍：去洛杉矶再回来": "Memory, 500× slower: to Los Angeles and back",
    # risc_cisc
    "指令越来越复杂": "ever more complex instructions",
    "写回内存": "write back",
    "相加": "add",
    "读内存": "read memory",
    "一条复杂指令": "one complex instruction",
    "硬件：复杂、昂贵": "Hardware: complex, costly",
    "CISC：复杂指令集计算机": "CISC: Complex Instruction Set Computer",
    "三条简单指令，每条只做一件事": "three simple instructions, one job each",
    "硬件：简单、快": "Hardware: simple, fast",
    "CISC：1 条复杂指令": "CISC: 1 complex instruction",
    "RISC：3 条简单指令": "RISC: 3 simple instructions",
    "时间": "time",
    "（示意）": "(schematic)",
    "先完成": "done first",
    "伯克利 RISC · 斯坦福 MIPS": "Berkeley RISC · Stanford MIPS",
    "RISC 项目": "RISC project",
    "MIPS 项目": "MIPS project",
    "图灵奖": "Turing Award",
    "Intel i3/i5/i7/i9、许多 AMD 处理器": "Intel i3/i5/i7/i9, many AMD chips",
    "许多 Windows 电脑": "many Windows PCs",
    "很多手机": "many phones",
    "苹果自研芯片（Apple silicon）": "Apple silicon",
    "都在快速发展": "both evolving fast",
    # card
    "太复杂": "very complex",
    "缺少真正的编译器和软件": "no real compilers or software",
    "老旧或“自创”的 ISA": "Old or made-up ISAs",
    "RISC-V 诞生": "RISC-V born",
    "开源": "Open source",
    "免授权费": "License-free",
    "商用": "Commercial",
    "教学": "Teaching",
    "研究": "Research",
    "嵌入式微控制器": "Embedded microcontrollers",
    "仓库级超级计算机": "Warehouse-scale supercomputers",
    "全球学术界与产业界共同推动": "Backed by academia and industry worldwide",
    # rv32i
    "RV32I 与“绿卡”": "RV32I and the Green Card",
    "32 位": "32-bit",
    "基础整数指令集": "base integer instructions",
    "RV32I 基础指令集": "RV32I base instruction set",
    "M：乘除法": "M: multiply/divide",
    "F：浮点": "F: floating point",
    "可选扩展": "optional extensions",
    "RISC-V 绿卡": "RISC-V Green Card",
    "名字来自 1960 年代的 IBM 360 绿卡": "named after the 1960s IBM 360 green card",
    # roadmap

    # ---- spoken beats and cue phrases (see references/narration-writing.md)
    "CS61C 的第一个伟大思想：抽象。计算机系统从上到下，分成一层又一层。":
        "The first great idea in CS61C is abstraction. A computer system is built in layers, "
        "from the top all the way down.",
    "最上层是高级语言，比如 C。编译器把它翻译成汇编语言，汇编器再把它变成机器码：机器能直接读懂的 0 和 1。":
        "At the top is a high-level language, such as C. A compiler translates it into "
        "assembly language, and an assembler then turns that into machine code, which is the "
        "zeros and ones the machine can read directly.",
    "编译器把它翻译成汇编语言": "A compiler translates it",
    "汇编器再把它变成机器码": "an assembler then turns",
    "再往下是硬件：先是用框图描述的架构，比如两个寄存器的值送进一个加法器。":
        "Below that is hardware. It starts with an architecture described by a block diagram, "
        "in which, for example, the values of two registers flow into an adder.",
    "比如两个寄存器的值送进": "the values of two registers",
    "一个加法器": "into an adder",
    "放大加法器，里面是逻辑门：两个比特相加，异或门给出和，与门给出进位。再放大一个逻辑门：它由晶体管搭成。这是最底层。":
        "Zoom in on the adder, and inside are logic gates. To add two bits, an XOR gate gives "
        "the sum, and an AND gate gives the carry. Zoom in on one gate, and it is built from "
        "transistors, which is the lowest layer of all.",
    "再放大一个逻辑门": "Zoom in on one gate",
    "相邻两层之间都有定义清晰的接口：只要遵守接口，就不必关心下一层的细节。":
        "Between every two neighboring layers there is a clearly defined interface. As long "
        "as you respect the interface, you don't need to care about the details of the layer "
        "below.",
    "只要遵守接口": "As long as you respect",
    "本系列关注软件和硬件之间的接口：指令集架构（ISA）。":
        "This series is about the interface between software and hardware, which is known as "
        "the instruction set architecture. We call it the ISA for short.",
    "ISA 规定了汇编语言有哪些指令、它们怎样编码成比特，以及寄存器、数据类型、内存寻址、输入输出等架构特性。":
        "The ISA specifies which instructions assembly language has, and how they are encoded "
        "as bits, as well as architectural features such as registers, data types, memory "
        "addressing, and input and output.",
    "程序和编译器以 ISA 为标准来编写；CPU 等硬件也以同一个 ISA 为标准来设计。":
        "Programs and compilers are written to the ISA, and hardware such as the CPU is "
        "designed to the same ISA.",
    "所以，程序能在任何遵循同一 ISA 的 CPU 上运行。本系列要学的 ISA，叫作 RISC-V。":
        "So a program can run on any CPU that follows the same ISA. The ISA we will study in "
        "this series is called RISC-V.",
    "叫作 RISC-V": "is called RISC-V",
    "汇编大多由编译器生成，很少有人手写。那为什么还要学它？":
        "Most assembly is generated by compilers, and hardly anyone writes it by hand. So why "
        "learn it?",
    "那为什么还要学它": "So why learn it",
    "2004 年 Slashdot 上有篇帖子甚至说：程序员平庸还是优秀，就看懂不懂汇编。懂汇编，就懂计算机怎样执行指令；用高级语言也能写出更快、更省资源、成本更低的程序。":
        "A post on Slashdot in two thousand four even claimed that whether a programmer is "
        "mediocre or excellent depends on whether they understand assembly. Understanding "
        "assembly means understanding how a computer executes instructions, and it lets you "
        "write faster, leaner, and cheaper programs, even in a high-level language.",
    "懂汇编": "Understanding assembly means",
    "学 ISA 之前，先来看计算机的基本布局：冯·诺依曼结构。处理器（CPU）负责计算，由两部分组成：控制单元（control）和数据通路（datapath）。":
        "Before studying an ISA, let's look at the basic layout of a computer, the von "
        "Neumann architecture. The processor, or CPU, does the computing, and it has two "
        "parts, the control unit and the datapath.",
    "处理器（CPU）负责计算": "The processor, or CPU",
    "数据通路的主角，是寄存器和负责运算的算术逻辑单元（ALU）。处理器之外，是存放程序和数据的内存（memory），以及键盘、显示器这样的输入输出设备（I/O）。控制、数据通路、内存、输入、输出：这就是计算机的五大部件。":
        "The stars of the datapath are the registers and the arithmetic logic unit, or ALU. "
        "Outside the processor are the memory, which stores programs and data, and input and "
        "output devices such as the keyboard and the display. Control, datapath, memory, "
        "input, and output are the five components of a computer.",
    "处理器之外": "Outside the processor",
    "控制": "Control, datapath, memory, input, and output",
    "以及键盘、显示器": "and input and output devices",
    "处理器发出地址来读写内存；“使能”信号保证只读的时候不会误改内存。":
        "The processor sends out an address to read or write memory, and an enable signal "
        "makes sure that a read can't change memory by mistake.",
    "处理器发出地址": "The processor sends out an address",
    "信号保证": "and an enable signal",
    "处理器非常快：4 GHz 的处理器，一个时钟周期只有 0.25 纳秒。这有多短？光速约每秒 30 万公里，而 0.25 纳秒只够光走 7.5 厘米。":
        "The processor is very fast. In a four gigahertz processor, one clock cycle lasts "
        "only a quarter of a nanosecond. How short is that? Light travels about three hundred "
        "thousand kilometers per second, and in a quarter of a nanosecond it covers only "
        "seven and a half centimeters.",
    "这有多短": "How short is that?",
    "一个时钟周期只有": "one clock cycle lasts",
    "0.25 纳秒只够光走": "and in a quarter of a nanosecond",
    "7.5 厘米": "only seven and a half",
    "数据哪怕只在 10 厘米外，光也要跑约 0.3 纳秒，超过一个周期。所以数据必须离处理器很近。":
        "Even if the data is only ten centimeters away, light needs about three tenths of a "
        "nanosecond to get there, which is longer than a cycle. So the data has to be very "
        "close to the processor.",
    "数据哪怕只在 10 厘米外": "Even if the data is only",
    "，超过一个周期": "which is longer than a cycle",
    "所以数据必须离处理器很近": "So the data has to be",
    "因此，现代计算机至少有两种存数据的硬件。一是寄存器：在处理器内部，空间小，但快如闪电。二是内存：在处理器之外，大得多，但访问一次约 100 纳秒，相当于 400 个周期。":
        "So a modern computer has at least two kinds of hardware for storing data. The first "
        "is registers, which sit inside the processor, are small, and are lightning fast. The "
        "second is memory, which sits outside the processor and is much larger, but each "
        "access takes about a hundred nanoseconds, or four hundred cycles.",
    "二是内存": "The second is memory",
    "空间小，但快如闪电": "are small, and are lightning fast",
    "访问一次约 100 纳秒": "but each access takes",
    "再比容量：32 个寄存器各 4 字节，总共才 128 字节；笔记本却有 2 到 64 GB 内存，服务器可达 1 TB。":
        "Now compare capacity. Thirty-two registers of four bytes each add up to only a "
        "hundred twenty-eight bytes. A laptop, on the other hand, has two to sixty-four "
        "gigabytes of memory, and a server can have up to a terabyte.",
    "把 128 字节画成小方块；同样比例下，64 GB 内存的面积约是它的 5 亿倍，小方块连一个像素都不到。":
        "Let's draw those hundred twenty-eight bytes as a small square. At the same scale, "
        "sixty-four gigabytes of memory has about five hundred million times the area, and "
        "the small square would be less than one pixel.",
    "同样比例下": "At the same scale",
    "小方块连一个像素都不到": "and the small square would be",
    "主存通常是另一块芯片上的 DRAM（如 DDR3/4/5、HBM），几十美元就能买好几 GB。但物理规律决定了：越小，越快。寄存器比 DRAM 快大约 50 到 500 倍。":
        "Main memory is usually DRAM on a separate chip, such as DDR memory or HBM, and a few "
        "tens of dollars buys several gigabytes. But the laws of physics say that smaller "
        "means faster, and a register is roughly fifty to five hundred times faster than "
        "DRAM.",
    "但物理规律决定了": "But the laws of physics",
    "借用 Jim Gray 的比喻：从寄存器取数据，好比在脑子里回想一件事，花 1 分钟，那么慢 100 倍的内存，就像为了一张忘带的纸，开车去萨克拉门托取回来。":
        "Let's borrow an analogy from Jim Gray. Getting data from a register is like "
        "recalling something in your head, and that takes one minute. Memory that is a "
        "hundred times slower is like driving to Sacramento to fetch a paper you forgot.",
    "那么慢 100 倍的内存": "Memory that is a hundred times slower",
    "好比在脑子里回想一件事": "is like recalling something",
    "开车去萨克拉门托": "driving to Sacramento",
    "要是慢 500 倍，就得开车去洛杉矶再回来，只为了取一个数据！":
        "And if it is five hundred times slower, you would have to drive all the way to Los "
        "Angeles and back, just to fetch a single piece of data!",
    "寄存器数量很少，和处理器核心共用宝贵的芯片面积，非常昂贵。所以设计 ISA 像跳一支探戈：尽量在寄存器里算，少跑内存和磁盘。":
        "Registers are few, and they share precious chip area with the processor core, so "
        "they are very expensive. That is why designing an ISA is like dancing a tango, where "
        "we compute in registers as much as possible and make as few trips to memory and disk "
        "as we can.",
    "和处理器核心共用宝贵的芯片面积": "they share precious chip area",
    "ISA 该怎样设计？七八十年代的潮流是让指令越来越复杂：一条指令同时读内存、运算、写回。程序更短，访存也可能更少；代价是硬件复杂、造价高。这类架构后来被称为 CISC：复杂指令集计算机。":
        "How should an ISA be designed? In the seventies and eighties the trend was to make "
        "instructions more and more complex, so that a single instruction could read memory, "
        "compute, and write back. Programs got shorter and could make fewer memory accesses, "
        "but the price was complicated, expensive hardware. These architectures were later "
        "called CISC, or complex instruction set computers.",
    "程序更短": "Programs got shorter",
    "一条指令同时读内存": "so that a single instruction",
    "这类架构后来被称为 CISC": "These architectures were later called",
    "80 年代初，IBM 的 John Cocke 设计出 IBM 801：第一台精简指令集计算机（RISC）。":
        "In the early eighties, John Cocke at IBM designed the IBM eight oh one, the first "
        "reduced instruction set computer, or RISC.",
    "思路正相反：指令集小而简单，复杂操作交给软件和编译器，用简单指令拼出来。指令条数变多了，但简单的硬件每秒能执行多得多的指令，整体反而更快。":
        "The idea was the opposite. The instruction set is small and simple, and complex "
        "operations are left to software and the compiler, which build them out of simple "
        "instructions. There are more instructions, but simple hardware can execute many more "
        "of them every second, so overall it is faster.",
    "指令条数变多了": "There are more instructions",
    "复杂操作交给软件和编译器": "and complex operations are left",
    "伯克利的 Dave Patterson 和斯坦福的 John Hennessy 把它推向极致，同时做出了 RISC 和 MIPS 项目。三位先驱后来都获得了图灵奖：Cocke 在 1987 年，Patterson 和 Hennessy 在 2017 年。":
        "Dave Patterson at Berkeley and John Hennessy at Stanford pushed the idea to its "
        "limit, and built the RISC and MIPS projects at the same time. All three pioneers "
        "later won the Turing Award, Cocke in nineteen eighty-seven, and Patterson and "
        "Hennessy in twenty seventeen.",
    "三位先驱后来都获得了图灵奖": "All three pioneers later won",
    "如今 RISC 和 CISC 都很流行、都在快速发展：许多 Windows 电脑用 x86，很多手机和苹果自研芯片用 ARM。":
        "Today both RISC and CISC are popular and are developing fast. Many Windows computers "
        "use x86, and many phones and Apple's own chips use ARM.",
    "许多 Windows 电脑用 x86": "Many Windows computers use x86",
    "教学总得选一个 ISA：x86 太复杂；老旧或“自创”的 ISA，又缺少真正的编译器和软件。RISC-V 于 2010 年诞生在 UC Berkeley 的 Par Lab，由 Patterson 和 Krste Asanovic 发起；到 2020 年前后，连 MIPS 都转向了它。":
        "Teaching needs an ISA, and x86 is too complicated, while old or homemade ISAs lack "
        "real compilers and software. RISC-V was born in two thousand ten, in the Par Lab at "
        "UC Berkeley, started by Patterson and Krste Asanovic. By around two thousand twenty, "
        "even MIPS had moved over to it.",
    "2010 年诞生": "in two thousand ten",
    "RISC-V 于": "RISC-V was born",
    "到 2020 年前后": "By around two thousand twenty",
    "它受欢迎有两大原因：开源、免授权费。谁都能免费用，教学、研究、商用都行。全球学界和业界共同推动它。从嵌入式微控制器，到仓库级超级计算机，都已经有人用它来打造。":
        "It is popular for two big reasons. It is open source, and it carries no license "
        "fees, so anyone can use it for free, whether for teaching, research, or business. A "
        "worldwide community of academia and industry drives it forward, and people have "
        "already used it to build everything from embedded microcontrollers to warehouse- "
        "scale supercomputers.",
    "全球学界和业界共同推动它": "A worldwide community",
    "RISC-V 有 32、64、128 位等变体。本系列学 RV32I：32 位基础整数指令集；乘法等功能则放在 M 等扩展里。":
        "RISC-V comes in thirty-two, sixty-four, and one hundred twenty-eight bit variants. "
        "This series covers RV32I, the thirty-two bit base integer instruction set, and "
        "things like multiplication live in extensions such as M.",
    "本系列学 RV32I": "This series covers",
    "乘法等功能": "and things like multiplication",
    "整个架构的定义一页纸就能装下，叫作“绿卡”，名字来自 1960 年代著名的 IBM 360 绿卡。简洁、优雅，学汇编、学设计计算机都合适：这正是 CS61C 教它的原因。Go Bears！":
        "The whole architecture definition fits on a single page, called the green card, "
        "named after the famous IBM three sixty green card of the nineteen sixties. It is "
        "simple and elegant, and good for learning assembly and for learning to design "
        "computers, which is exactly why CS61C teaches it. Go Bears!",
    "简洁": "It is simple and elegant",
    "全系列共 14 集。下一集，从一行 C 代码出发，看它怎样变成汇编，并认识 RISC-V 的寄存器。":
        "The series has fourteen episodes in all. In the next one, we start from a single "
        "line of C and see how it becomes assembly, and we meet the RISC-V registers.",
    "下一集": "In the next one",
}
