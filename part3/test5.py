from manim import *


class AdditiveFunctions(Scene):
    def construct(self):
        opte = Text("関数の和と積分").scale(3)
        self.play(Write(opte), run_time=2)
        self.wait(1)
        self.play(FadeOut(opte))
        self.wait(1)
        axes = (
            Axes(x_range=[0, 3.4, 1], x_length=12, y_range=[0, 14, 2], y_length=14)
            .add_coordinates()
            .shift(DOWN)
        )

        func1 = axes.plot(lambda x: x**2, x_range=[0, 3], color=YELLOW)
        func1_lab = (
            MathTex("y={x}^{2}").scale(1).next_to(axes, DOWN, buff=0.5).set_color(YELLOW)
        )

        func2 = axes.plot(lambda x: x, x_range=[0, 3], color=GREEN)
        func2_lab = MathTex("y=x").scale(1).next_to(func1_lab, RIGHT, buff=0.5).set_color(GREEN)

        func3 = axes.plot(lambda x: x**2 + x, x_range=[0, 3], color=PURPLE_D)
        func3_lab = (
            MathTex("y={x}^{2} + x")
            .scale(1)
            .next_to(func2_lab, RIGHT, buff=0.5)
            .set_color(PURPLE_D)
        )

        self.add(axes)
        # アニメーションでグラフを描画
        self.play(Create(func1), run_time=2)
        self.play(Write(func1_lab), run_time=0.5)
        self.play(Create(func2), run_time=2)
        self.play(Write(func2_lab), run_time=0.5)
        self.play(Create(func3), run_time=2)
        self.play(Write(func3_lab), run_time=0.5)

        self.wait()
        self.wait()

        for k in np.arange(0.2, 3.1, 0.2):
            line1 = DashedLine(
                start=axes.c2p(k, 0),
                end=axes.c2p(k, func1.underlying_function(k)),
                stroke_color=YELLOW,
                stroke_width=5,
            )

            line2 = DashedLine(
                start=axes.c2p(k, 0),
                end=axes.c2p(k, func2.underlying_function(k)),
                stroke_color=GREEN,
                stroke_width=7,
            )

            line3 = Line(
                start=axes.c2p(k, 0),
                end=axes.c2p(k, func3.underlying_function(k)),
                stroke_color=PURPLE,
                stroke_width=10,
            )

            self.play(Create(line1), run_time=0.2)
            self.play(Create(line2), run_time=0.2)

            if len(line1) > len(line2):
                self.play(line2.animate.shift(UP * line1.get_length()), run_time=0.3)
            else:
                self.play(line1.animate.shift(UP * line2.get_length()), run_time=0.3)

            self.play(Create(line3), run_time=0.5)
        self.wait()

        # Explaining the area additive rule
        area1 = axes.get_riemann_rectangles(
            graph=func1, x_range=[0, 3], dx=0.1, color=[BLUE, GREEN]
        )
        area2 = axes.get_riemann_rectangles(
            graph=func2, x_range=[0, 3], dx=0.1, color=[YELLOW, PURPLE]
        )

        self.play(Create(area1), run_time=1.0)
        self.play(area1.animate.set_opacity(0.5), run_time=1.0)
        self.play(Create(area2), run_time=0.5)
        self.wait()
        for k in range(30):
            self.play(area2[k].animate.shift(UP * area1[k].get_height()), run_time=0.2)
        self.wait()

        self.play(*[mob.animate.shift(DOWN * 4) for mob in self.mobjects], run_time=2)
        self.wait()

        text1=Text("これが定積分の基本式").scale(1).shift(UP*5)
        text2=Text("【関数の和】").scale(1)
        text2.next_to(text1, DOWN)
        

        self.play(Write(text1))
        self.wait(2)
        self.play(Write(text2))
        self.wait(2)
        
        text_PF = MathTex(
            r"\int_a^b\{f(x) \pm g(x)\} dx = \int_a^b f(x) dx \pm \int_a^b g(x) dx"
        )
        text_PF.next_to(text2, DOWN*2)

        self.play(Write(text_PF))
        self.wait(2)