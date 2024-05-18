from manim import *
from fractal import KochSnowflake

#これ入れないと日本語がバグる。
Tex.set_default(tex_template=TexTemplate(
    tex_compiler = "lualatex", 
    # tex_compiler = "luatex" でも可
    output_format = ".pdf", 
    preamble = r"""
        \usepackage{amsmath}
        \usepackage{amssymb}
        \usepackage{luatexja}
        \usepackage[haranoaji]{luatexja-preset}
    """
))

class CW_KochCurveSandwich(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        len = 25

        def KochCurve(
            n, length=len, stroke_width=8, color=("#0A68EF", "#4AF1F2", "#0A68EF")
        ):
            l = length / (3**n)
            LineGroup = Line().set_length(l)

            def NextLevel(LineGroup):
                return VGroup(
                    *[LineGroup.copy().rotate(i) for i in [0, PI / 3, -PI / 3, 0]]
                ).arrange(RIGHT, buff=0, aligned_edge=DOWN)

            for _ in range(n):
                LineGroup = NextLevel(LineGroup)

            KC = (
                VMobject(stroke_width=stroke_width)
                .set_points(LineGroup.get_all_points())
                .set_color(color)
            )
            return KC

        def InvertedKochCurve(
            n, length=len, stroke_width=8, color=("#0A68EF", "#4AF1F2", "#0A68EF")
        ):
            l = length / (3**n)
            LineGroup = Line().set_length(l)

            def NextLevel(LineGroup):
                return VGroup(
                    *[LineGroup.copy().rotate(i) for i in [0, -PI / 3, PI / 3, 0]]
                ).arrange(RIGHT, buff=0, aligned_edge=UP)

            for _ in range(n):
                LineGroup = NextLevel(LineGroup)

            KC = (
                VMobject(stroke_width=stroke_width)
                .set_points(LineGroup.get_all_points())
                .set_color(color)
            )
            return KC

        level = (
            Variable(0, Tex("次元"), var_type=Integer).scale(2).set_color("#4AF1F2")
        )
        txt = VGroup(level).shift(9 * UP + LEFT * 1)
        text = Tex("コッホ曲線").scale(2)

        # Create the initial Koch curve and its inverted version
        kc = KochCurve(0, stroke_width=12).scale(0.5).next_to(text, UP, buff=0.5)
        inverted_kc = (
            InvertedKochCurve(0, stroke_width=12)
            .scale(0.5)
            .next_to(text, DOWN, buff=0.5)
        )

        # self.add(txt, kc, text, inverted_kc)
        self.play(Write(text))
        self.play(FadeIn(txt))
        self.wait(1)
        self.play(FadeIn(kc, inverted_kc))
        self.wait()

        # Animate the Koch curve to grow and shrink
        for i in range(1, 6):
            self.play(
                level.tracker.animate.set_value(i),
                kc.animate.become(
                    KochCurve(i, stroke_width=12 - (2 * i))
                    .scale(0.5)
                    .next_to(text, UP, buff=0.5)
                ),
                inverted_kc.animate.become(
                    InvertedKochCurve(i, stroke_width=12 - (2 * i))
                    .scale(0.5)
                    .next_to(text, DOWN, buff=0.5)
                ),
            )
            self.wait()

        self.wait(2)

        self.play(self.camera.frame.animate.scale(0.2).move_to(kc.get_top()))
        self.wait(2)
        zoom_text = (
            Tex("一部分を抜き出しても全体と似た形になる")
            .scale(0.175)
            .next_to(kc.get_top(), UP)
        )
        self.play(Write(zoom_text))
        self.wait(2)
        self.play(FadeOut(zoom_text))
        self.play(Restore(self.camera.frame))
        self.play(FadeOut(txt, kc, inverted_kc, text))

        # self.play(
        #    kc.animate.shift(3.5 * LEFT + 5 * UP).scale(0.3),
        #    text.animate.shift(3.5 * LEFT + 10 * UP).scale(0.3),
        # )
        self.wait(1)

        txt = Tex("コッホ雪片")

        level = Variable(0, Tex("次元"), var_type=Integer).next_to(txt,DOWN).set_color("#4AF1F2")

        tex_group = VGroup(txt, level)
        tex_group.scale(2).shift(7 * UP)

        color = ("#0A68EF", "#4AF1F2")

        ks = (
            KochSnowflake(0, scale=10, stroke_width=6, fill_opacity=0.25)
            .set_color(color)
            .shift(2 * DOWN)
        )

        sw = np.linspace(6, 1, 6)  # thinning stroke width

        self.wait(0.25)

        self.play(FadeIn(tex_group, ks), run_time=1.5)

        self.wait(1.5)

        for i in range(1, 6):

            ks_next_level = (
                KochSnowflake(i, scale=10, stroke_width=sw[i], fill_opacity=0.25)
                .set_color(color)
                .shift(2 * DOWN)
            )

            self.play(
                level.tracker.animate.set_value(i),
                ks.animate.become(ks_next_level),
                run_time=1.5,
            )
            self.wait(1.5)

        self.wait(0.5)

        # self.play(FadeOut(tex_group, ks), run_time=1.5)

        self.wait(0.25)
