"""English for episode 5 (keys are the Chinese strings in ep05_branches_loops.py)."""

EN = {
    # ---- end card
    "PC 指向当前指令；顺序执行时每次加 4":
        "The PC points to the current instruction, and steps by four as the program runs in "
        "order",
    "条件分支：beq bne blt bge bltu bgeu":
        "There are six conditional branches, which are beq, bne, blt, bge, bltu, and bgeu",
    "if-else：条件取反，再用 j 跳过 else":
        "For an if-else, negate the condition, and then use j to jump over the else part",
    "位运算：and or xor，移位 sll srl sra":
        "The bitwise instructions are and, or, and xor, and the shifts are sll, srl, and sra",
    "循环：开头判断并跳出，末尾跳回开头":
        "A loop tests and exits at the top, and jumps back at the end",

    # ---- program counter

    # ---- branches
    "条件分支": "Conditional Branches",
    "如果 rs1 == rs2，跳到 Label；否则执行下一条":
        "If rs1 == rs2, jump to Label; otherwise run the next instruction",
    "< 无符号": "< unsigned",
    ">= 无符号": ">= unsigned",
    "Label  =  某条指令的地址": "Label  =  the address of an instruction",

    # ---- if / else
    "    bne s3, s4, Else  # i != j 就跳":
        "    bne s3, s4, Else  # jump if i != j",

    # ---- bitwise ops & shifts
    "位运算与移位": "Bitwise Operations & Shifts",
    "（只画出最低 8 位）": "(only the lowest 8 bits shown)",
    "andi t0, t1, 0xFF    # 取出最低字节":
        "andi t0, t1, 0xFF    # keep the low byte",
    "xori t0, t1, -1      # 按位取反 (not)":
        "xori t0, t1, -1      # flip every bit (not)",
    "（示意：假设寄存器只有 8 位）": "(pretend the register is only 8 bits wide)",
    "左边补 0：不再是负数": "0s fill in: no longer negative",
    "左边补符号位：−16 ÷ 4 = −4": "sign bit fills in: −16 ÷ 4 = −4",

    # ---- loop
    "    bge  t0, a1, Done   # i >= n 就结束":
        "    bge  t0, a1, Done   # i >= n: exit",
    "A 的地址": "address of A",

    # ---- spoken beats and cue phrases (see references/narration-writing.md)
    "程序就是内存里的一串指令。CPU 用一个特殊的寄存器——程序计数器（PC）——记住当前指令的地址。":
        "A program is just a series of instructions in memory. The CPU remembers the address "
        "of the current instruction in a special register, the program counter, or PC.",
    "记住当前指令的地址": "remembers the address",
    "每条指令占 4 个字节。执行完一条，PC 就加 4，指向下一条。可如果只能一条接一条地执行，就写不出 if，也写不出循环。我们需要能“跳”的指令。":
        "Every instruction takes four bytes, so after finishing one, the PC adds four and "
        "points to the next. But if we could only run instructions one after another, we "
        "couldn't write an if or a loop. We need instructions that can jump.",
    "条件分支 beq（branch if equal）：如果 rs1 等于 rs2，就跳到 Label；否则照常执行下一条。":
        "The conditional branch beq, which stands for branch if equal, jumps to the label if "
        "rs1 equals rs2, and otherwise carries on with the next instruction.",
    "如果 rs1 等于 rs2": "jumps to the label if",
    "RISC-V 一共 6 条条件分支：相等、不等、小于、大于等于，以及小于和大于等于的无符号版本。没有 bgt 和 ble？交换两个操作数就行：a > b 就是 b < a。汇编器也提供了这类伪指令。":
        "RISC-V has six conditional branches, which are equal, not equal, less than, greater "
        "than or equal, and the unsigned versions of less than and greater than or equal. "
        "There is no bgt instruction and no ble instruction, because we can simply swap the "
        "operands, since a is greater than b exactly when b is less than a. The assembler "
        "also offers pseudo-instructions for these.",
    "没有 bgt 和 ble": "There is no bgt instruction",
    "还有无条件跳转 j Label：直接跳过去。它是 jal x0, Label 的简写，第 7 集会讲 jal。Label 只是给代码中某个位置起的名字，汇编器会把它换算成地址。":
        "There is also an unconditional jump, j Label, which jumps straight there. It is "
        "shorthand for jal x0, Label, and we'll meet jal in episode seven. A label is just a "
        "name for a position in the code, and the assembler converts it into an address.",
    "Label 只是给代码中某个位置起的名字": "A label is just a name",
    "来翻译一个 if-else。f、g、h、i、j 分别放在 s0 到 s4。":
        "Let's translate an if-else. The variables f, g, h, i, and j live in s0 through s4.",
    "关键技巧是“条件取反”：C 里 i == j 时执行 then 部分，所以汇编里反过来用 bne——不相等就跳过它，直接去 Else。":
        "The key trick is inverting the condition. In C the then part runs when i equals j. "
        "So in assembly we turn it around and use bne, which skips the then part when the "
        "values are not equal and goes straight to Else.",
    "所以汇编里反过来用 bne": "So in assembly we turn it around",
    "情况一：i 等于 j。bne 不跳，执行 add，然后 j Exit 跳过 else 部分。":
        "Case one is when i equals j. The bne doesn't jump, so we execute the add, and then j "
        "Exit jumps over the else part.",
    "然后 j Exit": "and then j Exit",
    "bne 不跳": "The bne doesn't jump",
    "执行 add": "so we execute the add",
    "情况二：i 不等于 j。bne 直接跳到 Else，执行 sub，然后自然走到 Exit。注意 j Exit 不能省：否则执行完 then 部分，程序会一路“掉进” else 部分。":
        "Case two is when i does not equal j. The bne jumps straight to Else, we execute the "
        "sub, and then we naturally arrive at Exit. Notice that the j Exit can't be left out, "
        "because otherwise the program would fall right through into the else part after the "
        "then part.",
    "注意 j Exit 不能省": "Notice that the j Exit",
    "bne 直接跳到 Else": "The bne jumps straight to Else",
    "执行 sub": "we execute the sub",
    "自然走到 Exit": "naturally arrive at Exit",
    "在写循环之前，先认识几条位运算指令。它们对 32 位数据逐位操作。":
        "Before writing loops, let's meet a few bitwise instructions, which work on thirty-two bit data one bit at a time.",
    "and：两位都是 1，结果才是 1。它常用来做“掩码”：只保留想要的那些位。or：只要有一位是 1，结果就是 1，xor：两位不同，结果才是 1。":
        "The and instruction gives a one only when both bits are one, and it is often used as "
        "a mask, keeping just the bits we want. The or instruction gives a one when either "
        "bit is one, and the xor instruction gives a one only when the two bits differ.",
    "or：只要有一位是 1": "The or instruction",
    "xor：两位不同": "and the xor instruction",
    "它们都有立即数版本：andi、ori、xori。比如 andi t0, t1, 0xFF 取出最低的一个字节。RISC-V 没有真正的 not 指令：-1 的每一位都是 1，与它异或就是按位取反。伪指令 not 就是这么实现的。":
        "They all come in immediate versions, andi, ori, and xori, so andi t0, t1, 0xFF "
        "extracts the lowest byte. RISC-V has no real not instruction. Minus one has every "
        "bit set, so xor with it flips every bit, which is how the not pseudo-instruction "
        "works.",
    "RISC-V 没有真正的 not 指令": "RISC-V has no real not",
    "移位指令把所有位整体挪动。sll 是逻辑左移：往左挪，右边补 0。左移 k 位，相当于乘以 2 的 k 次方：22 左移 2 位，变成 88。":
        "The shift instructions move all the bits over together. The sll instruction is a "
        "logical left shift, which moves the bits to the left and fills in zeros on the "
        "right. Shifting left by k bits is the same as multiplying by two to the k, so "
        "twenty-two shifted left by two becomes eighty-eight.",
    "左移 k 位": "Shifting left by k bits",
    "sll 是逻辑左移": "The sll instruction",
    "往左挪": "moves the bits to the left",
    "右边补 0": "fills in zeros",
    "右移有两种。srl 是逻辑右移：左边补 0。sra 是算术右移：左边补符号位。这样负数除以 2 的幂之后，依然是负数。":
        "There are two kinds of right shift. The srl instruction is a logical right shift, "
        "which fills zeros on the left. The sra instruction is an arithmetic right shift, "
        "which fills in copies of the sign bit, so a negative number stays negative after "
        "division by powers of two.",
    "sra 是算术右移": "The sra instruction",
    "左边补 0": "which fills zeros",
    "这样负数除以 2 的幂": "so a negative number",
    "现在把这些组合起来：对数组 A 的 n 个元素求和。A 的地址在 a0，n 在 a1；i 用 t0，sum 用 s1。":
        "Now let's put all this together, to add up the n elements of an array A. The address "
        "of A is in a0 and n is in a1, while i uses t0 and sum uses s1.",
    "A 的地址在 a0": "The address of A",
    "循环的骨架：开头检查条件，不满足就跳出；循环体末尾，无条件跳回开头。条件又取反了：C 里 i < n 时继续，汇编里 i >= n 时跳出。":
        "Here is the skeleton of the loop. At the start we check the condition and jump out "
        "if it fails, and at the end of the body we jump back to the beginning "
        "unconditionally. The condition is inverted again, since the C loop continues while i "
        "is less than n, but the assembly jumps out when i is greater than or equal to n.",
    "条件又取反了": "The condition is inverted again",
    "A[i] 的地址是 A + 4i：用 slli 左移 2 位算出 4i，再加上基地址。":
        "The address of A[i] is A plus four times i, so we use slli to shift i left by two "
        "bits to get four i, and then add the base address.",
    "第一轮：i = 0。bge 不成立，算出地址 0x100，读到 A[0] = 3，sum 变成 3。":
        "In the first round, i is zero. The bge doesn't branch, we compute the address 0x100, "
        "we load A[0], which is three, and sum becomes three.",
    "之后每一轮都一样：算出 A + 4i，取出 A[i] 累加进 sum，再让 i 加 1，当 i 增加到 4，bge 条件成立，跳到 Done。sum = 3 + 1 + 4 + 1 = 9。":
        "Every round after that is the same. We compute A plus four i, load A[i] and add it "
        "into sum, and then increase i by one. When i reaches four, the bge condition holds "
        "and we jump to Done, with sum equal to three plus one plus four plus one, which is "
        "nine.",
    "当 i 增加到 4": "When i reaches four",
}
