from manim import *


class FourierSeriesLine(MovingCameraScene):
    def construct(self):
        gros_titre = Text("フーリエ級数展開").scale(3)
        sub_titre = Text("直線 y = x").next_to(gros_titre, 3 * DOWN).scale(2)
        title = VGroup(gros_titre, sub_titre)

        self.play(Write(title))
        self.wait()

        self.play(
            title.animate.shift(3.5 * LEFT + 8 * UP).scale(0.3),
        )

        axes = Axes(
            x_range=[-5, 5.1, 1],
            y_range=[-4.5, 4.5, 1],
            x_length=2 * TAU,
            y_length=1 * TAU,
            axis_config={"color": GREEN},
            tips=False,
        ).shift(
            DOWN * 3
        )  # 関数の位置をさらに低く設定

        self.play(Create(axes))

        # フーリエ級数展開
        def fourier_series(x, n_terms):
            result = 0
            for n in range(1, n_terms + 1):
                result += (-1) ** (n + 1) * (2 / n) * np.sin(n * x)
            return result

        # 直線 y = x を青色で表示し、「y = x」と表示
        line_graph = axes.plot(lambda x: x, x_range=[-2 * PI, 2 * PI], color=BLUE)
        line_text = MathTex("y = x").to_edge(UP).shift(UP * 2).scale(1)
        self.play(Create(line_graph), Write(line_text))
        self.wait(1)

        fourier_graphs = []
        term_texts = []

        # 各項の数式を生成
        term_texts = (
            MathTex(
                "y",
                "\\approx \\frac{2}{1} \\sin(x)",
                " - \\frac{2}{2} \\sin(2x)",
                " + \\frac{2}{3} \\sin(3x)",
                " - \\frac{2}{4} \\sin(4x)",
                " + \\cdots",
            )
            .to_edge(UP)
            .shift(UP * 2)
            .scale(1)
        )

        for i in range(5):
            fourier_graphs.append(
                axes.plot(
                    lambda x, i=i: fourier_series(x, i + 1),
                    x_range=(-2 * PI, 2 * PI, 0.01),
                    color=RED,
                )
            )

        # i=120として最終形態を表示
        fourier_graphs.append(
            axes.plot(
                lambda x, i=120: fourier_series(x, i + 1),
                x_range=(-2 * PI, 2 * PI, 0.01),
                color=RED,
            )
        )
        # 初期状態のプロット
        current_graph = fourier_graphs[0]
        current_text = term_texts[:2]
        self.play(Create(current_graph), Transform(line_text, current_text))
        self.wait(1)

        # 順次変形と数式の追加表示
        for i in range(2, 6):
            next_graph = fourier_graphs[i]
            next_text = term_texts[i]
            self.play(Transform(current_graph, next_graph), Write(next_text))
            self.wait(1)
            self.remove(current_graph)
            current_graph = next_graph

        # 原点にズームイン
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(axes.c2p(0, 0))
        )
        self.wait(1)

        all_objects = VGroup(term_texts)
        self.remove(line_text)
        self.play(
            all_objects.animate.shift(DOWN * 4),
            FadeOut(
                current_graph,
                axes,
                line_graph,
            ),
        )
        final_text = Text("直線のフーリエ級数展開").next_to(term_texts, UP * 3)
        final_form = MathTex(
            "y = x \\approx \\sum_{n=1}^{\\infty} (-1)^{n+1} \\frac{2}{n} \\sin(nx)"
        ).scale(1.5)

        self.play(Write(final_text))
        self.wait(1)
        self.play(Transform(term_texts, final_form))
        self.wait(1)

        self.play(Indicate(term_texts))
        self.wait(2)
