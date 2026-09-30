"""English for episode 1 (keys are the Chinese strings in ep01_newton_schulz.py)."""

EN = {
    # recap
    "Newton–Schulz 只改变奇异值：每个 σ 各自迭代 p(x)":
        "Newton–Schulz only changes singular values: each σ iterates p(x) on its own",
    "不动点 −1、0、1：±1 稳定（斜率 0），0 不稳定（斜率 1.5）":
        "Fixed points −1, 0, 1: ±1 are stable (slope 0), 0 is unstable (slope 1.5)",
    "√3 决定翻不翻号，√5 决定变小还是变大":
        "√3 decides whether the sign flips; √5 decides shrinking vs. growing",
    "√3 到 √5 之间：翻号次数的奇偶决定去 −1 还是 +1":
        "Between √3 and √5, the parity of the flips decides −1 or +1",
    "分界点 bn 挤向 √5，自身落到 0；√5 周期为 2，更大的发散":
        "Boundaries bn pile up at √5 and fall to 0; √5 has period 2, beyond it diverges",
    "所以迭代前先缩放 W，让所有奇异值小于 √3":
        "So scale W first, to put every singular value below √3",

    # 1. the mystery
    "取一个数，反复把它代入同一个三次多项式。":
        "Take a number and plug it into the same cubic polynomial, again and again.",
    "从三个挨得很近的数出发：2.00、2.20 和 2.23。":
        "Start from three numbers that sit very close together: 2.00, 2.20 and 2.23.",
    "每迭代一步，它们都在正负之间来回跳……":
        "With every step they jump back and forth between positive and negative...",
    "最后，2.00 停在 −1，2.20 停在 +1，2.23 又回到了 −1。":
        "In the end, 2.00 settles at −1, 2.20 at +1, and 2.23 back at −1.",
    "起点只差一点点，终点却正负交替。为什么？这就是这支视频要解开的谜。":
        "Nearly identical starts, alternating ends. Why? That is the puzzle this video solves.",

    # 2. where p comes from
    "Newton–Schulz 迭代": "Newton–Schulz iteration",
    "Newton–Schulz 迭代来自 CS182 第五次讨论课：它反复改写一个矩阵 W，这个多项式就藏在里面。":
        "It comes from the Newton–Schulz iteration of CS182 Discussion 5, which keeps rewriting a matrix W.",
    "旋转": "rotate",
    "拉伸": "stretch",
    "把 W 做奇异值分解：U 和 V 只负责旋转，拉伸的大小全在中间的 Σ 里。":
        "Take the SVD of W: U and V only rotate, and all the stretching lives in Σ in the middle.",
    "代进去一算，U 和 V 原封不动地留在两边，p 只作用在中间的 Σ 上。":
        "Plug it in: U and V stay untouched on the outside, and p acts only on the Σ in the middle.",
    "Σ 是对角矩阵，所以每个奇异值各自独立地变成 p(σ)，互不干扰。":
        "Σ is diagonal, so each singular value independently becomes p(σ), without touching the others.",
    "正交矩阵": "orthogonal matrix",
    "如果所有奇异值都被推到 1，W 就只剩下 U 乘 V 的转置：一个正交矩阵。这就是“正交化”。":
        "If every singular value reaches 1, W becomes U times V transpose, an orthogonal matrix: \"orthogonalization\".",
    "所以可以先忘掉矩阵，只盯着一个数 x，看它在 p 的反复作用下去哪。":
        "So forget the matrix for now. Follow one number x, and watch where repeated p takes it.",
    "第 (e) 问正是：奇异值从正数 σ 出发，最后去 +1、−1、0，还是发散？":
        "Part (e) asks exactly this: starting from a positive σ, does it end at +1, −1, 0, or blow up?",

    # 3. graph and cobweb
    "画出 y = p(x)，再画出对角线 y = x。": "Draw y = p(x), and the diagonal y = x.",
    "1. 竖直走到曲线：得到 p(x)": "1. Go vertically to the curve: that's p(x)",
    "2. 水平走到对角线：把 p(x) 当作新的 x": "2. Go across to the diagonal: p(x) is the new x",
    "3. 重复": "3. Repeat",
    "这叫蛛网图。从起点竖直走到曲线，到达的高度就是下一个值 p(x)；":
        "This is a cobweb diagram. Go straight up to the curve: the height you reach is the next value, p(x);",
    "再水平走到对角线，把这个高度搬回横轴的位置，作为新的 x。":
        "then across to the diagonal, which moves that height back over to the x position, as the new x.",
    "讨论课的例子从 0.3 出发：重复这两步，台阶一级一级爬向 1。":
        "The discussion's example starts at 0.3: repeat the two moves and the staircase climbs toward 1.",
    "从 1.2 出发，先落到 1 的下方，然后同样贴上 1。":
        "From 1.2, it first drops just below 1, then hugs 1 as well.",

    # 4. fixed points and stability
    "曲线和对角线的交点满足 p(x) = x，叫作不动点：一旦落在上面，就永远不动。":
        "Where the curve meets the diagonal, p(x) = x. These are fixed points: land on one and you never move again.",
    "解这个方程，化简后是 x 的立方等于 x，所以不动点是 −1、0 和 1。":
        "Solving it reduces to x cubed equals x, so the fixed points are −1, 0 and 1.",
    "但不动点分两种：吸引的和排斥的。区别在于 p 在那里的斜率。":
        "But fixed points come in two kinds, attracting and repelling. The slope of p there tells them apart.",
    "在 0 处斜率是 1.5：偏差每步放大 1.5 倍。从 0.05 出发，很快就被推开。":
        "At 0 the slope is 1.5: any offset grows 1.5 times per step. Start at 0.05 and you get pushed away fast.",
    "在 ±1 处斜率是 0：偏差每一步差不多被平方。从 1.2 出发，误差是 0.2、0.064、0.006……":
        "At ±1 the slope is 0: the error roughly squares each step. From 1.2 it goes 0.2, 0.064, 0.006...",
    "不稳定": "unstable",
    "稳定": "stable",
    "所以 0 是不稳定的不动点，像山顶；±1 是稳定的，像谷底。":
        "So 0 is an unstable fixed point, like a hilltop, and ±1 are stable, like valley floors.",

    # 5. 0 < σ < √3
    "现在回答第 (e) 问。先把 p 分解：p(x) 等于 x 乘以 3 减 x 的平方，再除以 2。":
        "Now for part (e). First factor p: p(x) is x times 3 minus x squared, over 2.",
    "当 0 < x < √3 时，两个因子都是正的，所以 p(x) 也是正的：不会翻号。":
        "When 0 < x < √3, both factors are positive, so p(x) is positive too: the sign never flips.",
    "而且这一段上 p 最高只到 1，在 x = 1 处取到。所以一步之后，x 就落在 0 和 1 之间。":
        "And on this stretch p peaks at exactly 1, at x = 1. So after one step, x lies between 0 and 1.",
    "在 0 和 1 之间，p(x) − x = x(1 − x 的平方)/2 大于 0：每步都往上走，又越不过 1，只能收敛到 1。":
        "Between 0 and 1, p(x) − x is positive: each step goes up, never past 1, so x converges to 1.",
    "比如从 1.6 出发：先掉到 0.35，再一级级爬回 1。0 < σ < √3 全都去 +1。":
        "From 1.6, say: it drops to 0.35, then climbs back up to 1. Every 0 < σ < √3 goes to +1.",
    "恰好 σ = √3 时，p(√3) = 0：一步掉进 0，然后永远停在这个不稳定的不动点上。":
        "Exactly at σ = √3, p(√3) = 0: one step lands on 0, and it sits on that unstable fixed point forever.",

    # 6. √3 and √5
    "越过 √3，因子 3 − x 的平方变成负的：p(x) 和 x 异号。每迭代一次，符号就翻一次。":
        "Past √3, the factor 3 − x squared turns negative: p(x) and x have opposite signs. Each step flips the sign.",
    "那大小呢？比较 |p(x)| 和 |x|：两者的比值是 |3 − x 的平方| 除以 2。":
        "What about the size? Compare |p(x)| with |x|: their ratio is |3 − x squared| over 2.",
    "在 |x| > √3 时，这个比值小于 1，当且仅当 x 的平方小于 5，也就是 |x| < √5。":
        "For |x| > √3 this ratio is below 1 exactly when x squared is below 5, that is, when |x| < √5.",
    "同号": "same\nsign",
    "翻号\n变小": "flips\nshrinks",
    "翻号\n变大": "flips\ngrows",
    "于是有了第二个关键数 √5。√3 管会不会翻号，√5 管翻号的同时是变小还是变大。":
        "So √5 is the second key number: √3 decides whether the sign flips, √5 whether each flip shrinks or grows.",

    # 7. the edge at √5
    "先看边缘。p(√5) = −√5，p(−√5) = √5：蛛网变成一个正方形，永远绕下去。":
        "First the edge. p(√5) = −√5 and p(−√5) = √5: the cobweb becomes a square that loops forever.",
    "周期为 2 的轨道": "period-2 orbit",
    "所以 σ = √5 既不收敛也不发散：它在 ±√5 之间来回，是周期为 2 的轨道，不是不动点。":
        "So σ = √5 neither converges nor diverges. It bounces between ±√5: a period-2 orbit, not a fixed point.",
    "再大一点，比如 2.3：每步翻号，还越来越大：−2.63、5.18、−61.8……发散。":
        "A bit larger, like 2.3: the sign flips and the size grows, −2.63, 5.18, −61.8... it diverges.",

    # 8. between √3 and √5
    "讨论课解答：σ > √3 时，“要么收敛到 −1，要么发散”":
        "Discussion solution: for σ > √3,\n\"either converge to −1 or even diverge\"",
    "剩下的就是 √3 和 √5 之间。讨论课的解答说：这里要么收敛到 −1，要么发散。":
        "That leaves √3 to √5. The discussion solution says this part either converges to −1 or diverges.",
    "可开头的 2.2 明明去了 +1。这一段里到底发生了什么？":
        "But at the start, 2.2 clearly went to +1. So what really happens in here?",
    "翻号 0 次": "0 flips",
    "翻号 1 次": "1 flip",
    "翻号 2 次": "2 flips",
    "翻号 3 次": "3 flips",
    "正": "positive",
    "负": "negative",
    "这一段里每步都翻号，同时绝对值变小。我们只画绝对值，用颜色记正负，再数翻号的次数。":
        "In here each step flips the sign and shrinks the size. Plot the size, color the sign, count the flips.",
    "一步一步看：绝对值不断往左走，颜色正负交替。":
        "Step by step: the size keeps moving left, and the color alternates.",
    "2.00 翻一次号就跌到了 √3 以下；2.20 翻了两次，2.23 翻了三次。":
        "2.00 drops below √3 after one flip; 2.20 needs two flips, and 2.23 needs three.",
    "绝对值一直变小，却不可能永远停在 √3 右边：能让它停住的只有 √5。所以它迟早跌进 √3 以内。":
        "The size keeps shrinking and can't stall right of √3, since only √5 could stop it. So it must drop below √3.",
    "一旦跌进去，就不再翻号，被同号的 ±1 吸走。":
        "Once inside, the sign stops flipping, and the ±1 of the same sign pulls it in.",
    "奇数次 → −1": "odd → −1",
    "偶数次 → +1": "even → +1",
    "从正数出发：翻了奇数次，最后是 −1；翻了偶数次，最后是 +1。":
        "Starting positive: an odd number of flips ends at −1, an even number ends at +1.",

    # 9. the first boundary
    "翻一次和翻两次的分界在哪？就在 p(x) 恰好等于 −√3 的地方。把这个点叫作 b1。":
        "Where is the border between one flip and two? Exactly where p(x) equals −√3. Call that point b1.",
    "p 在这里单调递减，所以 √3 和 b1 之间的点，一步落到 −√3 和 0 之间：只翻一次号，然后去 −1。":
        "p is decreasing here, so points between √3 and b1 land between −√3 and 0: one flip, then on to −1.",
    "2 就在这一段：p(2) 正好等于 −1，一步到位。":
        "2 lives in this piece: p(2) is exactly −1, done in one step.",

    # 10. the basins
    "依此类推，让 p(b2) = −b1，p(b3) = −b2，一直下去：每个 b 都由上一个唯一确定。":
        "Keep going: p(b2) = −b1, p(b3) = −b2, and so on. Each b is pinned down uniquely by the one before.",
    "算出来：b1 ≈ 2.1478，b2 ≈ 2.2212，b3 ≈ 2.2336……它们越来越靠近 √5。":
        "Numerically: b1 ≈ 2.1478, b2 ≈ 2.2212, b3 ≈ 2.2336, creeping closer and closer to √5.",
    "把 √3 到 √5 这一段按这些点切开，只看绝对值。关键在于：p 把每一段翻到上一段的镜像上。":
        "Cut √3 to √5 at these points. The key: p maps each piece onto the mirror image of the piece before it.",
    "第一段一步落进 √3 以内的负半边，去 −1。":
        "The first piece lands inside √3 on the negative side in one step, so it goes to −1.",
    "p 是奇函数，镜像的命运正好相反：第二段翻一次号，就变成了第一段的镜像，所以去 +1。":
        "p is odd, so a mirror image has the opposite fate: piece two lands on piece one's mirror, so it goes to +1.",
    "第三段变成第二段的镜像，又去 −1。就这样一段一段交替下去。":
        "The third piece becomes the second one's mirror, so back to −1. And so it alternates, piece after piece.",
    "结论：第 n 段里的点恰好翻 n 次号。n 为奇数去 −1，n 为偶数去 +1。":
        "Conclusion: points in piece n flip exactly n times. Odd n goes to −1, even n goes to +1.",
    "这些分界点越来越挤向 √5。放大去看，同样的图案一遍又一遍地重复。":
        "The boundaries crowd toward √5. Zoom in, and the same pattern repeats over and over.",
    "每一段大约只有上一段的六分之一：p 在 √5 处的斜率是 −6，离 √5 的距离每步放大 6 倍。":
        "Each piece is about a sixth of the last: p has slope −6 at √5, so distances from √5 grow 6 times per step.",
    "所以在 √3 和 √5 之间，有无穷多个吸引区，交替通向 −1、+1、−1、+1……":
        "So between √3 and √5 there are infinitely many basins, leading in turn to −1, +1, −1, +1...",

    # 11. the boundary points
    "那分界点本身呢？b1 一步到 −√3，再一步到 0。":
        "And the boundary points themselves? b1 goes to −√3 in one step, then to 0.",
    "b2 → −b1 → √3 → 0，b3 → −b2 → b1 → −√3 → 0。":
        "b2 → −b1 → √3 → 0, and b3 → −b2 → b1 → −√3 → 0.",
    "每个分界点经过有限步都精确撞上 ±√3，然后落在不稳定的不动点 0 上：既不去 +1，也不去 −1。":
        "Every boundary point hits ±√3 exactly after finitely many steps, then sits on the unstable fixed point 0.",
    "不过它们都是孤立的点：稍微推一下，就会掉进两边的某个吸引区。":
        "But they are isolated points: nudge one slightly and it falls into a basin on one side.",

    # 12. the answer
    "初值 σ": "start σ",
    "过程": "what happens",
    "结局": "limit",
    "不翻号，爬向 1": "no flips, climbs to 1",
    "一步到 0": "0 in one step",
    "翻号 n 次，同时变小": "n flips while shrinking",
    "有限步撞上 ±√3": "hits ±√3 in finitely many steps",
    "在 ±√5 之间来回": "bounces between ±√5",
    "周期为 2": "period 2",
    "翻号，同时变大": "flips while growing",
    "发散": "diverges",
    "把第 (e) 问的答案整理一下。": "Here is the full answer to part (e).",
    "0 到 √3 之间去 +1；√3 本身一步到 0。":
        "Between 0 and √3: +1. √3 itself: 0 in one step.",
    "√3 到 √5 之间按翻号次数交替去 −1、+1；分界点 bn 落到 0。":
        "Between √3 and √5: −1 or +1, alternating with the number of flips; the boundaries bn fall to 0.",
    "√5 在 ±√5 之间来回；再大就一边翻号一边发散。":
        "√5 bounces between ±√5; anything larger flips and diverges.",

    # 13. back to the matrix
    "回到矩阵。一个奇异值若被推到 −1，矩阵依然正交，只是那个方向被翻转了；但大于 √5 的奇异值会发散。":
        "Back to the matrix. A −1 is still orthogonal, with one direction flipped; a value above √5 blows up.",
    "所以迭代之前要先把 W 缩小。常见做法是除以 Frobenius 范数：它不小于最大的奇异值。":
        "So shrink W first, e.g. divide by its Frobenius norm, which is at least the largest singular value.",
    "缩放之后，所有奇异值都落进 0 和 1 之间，远离 √3。":
        "After scaling, every singular value lies between 0 and 1, safely below √3.",
    "接下来每个奇异值都走上通往 +1 的路；小的要多走几步，但最终都到 1，W 趋向 U 乘 V 的转置。":
        "Now every singular value heads to +1. Small ones take longer, and W tends to U times V transpose.",
    "一个矩阵问题，就这样变成了一维动力系统：不动点、稳定性、两个关键数，和它们之间无穷交替的吸引区。":
        "A matrix problem became a 1-D dynamical system: fixed points, two key numbers, and alternating basins.",
}
