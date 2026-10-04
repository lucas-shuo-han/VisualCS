# Newton–Schulz: where does a singular value go? — narration script

> **How to use this file.** Everything here is plain text.
> - **Body** = the plain lines under each `###` heading. That text is the on-screen caption and what the voice says.
> - **`speak:`** (optional) = a different wording for the voice only, for math the voice would misread.
> - **Notes** = any line starting with `>` or `//`, and `<!-- ... -->`. Never rendered. Use them freely.
> - Do not edit the `### name NN <!-- #hash -->` heading lines: they tie each line to the code.
> - Subtitles are **not drawn on the video** any more (`BURN_CAPTIONS = False` in `series.py`). Each render
>   writes a separate `.srt` next to the `.mp4`, cut into one cue per sentence, so a beat can be as long as
>   the explanation needs. (Set it back to `True` and the ~105-character limit per beat applies again.)
> - Preview: `render.py cs182/newton-schulz 1 --preview --voice` (only changed lines are re-voiced).
> - **Wording, tone and sentence order inside a scene** are edited here. **Which scene comes first, or
>   adding/removing a beat**, changes the animation code: write it in the scene's notes and ask Claude.
> - **台词优先 In this file, the words are the only source of truth.** This is a script/screenwriting
>   step: focus only on the narration text (the body under each `###` heading). Do **not** read or edit
>   any code files here (`ep01_*.py`, `narration.py`, `render.py`, ...), and do **not** let
>   `narration.py check`'s code-binding warnings (MISSING — code has a say() with no matching line here;
>   STALE — the code's hash changed; UNKNOWN — a line here has no say() yet) block the writing. Those
>   warnings are about the code side, which is handled separately and later. During script editing,
>   the text below is what we are shaping.

> ---
>
> **修订记录（2026-10-03）：03–14 逐句重写之后，哪里变长了，哪些动画要补。**
> 这一段写在第一个 `## ` 之前，属于注释，不会被渲染。
>
> **1. 总长度。** 03–14 的台词从约 2100 词增加到约 5850 词，整片约 5980 词，按每分钟 150 词算约 40 分钟
> （原来约 14 分钟）。变长的原因是每个结论都补上了"先试、再看、再说理由"的过程。08–12 五场带配音的预览合计约 13 分钟。
>
> **2. 字幕。** 字幕不再画进视频。渲染时在 mp4 旁边生成 `.srt`，按句子切分（每条最多 84 个字符），
> 时间按字符数在该拍内分配。开关是 `series.py` 里的 `BURN_CAPTIONS`。因此"每拍 105 字符"的限制不再检查。
> 画面底部原来留给字幕的那一条现在是空的，构图可以往下用。
>
> **3. 每场的长度变化和要补的动画。** "变长的拍"指词数至少翻倍且多出 25 词以上的拍：这些拍的旧动画
> 只有几秒，现在的旁白要讲 20–80 秒，画面必须跟着分步出现，否则会长时间静止。
>
> | 场 | 词数（旧 → 新） | 变长的拍 | 画面需要补的内容 |
> |---|---|---|---|
> | 03 why_p | 368 → 1101 | 01, 04–07, 09–13（09 和 11 各约 210 词） | **已补动画（第三轮），每一步用 cue() 挂在旁白上。** 代码里现在只有 10 拍，台词有 13 拍，需要重排。03：先试 W·W（3×2 的例子，形状对不上），再换成 Wᵀ W。04：展开 Wᵀ W = V Σ Uᵀ U Σ Vᵀ = V Σ² Vᵀ，标成失败（U 没了）。05：左乘 W 得 U Σ³ Vᵀ。06：diag(1.3, 0.5)³ = diag(2.2, 0.125)。07：两次尝试并排比较，再接一个 Wᵀ W。09：U(aΣ + bΣ³ + …)Vᵀ，然后是两项的候选 aσ + bσ³。10：p(1) = a + b = 1。11：p(1+e) = a(1+e) + b(1+e)³ ≈ (a+b) + (a+3b)e，含 1.1³ = 1.33 的例子。12：解出 a = 3/2、b = −1/2，写出 p 和矩阵那一步。 |
> | 04 try_numbers | 200 → 552 | 04, 05, 07–11 | **已补动画（第三轮），每一步用 cue() 挂在旁白上。** 第一步的算术要显示出来（1.5 × 0.5 = 0.75，0.5³/2 = 0.0625，相减 0.6875）。三条数列逐个出现：0.5、1.3、0.1（0.1 要八步）。代数三步分开写：p(x) = x → ½x − ½x³ = 0 → ½x(1−x)(1+x) = 0。 |
> | 05 cobweb | 117 → 361 | 01, 02, 04–07 | **已补动画（第三轮），每一步用 cue() 挂在旁白上。** 对角线 y = x 现在在 04 才出现，代码里是在 01 就画了，要挪。01 只画曲线，并标出 p(0) = 0、p(1) = 1。06 是从 1.2 出发的第二条阶梯。 |
> | 06 slopes | 141 → 445 | 02–05 | **已补动画（第三轮），每一步用 cue() 挂在旁白上。** 02：p(e) = 1.5e − 0.5e³ ≈ 1.5e。03：在 0 附近放大，画"横走 e、竖走 1.5e"的三角形。05：p(1+e) = 1 − 1.5e² − 0.5e³，以及 0.2 → 0.06 → 0.006。 |
> | 07 how_big | 251 → 579 | 02, 04（150 词）, 06, 10, 11 | **已补动画（第三轮），每一步用 cue() 挂在旁白上。** 04 要分四小步：2.7 − 2.92 = −0.216；一对镜像数 ±0.216 → ±0.32；"mirror rule"的名字；最后落到 −1。06：逐项提出 x/2。10–11：指出驼峰高度是 1、0 到 1 之间曲线在对角线上方。 |
> | 08 too_big | 238 → 560 | 02, 03, 05–08 | **已重写并补动画（第二轮）。** 05–07 不再画 y = −x：改成比较 |p(x)| 和 |x|，|p(x)| = |x| · (x² − 3)/2，后一项叫 "size factor"。06 用 2.0（0.5）和 2.3（1.14）验证，07 由 factor = 1 得 x² = 5，再给曲线上色。01–04、08–10 也已补上（第三轮）：3 的算术 4.5 − 13.5 = −9、−9 → +351，四个起点的大小比较，p(√5) = −√5 的来回跳，2.3 → −2.63 → 5.18 → −61.8。 |
> | 09 the_gap | 258 → 560 | 整场重写（8 拍） | **已重写并补动画（第二轮）。** 从蛛网图开始：缺口里每步翻号且 size factor < 1 → 大小一直变小，迟早进到 √3 以内，而里面已经全知道 → 在蛛网图上跟 2.0（翻 1 次，−1）、2.2（翻 2 次，+1）、2.23（翻 3 次，−1）→ 奇数次 −1、偶数次 +1 → 色带作为全貌 → 留下两个问题（翻转次数在哪里变；条纹是否铺满）。 |
> | 10 first_boundary | 74 → 570 | 整场重写（7 拍） | **已重写并补动画（第二轮）。** 用镜像规则把"大小"和"符号"分开：大小走 |x| → |p(x)|，符号只数翻转次数 → 把曲线在 x 轴下面的部分折上去 → 和对角线比较（下方缩小、上方变大、在 √5 相交）→ 折叠图上的蛛网（2.2 → 2.02 → 1.11）→ 放大缺口，画高度 √3 的水平线，曲线和它的交点是 b₁，√3 到 b₁ 是第一条条纹 → 方程和两次试值 → 用 1.8、2.0、2.2 核对。 |
> | 11 basins | 229 → 640 | 整场重写（9 拍） | **已重写并补动画（第二轮）。** 核心一步：第一步（按大小）落在第一条条纹里的起点，只需要再翻一次。把第一条条纹搬到纵轴上成为一条带，曲线离开这条带的地方是 b₂ → 用 2.2 核对 → 同样得到 b₃ → 三个数值 → 所有条纹画在一条色带上并向 √5 放大 → 为什么变窄：2.20 和 2.23 差 0.03，一步之后差 0.18，约 6 倍。 |
> | 12 boundary_points | 66 → 420 | 整场重写（5 拍） | **已重写并补动画（第二轮）。** 01–02 验证这个方法盖住了整个缺口：边界点是夹在折叠曲线和对角线之间的楼梯，一直向右且不超过 √5，所以收拢到曲线和对角线相碰的地方，而缺口里只有 √5。03–05 边界点本身：b₁ → −√3 → 0，b₂ 多一步，都停在 0；挪一点就滚到 ±1。 |
> | 13 summary | 49 → 175 | 01, 03, 04 | **已补动画（第三轮），每一步用 cue() 挂在旁白上。** 表格每一行出现时旁白多了一句理由，行与行之间要留出时间。 |
> | 14 back_to_matrix | 115 → 393 | 02, 03（112 词）, 06 | **已补动画（第三轮），每一步用 cue() 挂在旁白上。** 02：除以一个数时 U、Vᵀ 不变。03：Frobenius 范数的算法（平方、求和、开方）和"不小于最大奇异值"的理由。05：2.9 / 3.45 = 0.84。06：把矩阵那一步 3/2 W − 1/2 W Wᵀ W 再显示一次。 |
>
> **3b. √3 到 √5 这一段（08 的 05–07 和 09–12）已经按第二轮的思路重写，台词和动画一起改了。** 其余场（03–07、08 的其他拍、13、14）在第三轮也补完了，做法相同。01 ellipse 在代码里删掉了提前说出 Newton–Schulz 的四拍，现在到 07 拍结束。
> - 这几场的台词直接写在代码的 say() 里，本文件里对应的段落是从代码生成的，hash 对得上。以后改这几场的台词：
>   改本文件正文即可（标题行不要动）；如果改了代码里的 say() 文字，要重新生成该场的段落（不要用 `narration.py sync`）。
> - 同步规则：**以台词为准，话一定说完**。动画用 `self.cue("台词里的一小段原文", 动画…)` 挂在旁白讲到的那几个词上；
>   动画比台词短就等着，比台词长就加快（调 run_time），个别纯演示的动画（例如色带向 √5 放大的 6 秒）放在两句话之间不说话。
>   **如果改了台词，cue() 里引用的那几个词也要还在**，否则渲染时会打印 `[cue] phrase not in the current line`，动画会立刻播放。
> - **预览：`python preview.py 9`**（场景编号或名字，可以写多个，或 `all`，加 `--join` 拼成一个文件）。每场单独一个进程并行渲染，
>   带配音，字幕按句子画在画面底部。结果在 `preview/NN_场景名.mp4`，同名 `.srt` 在旁边。配音有缓存，只改动画时一场不到一分钟。
>   加 `--no-captions` 得到和成片一样不带字幕的画面，`--hq` 是 1080p。
> - 05–08 四场共用一张图（06–08 接着 05 的画面画）。单独预览 06、07、08 时，前面的场会被快进（不渲染、不出声），不用手动处理。
> - preview.py 会自己换到 C: 盘的临时目录里运行 manim。直接在 D: 的项目目录里运行 manim 时 dvisvgm 会失败，
>   报 “does not support converting .dvi files to SVG”。
>
> **4. 台词和代码的绑定。** `narration.py check` 现在报 0 个问题：14 场的台词都和代码里的 say() 对上了，渲染用的就是本文件的正文。
> - **仍然不要运行 `narration.py sync`。** 它只保留第一个 `## ` 之前的内容和各场景段落，"The story in one paragraph"和两张场景表会丢。
>
> **5. 已对照代码确认的数值。** cobweb 的起点是 0.3；teal 表示终点 +1，gold 表示终点 −1；
> 14 的奇异值是 2.9、1.6、0.9、0.35，Frobenius 范数 3.45，2.9 / 3.45 = 0.84。
>
> **6. 语音。** why_p 09–12 有 `speak:` 行，把系数读成 "ay" 和 "bee"。改这四拍的正文时要同步改 `speak:`。
> 实际发音还没有听过。`.srt` 用的是正文（写 a、b），不是 `speak:`。

> ---
>
> **修订记录（2026-10-04）：看完 35 分钟成片后的五条意见，原因和改法。**
> 顺序：先文案（本文件），确认后再改代码。本轮文案已写入下面各场，标 **[10-04]** 的注释是对应的动画待办。
>
> **1. 字体不一致。** 画面上有三套字体：公式和 `\text{}` 是 LaTeX Computer Modern；`txt()` 是 Pango 无衬线（Windows 上是 Arial）；
> 坐标轴刻度 `mono()` 是等宽字体。同一类标签有的在 `\text{}` 里、有的在 `txt()` 里；√3 有的是 `\sqrt3`、有的是 Unicode。
> 改法：全片只用 LaTeX 一套（和 3b1b 一致），`txt()` / `mono()` 改成走 Tex，Unicode 符号改成 LaTeX 写法，字号收成三级（公式 40、标签 28、刻度 22）。
>
> **2. 关键处没有放大，取点不合适。** `NarratedScene` 继承 `Scene`，镜头不能动；所有"zoom in"都是清屏换一张图，看不出新图是原图的哪一块。
> 改法：改为 `MovingCameraScene`，加 `zoom_to()` / `zoom_back()`。要放大的七处：
> the_gap 04–05（2.2 和 2.23 在全图上只差 0.03 个单位，两条蛛网重叠：全图只跟 2.0 和 2.2，2.23 放大后再跟）；
> first_boundary 05（先在原图上框出缺口，再推进）；basins 04–05（b₃ 和 √5 只差 0.002，推到 √5 附近）；
> boundary_points 01（从上一张图连续推到角落）；how_big 05、08（曲线过 √3 的交点）；too_big 07–08（(√5, √5) 和方形轨道）；slopes 03（台词说了 zoom，核对画面）。
>
> **3. 节奏太快。** 语速本身偏快（含停顿约 168 词/分钟，3b1b 约 130–140），而且没有停顿：拍与拍之间只留 0.35 秒；
> 长拍（why_p 09、11 各约 210 词）一口气念 80 秒；`cue()` 按文字位置估时间，拍越长越不准。
> 改法：台词不删。长拍按本文件里的换行拆成多个 `say()`（每个不超过约 60 词）；拍间停顿 0.9 秒；每个新公式出现后静 1.2–1.5 秒；
> TTS 语速 −15%（试听 −10% / −15% / −20% 后定）。目标含停顿 120–125 词/分钟。
>
> **3b. 分成三集。** 放慢后总长约 55 分钟，所以分集：
>
> | 集 | 场景 | 预计时长 | 结尾留下的问题 |
> |---|---|---|---|
> | 1 | 01 ellipse、02 why_orthogonal、03 why_p | 约 11 分钟 | 任意一个 σ 反复代入 p，会去哪？ |
> | 2 | 04 try_numbers – 08 too_big | 约 20 分钟 | √3 和 √5 之间发生什么？ |
> | 3 | 09 the_gap – 14 back_to_matrix | 约 25 分钟 | （收尾：回到矩阵） |
>
> 新增的台词：`ep1_closing`、`ep2_recap`、`ep2_closing`、`ep3_recap`（标题行的 hash 写的是 `#new`，代码里还没有对应的 say()，
> `narration.py check` 会报 UNKNOWN，属于预期）。三张片头卡念的标题写在各段的注释里。
> 代码待办：`series.py` 三项；`ep01` 拆成三个文件加一个共享模块；`preview.py` 能指定集数；第 2 集开头重新画出 p 的图，第 3 集开头重新给出 size factor 那一行。
>
> **4. 男声。** 现有成片用的是 Kokoro `af_heart`（女声）。先试听再定：edge 的 Andrew、Brian、Ryan（英音），Kokoro 的 am_michael、am_fenrir、bm_george。
>
> **5. 推导缺失（√3 到 √5）。** 09–12 场原来只用图像说法（折叠曲线、楼梯、没有空隙），屏幕上只有 |p(b₁)|=√3、|p(b₂)|=b₁ 两个式子。
> 现在按手写稿的顺序把推导写进台词，图在左、式子在右，一句台词一行式子：
>
> | 步 | 屏幕上的式子 | 位置 |
> |---|---|---|
> | D1 | \|p(x)\| = \|x\| · \|x²−3\|/2（从此留在屏幕角上，直到 12 场结束） | too_big 05（已有） |
> | D2 | √3 < x < √5 ⇒ 0 < (x²−3)/2 < 1 ⇒ \|p(x)\| < \|x\| | the_gap 01 |
> | D3 | 进到 (−√3, √3) 之后：正 → +1，负 → −1 | the_gap 02 |
> | D4 | 哪些起点一步就进去？\|p(x)\| < √3 | first_boundary 05 |
> | D5 | \|p\| 在缺口里只升不降，从 0 到 √5 ⇒ 只过高度 √3 一次：p(b₁) = −√3 | first_boundary 05 |
> | D6 | (√3, b₁) → (−√3, 0) → −1 | first_boundary 05 |
> | D7 | p(b₂) = −b₁；(b₁, b₂) → (−b₁, −√3) | basins 02 |
> | D8 | p(b₃) = −b₂；三个式子并排；数列 √3, b₁, b₂, b₃, … | basins 04 |
> | D9 | 边界点会一直到 √5 吗？ | boundary_points 01 |
> | D10 | 有界：b_n < √5 ⇒ b_{n+1} < √5 | boundary_points 02 |
> | D11 | 递增：b_n = \|p(b_{n+1})\| < b_{n+1} | boundary_points 02 |
> | D12 | 递增且有上界 ⇒ 收拢到某个 L（唯一不证明的事实） | boundary_points 02 |
> | D13 | L · (L²−3)/2 = L ⇒ L² = 5 ⇒ L = √5 | boundary_points 02 |
> | D14 | 缺口 = 所有条纹合起来 | boundary_points 02 |
>
> 和手写稿不同的四处（已确认方向，写台词时按右边的）：p(x) 第二项是 **−**(1/2)x³；"converge to √3 / bounded by √3" 是 **√5**；
> "Uniform" 是单调，且是 b_m < b_{m+1}；最后一行是对 p(b_{n+1}) = −b_n 取极限得 √5，不是求 √3 的牛顿迭代。手写稿的 b* 就是片中的 b₁。
> 先证有界、再证递增：b_{n+1} 存在的前提是 b_n < √5（曲线才够得到那个高度），所以顺序不能反。
>
> **实施记录（2026-10-04，同一天完成）。** 上面五条和分集都已经改进代码，`narration.py check` 报 0 个问题。
> - **文件。** `ep01_inventing_p.py`（01–03）、`ep02_two_thresholds.py`（04–08）、`ep03_the_gap.py`（09–14），共用部分在 `ns_common.py`。
>   原来的 `ep01_newton_schulz.py` 已删除。新增的四段台词在代码里是 `ep1_closing`、`ep2_recap`、`ep2_closing`、`ep3_recap` 四个方法。
> - **设置都在 `series.py`。** `TTS`（edge 的 Andrew，语速 −10%，这是你试听后选的）、`PACE`（句间 0.75 秒、段间 1.6 秒、拍间 1.8 秒）、`TEXT_FONT = "latex"`。
>   换音色前用 `python audition.py` 生成候选，在 `preview/voices/`。
> - **节奏的做法和计划不同。** 没有把长拍拆成多个 say()，而是让 kit 逐句合成配音：每句之间停 `PACE["sentence"]`，
>   本文件里一拍正文的每一行是一段，段间停 `PACE["paragraph"]`。`cue()` 现在按"那几个词在哪一句、那一句什么时候开始念"定时，不再按整拍估算。
>   `.srt` 也是一句一条、按实际念的时间。超过 60 词的单行拍已经用 `narration.py paragraphs` 自动分了段，分得不合适的地方直接在这里改换行。
> - **实测节奏**（480p 预览）：第 1 集 11.1 分钟、129 词/分钟；第 2 集 18.9 分钟、140 词/分钟；第 3 集 22.4 分钟、142 词/分钟。
>   计划里写的目标是 120–125，现在是 130–140。还想慢就把 `PACE` 三个数调大，不用重新配音。
> - **字号。** 文字 28，公式 36，大公式 44，刻度 22。why_p 里几条直接写 `MathTex(font_size=52/56)` 的主公式没有动。
> - **放大。** 镜头推进：slopes 03、how_big 05 和 08、too_big 07、first_boundary 05（b₁ 交点）、basins 04（b₃）。
>   框展开成新图：first_boundary 05（全图到缺口图）、boundary_points 01（缺口图到 √5 角落）。the_gap 05 用的是数轴放大镜（2.2、2.23、√5 三个点）。
> - **改台词时的规矩。** 改正文不动标题行。`narration.py check` 会检查 `cue()` 等的那几个词还在不在（报 CUE）。
>   代码里故意改了 say() 的文字之后运行 `narration.py rebind`。仍然不要运行 `narration.py sync`。
> - **终审（同日，第二轮）。** 语速改为 −4%。五处补得更严格：slopes 05 把丢掉的 e²、e³ 项放回去，写出 p(1+e) = 1 − 1.5e² − 0.5e³
>   （新误差带负号：不管从哪边来都落在 1 的下方）；how_big 11 补上"一直上升又过不了 1，所以会停在某处"；first_boundary 06 原来说
>   "no tidy answer" 不对，b₁ 有闭式 ∛(√3+√2) + ∛(√3−√2)，现在如实说并显示；basins 08 的 6 倍不再只靠两个数估计，
>   用 p(√5+e) ≈ −√5 − 6e 说明在 √5 处正好是 6；back_to_matrix 06 补上 σ = 0 的例外；总表里注明 b₀ = √3。
> - **终审第三轮。** 补上了原来直接引用的三处：ellipse 07 说明非方阵时准确的说法是 orthonormal columns；
>   boundary_points 02 取极限那一步说了 p 连续；back_to_matrix 03 说明了为什么元素平方和等于奇异值平方和
>   （左乘旋转不改每一列的长度，右乘旋转不改每一行的长度，所以 ‖UΣVᵀ‖² = ‖Σ‖²）。
>   现在唯一不证明的事实是：只升且有上界的数列会收拢到某个值。
> - **最终成片（语速 −4%）。** 第 1 集 10:46、135 词/分钟；第 2 集 18:38、147 词/分钟；第 3 集 22:52、150 词/分钟。
>   上面写的 Andrew −10% 和 129–142 词/分钟是第一轮的数字。
> - **预览。** `python preview.py 9`、`python preview.py ep2`、`python preview.py ep3_recap ep1_closing`、`python preview.py all`。

## The story in one paragraph

> A matrix W turns a circle into an ellipse; its singular values are the half-axes. Muon wants the
> update to be orthogonal (a circle, all stretches equal to 1). Xavier only controls the overall
> scale of the gradients, but the SVD says every single direction must keep its size, which is
> what orthogonal means. The SVD itself is too slow, so we repeat one matrix-product-only step,
> and the SVD tells us each singular value just follows a number map p.
> The rest of the video is one question about p: where does a starting value σ end up? The answer is
> "+1" below √3, a flip past √3, a blow-up past √5, and in the thin gap between, a pattern of stripes.
> The video ends by turning that into a recipe: scale W first so every σ is below √3.

## The viewer, scene by scene (what they know, what they now want to ask)

> | # | Scene | Viewer already knows | Viewer now wants to know |
> |---|---|---|---|
> | 1 | ellipse | what a matrix does to a circle | why would anyone want W to be a circle? |
> | 2 | why_orthogonal | Xavier controls only the overall gradient scale; SVD shows each direction's stretch | why must no single direction blow up or die? |
> | 3 | why_p | an orthogonal update means every σ is 1; SVD is slow | where does the cubic come from? |
> | 4 | try_numbers | p(σ) = 1.5σ − 0.5σ³ and how to evaluate it | does it really go to 1? what stays put? |
> | 5 | cobweb | numbers 0.5, 1.3, 0.1 all go to 1 | can I see the whole iteration at once? |
> | 6 | slopes | the staircase picture; fixed points −1, 0, 1 | why do ±1 attract and 0 repel? |
> | 7 | how_big | small starts work; ±1 attract | how big can σ be before it breaks? |
> | 8 | too_big | 1.8 flipped to −1; the hump crosses at √3 | does everything past √3 go to −1? (3 explodes) |
> | 9 | the_gap | the size factor: a flip shrinks up to √5 and grows beyond | what happens between √3 and √5? (follow 2.0, 2.2, 2.23 on the cobweb) |
> | 10 | first_boundary | the ending depends on the number of flips; the striped overview | where exactly does one flip turn into two? |
> | 11 | basins | the folded curve and the first edge b1 | what about starts above b1? (their first step lands on a stripe we already know) |
> | 12 | boundary_points | each stripe lands on the one before | do the stripes fill the whole gap? and what happens to the edges themselves? |
> | 13 | summary | the complete picture | what is the one-line answer? |
> | 14 | back_to_matrix | the table of fates | so what do I do with my matrix? |

> ---
>
> 下面这张表是上面的中文详细版，方便逐场讨论。**「注释」栏留空供你写评论。**
>
> | # | 场景 | 观众此时已经知道 | 观众现在想问 | 注释 |
> |---|---|---|---|---|
> | 1 | ellipse | 一个矩阵会把圆变成椭圆；SVD 把任意矩阵拆成「旋转 → 沿轴拉伸 → 旋转」三步，拉伸量 σ₁、σ₂ 就是椭圆的两个半轴（奇异值） | 为什么有人想让 W 变成圆？也就是为什么要把奇异值都变成 1？ | |
> | 2 | why_orthogonal | 课堂上只靠 Xavier 这样的方法控制「整体」梯度尺度，不让整体爆炸；SVD 能让我们看清矩阵每个「自然方向」上的拉伸 | 既然整体尺度控制住了，为什么还要管每一个方向？哪些方向会爆、哪些会消失？ | |
> | 3 | why_p | 正交更新意味着每个 σ 都等于 1；用 SVD 做正交化很慢 | 这个牛顿–舒尔茨多项式 p(x) = 1.5x − 0.5x³ 到底从哪来的？为什么偏偏是它？ | |
> | 4 | try_numbers | p 的表达式，以及怎么代入 p(σ) 一步一步算；0.5、1.3、0.1 三种起点最后都能到 1 | 它真的能精确收敛到 1 吗？有没有别的数待在原地不动？ | |
> | 5 | cobweb | 代入一次 p 就得到一个数 σ → p(σ) → p(p(σ)) → …，前面这些数都对得上 | 能不能把整条迭代一次性画出来，用图像看明白？ | |
> | 6 | slopes | 蛛网图里每一步是「向上碰到曲线、水平碰到对角线」；−1、0、1 是三个不动点 | 为什么 ±1 会被吸引（稳定），而 0 会推走（不稳定）？ | |
> | 7 | how_big | 小的起点都能到 1；±1 是稳定的吸引点 | σ 最大能多大？超过某个值会不会就崩掉？ | |
> | 8 | too_big | 1.8 会翻到 −1；p 的「拱」在图 x = √3 处穿过横轴，过去 p(x) 就变负 | 是不是所有大于 √3 的数最终都到 −1？（结果 3 直接爆炸） | |
> | 9 | the_gap | size factor：在 √5 之内每步翻号并缩小，超出 √5 就变大 | √3 和 √5 之间到底是什么情况？（在蛛网图上跟 2.0、2.2、2.23） | |
> | 10 | first_boundary | 结局取决于翻转次数（奇数 → −1，偶数 → +1）；看过色带全貌 | 翻一次和翻两次的分界到底在哪？ | |
> | 11 | basins | 折叠曲线（只看大小）和第一条边界 b₁（约 2.148） | b₁ 以上的起点怎么办？（第一步落到已经解决的条纹里） | |
> | 12 | boundary_points | 每条条纹都被一步送到前一条条纹上 | 这样的条纹能不能铺满整个缺口？边界点自己会去哪？ | |
> | 13 | summary | 现在有了完整的结局分布图（哪些 σ → +1、哪些 → −1、哪些会炸） | 用一句话收总：到底什么样的起点得到什么样的归宿？ | |
> | 14 | back_to_matrix | 上面那张「起点归宿对照表」 | 换回我的矩阵：知道了这些，我到底该怎么缩放 W、再迭代，才能让它真正正交化？ | |

## 第 1 集 · ep01_inventing_p.py（01–03）

## 01 · ellipse — Why would anyone iterate this? (motivation)

> **Purpose.** Give a reason to care before any formula. Muon wants an orthogonal update; the picture of 'orthogonal' is a circle.
> **Beats.** (1) W maps the unit circle to an ellipse. (2) SVD demo: rotate, stretch, rotate. (3) the stretches are σ1, σ2 = half-axes. (4) all stretches 1 means only rotations: orthogonal. The scene ends there; the next motivation lives in why_orthogonal, and the "SVD is slow, so build P" idea moves to why_p.
> **Tone.** Calm, concrete. No jargon before the picture.
> **Open choices.** Is the SVD demo too long before the viewer sees why? Would you start with the finished 5-step animation (the payoff) and then explain it?

### ellipse 01 <!-- #5ce9c7 -->
Think of a matrix W. It turns the unit circle into an ellipse.
> screen: Create, FadeIn

### ellipse 02 <!-- #a892b3 -->
Let's examine the singular value decomposition of W. It says any matrix is a combination of three steps, rotate, stretch the axes, and rotate.
> screen: FadeIn, Write

### ellipse 03 <!-- #e14429 -->
First, a rotation turns the arms onto the axes. That is the V transpose matrix from SVD.
> screen: Rotate, FadeIn, Indicate

### ellipse 04 <!-- #8ee4e9 -->
Next, sigma stretches each axis by its own amount, here one point three and zero point five. The circle becomes an ellipse.
> screen: demo.animate.apply_matrix, FadeIn, Indicate

### ellipse 05 <!-- #7f031e -->
Finally, U rotates it into place. Since rotations never change lengths, all the stretching takes place in sigma.
> screen: Rotate, FadeIn, Indicate

### ellipse 06 <!-- #ef972a -->
The two stretch factors, sigma one and sigma two, are the half-axes of the ellipse. They are called singular values.
> screen: Indicate, Indicate

### ellipse 07 <!-- #2492fc -->
If every singular value were exactly one, only the rotations would remain. Nothing gets stretched, and W would be orthogonal. If W is not square, the exact name for this is orthonormal columns. The picture is the same, so we will keep saying orthogonal.
> screen: FadeIn

## 02 · why_orthogonal — Why must every direction stay? (motivation)

> **Purpose.** Give the reason to care before any formula: Xavier controls the overall scale of the
> gradients, but the SVD lets us pin down every single direction so none blows up or dies; an
> orthogonal update keeps each singular value at one.
> **Beats.** SVD shows the stretch along each natural direction. Xavier is one average number. That
> average can hide a direction that blows up and another that vanishes. So we want every direction
> to keep its size, and Muon asks for exactly that: an orthogonal update where every singular value
> is one.
> **Tone.** Calm, concrete. Connect the lecture idea to the picture before any formula.

### why_orthogonal 01 <!-- #cbbfd6 -->
The singular value decomposition lets us watch the stretching along each natural direction of the matrix, one direction at a time.
> screen: FadeIn, FadeIn

### why_orthogonal 02 <!-- #7c5599 -->
In class we worried about one thing, that the overall scale of the gradients does not explode. That is the idea behind Xavier initialization.
> screen: FadeIn, FadeIn, FadeIn

### why_orthogonal 03 <!-- #1555f5 -->
But that is a single number, a rough average over the whole matrix. It says little about any one direction.
> screen: Indicate

### why_orthogonal 04 <!-- #51fbdc -->
Xavier does not solve every problem. The average can be fine while one direction still stretches too far and another gets squeezed to nothing.
> screen: Transform, Transform, FadeIn, FadeIn

### why_orthogonal 05 <!-- #273562 -->
We want every direction to keep its size, so none gets stretched too far and none gets squeezed away.
> screen: Transform, Transform, FadeOut, FadeOut

### why_orthogonal 06 <!-- #1f23d6 -->
That is why Muon asks for an orthogonal update, one where every singular value is exactly one. Nothing grows, nothing vanishes.
> screen: ReplacementTransform, FadeIn

### why_orthogonal 07 <!-- #b6ef54 -->
Every direction moves together, and the matrix stays healthy step after step.
> screen: Indicate

## 03 · why_p — You could have invented p (design)

> **Purpose.** Let the viewer invent p. The polynomial is never announced. It falls out of one constraint (only matrix products are cheap) and one calculation (W Wᵀ W = U Σ³ Vᵀ).
> **Logic chain.** Each beat answers the question the previous beat leaves open:
> 1. We want U Vᵀ, but the SVD is slow. → *What is cheap, then?*
> 2. Matrix multiplication is cheap. → *What can we build from W with products alone?*
> 3. So just start multiplying. The only matrix we have is W. W·W fails on shape, so try Wᵀ W. → *What does that product give?* (Do not list "the rules of the game" here. Scaling and adding only appear in beat 09, where they are obvious.)
> 4. Through the SVD: Wᵀ W = V Σ² Vᵀ. U is lost, so this is a failure. One more W gives W Wᵀ W = U Σ³ Vᵀ, and both rotations are back. → *Why did three work when two did not?*
> 5. An odd number of copies keeps U and Vᵀ and only changes each σ. So we get σ, σ³, σ⁵, … → *How do we combine them to reach U Vᵀ?*
> 6. A mix is an odd polynomial p(σ). The matrix problem is now a number problem. → *Which p?*
> 7. No p works in one step, so ask for a step that gets closer, and repeat. One term only rescales, so take two. → *What should a and b be?*
> 8. Both wishes are derived from "repeat until it settles at one", not announced. (a) To settle at one, one must stay: p(1)=1, so a+b=1. (b) Near one it must get closer: p(1+e) ≈ 1 + (a+3b)e, so the error is multiplied by a+3b; the best is zero. Then "two wishes, two unknowns" → a = 3/2, b = −1/2.
> 9. The question for the rest of the video: σ → p(σ) → p(p(σ)) → … → ?
> **Tone.** 'You could have done this yourself.' The viewer should feel the polynomial was forced on us, not picked. Slow on the two wishes.
> **Polish pass (novice check).** Every step a first-time viewer cannot do alone is now spoken: why W·W does not fit, what Wᵀ is in SVD form, why Uᵀ U cancels, what "diagonal" buys us (with the numbers 1.3 and 0.5 from scene 01), why odd products keep working, how U and Vᵀ factor out of a sum, why one step cannot be enough, why one term is not enough, where (1+e)³ ≈ 1+3e comes from, and how the two equations are solved. The sentence "the curve is flat at one" was removed from beat 11, because no graph exists yet; scene 06 makes that link.
> **Your original notes for 02–03 (kept for reference).** "what operation for matrix is cheap? maybe just operate on x itself because it is natural and you don't need to compute anything for each specific matrix / polynomials are a great class of funcs that is easy to compute and can represent a lot / what kind of polynomials? / A constant would treat every direction the same, but Muon must handle each direction on its own." The last idea is now in beat 09, as the reason one term is not enough.
> **Code changes needed (later).** 03 shows two attempts (W·W fails on shape with a 3×2 example, then Wᵀ W). 04 expands Wᵀ W = V Σ Uᵀ U Σ Vᵀ = V Σ² Vᵀ and marks it as a failure (U gone). 05 multiplies by W on the left to get U Σ³ Vᵀ. 06 shows diag(1.3, 0.5)³ = diag(2.2, 0.125). 07 compares the two attempts and attaches one more Wᵀ W. 09 shows U(aΣ + bΣ³ + …)Vᵀ, then the two-term candidate. 11 shows p(1+e) = a(1+e) + b(1+e)³ ≈ (a+b) + (a+3b)e. 12 shows the solved p and the matrix step 3/2 W − 1/2 W Wᵀ W.
> **Voice.** The coefficients a and b are written as letters in the caption and respelled in `speak:` as "ay" and "bee", so the voice does not read "a" as the article. Only the coefficient is respelled; the article in "a sigma", "a number" stays "a". If a caption changes, change its `speak:` line too.
> **Open choices.** Beats 09 and 11 are long. Each could be split into two or three `say()` calls in code without changing a word.

### why_p 01 <!-- #f2373c -->
We want every singular value to be one. The SVD hands us exactly that. Write W as U, sigma, V transpose, keep the two rotations, and replace every stretch in sigma with one. What remains is just U times V transpose.
But computing an SVD is a long procedure, and it runs slowly on a GPU.

### why_p 02 <!-- #cb23f8 -->
So we want that same result, U times V transpose, without ever computing the SVD.
What can a GPU do cheaply? It can multiply matrices. That is the one thing it is built for.

### why_p 03 <!-- #dd0e65 -->
So let's start multiplying. The only matrix we have is W, so the first thing to try is W times W.
But two matrices can only be multiplied when the number of columns of the first matches the number of rows of the second. If W has three rows and two columns, W times W does not fit.
The transpose swaps rows and columns. So W transpose times W always fits. Let's see what that product gives.
> screen: Write

### why_p 04 <!-- #64d094 -->
To see it, write W with its SVD, as U, sigma, V transpose. Transposing a product reverses the order, so W transpose is V, sigma, U transpose.
Now put them side by side. In the middle, U transpose meets U. The transpose of a rotation is the same rotation done backwards, and a rotation followed by its reverse does nothing. So the pair cancels.
What is left is V, sigma times sigma, V transpose. That is not what we want. Our target has U on the left, and here U has disappeared.
> screen: FadeIn, Write, FadeIn

### why_p 05 <!-- #32efd2 -->
So bring U back. Multiply by W one more time, on the left. Now the V transpose at the end of W meets the V at the start of our product, and that pair cancels too.
What survives is U on the left, V transpose on the right, and sigma three times in between. This time both rotations are back where they belong.
> screen: VGroup, Write

### why_p 06 <!-- #936ed4 -->
And the middle is easy to read. Sigma is diagonal, which means it only holds the singular values, one for each direction. Multiplying diagonal matrices just multiplies the matching entries.
So sigma three times in a row cubes each singular value on its own. In our example, one point three becomes about two point two, and zero point five becomes zero point one two five. No direction disturbs another.

### why_p 07 <!-- #bd8c5d -->
Look back at the two attempts. Two copies of W lost a rotation. Three copies kept both, and only the singular values changed.
And we can keep going. Attach another W transpose times W, and the same cancelling happens again. U and V transpose stay where they are, and the middle gains two more sigmas.

### why_p 08 <!-- #a4b47f -->
So the products with an odd number of copies are the ones we can use. W itself carries sigma. Three copies carry sigma cubed. Five copies carry sigma to the fifth, and so on.
> screen: LaggedStart

### why_p 09 <!-- #6a3be5 -->
Every one of these products has the same U on the left and the same V transpose on the right. So if we multiply each product by a number and add them up, U and V transpose factor out, and only the middle is a sum.
In that middle, each singular value becomes a number times sigma, plus a number times sigma cubed, and so on. A sum of powers like this is a polynomial. Call it p.
So turning W into U times V transpose now means one thing. We need a p that sends every sigma to one.
Can p do that in a single step? Then it would have to give one for every input. But p is made of powers of sigma, so a tiny sigma always gives a tiny output. One step is not enough.
So we ask for less. One step only has to bring sigma closer to one, and then we apply p again and again.
Which p? Every extra term costs more matrix products, so we want as few as possible. One term alone, a times sigma, only rescales every singular value by the same number, so the ellipse stays an ellipse.
So take two terms, a times sigma plus b times sigma cubed.
speak: Every one of these products has the same U on the left and the same V transpose on the right. So if we multiply each product by a number and add them up, U and V transpose factor out, and only the middle is a sum. In that middle, each singular value becomes a number times sigma, plus a number times sigma cubed, and so on. A sum of powers like this is a polynomial. Call it p. So turning W into U times V transpose now means one thing. We need a p that sends every sigma to one. Can p do that in a single step? Then it would have to give one for every input. But p is made of powers of sigma, so a tiny sigma always gives a tiny output. One step is not enough. So we ask for less. One step only has to bring sigma closer to one, and then we apply p again and again. Which p? Every extra term costs more matrix products, so we want as few as possible. One term alone, ay times sigma, only rescales every singular value by the same number, so the ellipse stays an ellipse. So take two terms, ay times sigma plus bee times sigma cubed.
> screen: odd.animate.scale, FadeIn

### why_p 10 <!-- #8b28c8 -->
What should a and b be? We want the repeated steps to settle at one. So a sigma that has reached one must stay there, or the steps would never settle.
Put sigma equals one into p. One cubed is still one, so p gives a plus b. For one to stay at one, a plus b must equal one. Call this our first wish.
speak: What should ay and bee be? We want the repeated steps to settle at one. So a sigma that has reached one must stay there, or the steps would never settle. Put sigma equals one into p. One cubed is still one, so p gives ay plus bee. For one to stay at one, ay plus bee must equal one. Call this our first wish.
> screen: FadeIn

### why_p 11 <!-- #915b49 -->
Staying at one is not enough. A sigma that is only close to one has to move closer. So take a sigma that misses one by a small error e, and put one plus e into p.
We need the cube of one plus e. Multiplied out, it is one, plus three e, plus terms with e squared and e cubed. When e is small, those last terms are far smaller still, so we drop them. For example, one point one cubed is one point three three, very close to one point three.
So p gives a times one plus e, plus b times one plus three e. Collect the pieces, and that is a plus b, plus a plus three b times e.
The first piece, a plus b, is one, by our first wish. So p gives one, plus a plus three b times e. We went in with an error of e, and we came out with an error of a plus three b times e.
One step multiplies the error by a plus three b. We want the error to shrink, and the most it can shrink is all the way to nothing. So our second wish is that a plus three b equals zero.
speak: Staying at one is not enough. A sigma that is only close to one has to move closer. So take a sigma that misses one by a small error e, and put one plus e into p. We need the cube of one plus e. Multiplied out, it is one, plus three e, plus terms with e squared and e cubed. When e is small, those last terms are far smaller still, so we drop them. For example, one point one cubed is one point three three, very close to one point three. So p gives ay times one plus e, plus bee times one plus three e. Collect the pieces, and that is ay plus bee, plus, ay plus three bee, times e. The first piece, ay plus bee, is one, by our first wish. So p gives one, plus, ay plus three bee, times e. We went in with an error of e, and we came out with an error of, ay plus three bee, times e. One step multiplies the error by ay plus three bee. We want the error to shrink, and the most it can shrink is all the way to nothing. So our second wish is that ay plus three bee equals zero.
> screen: FadeIn

### why_p 12 <!-- #25c434 -->
Two wishes and two unknowns, which is exactly enough. The second wish says a equals minus three b. Put that into the first, and minus three b plus b equals one, so b is minus one half. Then a is three halves.
So p of sigma is three halves sigma, minus one half sigma cubed. For the matrix, one step is three halves W, minus one half W times W transpose times W. That is the Newton–Schulz step, and you could have invented it yourself.
speak: Two wishes and two unknowns, which is exactly enough. The second wish says ay equals minus three bee. Put that into the first, and minus three bee plus bee equals one, so bee is minus one half. Then ay is three halves. So p of sigma is three halves sigma, minus one half sigma cubed. For the matrix, one step is three halves W, minus one half W times W transpose times W. That is the Newton Schulz step, and you could have invented it yourself.
> screen: FadeOut, ReplacementTransform, Create

### why_p 13 <!-- #612838 -->
We built p from what happens close to one. But a real sigma can start anywhere. So take any positive sigma and apply p over and over. Where does it end up? That is the question in part (e) of the worksheet.
> screen: FadeIn
> **[10-04]** 去掉了 "and the rest of this video answers it"：这一集到这里结束，问题留给下一集。

## 第 1 集片尾 · ep1_closing

> **[10-04] 新增。** 片头卡念："Newton–Schulz. You could have invented it."（不报集数，不列内容。）
> 片尾不给答案，只留问题。画面：p 的式子和矩阵那一步留在屏幕上，下面出现 σ → p(σ) → p(p(σ)) → … → ?

### ep1_closing 01 <!-- #010750 -->
So this is where we stand. We wanted U times V transpose without computing an SVD. Matrix products alone gave us a polynomial, and two wishes fixed its two numbers.
What we have not seen is the iteration itself. We only know what p does close to one. Where a sigma ends up when it starts far from one, we find out next time.

## 第 2 集 · ep02_two_thresholds.py（04–08）

## 第 2 集开头 · ep2_recap

> **[10-04] 新增。** 片头卡念："Newton–Schulz. Where does a singular value go?"
> 只说上一集得到的结论，三句以内，然后直接接 try_numbers 01。画面：矩阵那一步，然后变成 p(σ)，缩到右上角。

### ep2_recap 01 <!-- #067c3f -->
Last time we built one step out of nothing but matrix products. Three halves W, minus one half W, W transpose, W.
On each singular value, that step is a polynomial. p of sigma is three halves sigma, minus one half sigma cubed. We chose it so that one stays at one, and a value close to one moves closer.
But a real sigma can start anywhere.

## 04 · try_numbers — Just try numbers (easy cases first)

> **Purpose.** Build trust with starts that behave: 0.5, 1.3, 0.1 all go to 1, by hand arithmetic. Then ask what could stay put and solve p(x) = x step by step.
> **Logic chain.** Scene 03 ended on "where does a sigma end up?" → just try one: 0.5 → one above one: 1.3 → one far away: 0.1 → all reach one, and one stays put (first wish) → *if another number also stayed put, sigma could get stuck there. Is there one?* → try zero: it stays too → algebra finds them all: 0, 1, −1 → *but 0.1 left zero and went to one. Why does one fixed point pull and another push?* → cobweb.
> **Beats.** p(0.5) arithmetic; the staircase of values; the algebra x(1−x)(1+x)=0 gives 0, 1, −1.
> **Tone.** Unhurried. Say each arithmetic step aloud; let the numbers appear one at a time.
> **Polish pass (novice check).** The first step is now computed in full (cube first, then half). Each chain of values is spoken with its real numbers, so the viewer can pause and check. The switch from the letter sigma to the letter x is announced in beat 07. Each line of the algebra in 08–10 says what was done and what it gives, and minus one is checked by plugging it in.
> **Numbers used.** 0.5 → 0.6875 → 0.869 → 0.975 → 0.999. 1.3 → 0.8515 → 0.969 → 0.9985. 0.1 → 0.1495 → 0.223 → 0.328 → 0.475 → 0.659 → 0.845 → 0.966 → 0.998.

### try_numbers 01 <!-- #e12179 -->
Where does a sigma end up? No theory yet. Let's just pick a number and try it, say zero point five.
> screen: FadeIn

### try_numbers 02 <!-- #b2ca63 -->
One step of p takes three halves of the number, and subtracts one half of its cube. Three halves of zero point five is zero point seven five. Zero point five cubed is zero point one two five, and half of that is zero point zero six two five. Subtract, and we get zero point six eight seven five.
> screen: Write

### try_numbers 03 <!-- #ea3911 -->
Now feed that result back in, and keep going. Zero point six nine becomes zero point eight seven, then zero point nine eight, then zero point nine nine nine. It is closing in on one.
> screen: FadeOut, Write

### try_numbers 04 <!-- #f7274e -->
That start was below one. Now try one above it. One point three drops to zero point eight five, which is below one, and then it climbs, to zero point nine seven, and then zero point nine nine eight. It also closes in on one.
> screen: Write

### try_numbers 05 <!-- #56cc9c -->
Both of those were fairly close to one. So try a start that is far away, down near zero. Zero point one becomes zero point one five, then zero point two two, then zero point three three. It is slow at first, but it keeps climbing, and after eight steps it also reaches one.
> screen: Write

### try_numbers 06 <!-- #e96769 -->
All three starts end at one. And once a value is at one, it stays there. Three halves minus one half is one, so p of one equals one. That is our first wish at work.
> screen: FadeIn

### try_numbers 07 <!-- #769257 -->
But if some other number also stayed put, a sigma could get stuck there and never reach one. Is there such a number? Try zero. Three halves of zero is zero, and zero cubed is zero, so p of zero is zero. Zero stays put as well.
From here on, call the input x. A value where p of x equals x is called a fixed point. We have found two of them. Are there any more?
> screen: FadeIn

### try_numbers 08 <!-- #4eb4c7 -->
To find them all at once, write down p of x equals x. That is three halves x, minus one half x cubed, equals x. Subtract x from both sides, and we get one half x, minus one half x cubed, equals zero.
> screen: FadeIn

### try_numbers 09 <!-- #cb4264 -->
Both terms contain one half x, so pull it out. What is left inside is one minus x squared. And one minus x squared splits into one minus x, times one plus x. So the equation says one half x, times one minus x, times one plus x, equals zero.
> screen: FadeIn

### try_numbers 10 <!-- #81f7b9 -->
A product is zero only if one of its factors is zero. So x is zero, or x is one, or x is minus one. Those are all the fixed points there are, the two we found and a new one. And minus one does check out. Minus three halves, plus one half, is minus one.
A singular value is never negative, so for now minus one is just a point on the list.
> screen: FadeIn

### try_numbers 11 <!-- #e4b1cb -->
But zero matters right away. A sigma at exactly zero is stuck. And yet zero point one, right next to zero, walked away from it, all the way to one. Why would one fixed point pull values in and another push them away? To see what happens around each of them, we need a picture of the iteration.

## 05 · cobweb — The picture of the iteration

> **Purpose.** Turn the arithmetic into a graph: up to the curve, across to the diagonal, repeat.
> **Logic chain.** We need a picture of the iteration → the graph of p turns an input into a height → *but the next step needs that height as an input* → the diagonal turns a height into a position → one step = up to the curve, across to the diagonal → staircases from 0.3 and 1.2 → fixed points are the crossings → *the picture shows paths leaving zero and entering one, but not yet why* → slopes.
> **Order matters.** The diagonal is not drawn in beat 01. It appears in beat 04, as the answer to the problem raised in beat 03 (a height has to become a position). Code change needed: move the creation of y = x from beat 01 to beat 04.
> **Beats.** Axes with y=p(x); one step with labelled points; why the diagonal; the staircase from 0.3; the same from 1.2.
> **Tone.** Explain the diagonal as 'height equals position', the one idea students trip on.
> **Polish pass (novice check).** Beat 01 now describes the shape of the curve using values the viewer already computed (p(0)=0, p(1)=1). The second step is walked through in full in beat 05 before the word "repeat" is used. The crossings in beat 07 are tied to the definition of a fixed point from scene 04.
> **Numbers used.** 0.3 → 0.44 → 0.61 → 0.80 → 0.95 → 0.997. 1.2 → 0.936 → 0.994.

### cobweb 01 <!-- #b2675a -->
Start with the graph of p. Along the bottom is the input x, and the height of the curve above it is the output, p of x. We know a few points already. At zero the height is zero, and at one the height is one. The curve rises from zero, reaches a hump at one, and comes back down after it.
> screen: Create, FadeIn, Create, Create, FadeIn, FadeIn

### cobweb 02 <!-- #192798 -->
On this picture, one step of the iteration looks like this. Start at x equals zero point three on the bottom axis, and go straight up to the curve. The height you reach is p of zero point three, about zero point four four.
> screen: FadeIn, FadeIn, Create

### cobweb 03 <!-- #5f6d39 -->
For the next step, zero point four four has to become the new input. But right now it is a height, and inputs are measured along the bottom. We need a way to turn a height into a position.
> screen: FadeIn, Create

### cobweb 04 <!-- #cf6c96 -->
Here is a line that does exactly that, the diagonal y equals x. Every point on it is as far to the right as it is high. So go sideways from the curve until you hit the diagonal. You are still at height zero point four four, and now you are also above x equals zero point four four.
> screen: GrowFromCenter, FadeIn, Create

### cobweb 05 <!-- #373a2a -->
From there, the second step is the same move. Go straight up to the curve, which gives zero point six one, and sideways to the diagonal again. Keep repeating, and the path climbs like a staircase, zero point eight, zero point nine five, and into one.
> screen: FadeIn, self.draw

### cobweb 06 <!-- #df1d8d -->
Now a start above one. From one point two, the curve is below the diagonal, so the first move goes down, to zero point nine four. After that the path climbs the last little bit and settles on one as well.
> screen: FadeOut, FadeIn, self.draw

### cobweb 07 <!-- #23bcae -->
Now look at where the curve meets the diagonal. On the diagonal the height equals x, and on the curve the height is p of x. So at a crossing, p of x equals x. The three crossings are our three fixed points, minus one, zero, and one.
And the staircases show which way things move around them. Near zero the path walks away, and near one it walks in.
> screen: FadeOut, LaggedStart

## 06 · slopes — Why ±1 attract and 0 repels

> **Purpose.** Stability from the derivative. Linearize: p(x*+e) ≈ x* + p′(x*)·e.
> **Logic chain.** Paths leave zero and enter one → *why?* → we already know the answer at one: in scene 03 we put in 1+e and made the error multiplier zero → do the same at zero: p(e) ≈ 1.5e, so the error is multiplied by 1.5 and grows → this is the slow climb we watched from 0.1 → *what is this multiplier in the picture?* → the slope of the curve at the fixed point → back at one the slope is zero, so only the e² term is left and the error collapses → hilltop and valleys.
> **Beats.** p′(0)=1.5 pushes away; p′(±1)=0 (the wish from scene 3) squares the error, so convergence is very fast.
> **Tone.** Nothing new is introduced. This scene repeats the 1+e calculation of scene 03 at a second point and then gives it a picture.
> **Polish pass (novice check).** No "p prime" and no word "derivative". The slope is explained as rise over run on the zoomed-in curve. The 1.5 multiplier is checked against the 0.1 chain from scene 04 (0.1, 0.15, 0.22, 0.33). The "error gets squared" claim is now derived: the e² terms we dropped in scene 03 are all that is left, and they add up to about 1.5 e².
> **Code changes needed (later).** 02 is the calculation p(e) = 1.5e − 0.5e³ ≈ 1.5e near zero. 03 is the zoom-in with a rise-over-run triangle. 05 shows p(1+e) = 1 − 1.5e² − 0.5e³.
> **Numbers used.** 0.05 → 0.075 → 0.112. Errors from 1.2: 0.2 → 0.064 → 0.006.

### slopes 01 <!-- #bcc631 -->
Why does one pull values in, while zero pushes them away? For one, we already know. When we built p, we put in one plus a small error e, and we chose p so that one step multiplies that error by zero.
> screen: Write

### slopes 02 <!-- #527e99 -->
So do the same thing at zero. A value near zero is just a small error e. Put it into p, and we get one point five e, minus one half e cubed. For a small e, the cube is tiny. If e is zero point one, e cubed is only zero point zero zero one. So p gives about one point five e.
This time, one step multiplies the error by one point five, and the error grows.
> screen: FadeIn

### slopes 03 <!-- #c8d4c9 -->
We have seen this growth already. Zero point one went to zero point one five, then zero point two two, then zero point three three. Each value is about one and a half times the one before. That is why zero pushes values away.
On the graph, this multiplier is the slope of the curve. Zoom in at zero, and the curve looks like a straight line. Move e to the right, and it rises by one point five e. Rise over run is one point five.
> screen: Indicate

### slopes 04 <!-- #47c1ea -->
So here is the rule. Near a fixed point, each step multiplies the error by the slope of the curve there. If the slope is bigger than one in size, the error grows and values are pushed away. If it is smaller than one, the error shrinks and values are pulled in.
At zero the slope is one point five, and zero point zero five drifts to zero point zero seven five, then zero point one one, and on.
> screen: Create, FadeIn

### slopes 05 <!-- #719603 -->
At one, the multiplier is zero, so the slope is zero. The curve is flat at the top of its hump. That is our second wish, seen as a picture.
But an error cannot vanish completely in one step. When we built p, we dropped the terms with e squared and e cubed, because they were small. Now put them back.
p of one plus e is three halves times one plus e, minus one half times the full cube, one plus three e plus three e squared plus e cubed. The ones add up to one. The terms with e cancel, as we arranged. What is left is minus one and a half e squared, minus one half e cubed.
So the new error is about minus one and a half times e squared. The minus sign says that we land just below one, whichever side we started on.
Start at one point two. The error goes from zero point two, to zero point zero six, to zero point zero zero six. Each step roughly squares it, which is far faster than shrinking by a fixed factor. The same calculation at minus one gives the same result.
> screen: FadeOut, Create, FadeIn

### slopes 06 <!-- #384fc8 -->
So zero is unstable, like the top of a hill, where the smallest push sends you rolling away. One and minus one are stable, like the bottoms of two valleys, where everything nearby rolls in.
> screen: FadeIn

## 07 · how_big — How big can σ be? (first failure)

> **Purpose.** Find the first threshold by trying a start that 'should' work.
> **Logic chain.** One is a valley, and every start so far fell into it → *but the largest start we tried was 1.3. How big can sigma be?* → 1.5 fine → 1.8 lands below zero and ends at −1 → *why negative?* half the cube has overtaken three halves of the number → *where does that begin?* → factor p to find √3 → *is everything below √3 safe?* → yes: one step lands in (0, 1], then it climbs → *and exactly at √3?* → lands on zero.
> **Beats.** 1.5 works. Predict 1.8 (pause, let the viewer guess). It flips to −1. Factor p(x) = (x/2)(3−x²): the hump crosses the axis at √3. Shaded region shows (0, √3) → +1.
> **Tone.** A real pause before revealing 1.8. Ask the question and wait.
> **Polish pass (novice check).** The step from 1.8 is computed aloud (2.7 minus 2.92), so the negative result is seen, not announced. The mirror rule is shown on one pair of numbers (p(0.216) = 0.32, p(−0.216) = −0.32) before it is used. One sentence says what "ending at minus one" means for a singular value. The factoring is done term by term. "Safe below √3" is argued in two short steps that each point at something on the graph.
> **Numbers used.** 1.5 → 0.5625 → 0.755 → 0.917 → 0.990. 1.8 → −0.216 → −0.319 → −0.462 → −0.644 → −0.832 → −0.960 → −0.998.

### how_big 01 <!-- #b9119e -->
So far every start rolled into the valley at one. But the largest start we tried was one point three, and we don't get to choose sigma. How large can it be before something goes wrong?

### how_big 02 <!-- #0aa92a -->
Go a little bigger, to one point five. That is past the hump, where the curve is already coming down, so the first step drops all the way to zero point five six. But from there it climbs as before, zero point seven five, zero point nine two, and into one. Still fine.
> screen: FadeIn, FadeIn, self.draw

### how_big 03 <!-- #ac882f -->
A little bigger again, one point eight. Before we look, where do you think it ends up?
> screen: FadeOut, FadeIn

### how_big 04 <!-- #8a41e6 -->
Do the step. Three halves of one point eight is two point seven. But half of its cube is two point nine two, which is bigger. Subtract, and the result is negative, minus zero point two one six.
What does p do with a negative number? p has only odd powers, so flipping the sign of the input just flips the sign of the output. Plus zero point two one six goes to plus zero point three two, so minus zero point two one six goes to minus zero point three two.
The negative side is a mirror image of the positive side. Call this the mirror rule. So this value does what its mirror image would do, with the sign flipped. It moves away from zero and settles at minus one.
For a singular value, that has the right size but the wrong sign. This direction ends up reversed.
> screen: FadeIn, self.draw

### how_big 05 <!-- #a51ad9 -->
So what went wrong was the very first step, which landed below the axis. On the graph, that is where the curve, after its hump, comes down and crosses the axis. Past that crossing, p of x is negative.
> screen: FadeOut, FadeOut, Create, Create, GrowFromCenter

### how_big 06 <!-- #de5caa -->
Where is the crossing? Both terms of p contain x over two. Three halves x is x over two times three, and one half x cubed is x over two times x squared. So p of x is x over two, times three minus x squared.
> screen: Write

### how_big 07 <!-- #6c74e8 -->
For a positive x, the first factor, x over two, is positive. So the sign of p comes from the second factor, three minus x squared.
> screen: FadeIn, Indicate

### how_big 08 <!-- #afdac5 -->
Three minus x squared is positive while x squared is below three, and negative once x squared passes three. The change happens at x equals square root of three, about one point seven three.
> screen: FadeIn, Indicate, FadeIn, Flash

### how_big 09 <!-- #d9920c -->
One point five is below square root of three, and it was fine. One point eight is just above it, and it flipped. That matches.
> screen: Indicate

### how_big 10 <!-- #ff045e -->
Then is every start below square root of three safe? Look at the curve between zero and square root of three. It stays above the axis, and its highest point, the top of the hump, is at height one. So wherever we start in this range, the first step lands somewhere between zero and one.
> screen: FadeOut, Create, Indicate, FadeOut

### how_big 11 <!-- #676fd2 -->
And between zero and one, the curve sits above the diagonal. That means the output is bigger than the input, so every step climbs. It cannot climb past one, because the curve never goes higher than one. A value that keeps climbing and can never pass one has to settle somewhere. And the only place where it can settle is a fixed point, so it ends at one.
> screen: FadeIn, self.draw

### how_big 12 <!-- #7d7317 -->
So yes. Every sigma between zero and square root of three ends at one.
> screen: FadeOut

### how_big 13 <!-- #d097e3 -->
And exactly at square root of three, the second factor is zero, so p gives zero. The value lands on the fixed point at zero, and it stays there forever.
> screen: Create, FadeIn, Flash

## 08 · too_big — Try 3, and the size factor

> **Purpose.** Discover √5 as the boundary between shrinking and growing, by comparing |p(x)| with |x|.
> **Logic chain.** 1.8 flipped but still settled → *is a flip all that ever happens?* → 3 explodes → *both flip, so what differs?* size: 1.8 came out smaller, 3 came out bigger → narrow it down: 2.0 still smaller, 2.3 bigger → *where exactly is the turning point?* → compare the size after with the size before: |p(x)| = |x| · (x² − 3)/2, so one step multiplies the size by the "size factor" → check the factor at 2.0 (0.5) and 2.3 (1.14) → factor = 1 gives x² = 5 → at √5 it bounces forever, past it it diverges.
> **Tone.** The size factor is the one new idea; it is reused all through scenes 09–12, so say it slowly.
> **Polish pass (novice check).** The two steps from 3 are computed aloud. The word "size" is defined once (the number without its sign). The size factor is read off the factored form from scene 07, then checked on the two starts already tried, before it is used to find √5. The bounce at √5 is checked with the factored form. "Period two orbit" is kept as a name only, after the plain description.
> **Numbers used.** p(3) = −9; p(−9) = 351. p(2) = −1. p(2.3) = −2.63. Factor at 2.0: (4 − 3)/2 = 0.5. Factor at 2.3: (5.29 − 3)/2 = 1.145. 2.3 → −2.63 → 5.18 → −61.8.
> **Animation.** No y = −x line any more. Beat 05: |p(x)| = |x| · (x²−3)/2 builds up under the factored form, the factor gets a box and the name. Beat 06: one row per start. Beat 07: factor = 1 ⟺ x² = 5, the √5 tick, then the curve is coloured (shrink part, grow part).

### too_big 01 <!-- #1df1e8 -->
So past square root of three, the first step flips the sign. One point eight flipped and still settled, at minus one. Maybe a flip is all that ever happens. Test that with a much bigger start, three.

### too_big 02 <!-- #9b0755 -->
Three halves of three is four point five, and half of three cubed is thirteen point five. Subtract, and we get minus nine. It flipped, as expected. Now the next step. By the mirror rule, minus nine does what nine does, with the sign flipped. Nine goes to thirteen point five minus three hundred sixty four point five, which is minus three hundred fifty one. So minus nine goes to plus three hundred fifty one.
It flips every time, and it gets bigger every time. This one explodes.

### too_big 03 <!-- #5ff1d3 -->
Both one point eight and three flip, so the difference must be in the size, meaning the number without its sign. One point eight came out at size zero point two, smaller than it went in. Three came out at size nine, bigger than it went in.
So somewhere between them, shrinking turns into growing. Narrow it down. Two point zero goes to minus one, so its size is one. That is still smaller.

### too_big 04 <!-- #292d3e -->
But two point three goes to minus two point six three. Its size is bigger than where it started. So the turning point is somewhere between two point zero and two point three.

### too_big 05 <!-- #26b539 -->
Where exactly is the turning point? Compare the size after a step with the size before. Use the factored form. p of x is x over two, times three minus x squared.
So the size of p of x is the size of x, times the size of three minus x squared, over two. Past square root of three, that second part is x squared minus three, over two. Call it the size factor. Each step multiplies the size by this factor.

### too_big 06 <!-- #82b56f -->
Check it with the starts we tried. At two point zero, the factor is four minus three, over two, which is one half. And two did go to size one. At two point three, the factor is about one point one four, and two point three did come out bigger.
So a factor below one means flip and shrink. A factor above one means flip and grow.

### too_big 07 <!-- #25d1c3 -->
The turning point is where the factor is exactly one. That means x squared minus three equals two, so x squared equals five. The turning point is square root of five, about two point two four, and it does sit between two point zero and two point three. On the curve, between square root of three and square root of five a step shrinks the size, and beyond square root of five it grows.

### too_big 08 <!-- #e6b98a -->
What happens exactly at square root of five? Use the factored form. x over two, times three minus five, is minus x. So square root of five goes to minus square root of five. By the mirror rule, that goes straight back to plus square root of five. On the picture, the path becomes a square.

### too_big 09 <!-- #3840ae -->
So square root of five neither settles nor explodes. It jumps back and forth between plus and minus square root of five forever. This is called a period two orbit, because it repeats every two steps.

### too_big 10 <!-- #d9c1b8 -->
And past square root of five, every step flips and grows. Two point three goes to minus two point six three, then five point one eight, then minus sixty one point eight. Like three, it explodes.

## 第 2 集片尾 · ep2_closing

> **[10-04] 新增。** 画面：一条数轴，√3 以下涂 teal，√5 以上涂红，中间留灰，1.8 和 2.0 两个点标在灰色段里。
> 1.8 和 2.0 都在缺口里（√3 ≈ 1.73），而且都到了 −1，所以这里的钩子是"是不是都这样"。

### ep2_closing 01 <!-- #753a38 -->
So now we have two thresholds. Below square root of three, every start ends at one. Beyond square root of five, every start explodes.
Between them there is a gap, and we have only tried two starts in it, one point eight and two point zero. Both ended at minus one. Does every start in the gap do that? That is next time.

## 第 3 集 · ep03_the_gap.py（09–14）

## 第 3 集开头 · ep3_recap

> **[10-04] 新增。** 片头卡念："Newton–Schulz. Between square root of three and square root of five."
> 这一集要用到的东西全部来自上一集，开头各说一句，并且把式子重新放上屏幕：p(x)、镜像规则 p(−x) = −p(x)、
> size factor 那一行 |p(x)| = |x| · |x²−3|/2（D1，留在角上）。画面同时把 p 的图和 √3、√5 两个刻度画出来。

### ep3_recap 01 <!-- #ea4be3 -->
We are following one number as we apply p again and again. p of x is three halves x, minus one half x cubed.
Here is what we know so far. A negative value moves exactly like its positive twin, with the sign flipped. We called that the mirror rule.
Past square root of three, p of x is negative, so a step flips the sign.
And one step multiplies the size of the value by the size factor, x squared minus three, over two.

## 09 · the_gap — Follow three starts into the gap

> **Purpose.** See, on the cobweb picture, that starts between √3 and √5 do not all end the same way, and why: the number of flips before the value gets inside √3.
> **Logic chain.** In the gap every step flips and the size factor is below one → *so the size keeps shrinking; it must get inside √3, and inside we know everything (positive → +1, negative → −1)* → so just follow a start until it is inside and see on which side it arrives → cobweb for 2.0 (one flip, −1), 2.2 (two flips, +1), 2.23 (three flips, −1) → odd number of flips ends at −1, even at +1 → three starts are not the whole story: colour every start (the strip is the overview) → stripes → two open questions: where does the flip count change, and do the stripes fill the whole gap?
> **Tone.** Exploring. Nothing is claimed before it has been seen on the cobweb.
> **Polish pass (novice check).** Each start is followed step by step with its numbers; "inside" always means inside √3. The colour strip comes only after the three starts, as the whole picture, and its colours are named before it is read.
> **Numbers used.** 2.0 → −1. 2.2 → −2.02 → +1.11 → … → +1. 2.23 → −2.20 → +2.02 → −1.10 → … → −1.
> **Animation.** The p graph with the gap marked; the plan (inside √3: teal half, gold half); three cobwebs, each segment drawn when its number is said, with one row per start in the panel; the odd/even rule; then the colour strip and the zoom next to √5.

### the_gap 01 <!-- #1b30eb -->
So below square root of three, everything goes to one, and beyond square root of five, everything explodes. That leaves the gap between them. In the gap, every step flips the sign.
What about the size? One step multiplies it by the size factor, x squared minus three, over two. At the left end of the gap, x squared is three, so the factor is zero. At the right end, x squared is five, so the factor is one. In between, x squared is between three and five, so the factor is between zero and one.
Multiplying by a number between zero and one makes a size smaller. So in the gap, the size of p of x is less than the size of x. Every step brings the value closer to zero.
> **[10-04] D2.** 上屏三行，各挂在一句上：(x²−3)/2 在 x²=3 时 = 0、在 x²=5 时 = 1；0 < (x²−3)/2 < 1；|p(x)| < |x|。
> 建议拆成三个 say()（按上面的三段）。

### the_gap 02 <!-- #94820b -->
That suggests a plan. Suppose the size shrinks far enough to drop below square root of three. Inside square root of three we already know everything. A positive value goes to plus one. By the mirror rule, a negative value goes to minus one.
So we only have to follow a start until it gets inside, and see on which side it arrives.
> **[10-04] D3.** 原来说 "sooner or later it drops below"，这一点要到 12 场才证出来，所以改成 "Suppose"。
> 上屏：数轴上 (−√3, √3) 一段，右半 teal 标 +1，左半 gold 标 −1。

### the_gap 03 <!-- #cfa696 -->
Try it on the cobweb picture. Start at two point zero. Go down to the curve, which gives minus one. Then across to the diagonal. Minus one is inside, on the negative side, and it is already a fixed point. So two point zero ends at minus one, after one flip.

### the_gap 04 <!-- #e5a13d -->
Now two point two. Down to the curve, at minus two point zero two. That is smaller in size than two point two, but it is still outside.
So go across to the diagonal and step again. This time the curve sends it up, to plus one point one one. Now it is inside, on the positive side, and from there it settles at plus one. Two flips, and a different ending.

### the_gap 05 <!-- #1a1355 -->
And two point two three, just a little further out. Minus two point two zero. Then plus two point zero two. Then minus one point one zero. It takes three flips to get inside, it arrives on the negative side, and it ends at minus one.

### the_gap 06 <!-- #940710 -->
So the starts in the gap do not all end the same way. What matters is how many flips it takes to get inside. Every start here is positive, and each flip changes the sign. After an odd number of flips the value arrives negative, and ends at minus one. After an even number it arrives positive, and ends at plus one.

### the_gap 07 <!-- #e42be0 -->
Three starts are not the whole story, so here is every start at once. Take each start from zero to two point four, run the iteration, and color it by where it ends. Teal means plus one, gold means minus one, and red means it explodes.

### the_gap 08 <!-- #b4b6e4 -->
Below square root of three it is all teal, as we showed. The gap begins gold. That is where two point zero sits, with its one flip. Then comes a thin teal stripe, which holds two point two. And then more stripes, each thinner than the last, squeezed up against square root of five.

### the_gap 09 <!-- #610196 -->
So each stripe is a flip count. One flip, two flips, three flips, and so on. Two things are still open. Where exactly does one flip turn into two, and two into three? And do these stripes really fill the whole gap, all the way up to square root of five?

## 10 · first_boundary — Fold the curve, find b₁

> **Purpose.** Turn the problem into one about sizes only, and find where the first stripe ends: |p(b₁)| = √3, b₁ ≈ 2.148.
> **Logic chain.** Sign and size together are messy → the mirror rule lets us separate them: the size follows |x| → |p(x)|, and every step from outside √3 is one flip → fold the curve up (the graph of the size after one step) → compare with the diagonal: below it between √3 and √5 (|p(x)| < |x|, shrinks), above it beyond √5 (grows), they meet at √5 → the cobweb works on the folded picture (2.2 → 2.02 → 1.11) → zoom into the gap → one flip exactly when the first step lands below the level √3 → the folded curve reaches that level at one start: b₁ → everything from √3 to b₁ is the first stripe (one flip, ends at −1) → *where is b₁?* b(b² − 3)/2 = √3, try 2.1 and 2.2, close in on 2.148 → check 1.8, 2.0, 2.2.
> **Tone.** Slow; the folded picture is the tool for the rest of the section.
> **Polish pass (novice check).** "Fold" is shown, not only said. The comparison is always "size after" against "size before" (the diagonal), never the line y = −x. The name b is explained (b for boundary). Trying values is shown with two actual tries.
> **Numbers used.** 2√3 ≈ 3.46. 2.1³ − 3·2.1 = 2.96. 2.2³ − 3·2.2 = 4.05. b₁ ≈ 2.148.
> **Animation.** Mirror rule and the two bookkeeping lines; the part of the curve below the axis flips up; shrink/grow parts coloured, dot at √5; cobweb on the folded curve; then the stretched picture of the gap (x from 1.65 to 2.3) with the level line √3, the point b₁, the first stripe on the x-axis and where it lands on the y-axis; the equation and the two tries.

### first_boundary 01 <!-- #8c9a27 -->
Following the sign and the size together on this picture gets messy. But the mirror rule lets us take them apart. A negative value moves exactly like its positive twin, with the sign flipped.
So the size follows a rule of its own. The next size is the size of p of x. And the sign we can simply count. Every step that starts outside square root of three is one flip.

### first_boundary 02 <!-- #81ad2b -->
So fold the picture. We only need positive sizes, so look at the right half. Wherever the curve dips below the axis, flip that part up. This folded curve answers one question. If the size is x now, what is the size after one step?

### first_boundary 03 <!-- #0b2bd6 -->
Now compare it with the diagonal, where the size would stay the same. Between square root of three and square root of five, the folded curve is below the diagonal. The size after the step is smaller than the size before. Beyond square root of five it is above the diagonal, and the size grows.
They meet exactly at square root of five.

### first_boundary 04 <!-- #5dfaf7 -->
And the cobweb works on the folded picture too. Start at two point two. Up to the folded curve, at two point zero two. Across to the diagonal, and then to the curve again, at one point one one.
Now we are inside, and the size climbs to one. Two of these steps started outside square root of three. So two flips, and the sign ends up positive.

### first_boundary 05 <!-- #d8a8c8 -->
Now zoom in on the gap, and stretch it sideways so we can see. Start with the simplest case. Which starts get inside in a single step? Those whose size after one step is below square root of three. So draw that level as a horizontal line.
How often does the folded curve cross this line? Look at its formula, x times the size factor. As x moves to the right through the gap, x gets bigger, and the size factor gets bigger too. So their product only goes up. It starts at height zero, at square root of three, and it ends at height square root of five. Our line lies between those two heights. And a curve that only goes up passes each height once. So it crosses the line at exactly one point.
Call that start b one, b for boundary. Its size after one step is exactly square root of three. And in the gap, p is negative. So p of b one is minus square root of three.
Now take any start between square root of three and b one. It is to the left of the crossing, so its step lands below the line, on the negative side. That is somewhere between minus square root of three and zero. It is inside, and it is negative, so it ends at minus one. One flip. This is the first stripe.
> **[10-04] D4–D6，手写稿标了 "explain closely" 的地方。** 拆成四个 say()（按上面的四段）。
> 上屏：(1) 问题 |p(x)| < √3 ？和水平线；(2) x ↑、(x²−3)/2 ↑ ⇒ |p(x)| ↑，曲线两端标高度 0 和 √5，镜头推到交点；
> (3) |p(b₁)| = √3，然后变成 p(b₁) = −√3；(4) (√3, b₁) → (−√3, 0) → −1，x 轴上的第一条条纹搬到纵轴上。
> 新断言：|p| 在 [√3, √5] 上单调递增。

### first_boundary 06 <!-- #f2aea1 -->
Where is b one exactly? Its size after one step must be square root of three. With the size factor, that is b, times b squared minus three, over two, equals square root of three. Multiply by two, and we get b cubed, minus three b, equals two times square root of three, which is about three point four six.
There is an exact formula for this b, built from cube roots, but it does not tell us much. So just try values. Two point one gives two point nine six, which is too small. Two point two gives four point zero five, which is too big. Closing in between them gives about two point one four eight.

### first_boundary 07 <!-- #6b9f0a -->
That fits what we saw. One point eight and two point zero are both below b one, in the first stripe, and both ended at minus one. Two point two is above b one. Its first step did not get inside, and it needed a second flip.

## 11 · basins — Each stripe lands on the one before

> **Purpose.** Reduce every unknown stripe to the one already solved: one step (in size) carries stripe n onto stripe n − 1, so it needs exactly one more flip.
> **Logic chain.** Starts above b₁ do not get inside in one step → *but we need not follow them all the way*: if the first step lands in the first stripe, we already know the rest: one more flip → which starts land there? the folded curve passes through the band √3..b₁ on the vertical axis; it leaves it at height b₁: call that start b₂ → b₁..b₂ is the second stripe: two flips, ends at +1 → check with 2.2 (size 2.02 is in the first stripe) → the same step again gives b₃ and the third stripe → values of b₁, b₂, b₃ creep up to √5 → all stripes on one bar: stripe n flips n times, odd → −1, even → +1 → zoom: the pattern repeats → why so thin: near √5 one step stretches distances by six, so each stripe is a sixth of the one before.
> **Tone.** The "land on what we already know" step is the heart of the section; give it time, then let the repeats go faster.
> **Polish pass (novice check).** Each new stripe is defined by where it lands, read off the picture, before any formula. The factor six comes from two starts already seen (2.20 and 2.23), not from a derivative.
> **Numbers used.** b₁ ≈ 2.148, b₂ ≈ 2.221, b₃ ≈ 2.234, √5 ≈ 2.236. |p(2.20)| = 2.02, |p(2.23)| = 2.20; 0.03 in, 0.18 out.
> **Animation.** The stretched gap picture; the first stripe is copied onto the vertical axis as a band; the curve leaves the band at b₂; the path of 2.2; the second band and b₃; the values; then the bar with all stripes and the zoom towards √5; the two starts for the factor six.

### basins 01 <!-- #9eed20 -->
Now the starts above b one. Their first step does not get inside. But we do not have to follow them all the way. Suppose the first step lands, in size, somewhere in the first stripe. We already know the first stripe. From there it takes one more flip to get inside. So such a start flips exactly twice.

### basins 02 <!-- #c00dd2 -->
Which starts are those? Read it off the picture. On the vertical axis, the first stripe is the band of sizes from square root of three up to b one. The folded curve only goes up, so it passes through that band once. It enters at b one, where its height is square root of three. And it leaves where its height is exactly b one. Call that point b two.
So the size of p of b two is b one. The start is positive and the step flips it, so p of b two is minus b one.
Now take any start between b one and b two. Its step lands between minus b one and minus square root of three. That is the first stripe, mirrored. From there it takes one more flip, so two flips in all, an even number. It ends at plus one. This is the second stripe.
> **[10-04] D7.** 拆成三个 say()。上屏：|p(b₂)| = b₁ 变成 p(b₂) = −b₁；(b₁, b₂) → (−b₁, −√3)。

### basins 03 <!-- #d758fb -->
Check it with two point two. It sits between b one and b two. Its first step has size two point zero two. And two point zero two lies between square root of three and b one, in the first stripe.
So one more flip, and it is inside. That is the two flips we counted, and it ended at plus one.

### basins 04 <!-- #1866f8 -->
And the same step works again. Starts that land in the second stripe need one flip more than the second stripe does, so three flips. The curve leaves that band where its height is b two. Call that point b three. So p of b three is minus b two. The starts between b two and b three are the third stripe, and they end at minus one.
Put the three edges next to each other. p of b one is minus square root of three. p of b two is minus b one. p of b three is minus b two. One step sends each edge to the edge before it, with the sign flipped.
And nothing stops us from going on. So we get a whole list of edges. Square root of three, then b one, b two, b three, and so on. Each new stripe is carried onto the stripe before it, so it needs exactly one more flip.
> **[10-04] D8.** 拆成三个 say()。上屏：三个式子竖排 p(b₁) = −√3、p(b₂) = −b₁、p(b₃) = −b₂，然后收成一行 p(b_{n+1}) = −b_n；
> 数列 √3, b₁, b₂, b₃, … 排成一排。讲 b₃ 时镜头推到 √5 附近（b₃ 和 √5 只差 0.002）。

### basins 05 <!-- #19bd55 -->
Each edge is found like b one, by trying values. b one is about two point one four eight. b two is about two point two two one. b three is about two point two three four. They creep up toward square root of five, which is two point two three six.

### basins 06 <!-- #6b2a00 -->
So here are all the stripes on one line. Stripe number n flips n times. An odd n ends at minus one, and an even n ends at plus one. That is the striped picture we saw.

### basins 07 <!-- #477d72 -->
The stripes pile up against square root of five. Zoom in, and the same pattern shows up again and again.

### basins 08 <!-- #30781b -->
Why do the stripes get thin so quickly? Near square root of five the folded curve is steep. From two point two to two point two three, the start moves by zero point zero three.
But the size after the step moves from two point zero two to two point two zero, which is zero point one eight. That is six times as far.
So one step stretches a stripe to about six times its width.
Where does the six come from? Do what we did at zero and at one. Put square root of five plus a small e into p, and drop the terms with e squared and e cubed. Out comes minus square root of five, minus six e. So next to square root of five, one step multiplies a small distance by six, exactly.
And the stretched stripe has to fit onto the stripe before it. So each stripe is about a sixth as wide as the one before, and the closer to square root of five, the closer to exactly a sixth.

## 12 · boundary_points — Do the stripes fill the gap? And the edges

> **Purpose.** Check that the method covers everything between √3 and √5, and say what happens to the edges themselves.
> **Logic chain.** *Is there a last piece next to √5 that no stripe reaches?* → look at how the edges were found: across to the folded curve, up to the diagonal, across again: a staircase between the curve and the diagonal → every step goes right and never passes √5, so the edges close in on some point → there the staircase has no room, so the curve touches the diagonal → in the gap that only happens at √5 → so the edges come as close to √5 as we like, every start below √5 is in some stripe → *and the edges themselves?* b₁ lands exactly on −√3, then on 0 → b₂ lands on −b₁, one step more; every edge ends on 0 → should that worry us? no: single points, and 0 is the top of the hill; the tiniest nudge rolls to ±1.
> **Tone.** A short proof, then a calm closing remark.
> **Polish pass (novice check).** No limit notation; "close in on a point" and "no room left" carry the argument. The edge paths are shown as hops on a number line.
> **Numbers used.** b₁ → −√3 → 0. b₂ → −b₁ → √3 → 0. b₃ → −b₂ → b₁ → −√3 → 0.
> **Animation.** The corner of the gap picture next to √5 (x from 2.05 to 2.26); the staircase drawn step by step; the dot at √5; then three number lines with the hopping edges and their chains; two nudged starts rolling to −1 and +1.

### boundary_points 01 <!-- #8ff930 -->
One question is still open. Do the stripes really fill the whole gap? Or is there a last piece, right next to square root of five, that no stripe ever reaches?
The stripes end at the edges. So this is a question about our list of edges, square root of three, b one, b two, and so on. Do the edges get all the way up to square root of five?
Look at how we found them. Here is the corner of the picture next to square root of five. Start at the height square root of three, and go across to the folded curve. That is b one. Go up to the diagonal, and across to the curve again. That is b two. The edges are a staircase, squeezed between the curve and the diagonal.
> **[10-04] D9.** 拆成三个 say()。第二段时把问题单独放在屏幕上：√3, b₁, b₂, … → √5 ？然后停 1.5 秒。
> 角落图从上一张图连续推进过来，不清屏。

### boundary_points 02 <!-- #fbb48b -->
First, can an edge ever reach square root of five? The folded curve only goes up, and it gets to the height square root of five only at the very end of the gap. Each new edge is where the curve reaches the height of the edge before. If that height is below square root of five, the curve reaches it before the end of the gap. So the new edge is below square root of five as well. The list starts at square root of three, which is below. So every edge stays below square root of five.
Next, does the list always go up? One step takes each edge to the size of the edge before it. Every edge is in the gap, and in the gap a step makes the size smaller. So the edge before is the smaller one. Each edge is bigger than the last.
So the edges keep rising, and they can never pass square root of five. A list of numbers that only rises, under a ceiling it cannot pass, has to settle toward some value. Call that value L.
Where is L? Far down the list, an edge and the one after it are both as close to L as we like. One step takes the later one to the size of the earlier one. Now p is a polynomial, so a tiny change in the input makes only a tiny change in the output. So one step from L itself lands as close as we like to a value of size L. And a fixed number that is as close as we like to L can only be L. So one step takes L to a value of the same size, L. That means the size factor at L is exactly one. We have met that before. L squared minus three, over two, equals one, so L squared is five. L is square root of five. On the picture, that is where the folded curve meets the diagonal.
So the edges come as close to square root of five as we like. Every start below square root of five is passed by some edge, so it lies in some stripe. The stripes fill the whole gap. We now know where every start in the gap ends up.
> **[10-04] D10–D14.** 拆成五个 say()（按上面的五段）。上屏，一段一行，写在楼梯图右边：
> (1) b_n < √5 ⇒ b_{n+1} < √5；(2) b_n = |p(b_{n+1})| < b_{n+1}；(3) √3 < b₁ < b₂ < … < √5 ⇒ b_n → L；
> (4) L · (L²−3)/2 = L ⇒ (L²−3)/2 = 1 ⇒ L² = 5 ⇒ L = √5，同时在图上点亮 (√5, √5)；(5) 所有条纹一起亮一次。
> 顺序是先有界、后递增：b_{n+1} 存在要用到 b_n < √5。
> **唯一不证明的事实**：只升且有上界的数列会收拢到某个值（第三段）。p 的连续性现在说了一句（多项式：输入变一点，输出只变一点）。
> 新断言：b_n 递增、b_n < √5、(√5² − 3)/2 = 1。

### boundary_points 03 <!-- #62fe7d -->
And what about the edges themselves? Take b one. Its first step lands exactly on minus square root of three. And we know what happens at square root of three. The next step gives exactly zero, and by the mirror rule the same holds for minus square root of three. So b one ends on zero, and stays there.

### boundary_points 04 <!-- #ba4456 -->
b two lands on minus b one, and from there it follows the path of b one with the sign flipped. So it takes one step more. And b three takes one step more again. Every edge reaches plus or minus square root of three after a few steps, and then it sits on zero forever.
An edge never reaches one or minus one.

### boundary_points 05 <!-- #ea416e -->
Should that worry us? Not much. Each edge is a single point, and zero is the top of the hill. Move the start by the tiniest amount, and it is inside a stripe on one side or the other, and it rolls down to plus one or minus one.

## 13 · summary — The complete answer

> **Purpose.** One table of fates for every starting σ. Say it once, plainly.
> **Logic chain.** Walk the number line left to right, in the order the viewer discovered it: below √3, at √3, the gap, at √5, beyond. Each line carries the one-phrase reason we found for it. End on "only the first case is what we wanted", which hands over to back_to_matrix.
> **Polish pass (novice check).** Each case now repeats its reason in a few words (first step lands between zero and one; flips and shrinks; flips and grows), so the table is a reminder of arguments already seen and not a list to memorise.

### summary 01 <!-- #4f6d22 -->
Now we can answer the question we started with. Where does a positive sigma end up when we apply p again and again? Here is the full answer to part (e), from left to right along the number line.
> screen: FadeIn, Create

### summary 02 <!-- #30bd28 -->
Below square root of three, the first step lands between zero and one, and from there sigma climbs to plus one. Exactly at square root of three, it lands on zero and stays there.
> screen: FadeIn, FadeIn

### summary 03 <!-- #40b2a0 -->
Between square root of three and square root of five, each step flips the sign and shrinks the size, until the value is inside square root of three. An odd number of flips ends at minus one, and an even number ends at plus one. That gives the stripes. Their edges are single points that end on zero.
> screen: FadeIn, FadeIn

### summary 04 <!-- #74378b -->
Exactly at square root of five, sigma jumps between plus and minus square root of five forever. And beyond square root of five, each step flips and grows, so it explodes.
Out of all these cases, only the first one is what we wanted.
> screen: FadeIn, FadeIn

## 14 · back_to_matrix — So what do we do with W?

> **Purpose.** Close the loop: divide W by its Frobenius norm so every singular value is below √3, then iterate; all σ go to 1 and the ellipse becomes a circle.
> **Logic chain.** Only "below √3" is safe → *but a real W has singular values anywhere* → so shrink W first → *does shrinking change the answer?* no: dividing W by a number only divides the σ's, U and Vᵀ stay → *divide by what?* the largest σ would be ideal, but finding it needs the SVD → the Frobenius norm is cheap and never smaller than the largest σ → every σ now sits in (0, 1] → all walk to one → W becomes U Vᵀ, the circle from scene 1.
> **Tone.** Practical and short. End on the picture of the circle.
> **Polish pass (novice check).** Says why dividing W is harmless (the target U Vᵀ does not depend on the sizes). Says how the Frobenius norm is computed, why it is cheap, and why it is at least as large as the biggest σ (its square already contains that σ squared, plus more). The 2.9 example is carried through the division (2.9 / 3.45 = 0.84). The slow start of small σ's is tied to the factor 1.5 from scene 06. Second read as a novice: "the step" in beat 06 was ambiguous (number step or matrix step), so the matrix step from scene 03 is now said in full, with the reminder that it sends every σ through p once; "the middle is now all ones" links back to U Σ Vᵀ. "Gold stripe" relies on the colour strip of scene 09 (gold = ends at −1).
> **One fact taken on trust.** "The sum of the squared entries of W equals the sum of the squared singular values" is stated, not shown. It is standard, and proving it would start a new topic.
> **Code changes needed (later).** If the on-screen singular values differ from the ones implied here (largest 2.9, norm 3.45), change the two numbers in beats 02, 04, 05.

### back_to_matrix 01 <!-- #8a4aa3 -->
We wanted every singular value to end at one, and that only happens for starts below square root of three. But a real W can have singular values anywhere, some of them far above square root of five.
> screen: Create, FadeIn, FadeIn, LaggedStart

### back_to_matrix 02 <!-- #989d50 -->
This one, at two point nine, would explode. And one that sits in a gold stripe would end at minus one, with its direction reversed. So before we iterate, we have to bring every singular value down.
That is easy to do. Divide W by a number, and every singular value is divided by that number, while U and V transpose stay exactly the same. Our target, U times V transpose, does not change at all.
> screen: Create, FadeIn

### back_to_matrix 03 <!-- #dd42cc -->
Which number? Dividing by the largest singular value would be ideal, because then everything is at one or below. But finding the largest singular value takes the very SVD we are trying to avoid.
There is a cheap stand-in, called the Frobenius norm. Square every entry of W, add them all up, and take the square root. That only needs the entries, so it costs almost nothing.
And it is big enough. Here is why. The sum of the squared entries of a matrix is the sum of the squared lengths of its columns. A rotation on the left turns every column without changing its length, so that sum stays the same. A rotation on the right does the same to the rows. So W, which is U, sigma, V transpose, has the same sum as sigma alone.
And sigma holds only the singular values, so the sum of the squared entries equals the sum of the squared singular values. That sum already contains the largest one squared, plus more. So its square root, the Frobenius norm, is never smaller than the largest singular value.
> screen: FadeOut, Write

### back_to_matrix 04 <!-- #39d19b -->
Here the Frobenius norm comes out to about three point four five, a bit more than our largest singular value, two point nine. Divide every sigma by it.
> screen: FadeIn

### back_to_matrix 05 <!-- #2f01eb -->
Two point nine becomes zero point eight four, and the others are smaller still. Now every singular value sits between zero and one, safely below square root of three.
> screen: *[d.animate.move_to

### back_to_matrix 06 <!-- #f6864f -->
Now apply our matrix step, three halves W, minus one half W, W transpose, W, again and again. It needs nothing but matrix products. And each time, every singular value goes through p once.
So each singular value climbs to plus one. The small ones start slowly, growing by about one and a half times per step as zero point one did, but they all arrive. The one exception is a singular value of exactly zero. Zero is a fixed point, so it stays at zero.
And all along, U and V transpose never changed. So when no singular value is zero, the middle is now all ones, and W has become U times V transpose.
> screen: FadeIn

### back_to_matrix 07 <!-- #40417c -->
The ellipse has become a circle. All it took was matrix products, and a cubic built from two simple wishes.

## closing — The method in two lines, and the answer to the title

> **Purpose.** The closing card, right after the ellipse has become a circle. Not a recap list: scene 13 already gave the full table.
> **Logic chain.** The circle stays on screen → the whole method is two lines (divide once, then repeat the step) → the title's question, answered in one sentence.
> **Opening card.** The title card has no line here. The voice only says the title, "Newton–Schulz. Where does a singular value go?" (set in `opening()` in the code).

### closing 01 <!-- #a711a6 -->
So the whole method is two lines. Divide W by its Frobenius norm, once. Then apply the step, again and again.

### closing 02 <!-- #bf713b -->
And where does a singular value go? After that first division, every one of them goes to one.
