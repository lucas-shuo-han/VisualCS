"""English for episode 8 (keys are the Chinese strings in ep08_recursion.py)."""

EN = {
    # ---- end card
    "真正的跳转指令只有 jal（跳到标签）和 jalr（跳到寄存器里的地址）":
        "The only real jumps are jal, which goes to a label, and jalr, which goes to an "
        "address in a register",
    "j、jr、ret 都是 rd = x0 的伪指令：只跳，不链接":
        "The j, jr, and ret instructions are pseudo-instructions with rd equal to x0, so they "
        "jump without linking",
    "递归的每一层都有自己的栈帧，各存一份 ra 和 s0":
        "Each level of recursion gets its own stack frame, with its own saved ra and s0",
    "跨调用还要用的值，放进 s 寄存器或存到栈上":
        "Values needed after a call go in the s registers, or on the stack",
    "叶子函数不必保存 ra，常常连栈都不用":
        "Leaf functions don't need to save ra, and often don't touch the stack at all",

    # ---- jal / jalr
    "无条件跳转：jal 与 jalr": "Unconditional Jumps: jal and jalr",
    "真正的指令": "Real instructions",
    "也写作 jalr rd, imm(rs1)": "also written jalr rd, imm(rs1)",
    "伪指令（由汇编器展开）": "Pseudoinstructions (expanded by the assembler)",
    "只跳，不留返回地址": "jump, keep no return address",
    "调用：返回地址写进 ra": "call: return address goes in ra",
    "跳到寄存器里的地址": "jump to the address in a register",
    "从函数返回": "return from a function",
    "目标 = PC + 偏移：汇编时就确定了": "target = PC + offset: fixed at assembly time",
    "适合调用有名字的函数": "good for calling a function by name",
    "目标 = rs1 + imm：运行时才算出来": "target = rs1 + imm: computed at run time",
    "jr   ra         # 返回：回到哪里由 ra 决定":
        "jr   ra         # return to the address in ra",
    "jalr ra, t0, 0  # 函数指针：调用 t0 里的地址":
        "jalr ra, t0, 0  # call the function pointer in t0",
    "远跳转：auipc + jalr（第 12 集）": "far jumps: auipc + jalr (Episode 12)",

    # ---- clobbering
    "// 假设 n 是正整数": "// assume positive numbers",
    "每次调用：31 次 sw，再加 31 次 lw": "Every call: 31 sw, plus 31 lw",

    # ---- the contract
    "调用者可以指望": "The caller can count on",
    "调用后保持不变": "unchanged",
    "可能已经被改": "may change",
    "被调用者必须做到": "The callee must",
    "随便用": "use freely",
    "用前保存，返回前恢复": "save, then restore",
    "对 main：被调用者": "to main: callee",
    "对 factorial(2)：调用者": "to factorial(2): caller",

    # ---- the notes' factorial
    "序言": "prologue",
    "尾声": "epilogue",
    "8 字节的栈帧": "8-byte stack frame",

    # ---- trace of factorial(3)
    "main 的数据": "main's data",

    # ---- foo
    "foo(100) 最深时栈上有": "At its deepest, foo(100) has",
    "101 个栈帧，共 808 字节": "101 frames on the stack: 808 bytes",

    # ---- leaf functions
    "叶子": "leaves",
    "没有 sw，没有 lw，sp 一动不动": "No sw, no lw, and sp never moves",

    # ---- the register table
    "编号": "Register",
    "名字": "Name",
    "用途": "Use",
    "由谁保存": "Saved by",
    "常数 0": "Constant 0",
    "返回地址": "Return address",
    "栈指针": "Stack pointer",
    "全局指针": "Global pointer",
    "线程指针": "Thread pointer",
    "临时寄存器": "Temporary",
    "保存寄存器 / 帧指针": "Saved / frame pointer",
    "保存寄存器": "Saved",
    "参数 / 返回值": "Argument / return value",
    "参数": "Arguments",
    "调用者": "Caller",
    "被调用者": "Callee",

    # ---- func_a
    "存 t1": "save t1",
    "取回 t1": "restore t1",

    # ---- quiz
    "判断题": "True or False?",
    "函数返回后，t 寄存器可能变了，但 a 寄存器不会。":
        "After a call, t registers may have changed, but a registers can't.",
    "函数要用 s0–s11，必须先保存旧值，返回前恢复。":
        "To use s0–s11, a function must save them and later restore them.",
    "栈只能在函数的开头和结尾操作。":
        "The stack may only be touched at a function's start and end.",
    "错": "False",
    "对": "True",

    # ---- six steps and the analogy
    "六个步骤，再看一遍": "The Six Steps, Revisited",
    "要保留的 t、a 寄存器先存好；参数放进 a0–a7":
        "Save needed t/a registers; arguments in a0–a7",
    "jal ra, 函数名": "jal ra, func",
    "sp 减一次；保存要用的 s 寄存器，要调用别人就保存 ra":
        "Lower sp once; save used s regs, and ra if calling",
    "函数体": "Body",
    "做该做的事": "Do the work",
    "返回值放进 a0；恢复 ra 和 s 寄存器；sp 加回去":
        "Result in a0; restore ra and s registers; raise sp",
    "RISC-V 手册里的“过程”（procedure），就是函数":
        "In the RISC-V manual, a \"procedure\" is just a function",
    "桌子": "Table",
    "寄存器": "Registers",
    "壁橱": "Closet",
    "内存": "Memory",
    "父母": "Parents",
    "你": "You",
    "父母备在桌上的东西": "Essentials left out",
    "你留下的礼物": "Your gift",
    "返回值": "Return value",

    # ---- spoken beats and cue phrases (see references/narration-writing.md)
    "第 7 集用过 jal 和 jr ra。其实 RISC-V 真正的无条件跳转指令只有两条。jal rd, label 意为“跳转并链接”，其实先链接：把 PC + 4 写进 rd，再跳到 label。":
        "In episode seven we used jal and jr ra, but RISC-V really has only two unconditional "
        "jump instructions. The jal instruction takes rd and a label, and its name means jump "
        "and link, but it actually links first, writing PC plus four into rd, and then jumps "
        "to the label.",
    "jal rd, label 意为": "The jal instruction takes",
    "把 PC + 4 写进 rd": "writing PC plus four",
    "jalr rd, rs1, imm 同样先链接，但跳到 rs1 + imm：地址来自寄存器。":
        "The jalr instruction, which takes rd, rs1, and an immediate, also links first, but "
        "it jumps to rs1 plus the immediate, so its address comes from a register.",
    "其余跳转都是伪指令。j、jr、ret 把返回地址写进 x0，等于丢掉；省略 rd 的 jal 则链接到 ra。":
        "Every other jump is a pseudo-instruction. The j, jr, and ret instructions write the "
        "return address into x0, which throws it away, while a jal with no rd links into ra.",
    "写进 x0": "write the return address into x0",
    "为什么要两条？jal 的目标在汇编时就定了，正适合调用有名字的函数。jalr 的目标由寄存器在运行时给出：返回 ra 里的地址、调用函数指针，配合 auipc 还能跳得很远。":
        "So why two instructions? The target of jal is fixed at assembly time, which suits "
        "calling a function by name. The target of jalr is given by a register at run time, "
        "so it can return to the address in ra, call a function pointer, and, together with "
        "auipc, jump very far.",
    "jalr 的目标由寄存器": "The target of jalr is given",
    "本集的主角是阶乘：factorial(1) = 1，factorial(n) = n × factorial(n − 1)。":
        "The star of this episode is the factorial. The factorial of one is one, and the "
        "factorial of n is n times the factorial of n minus one.",
    "如果什么都不保存，会怎样？设 main 调用 factorial(2)：a0 = 2，ra 记着回 main 的地址。factorial(2) 把参数 1 放进 a0，再 jal：ra 被改成回 factorial(2) 的地址。":
        "What happens if we save nothing? Suppose main calls factorial of two, so a0 is two, "
        "and ra remembers the way back to main. Then factorial of two puts the argument one "
        "into a0 and does a jal, which changes ra to point back into factorial of two.",
    "factorial(2) 把参数 1": "Then factorial of two puts",
    "放进 a0": "puts the argument one into a0",
    "ra 被改成": "which changes ra",
    "factorial(1) 返回 1，可 factorial(2) 的 2 早被参数 1 覆盖了；ra 也还指着 factorial(2) 自己，再也回不到 main。":
        "When factorial of one returns one, the two that factorial of two needed was long ago "
        "overwritten by the argument one. Worse, ra still points into factorial of two "
        "itself, so we can never get back to main.",
    "factorial(2) 的 2 早被": "the two that factorial of two",
    "早被参数 1 覆盖了": "was long ago overwritten",
    "ra 也还指着": "ra still points",
    "最省事的办法：每次调用都把 x1 到 x31 全部压栈，返回后再全部取回。可访问内存很慢，而一次调用真正要保护的，往往只有几个寄存器。":
        "The easiest fix is to push all of x1 through x31 on every call, and pull them all "
        "back afterwards. But memory is slow, and a call really needs to protect only a few "
        "registers.",
    "可访问内存很慢": "But memory is slow",
    "返回后再全部取回": "and pull them all back",
    "解决办法是第 7 集的调用约定：调用者只能指望 s 寄存器和 sp 不变；被调用者要用 s 寄存器，得先存旧值、返回前恢复。":
        "The solution is the calling convention from episode seven. The caller can count only "
        "on the s registers and sp staying unchanged. A callee that wants to use an s "
        "register has to save the old value first, and restore it before returning.",
    "调用者只能指望": "The caller can count only on",
    "被调用者要用": "A callee that wants",
    "递归函数身兼两职：对上一层它是被调用者，对下一层它又是调用者。":
        "A recursive function wears two hats. To the level above it, it is a callee, and to "
        "the level below it, it is a caller.",
    "对上一层": "To the level above it",
    "对下一层": "and to the level below",
    "这是笔记里遵守调用约定的阶乘，从地址 0x2000 开始。先认出序言和尾声。":
        "Here is the factorial from the notes, which follows the calling convention, starting "
        "at address 0x2000. First let's pick out the prologue and the epilogue.",
    "先认出序言和尾声": "First let's pick out",
    "序言在栈上划出 8 字节，这就是本次调用的栈帧：后面的 jal 会覆盖 ra，要借用的 s0 也得先存旧值。mv s0 a0 把 n 放进 s0：s 寄存器跨调用不变，递归调用回来，n 还在。":
        "The prologue carves eight bytes out of the stack, which is the stack frame for this "
        "call. We need it because the later jal will overwrite ra, and s0, which we want to "
        "borrow, needs its old value saved. Then mv s0 a0 puts n into s0, and because the s "
        "registers survive calls, n is still there when the recursive call returns.",
    "mv s0 a0": "Then mv s0 a0",
    "bne 只能比较两个寄存器，所以先用 li 把 1 放进 t0；n ≠ 1 就跳到 recurse。否则是基本情况：a0 = 1。这里不能直接 jr ra：s0 还没恢复，栈帧也没弹，所以 j 到尾声。":
        "The bne instruction can compare only two registers, so first we use li to put one "
        "into t0, and if n is not one, we branch to recurse. Otherwise it is the base case, "
        "where a0 is one. We can't simply do jr ra here, because s0 hasn't been restored and "
        "the stack frame hasn't been popped, so we use j to go to the epilogue.",
    "否则是基本情况": "Otherwise it is the base case",
    "所以 j 到尾声": "so we use j",
    "recurse：a0 = n − 1，调用自己；回来时 a0 = (n − 1)!，再乘上 s0 里的 n。尾声的顺序和序言相反：先从栈上取回 ra 和 s0，再把 sp 加 8 弹掉栈帧，最后 jr ra。":
        "At recurse, a0 becomes n minus one, we call ourselves, and when we come back, a0 "
        "holds the factorial of n minus one, which we multiply by the n in s0. The epilogue "
        "runs in the reverse order of the prologue. So we first get ra and s0 back from the "
        "stack, then add eight to sp to pop the frame, and finally do jr ra.",
    "尾声的顺序": "The epilogue runs in the reverse order",
    "完整跟踪一次 factorial(3)。main 已经分配了 12 字节的栈帧，此时 sp = 0xFFFFFFD4。":
        "Let's trace the factorial of three from start to finish. Main has already set aside "
        "a twelve-byte stack frame, and sp points just below it.",
    "main 把 3 放进 a0，在 0x1004 执行 jal：ra = 0x1008，跳进 factorial。":
        "Main puts three into a0 and executes the jal at 0x1004, which makes ra equal 0x1008 "
        "and jumps into factorial.",
    "把 3 放进 a0": "Main puts three into a0",
    "factorial(3) 的序言：sp 减 8，变成 0xFFFFFFCC，再存下 ra = 0x1008 和 main 的 s0 = 42。":
        "In the prologue for the factorial of three, sp drops by eight, and then ra, which is "
        "0x1008, and main's s0, which is forty-two, are saved.",
    "mv 让 s0 = 3；3 ≠ 1，跳到 recurse：a0 = 2，在 0x2024 执行 jal，ra = 0x2028。":
        "The mv sets s0 to three. Since three is not one, we branch to recurse and set a0 to "
        "two, and then the jal at 0x2024 sets ra to 0x2028.",
    "factorial(2) 照样压栈帧：sp = 0xFFFFFFC4，存下 ra = 0x2028 和 s0 = 3，再以 a0 = 1 调用自己。":
        "The factorial of two pushes its own frame in the same way, saving ra, which is "
        "0x2028, and s0, which is three. Then it calls itself again with a0 equal to one.",
    "factorial(1) 也压一个：sp = 0xFFFFFFBC，存下 ra = 0x2028 和 s0 = 2。":
        "The factorial of one pushes one more frame, saving ra, which is 0x2028, and s0, "
        "which is two.",
    "三个栈帧各存一份 ra 和 s0：factorial(3) 存的 ra 回 main，另两份都回 0x2028 的 mul。":
        "Each of the three frames holds its own copy of ra and s0. The ra saved by the "
        "factorial of three leads back to main, while the other two both lead back to the mul "
        "at 0x2028.",
    "另两份都回": "while the other two",
    "factorial(1) 是基本情况：a0 = 1，然后 j 到尾声。尾声取回 ra = 0x2028 和 s0 = 2，sp 回到 0xFFFFFFC4，jr ra 回到 mul。":
        "The factorial of one is the base case, so a0 becomes one and we jump to the "
        "epilogue. The epilogue gets back ra, which is 0x2028, and s0, which is two, then sp "
        "returns to where it was, and jr ra goes back to the mul.",
    "a0 = s0 × a0 = 2 × 1 = 2。s0 里的 2 正是 factorial(2) 的 n：factorial(1) 用过 s0，但返回前恢复了。":
        "Now a0 is s0 times a0, which is two times one, or two. The two in s0 is exactly the "
        "n of the factorial of two, because the factorial of one used s0 but restored it "
        "before returning.",
    "factorial(2) 走完尾声：ra = 0x2028，s0 = 3，sp = 0xFFFFFFCC。回到 mul：a0 = 3 × 2 = 6。factorial(3) 取回 ra = 0x1008 和 main 的 s0 = 42，sp 回到 0xFFFFFFD4，返回 main。":
        "The factorial of two finishes its epilogue, getting back ra, s0, and sp, and returns "
        "to the mul, where a0 becomes three times two, which is six. Then the factorial of "
        "three gets back ra and main's s0, which is forty-two, sp returns to where it was, "
        "and we return to main.",
    "a0 = 3 × 2 = 6": "where a0 becomes three times two",
    "回到 main：a0 = 6，sp 和 s0 都和调用前一样。弹出的栈帧还留在内存里，只是没人再用了。":
        "Back in main, a0 is six, and sp, like s0, is exactly what it was before the call. "
        "The popped stack frames are still in memory, but nobody uses them any more.",
    "笔记里的 foo 也是递归：foo(i) = i + foo(i − 1)。它的汇编和阶乘并排一看，骨架完全一样。只有三处不同：直接和 x0 比较，省掉 li；基本情况返回 0；乘法换成加法。":
        "The foo function in the notes is recursive too, since foo of i is i plus foo of i "
        "minus one. Put its assembly next to the factorial, and the skeleton is exactly the "
        "same. Only three things differ. It compares directly with x0, which saves the li, "
        "the base case returns zero, and the multiplication becomes an addition.",
    "只有三处不同": "Only three things differ",
    "直接和 x0 比较": "It compares directly with x0",
    "笔记的 main 把 foo(3) 放进 s0，调用 foo(100) 后它还在。foo(100) 最深时压着 101 个栈帧，共 808 字节。":
        "The notes' main puts foo of three into s0, and it is still there after calling foo "
        "of a hundred. At its deepest, foo of a hundred has a hundred and one stack frames, "
        "eight hundred eight bytes in all.",
    "foo(100) 最深时": "At its deepest",
    "并非每个函数都需要栈。笔记里的 sum_square 调用两次 mult，而 mult 不再调用任何函数。mult 这样的函数叫叶子函数：它没有 jal，ra 不会被覆盖；只用 t、a 寄存器的话，连一条 sw、lw 都不用。":
        "Not every function needs a stack. In the notes, sum_square calls mult twice, and "
        "mult calls no function at all. A function like mult is called a leaf function, since "
        "it has no jal, so ra is never overwritten. If it uses only temporary and argument "
        "registers, it needs no sw instruction and no lw instruction.",
    "mult 这样的函数叫叶子函数": "A function like mult",
    "它没有 jal": "since it has no jal",
    "连一条 sw、lw 都不用": "it needs no sw instruction",
    "完整的寄存器约定表如下。gp 和 tp 另有专门用途，不归调用约定管，别去碰它们。s0 又叫 fp，即帧指针：sp 可能在函数中途移动，fp 则一直指着当前栈帧。":
        "Here is the complete table of register conventions. The gp register and the tp "
        "register have special purposes of their own and aren't covered by the calling "
        "convention, so don't touch them. And s0 is also called fp, the frame pointer, "
        "because sp may move in the middle of a function, while fp always points at the "
        "current stack frame.",
    "s0 又叫 fp": "And s0 is also called fp",
    "gp 和 tp 另有专门用途": "The gp register and the tp",
    "笔记里的 func_a 就在中途动了 sp：它要调用 func_b，调用前后都要用 t1。":
        "The func_a in the notes moves sp in the middle of the function, since it calls "
        "func_b, and it needs t1 both before and after the call.",
    "调用前后都要用 t1": "and it needs t1",
    "序言压 8 字节，存下 ra 和 s0。ra 本归调用者保存，但习惯上也在序言里存。":
        "The prologue pushes eight bytes, saving ra and s0. Normally ra is the caller's to "
        "save, but by habit it is saved in the prologue too.",
    "t1 = 10，s0 = 20。t1 归调用者保存，func_b 可能改掉它，所以调用前再压 4 字节存下 t1。":
        "Now t1 is ten and s0 is twenty. The t1 register is caller-saved, so func_b might "
        "change it, which is why, before the call, we push another four bytes to save t1.",
    "func_b 返回后，t1 里是什么已经说不准了。好在栈上有备份：取回 t1 = 10，马上弹掉这 4 字节。":
        "After func_b returns, we can't tell what is in t1 any more. Luckily there is a "
        "backup on the stack, so we get t1 back as ten, and pop those four bytes right away.",
    "sp 一动，偏移就跟着变：刚才 0(sp) 是 t1，弹掉之后才又是 ra。":
        "Once sp moves, the offsets move with it. A moment ago zero of sp was t1, and only "
        "after the pop is it ra again.",
    "最后 t1 = 15，s0 = 25。尾声取回 ra 和调用者的 s0 = 42，sp 复原，ret 返回。":
        "In the end, t1 is fifteen and s0 is twenty-five. The epilogue gets back ra and the "
        "caller's s0, which is forty-two, sp is restored, and ret returns.",
    "三道判断题，取自笔记的练习。先自己想一想。":
        "Here are three true-or-false questions, taken from the notes' exercises. Think about "
        "them for yourself first.",
    "第 1 题错：a0、a1 要带回返回值。a 寄存器和 t 一样，都由调用者保存。第 2 题对：s 寄存器由被调用者保存，通常在序言里存、在尾声里恢复。":
        "Statement one is false. The registers a0 and a1 carry back return values, and the "
        "argument registers, like the temporary ones, are saved by the caller. Statement two "
        "is true. The s registers are saved by the callee, usually in the prologue and "
        "restored in the epilogue.",
    "第 2 题对": "Statement two is true",
    "第 3 题错：func_a 就在中途压栈保存了 t1。只要压栈、弹栈配对，栈随时能用。":
        "Statement three is false. The func_a function pushed t1 right in the middle of the "
        "function. As long as pushes and pops are paired, the stack can be used at any time.",
    "最后，再过一遍第 7 集的六个步骤。第 1、2 步归调用者：存好还要用的 t、a 寄存器，放好参数，然后 jal。第 3 步序言：sp 只减一次，局部数组一并分配；存下要用的 s 寄存器，要调用别人就存 ra。":
        "Finally, let's go over the six steps from episode seven again. Steps one and two "
        "belong to the caller. It saves any temporary or argument registers it still needs, "
        "puts the arguments in place, and then does a jal. Step three is the prologue, where "
        "sp is lowered only once, so local arrays are allocated too. We also save the s "
        "registers we will use, and ra if we call other functions.",
    "第 3 步序言": "Step three is the prologue",
    "第 4 步是函数体；第 5、6 步是尾声：返回值放进 a0，恢复寄存器、弹栈帧，jr ra。":
        "Step four is the function body. Steps five and six are the epilogue, where we put "
        "the return value into a0, restore the registers, pop the stack frame, and finish "
        "with jr ra.",
    "笔记的比喻：调用函数就像替父母看家。父母是调用者，你是被调用者；桌子是寄存器，壁橱是内存。父母备在桌上的是参数。桌上别的东西，先收进壁橱（序言）；走前原样摆回，再留一份礼物：返回值（尾声）。":
        "The notes offer an analogy, where calling a function is like house-sitting for your "
        "parents. The parents are the caller and you are the callee, while the desk is the "
        "registers and the closet is memory. What the parents leave on the desk are the "
        "arguments. Whatever else is on the desk, you first put away in the closet, which is "
        "the prologue. When you leave, you put it all back exactly as it was, and leave a "
        "gift, the return value, which is the epilogue.",
    "父母备在桌上的是参数": "What the parents leave",
    "尾声取回": "The epilogue gets back",
    "factorial(3) 取回": "Then the factorial of three gets back",
}
