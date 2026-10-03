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
| 1 | Newton–Schulz: Where Does a Singular Value Go? | 从“椭圆变圆”讲起：为什么要把奇异值推到 1；p(W) = U p(Σ) Vᵀ；先试简单的数，再看蛛网图、不动点与斜率；追问“σ 能多大”发现 √3，追问“更大会怎样”发现 √5；(√3, √5) 里按翻号次数交替通向 −1、+1 的吸引区及分界点 bn；√5 周期为 2；迭代前先按 Frobenius 范数缩放 |

这一集只做英文版（英文撰写，英文配音）。成片在 [`videos/cs182-newton-schulz/`](videos/cs182-newton-schulz/)（1080p30，烧录字幕 + `.srt`）。
代码在 `cs182/newton-schulz/`（基于 skill 的 `manim_kit.py`），剧情与覆盖清单见 [`cs182/newton-schulz/PLAN.md`](cs182/newton-schulz/PLAN.md)，旁白脚本见 `SCRIPT.md`。

配音：`tts.py` 默认用 edge-tts（需能访问 `speech.platform.bing.com`）；设 `KIT_TTS_ENGINE=pico` 改用离线的 SVOX Pico（`apt install libttspico-utils`）。设 `KIT_TTS_ENGINE=kokoro` 用离线神经网络语音 Kokoro-82M（见 skill 的 bilingual-and-voice.md §4）。现有成片用的是 Kokoro（af_heart）。

```bash
KIT_TTS_ENGINE=kokoro .venv/bin/python .claude/skills/notes-to-3b1b-video/scripts/render.py cs182/newton-schulz --out videos/cs182-newton-schulz # 离线神经网络配音
.venv/bin/python .claude/skills/notes-to-3b1b-video/scripts/render.py cs182/newton-schulz --out videos/cs182-newton-schulz                       # edge-tts 神经网络语音
```

**改旁白和叙事逻辑（不用碰动画代码）**：所有字幕/配音文字都在 [`cs182/newton-schulz/narration.md`](cs182/newton-schulz/narration.md)。
- 正文 = `###` 标题下的普通行，就是屏幕字幕和配音。`speak:` 行是只给配音用的读法。
- 注释 = 以 `>` 或 `//` 开头的行和 `<!-- -->`，渲染时忽略，可以随便写想法。
- 每个场景开头有叙事逻辑注释（目的、节拍、语气、待定选择），文件开头有“观众每一幕知道什么、想问什么”的表格。
- 不要改 `### 场景 编号 <!-- #哈希 -->` 这种标题行。
- 改完先检查，再出预览（只有改过的句子会重新配音）：

```bash
.venv/bin/python cs182/newton-schulz/narration.py check
KIT_TTS_ENGINE=kokoro .venv/bin/python .claude/skills/notes-to-3b1b-video/scripts/render.py cs182/newton-schulz 1 --preview --voice
```

调整场景顺序、增删一个节拍要改动画代码：把想法写在该场景的注释里，让 Claude 来改，改完 Claude 会运行 `narration.py sync` 把新句子合并进 narration.md，不会覆盖你已改的文字。

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
