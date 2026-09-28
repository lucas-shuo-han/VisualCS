import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F403

assert bits_to_hex("0000000" + "01100" + "01011" + "000" + "01010" + "0110011") == "0x00C58533"

C_TEXT_SEG = PURPLE_B
C_DATA_SEG = GOLD_C


def seg_box(label, color, w=2.6, h=0.6, size=22):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.18)
    t = zh(label, size, WHITE).move_to(r)
    if t.width > w * 0.92:
        t.scale_to_fit_width(w * 0.92)
    return VGroup(r, t)


class Ep13CALL(NarratedScene):
    def construct(self):
        self.title_card()
        self.pipeline()
        self.assembler()
        self.linker()
        self.loader()
        self.wrap_up()
        self.end_card(
            [
                "编译器：C → 汇编（可以含伪指令）",
                "汇编器：展开伪指令，两遍扫描解决向前引用",
                "目标文件 = 机器码 + 符号表 + 重定位表",
                "链接器：拼接各段，按重定位表补全地址",
                "加载器：建立地址空间，复制代码和数据，跳到 main",
            ],
        )

    # ------------------------------------------------------------------ overview
    def pipeline(self):
        def stage(zh_name, en, color):
            b = box_label(zh_name, color, w=1.7, h=0.85, font_size=26)
            e = Text(en, font=CJK, font_size=20, color=GREY_A, t2c={"[0:1]": YELLOW_D})
            e.next_to(b, DOWN, buff=0.15)
            return VGroup(b, e)

        items = [
            file_icon("foo.c", BLUE_C, w=1.0, h=1.25, font_size=20),
            stage("编译器", "Compiler", BLUE_C),
            file_icon("foo.s", BLUE_C, w=1.0, h=1.25, font_size=20),
            stage("汇编器", "Assembler", TEAL_C),
            file_icon("foo.o", TEAL_C, w=1.0, h=1.25, font_size=20),
            stage("链接器", "Linker", GREEN_C),
            file_icon("a.out", GREEN_C, w=1.0, h=1.25, font_size=20),
            stage("加载器", "Loader", GOLD_C),
            box_label("运行", RED_C, w=1.1, h=0.85, font_size=26),
        ]
        row = VGroup(*items).arrange(RIGHT, buff=0.5)
        for k in (1, 3, 5, 7):
            items[k].shift(DOWN * (items[k][0].get_center()[1] - items[0].get_center()[1]))
        row.scale_to_fit_width(13.2).move_to(UP * 0.7)
        arrows = VGroup(*[
            Arrow(items[k].get_right() if k % 2 == 0 else items[k][0].get_right(),
                  items[k + 1].get_left() if k % 2 == 1 or k == 7 else items[k + 1][0].get_left(),
                  buff=0.08, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.35)
            for k in range(8)
        ])
        lib = file_icon("lib.o", TEAL_C, w=0.8, h=1.0, font_size=16).next_to(items[5], DOWN, buff=0.55)
        lib_arrow = Arrow(lib.get_top(), items[5][1].get_bottom(), buff=0.08, color=GREY_B, stroke_width=3)
        self.say("从一个 C 文件到一个正在运行的程序，要经过四个步骤。",
                 FadeIn(items[0], shift=RIGHT * 0.2))
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(arrows[k]), FadeIn(items[k + 1], shift=RIGHT * 0.2))
                                for k in range(8)], lag_ratio=0.35, run_time=4))
        self.play(FadeIn(lib, shift=UP * 0.2), GrowArrow(lib_arrow))
        self.say("编译 Compiler、汇编 Assembler、链接 Linker、加载 Loader。取首字母，就是 CALL。",
                 *[Indicate(items[k][1][0], color=YELLOW_D, scale_factor=1.6) for k in (1, 3, 5, 7)])
        self.hold()
        self.say("编译器把 C 翻译成汇编——前几集我们手工做的，正是编译器的工作。",
                 Circumscribe(items[1], color=BLUE_C))
        self.say("编译器输出的汇编里可以有伪指令，比如 mv、li、j，展开的活儿留给汇编器。")
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ assembler
    def assembler(self):
        head = self.heading("汇编器 Assembler")
        self.say("汇编器读入汇编代码，输出目标文件（object file）：机器码，外加一些“附加信息”。", Write(head))
        left = CodeListing(["mv   a0, s0", "li   t0, 0xDEADBEEF", "", "j    Loop", "ret"],
                           font_size=26, line_gap=0.56)
        right = CodeListing(["addi a0, s0, 0", "lui  t0, 0xDEADC", "addi t0, t0, -273", "jal  x0, Loop",
                             "jalr x0, 0(ra)"], font_size=26, line_gap=0.56)
        left.move_to(LEFT * 4.2 + UP * 0.5)
        right.next_to(left, RIGHT, buff=1.4).align_to(left, UP)
        arrows = VGroup(*[
            Arrow(LEFT * 0.4, RIGHT * 0.4, color=GREY_B, buff=0).move_to(
                [(left.get_right()[0] + right.get_left()[0]) / 2, left[i].get_center()[1], 0])
            for i in (0, 1, 3, 4)
        ])
        self.say("第一件事：把伪指令展开成真实的指令。",
                 FadeIn(left), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2),
                 FadeIn(right, lag_ratio=0.1))
        self.hold()
        self.play(FadeOut(VGroup(left, right, arrows)))

        code = CodeListing([
            "      bne  t0, t1, Skip",
            "      addi t0, t0, 1",
            "Skip: add  t2, t0, t1",
        ], font_size=30, line_gap=0.62).move_to(LEFT * 2.6 + UP * 0.9)
        addrs = VGroup(*[mono(f"0x{4 * i:02X}", 24, GREY).next_to(code.left_of(i, 0.4), LEFT, buff=0)
                         for i in range(3)])
        self.say("第二件事：把标签换算成偏移。可这里有个“向前引用”的问题——",
                 FadeIn(code), FadeIn(addrs))
        q = mono("?", 36, RED_B).next_to(code.glyphs(0, "Skip"), UP, buff=0.1)
        self.say("汇编器读到 bne 时，还没见过 Skip 的定义，不知道该跳多远。",
                 Circumscribe(code.glyphs(0, "Skip"), color=RED_B), FadeIn(q))
        self.hold()

        tbl_head = VGroup(zh("符号表", 26, YELLOW_D))
        tbl_box = Rectangle(width=3.4, height=1.6, stroke_color=YELLOW_D, stroke_width=2)
        tbl_box.move_to(RIGHT * 4.6 + UP * 0.7)
        tbl_head.next_to(tbl_box, UP, buff=0.15)
        self.say("解决办法：扫描两遍。第一遍不生成机器码，只记录每个标签的地址，存进符号表。",
                 Create(tbl_box), FadeIn(tbl_head))
        scan = code.line_box(0, color=BLUE_B)
        self.play(FadeIn(scan))
        for i in (1, 2):
            self.play(scan.animate.become(code.line_box(i, color=BLUE_B)), run_time=0.6)
        entry = mono("Skip  →  0x08", 28, C_LABEL).move_to(tbl_box)
        self.play(TransformFromCopy(VGroup(code.glyphs(2, "Skip"), addrs[2]), entry))
        self.play(FadeOut(scan))
        self.say("第二遍再生成机器码。这时 Skip 的地址已知：偏移 = 0x08 − 0x00 = 8。",
                 FadeOut(q))
        off = mono("+8", 30, YELLOW_D).next_to(code.glyphs(0, "Skip"), UP, buff=0.12)
        self.play(TransformFromCopy(entry, off))
        self.hold()
        self.play(FadeOut(VGroup(code, addrs, off)))

        ext = CodeListing([
            "jal  ra, printf     # printf 在别的文件里",
            "la   t0, A          # 静态数据 A 的地址",
        ], font_size=24, line_gap=0.62)
        ext.to_edge(LEFT, buff=0.6).set_y(0.8)
        self.say("但有些东西，汇编器无论扫几遍都解决不了：比如调用另一个文件里的 printf，或者取静态数据的地址。",
                 FadeIn(ext, shift=UP * 0.15))
        reloc_box = Rectangle(width=3.4, height=1.3, stroke_color=RED_B, stroke_width=2)
        reloc_box.next_to(tbl_box, DOWN, buff=0.75)
        reloc_head = zh("重定位表", 26, RED_B).next_to(reloc_box, UP, buff=0.15)
        rel = VGroup(mono("printf @ jal", 22, RED_B), mono("A @ la", 22, RED_B)).arrange(DOWN, buff=0.15)
        rel.move_to(reloc_box)
        self.say("它们的最终位置要等链接时才知道。汇编器把这些“待补的洞”记进重定位表，留给链接器。",
                 Create(reloc_box), FadeIn(reloc_head), TransformFromCopy(ext, rel))
        self.hold()
        self.clear_stage()

        parts = [("文件头 header", GREY_B), ("代码段 .text", C_TEXT_SEG), ("数据段 .data", C_DATA_SEG),
                 ("重定位表 relocation", RED_B), ("符号表 symbol table", YELLOW_D), ("调试信息 debug", GREY)]
        obj = VGroup(*[seg_box(n, c, w=4.6, h=0.62, size=24) for n, c in parts]).arrange(DOWN, buff=0)
        obj.move_to(DOWN * 0.1)
        obj_l = mono("foo.o", 30, TEAL_C).next_to(obj, UP, buff=0.25)
        self.say("所以一个目标文件包含：文件头、代码段、数据段、重定位表、符号表，还有调试信息。",
                 FadeIn(obj_l), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in obj], lag_ratio=0.2))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ linker
    def linker(self):
        head = self.heading("链接器 Linker")

        def obj(name, color):
            t = seg_box(f"{name} 代码", C_TEXT_SEG, w=2.4)
            d = seg_box(f"{name} 数据", C_DATA_SEG, w=2.4)
            g = VGroup(t, d).arrange(DOWN, buff=0)
            lab = mono(f"{name}.o", 26, color).next_to(g, UP, buff=0.15)
            return VGroup(g, lab)

        foo = obj("foo", TEAL_C).move_to(LEFT * 4.6 + UP * 1.3)
        lib = obj("lib", TEAL_C).move_to(LEFT * 4.6 + DOWN * 0.9)
        self.say("链接器把多个目标文件拼成一个可执行文件。", Write(head), FadeIn(foo), FadeIn(lib))
        out_segs = VGroup(
            seg_box("foo 代码", C_TEXT_SEG, w=2.8), seg_box("lib 代码", C_TEXT_SEG, w=2.8),
            seg_box("foo 数据", C_DATA_SEG, w=2.8), seg_box("lib 数据", C_DATA_SEG, w=2.8),
        ).arrange(DOWN, buff=0).move_to(RIGHT * 0.4 + UP * 0.2)
        out_l = mono("a.out", 28, GREEN_C).next_to(out_segs, UP, buff=0.15)
        self.say("第一步：把所有代码段首尾相接，所有数据段也首尾相接。", FadeIn(out_l))
        self.play(TransformFromCopy(foo[0][0], out_segs[0]), TransformFromCopy(lib[0][0], out_segs[1]), run_time=1.2)
        self.play(TransformFromCopy(foo[0][1], out_segs[2]), TransformFromCopy(lib[0][1], out_segs[3]), run_time=1.2)
        addr = VGroup(mono("0x10000", 20, GREY_B).next_to(out_segs[0], RIGHT, buff=0.2).align_to(out_segs[0], UP),
                      mono("0x10100", 20, GREY_B).next_to(out_segs[1], RIGHT, buff=0.2).align_to(out_segs[1], UP))
        self.say("第二步：各段的位置一旦排定，每个符号的最终地址也就确定了。printf 位于 0x10180。",
                 FadeIn(addr))
        sym = mono("printf = 0x10180", 24, YELLOW_D).next_to(out_segs[1], RIGHT, buff=0.2).align_to(out_segs[1], DOWN)
        self.play(FadeIn(sym, shift=LEFT * 0.1))
        hole = CodeListing(["0x10040:  jal ra, ???"], font_size=26)
        hole.move_to(DOWN * 2.2).set_x(-5.6 + hole.width / 2)
        self.say("第三步：按重定位表逐个补洞。foo 里 0x10040 处的 jal 要跳到 printf……",
                 FadeIn(hole, shift=UP * 0.15))
        filled = CodeListing(["0x10040:  jal ra, 0x140   # 0x10180 - 0x10040"], font_size=26).move_to(hole, aligned_edge=LEFT)
        self.say("……jal 用的是 PC 相对偏移：0x10180 − 0x10040 = 0x140。", Transform(hole, filled))
        self.hold()
        self.say("而文件内部的分支完全不用改：PC 相对偏移，整块挪动后依然正确。这正是前面说过的位置无关。",
                 Indicate(out_segs[0], color=PURPLE_B))
        self.say("顺便一提：现代系统还常用“动态链接”，库在程序运行时才载入。这里讲的是静态链接。")
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ loader
    def loader(self):
        head = self.heading("加载器 Loader")
        segs = [("栈 Stack", BLUE_C, 1.0), ("", GREY_E, 1.2), ("堆 Heap", GREEN_C, 0.7),
                ("静态数据", C_DATA_SEG, 0.7), ("代码 Text", C_TEXT_SEG, 0.8)]
        mem = VGroup()
        for name, col, h in segs:
            r = Rectangle(width=3.2, height=h, stroke_color=GREY_B, stroke_width=2,
                          fill_color=col, fill_opacity=0.0)
            t = zh(name, 24, WHITE).move_to(r)
            t.set_opacity(0)
            mem.add(VGroup(r, t))
        mem.arrange(DOWN, buff=0).move_to(RIGHT * 3.6 + DOWN * 0.1)
        mem_l = zh("新的地址空间", 24, GREY_A).next_to(mem, UP, buff=0.15)
        aout = file_icon("a.out", GREEN_C, w=1.2, h=1.5, font_size=22).move_to(LEFT * 4.8 + UP * 2.0)
        steps = VGroup(*[zh(s, 24, C_TEXT) for s in [
            "1. 读文件头，得知各段大小",
            "2. 创建新的地址空间",
            "3. 把代码和数据复制进内存",
            "4. 把命令行参数放到栈上",
            "5. 初始化寄存器，sp 指向栈顶",
            "6. 跳到启动例程，再由它调用 main",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(LEFT * 3.2 + DOWN * 0.9)
        self.say("最后，操作系统中的加载器负责把可执行文件真正运行起来。",
                 Write(head), FadeIn(aout))
        self.say("它先读文件头，得知代码段和数据段有多大，再为程序创建一个新的地址空间……",
                 FadeIn(steps[0]), FadeIn(steps[1]), FadeIn(mem_l),
                 LaggedStart(*[Create(s[0]) for s in mem], lag_ratio=0.2))
        text_copy = seg_box("代码", C_TEXT_SEG, w=1.2, h=0.4, size=18).move_to(aout)
        data_copy = seg_box("数据", C_DATA_SEG, w=1.2, h=0.4, size=18).move_to(aout)
        self.say("……然后把代码和数据复制进内存……", FadeIn(steps[2]))
        self.play(text_copy.animate.move_to(mem[4]).scale(1.3), data_copy.animate.move_to(mem[3]).scale(1.3),
                  run_time=1.4)
        self.play(FadeOut(text_copy), FadeOut(data_copy),
                  mem[4][0].animate.set_fill(C_TEXT_SEG, 0.25), mem[4][1].animate.set_opacity(1),
                  mem[3][0].animate.set_fill(C_DATA_SEG, 0.25), mem[3][1].animate.set_opacity(1),
                  mem[2][1].animate.set_opacity(1), mem[2][0].animate.set_fill(GREEN_C, 0.12))
        sp = VGroup(Arrow(RIGHT * 0.9, ORIGIN, buff=0, color=C_SP), mono("sp", 26, C_SP))
        sp[1].next_to(sp[0], RIGHT, buff=0.1)
        sp.next_to(mem[0], RIGHT, buff=0.08)
        argv = zh("argc / argv", 20, GREY_A)
        self.say("……把命令行参数放到栈上，初始化寄存器，让 sp 指向栈顶……",
                 FadeIn(steps[3]), FadeIn(steps[4]),
                 mem[0][0].animate.set_fill(BLUE_C, 0.25), mem[0][1].animate.set_opacity(1), FadeIn(sp))
        pc = VGroup(Arrow(RIGHT * 0.9, ORIGIN, buff=0, color=YELLOW_D), mono("PC", 26, YELLOW_D))
        pc[1].next_to(pc[0], RIGHT, buff=0.1)
        pc.next_to(mem[4], RIGHT, buff=0.08)
        self.say("……最后跳到启动例程，由它调用 main。程序开始运行！", FadeIn(steps[5]), FadeIn(pc))
        self.play(Indicate(mem[4], color=YELLOW_D))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ wrap up
    def wrap_up(self):
        chain = VGroup(
            CodeListing(["a = b + c;"], lang="c", font_size=30),
            CodeListing(["add a0, a1, a2"], font_size=30),
            mono("0x00C58533", 30, YELLOW_D),
            zh("在内存中运行", 30, RED_B),
        ).arrange(DOWN, buff=0.7).move_to(UP * 0.5)
        arrows = VGroup(*[Arrow(chain[k].get_bottom(), chain[k + 1].get_top(), buff=0.12, color=GREY_B)
                          for k in range(3)])
        self.say("到这里，我们走完了一整条路：C 代码，到汇编，到机器码，再到内存里运行的程序。",
                 LaggedStart(*[AnimationGroup(FadeIn(chain[k], shift=DOWN * 0.1),
                                              *([GrowArrow(arrows[k - 1])] if k else []))
                               for k in range(4)], lag_ratio=0.4, run_time=3))
        eps = VGroup(*[zh(s, 22, GREY_A) for s in [
            "①② 机器结构与算术", "③④ 内存", "⑤⑥ 分支与循环", "⑦⑧ 函数与栈",
            "⑨–⑫ 指令编码", "⑬⑭ CALL",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.9).shift(UP * 0.4)
        self.say("寄存器、内存、分支、函数调用、指令编码、编译链接——这就是 CS61C 中 RISC-V 部分的全貌。",
                 LaggedStart(*[FadeIn(e, shift=LEFT * 0.2) for e in eps], lag_ratio=0.15))
        self.hold(0.5)
