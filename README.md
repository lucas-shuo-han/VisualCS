# VisualCS

用 3Blue1Brown 风格的动画讲计算机课程。第一个系列：**CS61C · RISC-V**（伯克利 CS61C 中 RISC-V 指令集部分）。

动画用 [Manim Community](https://www.manim.community/) 制作：深色背景、按字段着色的指令编码、一步步执行的寄存器和内存。
每集都有烧录在画面里的中文字幕，另附同步的 `.srt` 字幕文件（可以直接拿来配音或做 TTS）。

## CS61C RISC-V 系列

| 集 | 标题 | 内容 |
|---|---|---|
| 1 | 从 C 到汇编 | ISA 是软硬件的契约；32 个寄存器与 ABI 名字；x0；`add` / `sub` / `addi`；伪指令 `mv` `li` `nop` |
| 2 | 内存 | 字节寻址、字与对齐、小端序；`lw` / `sw` 与 `偏移(基址)`；`A[i]` 的偏移是 `4×i`；`lb` / `lbu` 的符号扩展与零扩展 |
| 3 | 决策与循环 | PC；六条条件分支；if-else 的“条件取反”；`and/or/xor` 与 `sll/srl/sra`；逐步执行一个数组求和循环 |
| 4 | 函数调用与栈 | 调用函数的六个步骤；`jal` / `jr ra`；调用者保存与被调用者保存；栈与压栈出栈；`sumSquare` 的序言与尾声 |
| 5 | 指令格式（上） | 存储程序；R / I / S 型逐位编码（`add`、`addi`、`lw`、`sw`）；为什么 S 型要把立即数拆开 |
| 6 | 指令格式（下） | PC 相对寻址；B 型的“打乱”位序与 `beq` 编码；`lui` + `addi` 的符号扩展陷阱；J 型与 `auipc`+`jalr`；六种格式总览 |
| 7 | CALL | 编译、汇编（伪指令展开、两遍扫描、符号表与重定位表）、链接、加载 |

成片在 [`videos/cs61c-riscv/`](videos/cs61c-riscv/)（1080p30，每集约 3.5–4 分钟），全部旁白文字见 [`cs61c/riscv/SCRIPT.md`](cs61c/riscv/SCRIPT.md)。

## 目录结构

```
cs61c/riscv/common.py      共享组件：带字幕计时的 NarratedScene、代码高亮、寄存器、内存、指令位字段……
cs61c/riscv/epXX_*.py      每集一个 Scene
tools/render.py            渲染全部（或指定）剧集，并把 mp4 + srt 收集到 videos/
tools/contact_sheet.py     按字幕时间点截帧、拼成联系表，用来快速检查排版
tools/srt_to_script.py     从字幕生成旁白脚本 SCRIPT.md
```

## 自己渲染

系统依赖：`ffmpeg`、`libcairo2-dev`、`libpango1.0-dev`、`pkg-config`，以及中文字体 Noto Sans CJK（Ubuntu 上是 `fonts-noto-cjk`）。

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python tools/render.py --manim .venv/bin/manim            # 全部剧集，1080p30
.venv/bin/python tools/render.py --manim .venv/bin/manim --preview 3  # 第 3 集 480p 快速预览
```

## 用 skill 做新课程

`.claude/skills/notes-to-3b1b-video/` 是从这个系列提炼出来的 Claude skill：通用组件库 `manim_kit.py`、渲染和逐帧检查脚本、可视化模式参考、踩坑清单。在这个仓库里开 Claude Code 会话会自动加载；打包好的 `dist/notes-to-3b1b-video.skill` 可以装到任何地方。下一门课（CS182）的起始提示词在 [`prompts/cs182-kickoff.md`](prompts/cs182-kickoff.md)。

## 说明

- 目前没有配音，旁白以字幕形式呈现；字幕停留时长按阅读速度自动计算。
- 内容按 CS61C 中 RISC-V 部分的知识点和 RISC-V 规范整理；各集示例里的机器码都在代码里用断言核对过。

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
