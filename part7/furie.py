from manim import *


class TaylorSeriesSin(Scene):
    def construct(self):
        gros_titre = Text("テイラー展開")
        gros_titre.scale(3)

        self.play(Write(gros_titre))
        self.wait()

        self.play(
            gros_titre.animate.shift(3.5 * LEFT + 8 * UP).scale(0.3),
        )

        axes = Axes(
            x_range=[-5, 5.1, 1],
            y_range=[-1.5, 1.5, 1],  # y軸をさらに短く設定
            x_length=2 * TAU,
            y_length=1 * TAU,
            axis_config={"color": GREEN},
            tips=False,
        ).shift(
            DOWN * 1.5
        )  # 関数の位置をさらに低く設定

        self.play(Create(axes))

        # SINのテイラー展開
        def SINN(x, n):
            result = 0
            for k in range(n + 1):
                result += (
                    ((-1) ** k) * (x ** (2 * k + 1)) / np.math.factorial(2 * k + 1)
                )
            return result

        # 短い周期のsin(x)を青色で表示し、「sin x」と表示
        sin_graph = axes.plot(
            lambda x: np.sin(2 * x), x_range=(-5, 5.1, 0.01), color=BLUE
        )
        sin_text = MathTex("\\sin x").next_to(sin_graph, UP).shift(UP * 2).scale(1.5)
        self.play(Create(sin_graph), Write(sin_text))
        self.wait(1)

        taylor_graphs = []
        term_texts = []

        # 各項の数式を生成
        terms = [
            "\\sin x = x",
            "\\sin x = x - \\frac{x^3}{3!}",
            "\\sin x = x - \\frac{x^3}{3!} + \\frac{x^5}{5!}",
            "\\sin x = x - \\frac{x^3}{3!} + \\frac{x^5}{5!} - \\frac{x^7}{7!}",
            "\\sin x = x - \\frac{x^3}{3!} + \\frac{x^5}{5!} - \\frac{x^7}{7!} + \\frac{x^9}{9!}",
            "\\sin x = x - \\frac{x^3}{3!} + \\frac{x^5}{5!} - \\frac{x^7}{7!} + \\frac{x^9}{9!} - \\frac{x^{11}}{11!}",
        ]

        for i in range(6):
            taylor_graphs.append(
                axes.plot(
                    lambda x, i=i: SINN(2 * x, i),
                    x_range=(-5, 5.1, 0.01),
                    color=RED,
                    discontinuities=[-1.5, 1.5],  # y軸を超える部分をカット
                )
            )
            term_text = MathTex(terms[i]).to_edge(UP).shift(UP * 2).scale(1.5)
            term_texts.append(term_text)

        # 初期状態のプロット
        current_graph = taylor_graphs[0]
        current_text = term_texts[0]
        self.play(Create(current_graph), Transform(sin_text, current_text))
        self.wait(1)
        self.remove(sin_text)

        # 順次変形と数式の追加表示
        for i in range(1, 6):
            next_graph = taylor_graphs[i]
            next_text = term_texts[i]
            self.play(
                Transform(current_graph, next_graph), Transform(current_text, next_text)
            )
            self.wait(1)
            self.remove(current_graph)
            self.remove(current_text)
            current_graph = next_graph
            current_text = next_text

        all_objects = VGroup(current_text)
        self.play(
            all_objects.animate.shift(DOWN * 4),
            FadeOut(
                current_graph,
                axes,
                sin_graph,
            )
        )
        final_text = Text("sin(x)のテイラー展開").next_to(current_text, UP * 3)
        final_form = MathTex(
            "\\sin x=\\sum_{n=0}^{\\infty}(-1)^n \\frac{x^{2 n+1}}{(2 n+1)!}"
        ).scale(1.5)

        self.play(Write(final_text))
        self.wait(1)
        self.play(Transform(current_text, final_form))
        self.wait(1)

        self.play(Indicate(current_text))
        self.wait(1)
        # commnet


