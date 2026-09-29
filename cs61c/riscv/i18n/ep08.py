"""English for episode 8 (keys are the Chinese strings in ep08_recursion.py)."""

EN = {
    # ---- end card
    "真正的跳转指令只有 jal（跳到标签）和 jalr（跳到寄存器里的地址）":
        "The only real jumps: jal (to a label) and jalr (to an address in a register)",
    "j、jr、ret 都是 rd = x0 的伪指令：只跳，不链接":
        "j, jr and ret are pseudoinstructions with rd = x0: they jump without linking",
    "递归的每一层都有自己的栈帧，各存一份 ra 和 s0":
        "Each level of recursion gets its own frame, with its own saved ra and s0",
    "跨调用还要用的值，放进 s 寄存器或存到栈上":
        "Values needed after a call go in s registers or on the stack",
    "叶子函数不必保存 ra，常常连栈都不用":
        "Leaf functions needn't save ra, and often don't touch the stack at all",

    # ---- jal / jalr
    "无条件跳转：jal 与 jalr": "Unconditional Jumps: jal and jalr",
    "真正的指令": "Real instructions",
    "也写作 jalr rd, imm(rs1)": "also written jalr rd, imm(rs1)",
    "第 7 集用过 jal 和 jr ra。其实 RISC-V 真正的无条件跳转指令只有两条。":
        "Episode 7 used jal and jr ra. In fact, RISC-V has only two real unconditional "
        "jump instructions.",
    "jal rd, label 意为“跳转并链接”，其实先链接：把 PC + 4 写进 rd，再跳到 label。":
        "jal rd, label stands for \"jump and link,\" but it really links first: it writes "
        "PC + 4 into rd, then jumps to label.",
    "jalr rd, rs1, imm 同样先链接，但跳到 rs1 + imm：地址来自寄存器。":
        "jalr rd, rs1, imm also links first, but jumps to rs1 + imm: the address "
        "comes from a register.",
    "伪指令（由汇编器展开）": "Pseudoinstructions (expanded by the assembler)",
    "只跳，不留返回地址": "jump, keep no return address",
    "调用：返回地址写进 ra": "call: return address goes in ra",
    "跳到寄存器里的地址": "jump to the address in a register",
    "从函数返回": "return from a function",
    "其余跳转都是伪指令。j、jr、ret 把返回地址写进 x0，等于丢掉；省略 rd 的 jal 则链接到 ra。":
        "Every other jump is a pseudoinstruction: j, jr and ret write the link to x0, "
        "discarding it; jal without rd links to ra.",
    "目标 = PC + 偏移：汇编时就确定了": "target = PC + offset: fixed at assembly time",
    "适合调用有名字的函数": "good for calling a function by name",
    "目标 = rs1 + imm：运行时才算出来": "target = rs1 + imm: computed at run time",
    "jr   ra         # 返回：回到哪里由 ra 决定":
        "jr   ra         # return to the address in ra",
    "jalr ra, t0, 0  # 函数指针：调用 t0 里的地址":
        "jalr ra, t0, 0  # call the function pointer in t0",
    "远跳转：auipc + jalr（第 12 集）": "far jumps: auipc + jalr (Episode 12)",
    "为什么要两条？jal 的目标在汇编时就定了，正适合调用有名字的函数。":
        "Why two? jal's target is fixed at assembly time, which is just right for "
        "calling a function by name.",
    "jalr 的目标由寄存器在运行时给出：返回 ra 里的地址、调用函数指针，配合 auipc 还能跳得很远。":
        "jalr's target comes from a register at run time. That covers returning to the "
        "address in ra, calling through a function pointer, and, with auipc, jumping far.",

    # ---- clobbering
    "// 假设 n 是正整数": "// assume positive numbers",
    "本集的主角是阶乘：factorial(1) = 1，factorial(n) = n × factorial(n − 1)。":
        "This episode's star is factorial, defined by factorial(1) = 1 "
        "and factorial(n) = n × factorial(n − 1).",
    "如果什么都不保存，会怎样？设 main 调用 factorial(2)：a0 = 2，ra 记着回 main 的地址。":
        "What if we save nothing? Say main calls factorial(2): a0 = 2, and ra holds "
        "the way back to main.",
    "factorial(2) 把参数 1 放进 a0，再 jal：ra 被改成回 factorial(2) 的地址。":
        "factorial(2) puts the argument 1 in a0 and does a jal: now ra points back "
        "into factorial(2).",
    "factorial(1) 返回 1，可 factorial(2) 的 2 早被参数 1 覆盖了；ra 也还指着 factorial(2) 自己，再也回不到 main。":
        "factorial(1) returns 1, but factorial(2)'s 2 was overwritten by the argument 1; "
        "and ra still points into factorial(2), so it can never get back to main.",
    "每次调用：31 次 sw，再加 31 次 lw": "Every call: 31 sw, plus 31 lw",
    "最省事的办法：每次调用都把 x1 到 x31 全部压栈，返回后再全部取回。":
        "The lazy fix: on every call, push all of x1 through x31, then load them "
        "all back afterward.",
    "可访问内存很慢，而一次调用真正要保护的，往往只有几个寄存器。":
        "But memory is slow, and a call usually needs to protect only a few registers.",

    # ---- the contract
    "调用者可以指望": "The caller can count on",
    "调用后保持不变": "unchanged",
    "可能已经被改": "may change",
    "被调用者必须做到": "The callee must",
    "随便用": "use freely",
    "用前保存，返回前恢复": "save, then restore",
    "解决办法是第 7 集的调用约定：调用者只能指望 s 寄存器和 sp 不变；被调用者要用 s 寄存器，得先存旧值、返回前恢复。":
        "The fix is Episode 7's calling convention: callers can rely only on s registers "
        "and sp; a callee that uses an s register saves it first and restores it before returning.",
    "对 main：被调用者": "to main: callee",
    "对 factorial(2)：调用者": "to factorial(2): caller",
    "递归函数身兼两职：对上一层它是被调用者，对下一层它又是调用者。":
        "A recursive function plays both roles: callee to the level above, "
        "caller to the level below.",

    # ---- the notes' factorial
    "序言": "prologue",
    "尾声": "epilogue",
    "这是笔记里遵守调用约定的阶乘，从地址 0x2000 开始。先认出序言和尾声。":
        "Here is the notes' factorial, which follows the calling convention, "
        "starting at address 0x2000. First, spot the prologue and epilogue.",
    "8 字节的栈帧": "8-byte stack frame",
    "序言在栈上划出 8 字节，这就是本次调用的栈帧：后面的 jal 会覆盖 ra，要借用的 s0 也得先存旧值。":
        "The prologue carves out 8 bytes on the stack: this call's stack frame. The jal "
        "further down will overwrite ra, and s0 is borrowed, so its old value is saved too.",
    "mv s0 a0 把 n 放进 s0：s 寄存器跨调用不变，递归调用回来，n 还在。":
        "mv s0 a0 copies n into s0. s registers survive calls, so n is still there "
        "when the recursive call returns.",
    "bne 只能比较两个寄存器，所以先用 li 把 1 放进 t0；n ≠ 1 就跳到 recurse。":
        "bne compares two registers, so li first puts 1 in t0. If n ≠ 1, "
        "branch to recurse.",
    "否则是基本情况：a0 = 1。这里不能直接 jr ra：s0 还没恢复，栈帧也没弹，所以 j 到尾声。":
        "Otherwise it's the base case: a0 = 1. It can't just jr ra: s0 isn't restored "
        "and the frame isn't popped yet, so it jumps to the epilogue.",
    "recurse：a0 = n − 1，调用自己；回来时 a0 = (n − 1)!，再乘上 s0 里的 n。":
        "recurse: a0 = n − 1, and it calls itself. On return a0 = (n − 1)!, "
        "which is multiplied by n from s0.",
    "尾声的顺序和序言相反：先从栈上取回 ra 和 s0，再把 sp 加 8 弹掉栈帧，最后 jr ra。":
        "The epilogue runs in the opposite order: load ra and s0 back from the stack, "
        "then add 8 to sp to pop the frame, and finally jr ra.",

    # ---- trace of factorial(3)
    "main 的数据": "main's data",
    "完整跟踪一次 factorial(3)。main 已经分配了 12 字节的栈帧，此时 sp = 0xFFFFFFD4。":
        "Let's trace factorial(3) all the way through. main has already allocated a "
        "12-byte frame, so sp = 0xFFFFFFD4.",
    "main 把 3 放进 a0，在 0x1004 执行 jal：ra = 0x1008，跳进 factorial。":
        "main puts 3 in a0 and executes the jal at 0x1004: ra = 0x1008, and control "
        "enters factorial.",
    "factorial(3) 的序言：sp 减 8，变成 0xFFFFFFCC，再存下 ra = 0x1008 和 main 的 s0 = 42。":
        "factorial(3)'s prologue: sp drops by 8 to 0xFFFFFFCC, then it saves "
        "ra = 0x1008 and main's s0 = 42.",
    "mv 让 s0 = 3；3 ≠ 1，跳到 recurse：a0 = 2，在 0x2024 执行 jal，ra = 0x2028。":
        "mv sets s0 = 3. Since 3 ≠ 1, it branches to recurse: a0 = 2, and the jal "
        "at 0x2024 sets ra = 0x2028.",
    "factorial(2) 照样压栈帧：sp = 0xFFFFFFC4，存下 ra = 0x2028 和 s0 = 3，再以 a0 = 1 调用自己。":
        "factorial(2) pushes a frame the same way: sp = 0xFFFFFFC4, saving ra = 0x2028 "
        "and s0 = 3, then calls itself with a0 = 1.",
    "factorial(1) 也压一个：sp = 0xFFFFFFBC，存下 ra = 0x2028 和 s0 = 2。":
        "factorial(1) pushes one too: sp = 0xFFFFFFBC, saving ra = 0x2028 and s0 = 2.",
    "三个栈帧各存一份 ra 和 s0：factorial(3) 存的 ra 回 main，另两份都回 0x2028 的 mul。":
        "Each of the three frames holds its own ra and s0. factorial(3)'s ra leads back "
        "to main; the other two lead to the mul at 0x2028.",
    "factorial(1) 是基本情况：a0 = 1，然后 j 到尾声。":
        "factorial(1) is the base case: a0 = 1, then j to the epilogue.",
    "尾声取回 ra = 0x2028 和 s0 = 2，sp 回到 0xFFFFFFC4，jr ra 回到 mul。":
        "The epilogue restores ra = 0x2028 and s0 = 2, sp goes back to 0xFFFFFFC4, "
        "and jr ra returns to the mul.",
    "a0 = s0 × a0 = 2 × 1 = 2。s0 里的 2 正是 factorial(2) 的 n：factorial(1) 用过 s0，但返回前恢复了。":
        "a0 = s0 × a0 = 2 × 1 = 2. The 2 in s0 is factorial(2)'s own n: "
        "factorial(1) used s0, but restored it before returning.",
    "factorial(2) 走完尾声：ra = 0x2028，s0 = 3，sp = 0xFFFFFFCC。回到 mul：a0 = 3 × 2 = 6。":
        "factorial(2) runs its epilogue: ra = 0x2028, s0 = 3, sp = 0xFFFFFFCC. "
        "Back at the mul: a0 = 3 × 2 = 6.",
    "factorial(3) 取回 ra = 0x1008 和 main 的 s0 = 42，sp 回到 0xFFFFFFD4，返回 main。":
        "factorial(3) restores ra = 0x1008 and main's s0 = 42, sp goes back to "
        "0xFFFFFFD4, and it returns to main.",
    "回到 main：a0 = 6，sp 和 s0 都和调用前一样。弹出的栈帧还留在内存里，只是没人再用了。":
        "Back in main: a0 = 6, and sp and s0 are just as they were before the call. "
        "The popped frames are still in memory; nobody uses them anymore.",

    # ---- foo
    "笔记里的 foo 也是递归：foo(i) = i + foo(i − 1)。它的汇编和阶乘并排一看，骨架完全一样。":
        "The notes' foo is recursive too: foo(i) = i + foo(i − 1). Put it next to factorial and the skeleton is identical.",
    "只有三处不同：直接和 x0 比较，省掉 li；基本情况返回 0；乘法换成加法。":
        "Only three things differ: it compares against x0 directly, saving an li; "
        "the base case returns 0; and multiply becomes add.",
    "foo(100) 最深时栈上有": "At its deepest, foo(100) has",
    "101 个栈帧，共 808 字节": "101 frames on the stack: 808 bytes",
    "笔记的 main 把 foo(3) 放进 s0，调用 foo(100) 后它还在。foo(100) 最深时压着 101 个栈帧，共 808 字节。":
        "The notes' main keeps foo(3) in s0, where it survives the call to foo(100). "
        "At its deepest, foo(100) has 101 frames on the stack: 808 bytes.",

    # ---- leaf functions
    "并非每个函数都需要栈。笔记里的 sum_square 调用两次 mult，而 mult 不再调用任何函数。":
        "Not every function needs the stack. In the notes, sum_square calls mult twice, "
        "and mult calls nothing at all.",
    "叶子": "leaves",
    "mult 这样的函数叫叶子函数：它没有 jal，ra 不会被覆盖；只用 t、a 寄存器的话，连一条 sw、lw 都不用。":
        "A function like mult is a leaf function: with no jal, ra is never overwritten, "
        "and if it uses only t and a registers, it needs no sw or lw at all.",
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
    "完整的寄存器约定表如下。gp 和 tp 另有专门用途，不归调用约定管，别去碰它们。":
        "Here's the full register convention table. gp and tp have special jobs "
        "outside the calling convention, so leave them alone.",
    "s0 又叫 fp，即帧指针：sp 可能在函数中途移动，fp 则一直指着当前栈帧。":
        "s0 is also called fp, the frame pointer: sp may move partway through a function, "
        "but fp keeps pointing at the current frame.",

    # ---- func_a
    "存 t1": "save t1",
    "取回 t1": "restore t1",
    "笔记里的 func_a 就在中途动了 sp：它要调用 func_b，调用前后都要用 t1。":
        "The notes' func_a moves sp partway through: it calls func_b and needs t1 "
        "both before and after the call.",
    "序言压 8 字节，存下 ra 和 s0。ra 本归调用者保存，但习惯上也在序言里存。":
        "The prologue pushes 8 bytes and saves ra and s0. ra is caller-saved, but by "
        "convention it is saved in the prologue anyway.",
    "t1 = 10，s0 = 20。t1 归调用者保存，func_b 可能改掉它，所以调用前再压 4 字节存下 t1。":
        "t1 = 10, s0 = 20. t1 is caller-saved and func_b may change it, so before "
        "the call, func_a pushes 4 more bytes to save t1.",
    "func_b 返回后，t1 里是什么已经说不准了。好在栈上有备份：取回 t1 = 10，马上弹掉这 4 字节。":
        "After func_b returns, t1 could hold anything. Luckily the stack has a copy: "
        "t1 = 10 comes back, and those 4 bytes are popped right away.",
    "sp 一动，偏移就跟着变：刚才 0(sp) 是 t1，弹掉之后才又是 ra。":
        "When sp moves, the offsets move with it: a moment ago 0(sp) was t1; "
        "only after the pop is it ra again.",
    "最后 t1 = 15，s0 = 25。尾声取回 ra 和调用者的 s0 = 42，sp 复原，ret 返回。":
        "Finally t1 = 15 and s0 = 25. The epilogue restores ra and the caller's "
        "s0 = 42, puts sp back, and ret returns.",

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
    "三道判断题，取自笔记的练习。先自己想一想。":
        "Three true-or-false questions from the notes' exercises. Think them over first.",
    "第 1 题错：a0、a1 要带回返回值。a 寄存器和 t 一样，都由调用者保存。":
        "1 is false: a0 and a1 carry return values back. Like the t registers, "
        "the a registers are caller-saved.",
    "第 2 题对：s 寄存器由被调用者保存，通常在序言里存、在尾声里恢复。":
        "2 is true: s registers are callee-saved, usually saved in the prologue "
        "and restored in the epilogue.",
    "第 3 题错：func_a 就在中途压栈保存了 t1。只要压栈、弹栈配对，栈随时能用。":
        "3 is false: func_a pushed t1 partway through. As long as every push has a "
        "matching pop, the stack can be used anywhere.",

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
    "最后，再过一遍第 7 集的六个步骤。第 1、2 步归调用者：存好还要用的 t、a 寄存器，放好参数，然后 jal。":
        "Finally, Episode 7's six steps once more. Steps 1 and 2 belong to the caller: "
        "save any t and a registers it still needs, set up the arguments, then jal.",
    "第 3 步序言：sp 只减一次，局部数组一并分配；存下要用的 s 寄存器，要调用别人就存 ra。":
        "Step 3, the prologue: lower sp once, making room for local arrays too; "
        "save the s registers it uses, and ra if it calls others.",
    "第 4 步是函数体；第 5、6 步是尾声：返回值放进 a0，恢复寄存器、弹栈帧，jr ra。":
        "Step 4 is the body. Steps 5 and 6 are the epilogue: return value in a0, "
        "restore registers, pop the frame, jr ra.",
    "桌子": "Table",
    "寄存器": "Registers",
    "壁橱": "Closet",
    "内存": "Memory",
    "父母": "Parents",
    "你": "You",
    "父母备在桌上的东西": "Essentials left out",
    "你留下的礼物": "Your gift",
    "返回值": "Return value",
    "笔记的比喻：调用函数就像替父母看家。父母是调用者，你是被调用者；桌子是寄存器，壁橱是内存。":
        "The notes' analogy: a call is like house-sitting for your parents. They're the "
        "caller, you're the callee; the table is the registers, the closet is memory.",
    "父母备在桌上的是参数。桌上别的东西，先收进壁橱（序言）；走前原样摆回，再留一份礼物：返回值（尾声）。":
        "The arguments are the essentials on the table. Stash the rest in the closet "
        "(prologue); before leaving, put it back and leave a gift: the return value (epilogue).",
}
