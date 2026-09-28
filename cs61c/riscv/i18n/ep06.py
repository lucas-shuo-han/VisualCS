"""English for episode 6 (keys are the Chinese strings in ep06_control_patterns.py)."""

EN = {
    # end card
    "控制单元的循环：读 PC → 取指令 → 执行 → 更新 PC":
        "The control unit's loop: read PC → fetch → execute → update PC",
    "slt、sltu、slti、sltiu：比较结果写成 1 或 0":
        "slt, sltu, slti, sltiu write a comparison's result as 1 or 0",
    "比特没有类型：有符号还是无符号，由指令决定":
        "Bits have no type: the instruction decides signed or unsigned",
    "没有 else 的 if：条件取反，直接跳过，指令更少":
        "if without else: negate the condition and skip; fewer instructions",
    "任何循环都能先改写成 goto，再换成分支和 j":
        "Rewrite any loop with goto, then turn it into branches and j",

    # ---- fetch / execute
    "内存": "Memory",
    "每条指令占 4 个字节": "4 bytes each",
    "程序运行前先被装进内存的代码段（text segment）：每条指令是一个 32 位的字，占 4 个字节，一条挨着一条。":
        "Before a program runs, it's loaded into the text segment of memory: each instruction is "
        "a 32-bit word, 4 bytes, one right after another.",
    "处理器": "Processor",
    "控制单元": "Control unit",
    "数据通路": "Datapath",
    "32 个寄存器 x0–x31": "32 registers x0–x31",
    "处理器由控制单元（control unit）和数据通路（datapath）组成。数据通路里有 32 个寄存器 x0–x31。":
        "The processor consists of a control unit and a datapath. The datapath holds the 32 registers, x0–x31.",
    "单独的寄存器，不属于 x0–x31": "Separate from x0–x31",
    "PC 也在数据通路里，存着当前指令的地址。它也是寄存器，但不属于 x0–x31，指令一般不会直接读写它。":
        "The PC sits in the datapath too, holding the current instruction's address. It's a register, "
        "but not one of x0–x31, and instructions rarely read or write it explicitly.",
    "读 PC": "Read PC",
    "从内存取指令": "Fetch instruction",
    "执行指令": "Execute",
    "更新 PC": "Update PC",
    "控制单元不停地重复四步：读 PC，从内存取出指令，执行，再更新 PC。":
        "The control unit repeats four steps forever: read the PC, fetch the instruction "
        "from memory, execute it, and update the PC.",
    "用课程笔记里的例子走一遍。第一步：读 PC，得到 0x00000008。":
        "Let's walk through the example from the course notes. Step 1: read the PC, which holds 0x00000008.",
    "第二步：到内存里这个地址取出指令。在内存里，它只是一个 32 位的数：0x01051613。":
        "Step 2: fetch the instruction at that address. In memory it's just a 32-bit number: 0x01051613.",
    "控制单元把它解读成 slli x12 x10 0x10。这一集沿用笔记的写法，操作数之间不写逗号。编码细节留到第 9 集。":
        "The control unit decodes it as slli x12 x10 0x10. Like the notes, this episode leaves out "
        "the commas between operands. Episode 9 covers the encoding.",
    "第三步：执行。x10 是 0x000034FF，左移 0x10 位（也就是 16 位），x12 变成 0x34FF0000。":
        "Step 3: execute. x10 is 0x000034FF; shifted left by 0x10 (that is, 16) bits, "
        "it puts 0x34FF0000 in x12.",
    "第四步：更新 PC。每条指令占 4 个字节，所以默认让 PC 加 4，变成 0x0000000C，指向下一条指令。":
        "Step 4: update the PC. Every instruction is 4 bytes, so by default the PC goes up by 4, "
        "to 0x0000000C: the next instruction.",
    "所以这条算术指令其实改了两个寄存器：目的寄存器 x12，以及 PC。":
        "So this arithmetic instruction actually changes two registers: "
        "the destination register x12, and the PC.",
    "分支、跳转：换成标签地址": "Branch/jump: go to a label",
    "分支和跳转则会在第四步把 PC 换成标签的地址（条件分支只在条件成立时才换）。":
        "Branches and jumps instead set the PC to a label's address in step 4 "
        "(a conditional branch only when its condition holds).",

    # ---- practice problem
    "内存里那 5 个字，写成汇编是这 4 行。它们正好是笔记里的一道练习题。":
        "Those 5 words in memory are these 4 lines of assembly, "
        "which happen to be a practice problem from the notes.",
    "伪指令：展开成 2 条，占 0x00 和 0x04": "Pseudo-instruction: 2 instructions, at 0x00 and 0x04",
    "li 要装的 0x34FF 超出了 12 位立即数的范围，会展开成两条指令（第 12 集细讲），所以 slli 在 0x08。":
        "0x34FF doesn't fit in a 12-bit immediate, so li expands into two instructions "
        "(more in Episode 12). That's why slli is at 0x08.",
    "F. 其他": "F. Other",
    "问题：这 4 行执行完，x12 里是什么？先暂停，自己想一想。":
        "Question: after these 4 lines run, what's in x12? Pause and think it through.",
    "第一条执行完，x10 = 0x000034FF。把 32 位全画出来，每 4 位对应一个十六进制数字。":
        "After the first line, x10 = 0x000034FF. Here are all 32 bits; each group of 4 bits is one hex digit.",
    "slli 左移 16 位，右边补 0：x12 = 0x34FF0000，和刚才处理器里算的一样。":
        "slli shifts left by 16, filling in 0s on the right: x12 = 0x34FF0000, "
        "just as the processor computed earlier.",
    "srli 右移 8 位，左边补 0：x12 = 0x0034FF00。最高位本来是 0，所以用 srai 也一样。":
        "srli shifts right by 8, filling in 0s on the left: x12 = 0x0034FF00. "
        "The top bit was 0, so srai would give the same result.",
    "最后 and 逐位相与：同一位上两个都是 1，结果才是 1。":
        "Finally, and works bit by bit: a result bit is 1 only where both inputs have a 1.",
    "只有 3 列上下都是 1，所以 x12 = 0x00003400，答案是 B。":
        "Only 3 columns have 1s in both rows, so x12 = 0x00003400. The answer is B.",

    # ---- slt family
    "比较指令：slt 家族": "Comparisons: the slt family",
    "分支指令比较完就跳转。但有时我们只想要比较的结果，比如 C 里的 lt = (a < b)：成立是 1，不成立是 0。":
        "A branch compares and then jumps. But sometimes we just want the result of the comparison, "
        "like lt = (a < b) in C: 1 if true, 0 if false.",
    "对应的指令是 slt（set less than）：rs1 < rs2 时把 rd 置为 1，否则置为 0。":
        "The instruction for this is slt, set less than: it sets rd to 1 if rs1 < rs2, and to 0 otherwise.",
    "a、b 放在 x5、x6，结果放进 x7：slt x7 x5 x6。3 < 5 成立，x7 = 1。":
        "With a and b in x5 and x6 and the result in x7: slt x7 x5 x6. 3 < 5 is true, so x7 = 1.",
    "sltu 是它的无符号版本（u 代表 unsigned）。两者什么时候结果不同？看一个例子。":
        "sltu is the unsigned version (u for unsigned). When do the two give different answers? "
        "Here's an example.",
    "当作有符号数：−1": "As signed: −1",
    "当作无符号数：4294967295": "As unsigned: 4294967295",
    "x5 = 0xFFFFFFFF，32 位全是 1。当作有符号数，它是 −1；当作无符号数，它是 4294967295。":
        "x5 = 0xFFFFFFFF: all 32 bits are 1. As a signed number it's −1; "
        "as an unsigned number it's 4294967295.",
    "slt  x7 x5 x6    # -1 < 1 成立：x7 = 1": "slt  x7 x5 x6    # -1 < 1 is true: x7 = 1",
    "sltu x7 x5 x6    # 4294967295 < 1 不成立：x7 = 0": "sltu x7 x5 x6    # 4294967295 < 1 is false: x7 = 0",
    "slt 比的是 −1 < 1，成立，得 1；sltu 比的是 4294967295 < 1，不成立，得 0。":
        "slt compares −1 < 1: true, so 1. sltu compares 4294967295 < 1: false, so 0.",
    "在 C 里，类型由变量的声明决定；在汇编里，比特本身没有类型，当有符号数还是无符号数，由指令决定。":
        "In C, a variable's declaration determines its type. In assembly, bits have no type: "
        "the instruction decides whether they're signed or unsigned.",
    "slti  x7 x5 10    # -1 < 10 成立：x7 = 1": "slti  x7 x5 10    # -1 < 10 is true: x7 = 1",
    "sltiu x7 x5 10    # 4294967295 < 10 不成立：x7 = 0": "sltiu x7 x5 10    # 4294967295 < 10 is false: x7 = 0",
    "立即数版本 slti 和 sltiu 拿寄存器和常数比较。x5 不变：slti x7 x5 10 得 1，sltiu 得 0。":
        "The immediate versions, slti and sltiu, compare a register with a constant. "
        "Same x5: slti x7 x5 10 gives 1, sltiu gives 0.",
    "RV32I 基础指令集": "RV32I base instruction set",
    "M 扩展：乘法与除法": "M extension: mul & div",
    "F 扩展：浮点运算": "F extension: floating point",
    "顺便一提：乘法 mul 不在 RV32I 基础指令集里，它属于 M 扩展（M extension）。":
        "By the way, multiplication (mul) isn't in the RV32I base instruction set. "
        "It belongs to the M extension.",
    "通用乘法的电路比移位复杂得多，所以不放进基础指令集。除法、取余也在 M 扩展里，浮点运算在 F 扩展里。":
        "General multiplication needs far more complex circuitry than shifting, so the base set leaves it out. "
        "Division and remainder are in M too; floating point is in F.",

    # ---- if without else
    "回到分支。先看一个 if-else，变量 x、y、z、i、j 依次放在 x10 到 x14。":
        "Back to branches. First, an if-else, with the variables x, y, z, i, j in x10 through x14.",
    "选项 A": "Choice A",
    "选项 B": "Choice B",
    "这个 if-else 有两种翻译。选项 B 和第 5 集一样：用 bne 把条件取反。":
        "There are two ways to translate it. Choice B is what we did in Episode 5: "
        "negate the condition with bne.",
    "选项 A 不取反：用 beq，相等就跳到 If，于是 else 部分反而写在前面。两种都对，都是 4 条指令。":
        "Choice A keeps the condition: beq jumps to If when they're equal, so the else part comes first. "
        "Both are correct, and both take 4 instructions.",
    "那如果没有 else 呢？": "What if there's no else?",
    "选项 A 用 beq：相等时跳到 If 执行 add；不相等时，还得靠 j End 绕过 add。":
        "Choice A uses beq: if equal, jump to If and run the add; "
        "if not, it still needs j End to skip over the add.",
    "选项 B 用 bne：不相等就直接跳到 End；相等时顺着往下执行 add。":
        "Choice B uses bne: if not equal, jump straight to End; if equal, fall through to the add.",
    "3 条指令": "3 instructions",
    "2 条指令": "2 instructions",
    "两种都对。但 B 和 C 代码的结构一致，只要 2 条指令，比 A 少一条，性能也更好。":
        "Both work. But B mirrors the structure of the C code and needs only 2 instructions, "
        "one fewer than A, so it performs better too.",

    # ---- goto recipes
    "循环的套路：先改写成 goto": "Loop recipes: rewrite with goto first",
    "汇编里没有 while 和 for，只有分支和跳转。它们相当于 C 里的 goto：跳到某个标签处接着执行。":
        "Assembly has no while or for, only branches and jumps. "
        "They're like C's goto: execution continues at some label.",
    "在真正的 C 程序里别写 goto，它让代码很难读（xkcd 292 甚至说会招来迅猛龙）。但它很适合当翻译的中间一步。":
        "Don't use goto in real C code: it makes programs hard to read (xkcd 292 warns it attracts "
        "velociraptors). But it's a great intermediate step for translation.",
    "goto 形式": "goto form",
    "汇编": "Assembly",
    "套路是：先把控制结构改写成 goto，再一行一行换成指令。为了写出真实的指令，设 cond 为 x5 < x6。":
        "The recipe: rewrite the control structure with goto, then turn it into instructions line by line. "
        "To get real instructions, let cond be x5 < x6.",
    "刚才的 if 就是这样：if (!cond) goto AfterIf。条件不成立，就跳过 then 部分。":
        "The if we just saw works this way: if (!cond) goto AfterIf. "
        "When the condition fails, we skip the then-part.",
    "while：开头判断，不成立就跳出；末尾 goto Loop 回到开头。第 5 集的循环就是这个样子。":
        "while: test at the top and exit if the condition fails; goto Loop at the bottom jumps back. "
        "Episode 5's loop had exactly this shape.",
    "break 就是一句跳到循环后面的 goto，翻译出来是一条 j。":
        "A break is just a goto to the code after the loop, which becomes a single j.",
    "for 先改写成 while：初始化 startline 提到循环前面，递增 incline 放到循环体末尾……":
        "Turn a for into a while first: move the initialization, startline, before the loop, "
        "and the increment, incline, to the end of the body…",
    "……然后照 while 的套路翻译。": "…then translate it like any while loop.",
    "do-while 先执行循环体，最后才判断，成立就跳回 Loop。条件不用取反，也不需要 j。":
        "do-while runs the body first and tests at the end, jumping back to Loop if the condition holds. "
        "No negation, and no j.",

    # ---- pointer loop + quiz
    "... // 给 arr 填入数据": "... // fill arr with data",
    "最后看一个完整的例子：把 int 数组 arr 的 20 个元素加起来。":
        "Finally, a complete example: add up the 20 elements of the int array arr.",
    "先按套路改写成 goto：条件取反，i >= 20 就跳到 End。":
        "First, the recipe: rewrite it with goto, negating the condition, so i >= 20 jumps to End.",
    "这是笔记给出的汇编，一行注释也没有。每个寄存器对应 C 里的什么？":
        "Here's the assembly from the notes, without a single comment. "
        "What does each register stand for in the C code?",
    "把上面的寄存器和下面的 C 表达式配对。提示：x8 存的是 arr 的地址。暂停一下，自己试试。":
        "Match each register above with a C expression below. Hint: x8 holds the address of arr. "
        "Pause and give it a try.",
    "x8 是 &arr[0]：数组首元素的地址，也就是数组 arr 的地址。":
        "x8 is &arr[0]: the address of the first element, which is also the address of arr.",
    "x11 是 i：循环前清零，每轮末尾加 1。":
        "x11 is i: zeroed before the loop, incremented at the end of each iteration.",
    "x9 是 &arr[i]：从 x8 出发，每轮加 4 而不是 1，因为一个 int 占 4 个字节。这就是指针运算。":
        "x9 is &arr[i]: it starts at x8 and grows by 4, not 1, each iteration, since an int is 4 bytes. "
        "That's pointer arithmetic.",
    "x12 是 arr[i]，是值而不是地址：lw 从 x9 指向的地址读出当前元素。":
        "x12 is arr[i], the value, not the address: lw loads the current element from the address in x9.",
    "x10 是 sum：先清零，循环里的 add x10 x10 x12 就是 sum += arr[i]。":
        "x10 is sum: set to 0 first, and add x10 x10 x12 inside the loop is sum += arr[i].",
    "x13 是常数 20：bge 只能比较两个寄存器，所以先用 addi x13 x0 20（即 li x13 20）把 20 放进寄存器。":
        "x13 is the constant 20: bge can only compare two registers, so addi x13 x0 20 "
        "(that is, li x13 20) puts 20 in a register first.",
    "注意 Loop 和 End 不是指令，只是地址的名字：Loop 就是 bge 那条指令的地址。":
        "Note that Loop and End aren't instructions, just names for addresses: "
        "Loop is the address of the bge instruction.",
    "这里：每轮 6 条指令": "Here: 6 instructions per iteration",
    "第 5 集：每轮 7 条指令": "Episode 5: 7 per iteration",
    "和第 5 集比一比：那里每轮用 slli 和 add 重新算 A + 4i；这里让指针每轮后移 4 个字节，每轮少一条指令。":
        "Compare with Episode 5: there, each iteration recomputed A + 4i with slli and add; "
        "here the pointer just moves 4 bytes, saving one instruction per iteration.",
    "笔记还附了一个能在模拟器 Venus 里运行的完整版：arr 装着 1 到 20，程序最后打印出 210。":
        "The notes also include a complete version you can run in the Venus simulator: "
        "arr holds 1 through 20, and the program prints 210.",
}
