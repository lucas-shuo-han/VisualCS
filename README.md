# VisualCS

用 3Blue1Brown 风格的动画讲计算机课程。第一个系列：**CS61C · RISC-V**（伯克利 CS61C 中 RISC-V 指令集部分，按 Fall 2026 课程笔记编排）。

*3Blue1Brown-style animated lectures on computer science. First series: the RISC-V unit of UC Berkeley's CS61C, following the Fall 2026 course notes. Every episode comes in **Chinese and English**, with a voice-over and burned-in subtitles.*

动画用 [Manim Community](https://www.manim.community/) 制作：深色背景、按字段着色的指令编码、一步步执行的寄存器和内存。
每集有中文、英文两个版本，都带神经网络语音旁白和烧录字幕，另附同步的 `.srt` 字幕文件。

## CS61C RISC-V 系列 · 14 集

| 集 | 标题 | Title | 内容 |
|---|---|---|---|
| 1 | 机器结构与 RISC-V | Machine Structures & RISC-V | 抽象层次；冯·诺依曼结构；ISA；RISC 与 CISC；RISC-V 的由来 |
| 2 | 从 C 到汇编 | From C to Assembly | ISA 是软硬件的契约；32 个寄存器与 ABI 名字；x0；`add` / `sub` / `addi`；伪指令 `mv` `li` `nop` |
| 3 | 内存 | Memory | 字节寻址、字与对齐、小端序；`lw` / `sw` 与 `偏移(基址)`；`A[i]` 的偏移是 `4×i`；`lb` / `lbu` 的符号扩展与零扩展 |
| 4 | 汇编实战：表达式与数组 | Assembly in Practice | 寄存器没有类型；表达式的翻译；栈上的数组与对齐；字节与符号 |
| 5 | 决策与循环 | Decisions & Loops | PC；六条条件分支；if-else 的“条件取反”；`and/or/xor` 与 `sll/srl/sra`；逐步执行一个数组求和循环 |
| 6 | 控制流进阶 | Control Flow Patterns | 取指–执行循环；`slt` 系列比较指令；各种循环的套路 |
| 7 | 函数调用 | Function Calls | 调用函数的六个步骤；`jal` / `jr ra`；调用者保存与被调用者保存；栈与压栈出栈；序言与尾声 |
| 8 | 递归与栈帧 | Recursion & Stack Frames | `jal` / `jalr`；递归阶乘逐帧展开；叶子函数；栈帧 |
| 9 | 指令格式（上） | Instruction Formats, Part 1 | 存储程序；R / I / S 型逐位编码；为什么 S 型要把立即数拆开 |
| 10 | 读懂机器码 | Reading Machine Code | 反汇编；字段复用；I 型全家；汇编 ↔ 机器码的互译清单 |
| 11 | 指令格式（下） | Instruction Formats, Part 2 | PC 相对寻址；B 型的“打乱”位序；`lui` + `addi` 的符号扩展陷阱；J 型与 `auipc` + `jalr` |
| 12 | 寻址方式与大常数 | Addressing & Big Constants | 各种寻址方式；远跳转；`li` 的展开；手工汇编 |
| 13 | CALL | CALL | 编译、汇编（伪指令展开、两遍扫描、符号表与重定位表）、链接、加载 |
| 14 | Hello World 的一生 | The Life of Hello World | 目标文件；符号表；重定位；静态与动态链接 |

成片在 [`videos/cs61c-riscv/zh/`](videos/cs61c-riscv/zh/) 与 [`videos/cs61c-riscv/en/`](videos/cs61c-riscv/en/)（1080p30）。
全部旁白文字见 [`cs61c/riscv/SCRIPT.md`](cs61c/riscv/SCRIPT.md)（中文）与 [`cs61c/riscv/SCRIPT.en.md`](cs61c/riscv/SCRIPT.en.md)（English）。

## CS182 · Newton–Schulz 迭代（第五次讨论课）

| 集 | Title | 内容 |
|---|---|---|
| 1 | Newton–Schulz: You Could Have Invented It | 从“椭圆变圆”讲起：为什么要把每个奇异值推到 1；SVD 太慢，只用矩阵乘法能做什么；Wᵀ W 丢了 U、W Wᵀ W 保住两个旋转；两个愿望定出 p(σ) = 3/2 σ − 1/2 σ³ |
| 2 | Newton–Schulz: Where Does a Singular Value Go? | 先试简单的数，再看蛛网图、不动点与斜率；追问“σ 能多大”发现 √3，追问“更大会怎样”发现 size factor 和 √5 |
| 3 | Newton–Schulz: Between √3 and √5 | 缺口里每步翻号且变小；按翻号次数交替通向 −1、+1 的条纹；边界点 p(b_{n+1}) = −b_n，单调有界收敛到 √5，条纹铺满缺口；总表；迭代前先按 Frobenius 范数缩放 |

只做英文版（英文撰写，英文配音）。成片在 [`videos/cs182-newton-schulz/`](videos/cs182-newton-schulz/)（1080p30，字幕在同名 `.srt` 里，不烧进画面）。
代码在 `cs182/newton-schulz/`：三集各一个 `epNN_*.py`，共用的数学、颜色和画图辅助在 `ns_common.py`，kit 是 `manim_kit.py`。

本系列的设置都在 `cs182/newton-schulz/series.py`：
- `TTS`：配音引擎、音色、语速。现在是 edge-tts 的 `en-US-AndrewNeural`，语速 −10%。换音色前可以用 `python audition.py` 生成候选试听（`preview/voices/`）。
- `PACE`：句间、段间、拍间的停顿秒数。配音是逐句合成的，narration.md 里一拍正文的换行就是一段，段间停顿更长。
- `TEXT_FONT = "latex"`：画面上的文字、数字、公式全部由 LaTeX 排版，只有一种字体。

```bash
.venv/bin/python .claude/skills/notes-to-3b1b-video/scripts/render.py cs182/newton-schulz --out videos/cs182-newton-schulz   # 三集成片
.venv/bin/python cs182/newton-schulz/preview.py 9            # 单场带配音预览（场景编号 1–14，或名字，或 ep2、all）
```

**改旁白和叙事逻辑（不用碰动画代码）**：所有字幕/配音文字都在 [`cs182/newton-schulz/narration.md`](cs182/newton-schulz/narration.md)。
- 正文 = `###` 标题下的普通行，就是屏幕字幕和配音。`speak:` 行是只给配音用的读法。
- 注释 = 以 `>` 或 `//` 开头的行和 `<!-- -->`，渲染时忽略，可以随便写想法。
- 每个场景开头有叙事逻辑注释（目的、节拍、语气、待定选择），文件开头有“观众每一幕知道什么、想问什么”的表格。
- 不要改 `### 场景 编号 <!-- #哈希 -->` 这种标题行。
- 改完先检查，再出预览（只有改过的句子会重新配音）：

```bash
.venv/bin/python cs182/newton-schulz/narration.py check      # 也会检查 cue() 等待的那几个词还在不在
.venv/bin/python cs182/newton-schulz/preview.py why_p
```

调整场景顺序、增删一个节拍要改动画代码：把想法写在该场景的注释里，让 Claude 来改。代码里故意改了某句 say() 的文字之后，运行 `narration.py rebind` 让 narration.md 的标题重新对上代码（保留文件里的措辞）；不要运行 `narration.py sync`。

## 目录结构

```
cs61c/riscv/series.py      剧集列表：顺序、中英文标题、输出文件名
cs61c/riscv/manim_kit.py   共享组件：带字幕计时与配音的 NarratedScene、cue()、代码高亮、寄存器、内存、指令位字段……（skill 的副本）
cs61c/riscv/epNN_*.py      每集一个 Scene（中文撰写；一个 say() 是一段 2–4 句的旁白，cue() 在语音念到某个短语时播放动画）
cs61c/riscv/i18n/epNN.py   每集的英文：{中文字符串: English}，旁白按“念出来”的英文改写，不是逐句翻译
cs61c/riscv/tts.py         语音旁白：把字幕改写成适合朗读的形式，再合成（skill 的副本，缓存在 media/tts/）
cs61c/riscv/say_as.py      本课程的读法：寄存器、指令名、十六进制、人名、文件名……
tools/beats_apply.py       把逐句的 say() 合并成旁白段（beat），并把后面几句的动画改成 cue()
tools/cue_tables.py        把 L("中文短语", "English phrase") 形式的 cue 短语写进英文对照表
tools/en_set.py            只改对照表里的英文值（片尾小结要写成能念出来的句子）
.claude/skills/notes-to-3b1b-video/scripts/   渲染、i18n 检查、旁白检查（narration_lint.py）、逐帧联系表、台词导出
```

## 自己渲染

系统依赖：`ffmpeg`、Cairo 与 Pango（Ubuntu 上是 `libcairo2-dev`、`libpango1.0-dev`、`pkg-config`），以及字体 Noto Sans CJK SC 和 DejaVu Sans Mono。
Windows 上装好字体后运行一次 `python .claude/skills/notes-to-3b1b-video/scripts/win_fonts.py`。
配音：默认 edge-tts（需联网）；离线用 Kokoro（`KIT_TTS_ENGINE=kokoro`，模型文件放在 `KIT_KOKORO_DIR`，见 skill 的 bilingual-and-voice.md）。**现有的英文成片用的是 Kokoro（af_heart）。**

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
R=.claude/skills/notes-to-3b1b-video/scripts
KIT_TTS_ENGINE=kokoro .venv/bin/python $R/render.py cs61c/riscv --lang en --out videos/cs61c-riscv --manim .venv/bin/manim   # 14 集英文版，1080p30，带配音
.venv/bin/python $R/render.py cs61c/riscv 3 5 --lang en --manim .venv/bin/manim                                              # 只渲染第 3、5 集
KIT_TTS_ENGINE=kokoro .venv/bin/python $R/render.py cs61c/riscv 3 --lang en --preview --voice --manim .venv/bin/manim        # 480p 预览，只配音、不收集成片
```

## 旁白与翻译流程

剧集用中文撰写；渲染英文时，画面上的每个中文字符串（字幕、标签、代码注释）都会在 `i18n/epNN.py` 里查找英文，缺条目会直接报错。
英文旁白不是逐句翻译，而是为“听”重新写的：一段旁白（2–4 句）一次配音，`cue("短语", 动画…)` 让动画在语音念到那个短语时才出现。
改了旁白或中文字符串之后：

```bash
R=.claude/skills/notes-to-3b1b-video/scripts
python $R/i18n_check.py cs61c/riscv 5                              # 第 5 集的对照表是否完整
KIT_TTS_ENGINE=kokoro python $R/narration_lint.py cs61c/riscv 5 --lang en   # 句子过长、拼读风险、冒号式小标题……
KIT_TTS_ENGINE=kokoro python $R/captions.py cs61c/riscv 5 --lang en --spoken # 逐条列出字幕和实际念出来的读法
python tools/beats_apply.py 5 --list                               # 列出可合并的 say()；`beats_apply.py 5 spec.py` 应用一份合并方案
```

英文对照表里片尾小结等条目要写成能念出来的句子（数字拼成单词，不用冒号和括号）；读错的词在 `say_as.py` 里加读法。

## 用 skill 做新课程

`.claude/skills/notes-to-3b1b-video/` 是从这个系列提炼出来的 Claude skill：通用组件库 `manim_kit.py`（字幕、配音、双语翻译表、标题/小结卡）、`tts.py` 配音、渲染 / 逐帧检查 / 台词导出 / 翻译检查脚本（Linux、macOS、Windows 都能用），以及可视化模式、制作流程（笔记覆盖清单、并行 agent、审稿）、双语与配音、踩坑清单等参考文档。在这个仓库里开 Claude Code 会话会自动加载；打包好的 `dist/notes-to-3b1b-video.skill` 可以装到任何地方。下一门课（CS182）的起始提示词在 [`prompts/cs182-kickoff.md`](prompts/cs182-kickoff.md)。

## 说明

- 英文版旁白由离线神经网络语音 Kokoro-82M（`af_heart`）合成；中文版成片（`videos/cs61c-riscv/zh/`）是早先用 edge-tts（`zh-CN-YunxiNeural`）合成的，中文旁白还没有按新的“旁白段 + cue”写法重做，代码已按新结构合并，下次渲染中文时会按新结构出片。
- 字幕停留时间取阅读时间与语音时长中较长者；长旁白按句切换，同步的 `.srt` 与烧录字幕同一套时间。
- 内容按 CS61C Fall 2026 课程笔记中 RISC-V 部分的知识点和 RISC-V 规范整理；各集示例里的机器码、地址和寄存器值都在代码里用断言核对过。

## CS182 · Function Approximation 系列

依据 CS182 Note 1（Function Approximation）制作，5 集，英文字幕 + 英文配音（edge-tts）。成片和 `.srt` 在 [`videos/cs182-function-approximation/`](videos/cs182-function-approximation/)，旁白全文见 [`cs182/function-approximation/SCRIPT.md`](cs182/function-approximation/SCRIPT.md)，资料覆盖清单见 [`COVERAGE.md`](cs182/function-approximation/COVERAGE.md)，术语表见 [`GLOSSARY.md`](cs182/function-approximation/GLOSSARY.md)。

| # | 标题 | 内容 |
|---|---|---|
| 1 | Learning a Function from Samples | 只有样本点时要学什么；分段常数逼近；为什么 0/1 阶跃函数没有梯度、ReLU 斜坡才有 |
| 2 | ReLU Ramps Are a Spline Basis | 一组 ReLU 斜坡叠加恰好画出任意分段线性曲线（5 个隐藏单元的算例）；存在性 ≠ 训练得到 |
| 3 | From Ramps to a Layer | 一个单元怎么算；affine → ReLU → affine 的一层网络；去掉 ReLU 两层塌缩成一条直线 |
| 4 | Looking Where the Light Is | 指标、代理损失；经验风险与总体风险；过拟合；ridge 正则；用验证集选 λ，测试集只看一次 |
| 5 | Hold Out What Will Be New | 按行划分 vs 按患者划分（1-NN 记忆器 ≈100% vs ≈50%）；医院捷径与 Zech 等人的胸片结果；问题是否自洽的四问；术语地图 |

重新渲染：`source cs182/env.sh`（Windows 路径与环境变量），然后 `python .claude/skills/notes-to-3b1b-video/scripts/render.py cs182/function-approximation --out videos/cs182-function-approximation`。

## CS182 其余单元（课程网站公开的 notes 和 iPad notes）

来源：<https://berkeley-cs182.github.io/fa26/schedule/> 上已经公开的全部 notes / iPad notes（讲座 6 只有 Google Drive 幻灯片，第 4、5、9–12 讲尚无 notes，未做）。英文字幕 + 英文配音，每个单元都有 `COVERAGE.md`（资料覆盖清单）、`GLOSSARY.md`、`SCRIPT.md`（旁白全文）。

| 单元 | 视频 | 代码 | 资料 | 集数 |
|---|---|---|---|---|
| Introduction | [`videos/cs182-introduction/`](videos/cs182-introduction/) | [`cs182/introduction/`](cs182/introduction/) | Lecture 0 notes | 2：What Is Deep Learning? · Engineering or Alchemy? |
| Optimization | [`videos/cs182-optimization/`](videos/cs182-optimization/) | [`cs182/optimization/`](cs182/optimization/) | Least Squares/Ridge、GD/SGD、Momentum/Adam notes + Lecture 2、3 iPad notes | 9：梯度下降与最小二乘 → 零空间 → Ridge → 早停 → SGD → Momentum → 阻尼与稳定性 → Adam/AdamW → 标准化与初始化 |
| Scaling and μP | [`videos/cs182-scaling/`](videos/cs182-scaling/) | [`cs182/scaling/`](cs182/scaling/) | Lecture 7、8 iPad notes | 6：Steepest Descent Under a Norm → Spectral Norm → RMS Norm → Muon → Transfer → μP |

重新渲染某个单元：`source cs182/env.sh`，然后 `python .claude/skills/notes-to-3b1b-video/scripts/render.py cs182/<单元> --out videos/cs182-<单元>`。
