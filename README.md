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

## 目录结构

```
cs61c/riscv/series.py      剧集列表：顺序、中英文标题、输出文件名
cs61c/riscv/common.py      共享组件：带字幕计时与配音的 NarratedScene、代码高亮、寄存器、内存、指令位字段……
cs61c/riscv/epNN_*.py      每集一个 Scene（中文撰写）
cs61c/riscv/i18n/epNN.py   每集的英文对照表：{中文字符串: English}
cs61c/riscv/tts.py         语音旁白：把字幕改写成适合朗读的形式，再用 edge-tts 合成（缓存在 media/tts/）
tools/render.py            渲染剧集（中/英、预览/成片），把 mp4 + srt 收集到 videos/
tools/i18n_check.py        检查英文对照表是否完整
tools/captions.py          按顺序列出每集的中英文字幕，方便校对
tools/contact_sheet.py     按字幕时间点截帧、拼成联系表，用来快速检查排版
tools/srt_to_script.py     从字幕生成旁白脚本 SCRIPT.md / SCRIPT.en.md
tools/win_fonts.py         Windows：在当前登录会话里注册字体
```

## 自己渲染

系统依赖：`ffmpeg`、Cairo 与 Pango（Ubuntu 上是 `libcairo2-dev`、`libpango1.0-dev`、`pkg-config`），以及字体 Noto Sans CJK SC 和 DejaVu Sans Mono。
Windows 上装好字体后运行一次 `python tools/win_fonts.py`。配音需要联网（首次合成后会缓存）。

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python tools/render.py --manim .venv/bin/manim                     # 全部 14 集，中英文，1080p30，带配音
.venv/bin/python tools/render.py --manim .venv/bin/manim --lang en 3 5       # 只渲染第 3、5 集的英文版
.venv/bin/python tools/render.py --manim .venv/bin/manim --preview 3         # 480p 快速预览（默认无配音，加 --voice 开启）
```

## 翻译流程

剧集用中文撰写；`VCS_LANG=en` 时，画面上的每个中文字符串（字幕、标签、代码注释）都会在 `i18n/epNN.py` 里查找英文。
缺少条目会直接报错，所以英文版里不会漏出中文。改了中文字符串之后：

```bash
python tools/i18n_check.py 5              # 第 5 集的对照表是否完整
python tools/i18n_check.py 5 --skeleton   # 打印缺失条目，可直接粘贴补全
python tools/captions.py 5                # 中英文字幕逐条对照
```

## 用 skill 做新课程

`.claude/skills/notes-to-3b1b-video/` 是从这个系列提炼出来的 Claude skill：通用组件库 `manim_kit.py`（字幕、配音、双语翻译表、标题/小结卡）、`tts.py` 配音、渲染 / 逐帧检查 / 台词导出 / 翻译检查脚本（Linux、macOS、Windows 都能用），以及可视化模式、制作流程（笔记覆盖清单、并行 agent、审稿）、双语与配音、踩坑清单等参考文档。在这个仓库里开 Claude Code 会话会自动加载；打包好的 `dist/notes-to-3b1b-video.skill` 可以装到任何地方。下一门课（CS182）的起始提示词在 [`prompts/cs182-kickoff.md`](prompts/cs182-kickoff.md)。

## 说明

- 旁白由 Microsoft 神经网络语音合成（中文 `zh-CN-YunxiNeural`，英文 `en-US-AndrewNeural`）；字幕停留时间取阅读时间与语音时长中较长者。
- 内容按 CS61C Fall 2026 课程笔记中 RISC-V 部分的知识点和 RISC-V 规范整理；各集示例里的机器码、地址和寄存器值都在代码里用断言核对过。
