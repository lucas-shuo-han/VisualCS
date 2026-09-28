"""English for episode 5 (keys are the Chinese strings in ep05_branches_loops.py)."""

EN = {
    # ---- end card
    "PC 指向当前指令；顺序执行时每次加 4":
        "PC points to the current instruction; it steps by 4",
    "条件分支：beq bne blt bge bltu bgeu":
        "Conditional branches: beq bne blt bge bltu bgeu",
    "if-else：条件取反，再用 j 跳过 else":
        "if-else: negate the condition, then j over the else",
    "位运算：and or xor，移位 sll srl sra":
        "Bitwise: and or xor; shifts: sll srl sra",
    "循环：开头判断并跳出，末尾跳回开头":
        "Loops: test and exit at the top, jump back at the end",

    # ---- program counter
    "程序就是内存里的一串指令。CPU 用一个特殊的寄存器——程序计数器（PC）——记住当前指令的地址。":
        "A program is a sequence of instructions in memory. A special register, the program "
        "counter (PC), holds the address of the current instruction.",
    "每条指令占 4 个字节。执行完一条，PC 就加 4，指向下一条。":
        "Each instruction is 4 bytes long. After each one, the PC goes up by 4 to point at the next.",
    "可如果只能一条接一条地执行，就写不出 if，也写不出循环。我们需要能“跳”的指令。":
        "But if we could only run one instruction after another, we could never write an if "
        "or a loop. We need instructions that jump.",

    # ---- branches
    "条件分支": "Conditional Branches",
    "如果 rs1 == rs2，跳到 Label；否则执行下一条":
        "If rs1 == rs2, jump to Label; otherwise run the next instruction",
    "条件分支 beq（branch if equal）：如果 rs1 等于 rs2，就跳到 Label；否则照常执行下一条。":
        "The conditional branch beq (branch if equal): if rs1 equals rs2, jump to Label; "
        "otherwise carry on with the next instruction.",
    "< 无符号": "< unsigned",
    ">= 无符号": ">= unsigned",
    "RISC-V 一共 6 条条件分支：相等、不等、小于、大于等于，以及小于和大于等于的无符号版本。":
        "RISC-V has six conditional branches: equal, not equal, less than, greater or equal, "
        "plus unsigned versions of the last two.",
    "没有 bgt 和 ble？交换两个操作数就行：a > b 就是 b < a。汇编器也提供了这类伪指令。":
        "No bgt or ble? Swap the operands, since a > b means b < a. "
        "The assembler also provides them as pseudo-instructions.",
    "还有无条件跳转 j Label：直接跳过去。它是 jal x0, Label 的简写，第 7 集会讲 jal。":
        "There's also an unconditional jump, j Label: it always jumps. It's shorthand for "
        "jal x0, Label; Episode 7 covers jal.",
    "Label  =  某条指令的地址": "Label  =  the address of an instruction",
    "Label 只是给代码中某个位置起的名字，汇编器会把它换算成地址。":
        "A label is just a name for a place in the code; the assembler converts it into an address.",

    # ---- if / else
    "来翻译一个 if-else。f、g、h、i、j 分别放在 s0 到 s4。":
        "Let's translate an if-else. The variables f, g, h, i, j live in s0 through s4.",
    "    bne s3, s4, Else  # i != j 就跳":
        "    bne s3, s4, Else  # jump if i != j",
    "关键技巧是“条件取反”：C 里 i == j 时执行 then 部分，所以汇编里反过来用 bne——不相等就跳过它，直接去 Else。":
        "The key trick: negate the condition. C runs the then-part when i == j, so the assembly "
        "uses bne instead, skipping straight to Else when they differ.",
    "情况一：i 等于 j。bne 不跳，执行 add……":
        "Case 1: i equals j. bne doesn't branch, so we run the add…",
    "……然后 j Exit 跳过 else 部分。":
        "…then j Exit skips over the else part.",
    "情况二：i 不等于 j。bne 直接跳到 Else，执行 sub，然后自然走到 Exit。":
        "Case 2: i doesn't equal j. bne jumps straight to Else, runs the sub, "
        "and simply falls through to Exit.",
    "注意 j Exit 不能省：否则执行完 then 部分，程序会一路“掉进” else 部分。":
        "Don't leave out j Exit: without it, the program would finish the then-part "
        "and fall right through into the else part.",

    # ---- bitwise ops & shifts
    "位运算与移位": "Bitwise Operations & Shifts",
    "在写循环之前，先认识几条位运算指令。它们对 32 位数据逐位操作。":
        "Before writing loops, let's meet a few bitwise instructions. "
        "They work on 32-bit values bit by bit.",
    "（只画出最低 8 位）": "(only the lowest 8 bits shown)",
    "and：两位都是 1，结果才是 1。它常用来做“掩码”：只保留想要的那些位。":
        "and: a result bit is 1 only if both bits are 1. It's often used as a mask, "
        "keeping just the bits you want.",
    "or：只要有一位是 1，结果就是 1……":
        "or: the result is 1 if either bit is 1…",
    "……xor：两位不同，结果才是 1。":
        "…xor: the result is 1 only if the two bits differ.",
    "andi t0, t1, 0xFF    # 取出最低字节":
        "andi t0, t1, 0xFF    # keep the low byte",
    "xori t0, t1, -1      # 按位取反 (not)":
        "xori t0, t1, -1      # flip every bit (not)",
    "它们都有立即数版本：andi、ori、xori。比如 andi t0, t1, 0xFF 取出最低的一个字节。":
        "Each has an immediate version: andi, ori, xori. For example, andi t0, t1, 0xFF "
        "extracts the lowest byte.",
    "RISC-V 没有真正的 not 指令：-1 的每一位都是 1，与它异或就是按位取反。伪指令 not 就是这么实现的。":
        "There's no real not instruction: -1 is all 1s, so xor with -1 flips every bit. "
        "The not pseudo-instruction does just that.",
    "移位指令把所有位整体挪动。sll 是逻辑左移：往左挪，右边补 0。":
        "Shifts slide all the bits over together. sll is shift left logical: "
        "move left, filling the right with 0s.",
    "左移 k 位，相当于乘以 2 的 k 次方：22 左移 2 位，变成 88。":
        "Shifting left by k multiplies by 2^k: 22 shifted left by 2 becomes 88.",
    "（示意：假设寄存器只有 8 位）": "(pretend the register is only 8 bits wide)",
    "左边补 0：不再是负数": "0s fill in: no longer negative",
    "左边补符号位：−16 ÷ 4 = −4": "sign bit fills in: −16 ÷ 4 = −4",
    "右移有两种。srl 是逻辑右移：左边补 0。":
        "There are two right shifts. srl, shift right logical, fills the left with 0s.",
    "sra 是算术右移：左边补符号位。这样负数除以 2 的幂之后，依然是负数。":
        "sra, shift right arithmetic, fills the left with the sign bit, so a negative number "
        "divided by a power of 2 stays negative.",

    # ---- loop
    "现在把这些组合起来：对数组 A 的 n 个元素求和。":
        "Now let's put it all together: add up the n elements of an array A.",
    "    bge  t0, a1, Done   # i >= n 就结束":
        "    bge  t0, a1, Done   # i >= n: exit",
    "A 的地址": "address of A",
    "A 的地址在 a0，n 在 a1；i 用 t0，sum 用 s1。":
        "A's address is in a0 and n is in a1; i lives in t0 and sum in s1.",
    "循环的骨架：开头检查条件，不满足就跳出；循环体末尾，无条件跳回开头。":
        "The skeleton of a loop: at the top, test the condition and exit if it fails; "
        "at the end of the body, jump back to the top.",
    "条件又取反了：C 里 i < n 时继续，汇编里 i >= n 时跳出。":
        "Once again the condition is negated: C keeps going while i < n, "
        "so the assembly exits when i >= n.",
    "A[i] 的地址是 A + 4i：用 slli 左移 2 位算出 4i，再加上基地址。":
        "A[i] is at address A + 4i: slli by 2 computes 4i, then we add the base address.",
    "第一轮：i = 0。bge 不成立，算出地址 0x100，读到 A[0] = 3，sum 变成 3。":
        "First pass: i = 0. The bge isn't taken; we compute address 0x100, load A[0] = 3, "
        "and sum becomes 3.",
    "之后每一轮都一样：算出 A + 4i，取出 A[i] 累加进 sum，再让 i 加 1……":
        "Every pass after that is the same: compute A + 4i, load A[i] and add it to sum, "
        "then increment i…",
    "当 i 增加到 4，bge 条件成立，跳到 Done。sum = 3 + 1 + 4 + 1 = 9。":
        "When i reaches 4, the bge condition holds and we jump to Done. sum = 3 + 1 + 4 + 1 = 9.",
}
