"""English for episode 7 (keys are the Chinese strings in ep07_procedures.py)."""

EN = {
    # ---- end card
    "参数放在 a0–a7，返回值放在 a0（和 a1）":
        "Arguments go in a0 through a7, and the return value goes in a0 and a1",
    "jal 把返回地址存进 ra 再跳转；jr ra 返回":
        "The jal instruction saves the return address in ra and then jumps, and jr ra returns",
    "t、a、ra 由调用者保存；s、sp 由被调用者保存":
        "The caller saves the temporary registers, the argument registers, and ra, while the "
        "callee saves s0 through s11, and sp",
    "栈向低地址增长：减 sp 压栈，加 sp 出栈":
        "The stack grows downward, so we subtract from sp to push, and add to sp to pop",
    "会调用别的函数的函数，必须先保存 ra":
        "A function that calls another must save ra first",

    # ---- six steps
    "调用一个函数，要做哪些事？": "What Does a Function Call Take?",
    "把参数放到函数拿得到的地方": "Put the arguments where the function can reach them",
    "跳转到函数": "Jump to the function",
    "为函数准备局部存储": "Set up local storage for the function",
    "栈": "stack",
    "执行函数体": "Run the function body",
    "把返回值放到调用者拿得到的地方": "Put the return value where the caller can reach it",
    "跳回调用的位置": "Jump back to where it was called",

    # ---- jal / jr
    "jal  ra, sum    # 调用": "jal  ra, sum    # call",
    "mv   s0, a0     # a = 返回值": "mv   s0, a0     # a = result",

    # ---- calling convention
    "调用者": "Caller",
    "被调用的函数 f": "Callee f",
    "重要数据，调用后还要用": "important data, needed after the call",
    "调用者保存 caller-saved": "Caller-saved",
    "函数可以随意改写。\n调用者若之后还要用，要自己先存好。":
        "The callee may overwrite them.\nIf the caller needs them later,\nit saves them first.",
    "被调用者保存 callee-saved": "Callee-saved",
    "函数若要使用，必须先保存旧值，\n返回前原样恢复。":
        "A callee that uses one must save\nthe old value first and restore it\nbefore returning.",

    # ---- the stack
    "栈 Stack": "Stack",
    "堆 Heap": "Heap",
    "静态数据 Static": "Static data",
    "代码 Text": "Code (text)",
    "高地址": "high addresses",
    "低地址": "low addresses",
    "调用者的数据": "caller's data",
    "addi sp, sp, -8   # 腾出 2 个字": "addi sp, sp, -8   # alloc 2 words",
    "addi sp, sp, 8    # 归还空间": "addi sp, sp, 8    # free 2 words",

    # ---- sumSquare
    "    addi sp, sp, -8    # 腾出空间": "    addi sp, sp, -8    # make room",
    "    sw   ra, 4(sp)     # 保存 ra": "    sw   ra, 4(sp)     # save ra",
    "    sw   a1, 0(sp)     # 保存 y": "    sw   a1, 0(sp)     # save y",
    "    jal  ra, mult      # ra 被覆盖！": "    jal  ra, mult      # clobbers ra",
    "    lw   a1, 0(sp)     # 恢复 y": "    lw   a1, 0(sp)     # restore y",
    "    lw   ra, 4(sp)     # 恢复 ra": "    lw   ra, 4(sp)     # restore ra",
    "x = 3，y = 5": "x = 3, y = 5",
    "mult：a0 = 3 × 3 = 9": "mult: a0 = 3 × 3 = 9",
    "序言": "prologue",
    "尾声": "epilogue",

    # ---- spoken beats and cue phrases (see references/narration-writing.md)
    "调用一个函数，要经过六个基本步骤。先把参数放到函数拿得到的地方，然后跳过去，函数给自己准备局部存储，执行函数体，把返回值放好，最后跳回调用它的地方。":
        "Calling a function takes six basic steps. First we put the arguments where the "
        "function can get them, and then jump over to it. The function sets up local storage "
        "for itself and runs its body. Then it puts the return value in place, and finally "
        "jumps back to where it was called from.",
    "先把参数放到函数拿得到的地方": "First we put the arguments",
    "函数给自己准备局部存储": "The function sets up local storage",
    "把返回值放好": "Then it puts the return value",
    "看一个最简单的例子：a = sum(a, b)。a 在 s0，b 在 s1。第一步：把参数放进 a0、a1。返回值将来也通过 a0 带回来。":
        "Let's look at the simplest example, a is set to sum of a and b, where a is in s0 and "
        "b is in s1. In step one we put the arguments into a0 and a1, and the return value "
        "will come back through a0 too.",
    "把参数放进": "In step one we put",
    "、a1": "and a1",
    "返回值将来也通过": "and the return value",
    "jal 是 jump and link：先把下一条指令的地址 PC + 4 存进 ra，再跳到 sum。":
        "The jal instruction first stores the address of the next instruction, PC plus four, "
        "into ra, and then jumps to sum, which is why it is called jump and link.",
    "先把下一条指令的地址": "first stores",
    "再跳到 sum": "and then jumps to sum",
    "函数把结果算好放进 a0，然后 jr ra：跳回 ra 记下的地址 0x100C，接着往下执行。":
        "The function computes its result and puts it into a0. Then jr ra jumps back to the "
        "address that ra remembers, 0x100C, and execution carries on from there.",
    "然后 jr ra": "Then jr ra jumps back",
    "放进 a0": "puts it into a0",
    "跳回 ra 记下的地址": "to the address that ra",
    "接着往下执行": "and execution carries on",
    "为什么不用 j 跳回去？因为 sum 可能在很多地方被调用，只有 ra 知道这一次该回到哪里。jr ra 是 jalr x0, 0(ra) 的简写，也常写成 ret。":
        "Why not jump back with a plain j? Because sum can be called from many places, and "
        "only ra knows where this particular call should return to. The instruction jr ra is "
        "shorthand for jalr x0, 0(ra), and it is often written ret.",
    "jr ra 是 jalr": "The instruction jr ra",
    "麻烦来了：寄存器只有一套，调用者和被调用的函数共用它们。可 f 也要用寄存器。如果它改写了调用者还要用的值，数据就被悄悄破坏了。所以大家约定了一套规则，叫做调用约定（calling convention）。":
        "Here is the trouble. There is only one set of registers, and the caller and the "
        "function being called share them. But f needs registers too, and if it overwrites a "
        "value the caller still needs, that data is quietly destroyed. So everyone agreed on "
        "a set of rules, called the calling convention.",
    "可 f 也要用寄存器": "But f needs registers too",
    "调用者和被调用的函数共用": "the caller and the function",
    "如果它改写了": "and if it overwrites",
    "数据就被悄悄破坏了": "that data is quietly destroyed",
    "t、a 寄存器和 ra 是“调用者保存”的：被调用的函数可以随便改。调用者如果之后还要用，得自己先存好。s 寄存器和 sp 是“被调用者保存”的：函数要用，就得先存旧值，返回前原样恢复。":
        "The registers t0 through t6 and a0 through a7, along with ra, are caller-saved, "
        "which means the function being called may change them freely. The caller has to save "
        "them first if it needs them afterwards. The registers s0 through s11, and sp, are "
        "callee-saved, so if a function wants to use them, it must save the old values first "
        "and restore them exactly before returning.",
    "s 寄存器和 sp": "The registers s0 through s11",
    "换句话说：跨过一次函数调用，s 寄存器的值保证不变；t、a 寄存器则不保证。那么，这些旧值要存到哪里？答案是内存里的“栈”。":
        "In other words, across a function call the saved registers are guaranteed to be "
        "unchanged, while the temporary and argument registers are not. So where do we keep "
        "those old values? The answer is the stack in memory.",
    "一个程序的内存大致分成几块：代码、静态数据、堆，以及位于高地址的栈。栈从高地址往低地址“向下”生长。sp（栈指针）指向栈顶，也就是当前用到的最低地址。":
        "A program's memory is roughly divided into blocks, which are the code, the static "
        "data, the heap, and, at high addresses, the stack. The stack grows downward from "
        "high addresses toward low ones, and sp, the stack pointer, points to the top of the "
        "stack, which is the lowest address currently in use.",
    "栈从高地址往低地址“向下”生长": "The stack grows downward",
    "放大来看。假设函数要保存 ra 和 s0 两个寄存器。":
        "Let's zoom in. Suppose a function needs to save two registers, ra and s0.",
    "压栈：先把 sp 减 8，腾出两个字的空间，再用 sw 把寄存器存进去：ra 放在 sp + 4，s0 放在 sp + 0。":
        "To push, we first subtract eight from sp, making room for two words. Then we use sw "
        "to store the registers, with ra at sp plus four, and s0 at sp plus zero.",
    "再用 sw 把寄存器存进去": "Then we use sw",
    "先把 sp 减 8": "we first subtract eight",
    "ra 放在 sp + 4": "with ra at sp plus four",
    "s0 放在 sp + 0": "and s0 at sp plus zero",
    "函数现在可以放心地改 ra 和 s0 了。返回之前出栈，顺序正好反过来：用 lw 取回旧值，再把 sp 加回去。":
        "The function can now change ra and s0 freely. Before returning, we pop in exactly "
        "the opposite order, using lw to get the old values back, and then adding to sp to "
        "give the space back.",
    "返回之前出栈": "Before returning",
    "用 lw 取回旧值": "using lw to get the old values",
    "再把 sp 加回去": "and then adding to sp",
    "sp 回到原处，寄存器恢复原值。存过的数据不用清除，它们只是不再属于任何人。":
        "Now sp is back where it started, and the registers have their old values. The data "
        "we stored doesn't need clearing, since it just no longer belongs to anyone.",
    "最后看一个完整的例子：sumSquare 会调用另一个函数 mult。":
        "Finally, a complete example, in which sumSquare calls another function, mult.",
    "调用时 x = 3 在 a0，y = 5 在 a1，ra 里是调用者的返回地址。sumSquare 自己也要 jal 调用 mult，而 jal 会覆盖 ra。不先保存 ra，就再也回不到调用者了。y 也得存到栈上：a1 马上要用来传 x，而且 a 寄存器由调用者保存，mult 也可能改掉它。":
        "When it is called, the argument x, which is three, is in a0, the argument y, which "
        "is five, is in a1, and ra holds the caller's return address. Since sumSquare itself "
        "calls mult with jal, and jal overwrites ra, it has to save ra first, or it could "
        "never get back to its caller. It must also save y on the stack, because a1 is about "
        "to be used to pass x, and a1 is caller-saved, so mult might change it.",
    "sumSquare 自己也要": "Since sumSquare itself calls mult",
    "y 也得存到栈上": "It must also save y",
    "先是序言（prologue）：腾出两个字，存好 ra 和 y。":
        "First comes the prologue, which makes room for two words and saves ra and y.",
    "腾出两个字": "makes room for two words",
    "存好 ra": "and saves ra",
    "和 y": "and y",
    "准备参数 mult(3, 3)，然后 jal：ra 被改成 jal 下一条指令的地址，这里是 0x2014。mult 返回后，a1 里是什么已经说不准了——幸好 y 存在栈上。":
        "Next we set up the arguments for mult of three and three, and then jal changes ra to "
        "the address of the instruction after the jal, which here is 0x2014. When mult "
        "returns, we can't be sure what is in a1 any more, but luckily y is saved on the "
        "stack.",
    "mult 返回后": "When mult returns",
    "准备参数": "Next we set up the arguments",
    "算出 9 + 5 = 14。然后是尾声（epilogue）：恢复 ra，sp 加回 8，最后 jr ra 回到调用者。序言保存现场，尾声恢复现场。几乎每个会调用其他函数的函数，都是这个结构。":
        "Now we work out nine plus five, which is fourteen. Then comes the epilogue, which "
        "restores ra, adds eight back to sp, and finally uses jr ra to return to the caller. "
        "The prologue saves the state and the epilogue restores it, and almost every function "
        "that calls other functions has this structure.",
    "序言保存现场": "The prologue saves the state",
    "然后 jal": "and then jal changes ra",
    "恢复 ra": "which restores ra",
    "sp 加回 8": "adds eight back to sp",
    "最后 jr ra": "and finally uses jr ra",
}
