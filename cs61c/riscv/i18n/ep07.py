"""English for episode 7 (keys are the Chinese strings in ep07_procedures.py)."""

EN = {
    # ---- end card
    "参数放在 a0–a7，返回值放在 a0（和 a1）":
        "Arguments go in a0–a7; the return value in a0 (and a1)",
    "jal 把返回地址存进 ra 再跳转；jr ra 返回":
        "jal saves the return address in ra, then jumps; jr ra returns",
    "t、a、ra 由调用者保存；s、sp 由被调用者保存":
        "t, a and ra are caller-saved; s and sp are callee-saved",
    "栈向低地址增长：减 sp 压栈，加 sp 出栈":
        "The stack grows down: subtract from sp to push, add to pop",
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
    "调用一个函数，要经过六个基本步骤。":
        "Calling a function takes six basic steps.",
    "先把参数放到函数拿得到的地方，然后跳过去……":
        "First, put the arguments where the function can find them, then jump there…",
    "……函数给自己准备局部存储，执行函数体……":
        "…the function sets up its own local storage and runs its body…",
    "……把返回值放好，最后跳回调用它的地方。":
        "…puts the return value in place, and finally jumps back to where it was called.",

    # ---- jal / jr
    "jal  ra, sum    # 调用": "jal  ra, sum    # call",
    "mv   s0, a0     # a = 返回值": "mv   s0, a0     # a = result",
    "看一个最简单的例子：a = sum(a, b)。a 在 s0，b 在 s1。":
        "Here's the simplest example: a = sum(a, b), with a in s0 and b in s1.",
    "第一步：把参数放进 a0、a1。返回值将来也通过 a0 带回来。":
        "Step one: put the arguments in a0 and a1. The return value will come back in a0, too.",
    "jal 是 jump and link：先把下一条指令的地址 PC + 4 存进 ra，再跳到 sum。":
        "jal means jump and link: it saves the address of the next instruction, PC + 4, "
        "in ra, then jumps to sum.",
    "函数把结果算好放进 a0……":
        "The function computes its result into a0…",
    "……然后 jr ra：跳回 ra 记下的地址 0x100C，接着往下执行。":
        "…then jr ra jumps back to the address saved in ra, 0x100C, and execution carries on.",
    "为什么不用 j 跳回去？因为 sum 可能在很多地方被调用，只有 ra 知道这一次该回到哪里。":
        "Why not just j back? Because sum may be called from many places; only ra knows "
        "where to return this time.",
    "jr ra 是 jalr x0, 0(ra) 的简写，也常写成 ret。":
        "jr ra is shorthand for jalr x0, 0(ra), and is often written as ret.",

    # ---- calling convention
    "调用者": "Caller",
    "被调用的函数 f": "Callee f",
    "重要数据，调用后还要用": "important data, needed after the call",
    "麻烦来了：寄存器只有一套，调用者和被调用的函数共用它们。":
        "Here's the catch: there's only one set of registers, shared by the caller and the callee.",
    "可 f 也要用寄存器。如果它改写了调用者还要用的值，数据就被悄悄破坏了。":
        "But f needs registers too. If it overwrites a value the caller still needs, "
        "that data is silently clobbered.",
    "所以大家约定了一套规则，叫做调用约定（calling convention）。":
        "So everyone agrees on a set of rules, called the calling convention.",
    "调用者保存 caller-saved": "Caller-saved",
    "函数可以随意改写。\n调用者若之后还要用，要自己先存好。":
        "The callee may overwrite them.\nIf the caller needs them later,\nit saves them first.",
    "被调用者保存 callee-saved": "Callee-saved",
    "函数若要使用，必须先保存旧值，\n返回前原样恢复。":
        "A callee that uses one must save\nthe old value first and restore it\nbefore returning.",
    "t、a 寄存器和 ra 是“调用者保存”的：被调用的函数可以随便改。调用者如果之后还要用，得自己先存好。":
        "The t and a registers and ra are caller-saved: the callee may change them freely. "
        "If the caller needs them afterward, it must save them itself.",
    "s 寄存器和 sp 是“被调用者保存”的：函数要用，就得先存旧值，返回前原样恢复。":
        "The s registers and sp are callee-saved: a function that uses one must save the old "
        "value first and restore it before returning.",
    "换句话说：跨过一次函数调用，s 寄存器的值保证不变；t、a 寄存器则不保证。":
        "In other words: across a function call, the s registers are guaranteed to keep "
        "their values; the t and a registers are not.",
    "那么，这些旧值要存到哪里？答案是内存里的“栈”。":
        "So where do these old values go? Into a region of memory called the stack.",

    # ---- the stack
    "栈 Stack": "Stack",
    "堆 Heap": "Heap",
    "静态数据 Static": "Static data",
    "代码 Text": "Code (text)",
    "高地址": "high addresses",
    "低地址": "low addresses",
    "一个程序的内存大致分成几块：代码、静态数据、堆，以及位于高地址的栈。":
        "A program's memory is split into a few regions: code, static data, the heap, "
        "and, up at the high addresses, the stack.",
    "栈从高地址往低地址“向下”生长。sp（栈指针）指向栈顶，也就是当前用到的最低地址。":
        "The stack grows down, from high addresses toward low ones. sp, the stack pointer, "
        "points to the top of the stack: the lowest address in use.",
    "调用者的数据": "caller's data",
    "addi sp, sp, -8   # 腾出 2 个字": "addi sp, sp, -8   # alloc 2 words",
    "放大来看。假设函数要保存 ra 和 s0 两个寄存器。":
        "Let's zoom in. Suppose a function needs to save two registers, ra and s0.",
    "压栈：先把 sp 减 8，腾出两个字的空间……":
        "To push, first subtract 8 from sp to make room for two words…",
    "……再用 sw 把寄存器存进去：ra 放在 sp + 4，s0 放在 sp + 0。":
        "…then store the registers with sw: ra at sp + 4, s0 at sp + 0.",
    "函数现在可以放心地改 ra 和 s0 了。":
        "Now the function is free to change ra and s0.",
    "addi sp, sp, 8    # 归还空间": "addi sp, sp, 8    # free 2 words",
    "返回之前出栈，顺序正好反过来：用 lw 取回旧值，再把 sp 加回去。":
        "Before returning, pop in reverse order: lw brings back the old values, "
        "then sp is moved back up.",
    "sp 回到原处，寄存器恢复原值。存过的数据不用清除，它们只是不再属于任何人。":
        "sp is back where it started, and the registers hold their old values. The saved data "
        "isn't erased; it just no longer belongs to anyone.",

    # ---- sumSquare
    "最后看一个完整的例子：sumSquare 会调用另一个函数 mult。":
        "Finally, a complete example: sumSquare calls another function, mult.",
    "    addi sp, sp, -8    # 腾出空间": "    addi sp, sp, -8    # make room",
    "    sw   ra, 4(sp)     # 保存 ra": "    sw   ra, 4(sp)     # save ra",
    "    sw   a1, 0(sp)     # 保存 y": "    sw   a1, 0(sp)     # save y",
    "    jal  ra, mult      # ra 被覆盖！": "    jal  ra, mult      # clobbers ra",
    "    lw   a1, 0(sp)     # 恢复 y": "    lw   a1, 0(sp)     # restore y",
    "    lw   ra, 4(sp)     # 恢复 ra": "    lw   ra, 4(sp)     # restore ra",
    "x = 3，y = 5": "x = 3, y = 5",
    "调用时 x = 3 在 a0，y = 5 在 a1，ra 里是调用者的返回地址。":
        "On entry, x = 3 is in a0, y = 5 is in a1, and ra holds the caller's return address.",
    "sumSquare 自己也要 jal 调用 mult，而 jal 会覆盖 ra。不先保存 ra，就再也回不到调用者了。":
        "sumSquare itself calls mult with jal, and jal overwrites ra. Without saving ra first, "
        "it could never get back to its caller.",
    "y 也得存到栈上：a1 马上要用来传 x，而且 a 寄存器由调用者保存，mult 也可能改掉它。":
        "y must go on the stack too: a1 is about to carry x, and since the a registers are "
        "caller-saved, mult may change a1 as well.",
    "先是序言（prologue）：腾出两个字，存好 ra 和 y。":
        "First comes the prologue: make room for two words, then save ra and y.",
    "准备参数 mult(3, 3)，然后 jal：ra 被改成 jal 下一条指令的地址，这里是 0x2014。":
        "Set up the arguments for mult(3, 3), then jal: ra now holds the address of the "
        "instruction after the jal, here 0x2014.",
    "mult：a0 = 3 × 3 = 9": "mult: a0 = 3 × 3 = 9",
    "mult 返回后，a1 里是什么已经说不准了——幸好 y 存在栈上。":
        "After mult returns, there's no telling what's in a1. Luckily, y is safe on the stack.",
    "算出 9 + 5 = 14。然后是尾声（epilogue）：恢复 ra，sp 加回 8，最后 jr ra 回到调用者。":
        "That gives 9 + 5 = 14. Then the epilogue: restore ra, add 8 back to sp, "
        "and jr ra returns to the caller.",
    "序言": "prologue",
    "尾声": "epilogue",
    "序言保存现场，尾声恢复现场。几乎每个会调用其他函数的函数，都是这个结构。":
        "The prologue saves the state; the epilogue restores it. Almost every function that "
        "calls another has this shape.",
}
