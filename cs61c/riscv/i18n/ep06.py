"""English for episode 6 (keys are the Chinese strings in ep06_control_patterns.py)."""

EN = {
    # end card
    "控制单元的循环：读 PC → 取指令 → 执行 → 更新 PC":
        "The control unit loops by reading the PC, fetching an instruction, executing it, and "
        "updating the PC",
    "slt、sltu、slti、sltiu：比较结果写成 1 或 0":
        "The instructions slt, sltu, slti, and sltiu write the result of a comparison as one "
        "or zero",
    "比特没有类型：有符号还是无符号，由指令决定":
        "Bits have no type, and the instruction decides whether they are signed or unsigned",
    "没有 else 的 if：条件取反，直接跳过，指令更少":
        "An if without an else negates the condition and skips ahead, using fewer "
        "instructions",
    "任何循环都能先改写成 goto，再换成分支和 j":
        "Any loop can be rewritten with goto first, and then turned into branches and j",

    # ---- fetch / execute
    "内存": "Memory",
    "每条指令占 4 个字节": "4 bytes each",
    "处理器": "Processor",
    "控制单元": "Control unit",
    "数据通路": "Datapath",
    "32 个寄存器 x0–x31": "32 registers x0–x31",
    "单独的寄存器，不属于 x0–x31": "Separate from x0–x31",
    "读 PC": "Read PC",
    "从内存取指令": "Fetch instruction",
    "执行指令": "Execute",
    "更新 PC": "Update PC",
    "分支、跳转：换成标签地址": "Branch/jump: go to a label",

    # ---- practice problem
    "伪指令：展开成 2 条，占 0x00 和 0x04": "Pseudo-instruction: 2 instructions, at 0x00 and 0x04",
    "F. 其他": "F. Other",

    # ---- slt family
    "比较指令：slt 家族": "Comparisons: the slt family",
    "当作有符号数：−1": "As signed: −1",
    "当作无符号数：4294967295": "As unsigned: 4294967295",
    "slt  x7 x5 x6    # -1 < 1 成立：x7 = 1": "slt  x7 x5 x6    # -1 < 1 is true: x7 = 1",
    "sltu x7 x5 x6    # 4294967295 < 1 不成立：x7 = 0": "sltu x7 x5 x6    # 4294967295 < 1 is false: x7 = 0",
    "slti  x7 x5 10    # -1 < 10 成立：x7 = 1": "slti  x7 x5 10    # -1 < 10 is true: x7 = 1",
    "sltiu x7 x5 10    # 4294967295 < 10 不成立：x7 = 0": "sltiu x7 x5 10    # 4294967295 < 10 is false: x7 = 0",
    "RV32I 基础指令集": "RV32I base instruction set",
    "M 扩展：乘法与除法": "M extension: mul & div",
    "F 扩展：浮点运算": "F extension: floating point",

    # ---- if without else
    "选项 A": "Choice A",
    "选项 B": "Choice B",
    "3 条指令": "3 instructions",
    "2 条指令": "2 instructions",

    # ---- goto recipes
    "循环的套路：先改写成 goto": "Loop recipes: rewrite with goto first",
    "goto 形式": "goto form",
    "汇编": "Assembly",
    "刚才的 if 就是这样：if (!cond) goto AfterIf。条件不成立，就跳过 then 部分。":
        "That is how the if we just saw works. It becomes if not cond, goto AfterIf, so when "
        "the condition fails, we skip the then part.",
    "while：开头判断，不成立就跳出；末尾 goto Loop 回到开头。第 5 集的循环就是这个样子。":
        "A while loop tests at the top and exits when the condition fails, and a goto Loop at "
        "the bottom returns to the top, which is just what the loop in episode five did.",
    "break 就是一句跳到循环后面的 goto，翻译出来是一条 j。":
        "A break is just a goto to the code after the loop, which becomes a single j.",
    "for 先改写成 while：初始化 startline 提到循环前面，递增 incline 放到循环体末尾，然后照 while 的套路翻译。":
        "A for loop is first rewritten as a while loop, with the initialization startline moved in front of the loop "
        "and the increment incline put at the end of the body, and then it is translated just like a while loop.",
    "初始化 startline": "with the initialization",
    "然后照 while 的套路翻译": "and then it is translated",
    "do-while 先执行循环体，最后才判断，成立就跳回 Loop。条件不用取反，也不需要 j。":
        "A do-while runs the body first and tests at the end, jumping back to Loop if the "
        "condition holds, so there is no negation and no j.",

    # ---- pointer loop + quiz
    "... // 给 arr 填入数据": "... // fill arr with data",
    "x8 是 &arr[0]：数组首元素的地址，也就是数组 arr 的地址。":
        "The register x8 holds the address of the first element, which is the address of the "
        "array arr.",
    "x11 是 i：循环前清零，每轮末尾加 1。":
        "The register x11 is i, which is cleared before the loop and goes up by one at the "
        "end of every round.",
    "x9 是 &arr[i]：从 x8 出发，每轮加 4 而不是 1，因为一个 int 占 4 个字节。这就是指针运算。":
        "The register x9 holds the address of arr[i]. It starts from x8 and adds four every "
        "round rather than one, because an int takes four bytes, and that is pointer "
        "arithmetic.",
    "x12 是 arr[i]，是值而不是地址：lw 从 x9 指向的地址读出当前元素。":
        "The register x12 is arr[i], a value rather than an address, which lw reads from the "
        "address that x9 points to.",
    "x10 是 sum：先清零，循环里的 add x10 x10 x12 就是 sum += arr[i]。":
        "The register x10 is sum, which starts at zero, and the add x10 x10 x12 in the loop "
        "is sum plus equals arr[i].",
    "x13 是常数 20：bge 只能比较两个寄存器，所以先用 addi x13 x0 20（即 li x13 20）把 20 放进寄存器。":
        "The register x13 is the constant twenty. Since bge can compare only two registers, "
        "we first use addi x13 x0 20, which is li x13 20, to put twenty into a register.",
    "这里：每轮 6 条指令": "Here: 6 instructions per iteration",
    "第 5 集：每轮 7 条指令": "Episode 5: 7 per iteration",

    # ---- spoken beats and cue phrases (see references/narration-writing.md)
    "程序运行前先被装进内存的代码段（text segment）：每条指令是一个 32 位的字，占 4 个字节，一条挨着一条。":
        "Before a program runs, it is loaded into the code segment of memory, where each "
        "instruction is a thirty-two bit word that takes four bytes, one right after another.",
    "占 4 个字节": "that takes four bytes",
    "处理器由控制单元（control unit）和数据通路（datapath）组成。数据通路里有 32 个寄存器 x0–x31。PC 也在数据通路里，存着当前指令的地址。它也是寄存器，但不属于 x0–x31，指令一般不会直接读写它。":
        "The processor is made of a control unit and a datapath, and the datapath holds the "
        "thirty-two registers, x0 to x31. The PC also lives in the datapath, and it holds the "
        "address of the current instruction. It is a register too, but it isn't one of x0 to "
        "x31, and instructions don't normally read or write it directly.",
    "PC 也在数据通路里": "The PC also lives",
    "控制单元不停地重复四步：读 PC，从内存取出指令，执行，再更新 PC。":
        "The control unit repeats four steps forever, which are reading the PC, fetching the "
        "instruction from memory, executing it, and updating the PC.",
    "用课程笔记里的例子走一遍。第一步：读 PC，得到 0x00000008。第二步：到内存里这个地址取出指令。在内存里，它只是一个 32 位的数：0x01051613。":
        "Let's walk through an example from the course notes. In the first step we read the "
        "PC, which gives 0x00000008. In the second step we fetch the instruction at that "
        "address from memory, where it is just a thirty-two bit number, 0x01051613.",
    "第二步": "In the second step",
    "得到 0x00000008": "which gives",
    "它只是一个 32 位的数": "where it is just",
    "控制单元把它解读成 slli x12 x10 0x10。这一集沿用笔记的写法，操作数之间不写逗号。编码细节留到第 9 集。":
        "The control unit reads that number as slli x12 x10 0x10. This episode follows the "
        "notes in leaving out the commas between operands, and the encoding details wait "
        "until episode nine.",
    "第三步：执行。x10 是 0x000034FF，左移 0x10 位（也就是 16 位），x12 变成 0x34FF0000。":
        "In step three we execute. The register x10 holds 0x000034FF, and shifting it left by "
        "0x10 bits, which is sixteen, makes x12 become 0x34FF0000.",
    "x12 变成": "makes x12 become",
    "第四步：更新 PC。每条指令占 4 个字节，所以默认让 PC 加 4，变成 0x0000000C，指向下一条指令。所以这条算术指令其实改了两个寄存器：目的寄存器 x12，以及 PC。":
        "In step four we update the PC. Every instruction takes four bytes, so by default the "
        "PC adds four, becoming 0x0000000C and pointing at the next instruction. So this "
        "arithmetic instruction really changed two registers, the destination register x12 "
        "and the PC.",
    "所以这条算术指令其实改了两个寄存器": "So this arithmetic instruction",
    "所以默认让 PC 加 4": "so by default the PC adds four",
    "分支和跳转则会在第四步把 PC 换成标签的地址（条件分支只在条件成立时才换）。":
        "Branches and jumps instead put the address of a label into the PC in step four, "
        "although a conditional branch does this only when its condition holds.",
    "内存里那 5 个字，写成汇编是这 4 行。它们正好是笔记里的一道练习题。li 要装的 0x34FF 超出了 12 位立即数的范围，会展开成两条指令（第 12 集细讲），所以 slli 在 0x08。":
        "Those five words in memory are written in assembly as these four lines, and they are "
        "exactly an exercise from the course notes. The li instruction wants to load 0x34FF, "
        "which is beyond what a twelve-bit immediate can hold. So it expands into two "
        "instructions, which we'll cover in episode twelve, and that is why slli sits at "
        "0x08.",
    "li 要装的": "The li instruction wants",
    "问题：这 4 行执行完，x12 里是什么？先暂停，自己想一想。":
        "Here is the question. After these four lines run, what is in x12? Pause the video "
        "and think about it for yourself.",
    "第一条执行完，x10 = 0x000034FF。把 32 位全画出来，每 4 位对应一个十六进制数字。":
        "After the first instruction runs, x10 is 0x000034FF. Let's draw all thirty-two bits, "
        "where every four bits correspond to one hexadecimal digit.",
    "每 4 位对应": "where every four bits",
    "slli 左移 16 位，右边补 0：x12 = 0x34FF0000，和刚才处理器里算的一样。srli 右移 8 位，左边补 0：x12 = 0x0034FF00。最高位本来是 0，所以用 srai 也一样。":
        "The slli instruction shifts left by sixteen and fills zeros on the right, so x12 "
        "becomes 0x34FF0000, the same as the processor computed earlier. The srli instruction "
        "then shifts right by eight and fills zeros on the left, giving 0x0034FF00, and since "
        "the top bit was zero anyway, srai would give the same answer.",
    "srli 右移 8 位": "The srli instruction then",
    "最后 and 逐位相与：同一位上两个都是 1，结果才是 1。只有 3 列上下都是 1，所以 x12 = 0x00003400，答案是 B。":
        "Finally, the and instruction works bit by bit, and gives a one only where both bits "
        "are one. Only three columns have a one in both rows, so x12 is 0x00003400, and the "
        "answer is B.",
    "只有 3 列": "Only three columns",
    "同一位上两个都是 1": "and gives a one only where",
    "结果才是 1": "both bits are one",
    "分支指令比较完就跳转。但有时我们只想要比较的结果，比如 C 里的 lt = (a < b)：成立是 1，不成立是 0。对应的指令是 slt（set less than）：rs1 < rs2 时把 rd 置为 1，否则置为 0。":
        "A branch compares and then jumps, but sometimes we want only the result of the "
        "comparison, such as the C statement that sets lt to whether a is less than b. It is "
        "one if true, and zero if false. The matching instruction is slt, set less than, "
        "which sets rd to one if rs1 is less than rs2, and to zero otherwise.",
    "对应的指令是": "The matching instruction",
    "a、b 放在 x5、x6，结果放进 x7：slt x7 x5 x6。3 < 5 成立，x7 = 1。":
        "Suppose a and b are in x5 and x6, with the result going into x7, so we write slt x7 "
        "x5 x6. Since three is less than five, x7 becomes one.",
    "3 < 5 成立": "Since three is less than five",
    "sltu 是它的无符号版本（u 代表 unsigned）。两者什么时候结果不同？看一个例子。x5 = 0xFFFFFFFF，32 位全是 1。当作有符号数，它是 −1；当作无符号数，它是 4294967295。":
        "The sltu instruction is the unsigned version, where the u stands for unsigned. When "
        "do the two give different results? Take x5 equal to 0xFFFFFFFF, with all thirty-two "
        "bits set to one. As a signed number it is minus one, and as an unsigned number it is "
        "over four billion.",
    "x5 = 0xFFFFFFFF": "Take x5 equal to",
    "当作有符号数": "As a signed number",
    "当作无符号数": "and as an unsigned number",
    "slt 比的是 −1 < 1，成立，得 1；sltu 比的是 4294967295 < 1，不成立，得 0。在 C 里，类型由变量的声明决定；在汇编里，比特本身没有类型，当有符号数还是无符号数，由指令决定。":
        "So slt compares minus one with one, which is true, and gives one. But sltu compares "
        "a number over four billion with one, which is false, and gives zero. In C the type "
        "comes from a variable's declaration, but in assembly the bits have no type, and the "
        "instruction decides whether they are signed or unsigned.",
    "在 C 里，类型由变量的声明决定": "In C the type comes",
    "sltu 比的是": "But sltu compares",
    "立即数版本 slti 和 sltiu 拿寄存器和常数比较。x5 不变：slti x7 x5 10 得 1，sltiu 得 0。":
        "The immediate versions compare a register with a constant, and they are called slti, "
        "and sltiu. With x5 unchanged, slti x7 x5 10 gives one, and sltiu gives zero.",
    "顺便一提：乘法 mul 不在 RV32I 基础指令集里，它属于 M 扩展（M extension）。通用乘法的电路比移位复杂得多，所以不放进基础指令集。除法、取余也在 M 扩展里，浮点运算在 F 扩展里。":
        "By the way, multiplication, mul, is not in the RV32I base instruction set, but "
        "belongs to the M extension. General multiplication needs far more circuitry than a "
        "shift, so it stays out of the base set. Division and remainder are in the M "
        "extension too, and floating point is in the F extension.",
    "通用乘法的电路": "General multiplication needs",
    "回到分支。先看一个 if-else，变量 x、y、z、i、j 依次放在 x10 到 x14。":
        "Back to branches. First an if-else, where the variables x, y, z, i, and j live in "
        "x10 through x14.",
    "这个 if-else 有两种翻译。选项 B 和第 5 集一样：用 bne 把条件取反。选项 A 不取反：用 beq，相等就跳到 If，于是 else 部分反而写在前面。两种都对，都是 4 条指令。":
        "This if-else has two translations. Option B is the same as in episode five, using "
        "bne to invert the condition. Option A doesn't invert, and uses beq to jump to If "
        "when the values are equal, so the else part ends up written first. Both are correct, "
        "and both take four instructions.",
    "选项 A 不取反": "Option A doesn't invert",
    "用 bne 把条件取反": "using bne to invert",
    "那如果没有 else 呢？选项 A 用 beq：相等时跳到 If 执行 add；不相等时，还得靠 j End 绕过 add。":
        "What if there is no else? Option A uses beq, jumping to If to run the add when the "
        "values are equal, but when they are not equal, it needs a j End to get around the "
        "add.",
    "选项 A 用 beq": "Option A uses beq",
    "不相等时": "but when they are not equal",
    "选项 B 用 bne：不相等就直接跳到 End；相等时顺着往下执行 add。两种都对。但 B 和 C 代码的结构一致，只要 2 条指令，比 A 少一条，性能也更好。":
        "Option B uses bne, jumping straight to End when the values are not equal, and "
        "running on down into the add when they are equal. Both are correct, but B follows "
        "the structure of the C code and needs only two instructions, one fewer than A, so it "
        "performs better too.",
    "两种都对": "Both are correct",
    "汇编里没有 while 和 for，只有分支和跳转。它们相当于 C 里的 goto：跳到某个标签处接着执行。在真正的 C 程序里别写 goto，它让代码很难读（xkcd 292 甚至说会招来迅猛龙）。但它很适合当翻译的中间一步。":
        "Assembly has no while or for, only branches and jumps. They work like the goto in C, "
        "jumping to a label and carrying on from there. In real C programs you shouldn't "
        "write goto, because it makes code hard to read, and xkcd even says it summons "
        "velociraptors, but it is a very handy intermediate step for translation.",
    "套路是：先把控制结构改写成 goto，再一行一行换成指令。为了写出真实的指令，设 cond 为 x5 < x6。":
        "The recipe is to rewrite a control structure into gotos first, and then turn them "
        "into instructions one line at a time. To write real instructions, let cond be x5 "
        "less than x6.",
    "最后看一个完整的例子：把 int 数组 arr 的 20 个元素加起来。先按套路改写成 goto：条件取反，i >= 20 就跳到 End。":
        "Finally, a complete example that adds up the twenty elements of the int array arr. "
        "First we rewrite it as gotos, inverting the condition so that when i is at least "
        "twenty, we jump to End.",
    "先按套路改写成 goto": "First we rewrite it",
    "条件取反": "inverting the condition",
    "这是笔记给出的汇编，一行注释也没有。每个寄存器对应 C 里的什么？把上面的寄存器和下面的 C 表达式配对。提示：x8 存的是 arr 的地址。暂停一下，自己试试。":
        "This is the assembly from the notes, with not a single comment. What does each "
        "register correspond to in the C code? Match the registers above with the C "
        "expressions below. As a hint, x8 holds the address of arr. Pause for a moment and "
        "try it yourself.",
    "把上面的寄存器和下面的 C 表达式配对": "Match the registers above",
    "注意 Loop 和 End 不是指令，只是地址的名字：Loop 就是 bge 那条指令的地址。":
        "Note that Loop and End are not instructions, just names for addresses, and Loop is "
        "the address of the bge instruction.",
    "和第 5 集比一比：那里每轮用 slli 和 add 重新算 A + 4i；这里让指针每轮后移 4 个字节，每轮少一条指令。笔记还附了一个能在模拟器 Venus 里运行的完整版：arr 装着 1 到 20，程序最后打印出 210。":
        "Compare this with episode five. There, every round used slli and add to work out A "
        "plus four i again, but here a pointer moves forward four bytes each round, which "
        "saves one instruction per round. The notes also include a full version that runs in "
        "the Venus simulator, where arr holds one to twenty, and the program prints two "
        "hundred ten at the end.",
    "笔记还附了一个": "The notes also include",
    "那里每轮用": "There, every round used",
}
