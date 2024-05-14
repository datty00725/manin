from manim import *

class FourierSeriesLine(Scene):
    def construct(self):
        gros_titre = Text("フーリエ級数展開")
        gros_titre.scale(3)

        self.play(Write(gros_titre))
        self.wait()

        self.play(
            gros_titre.animate.shift(3.5 * LEFT + 8 * UP).scale(0.3),
        )

        axes = Axes(
            x_range=[-5, 5.1, 1],
            y_range=[-5, 5.1, 1],  # y軸をさらに短く設定
            x_length=2 * TAU,
            y_length=2 * TAU,
            axis_config={"color": GREEN},
            tips=False,
        ).shift(
            DOWN * 1.5
        )  # 関数の位置をさらに低く設定

        self.play(Create(axes))

        # フーリエ級数展開
        def fourier_series(x, n_terms):
            result = 0
            for n in range(1, n_terms + 1):
                result += (-1)**(n + 1) * (2 / n) * np.sin(n * x)
            return result

        # 短い周期のsin(x)を青色で表示し、「y = x」と表示
        x_vals = np.linspace(-2 * PI, 2 * PI, 200)
        y_vals = [x for x in x_vals]

        line_graph = axes.plot_line_graph(
            x_values=x_vals,
            y_values=y_vals,
            line_color=BLUE
        )
        line_text = MathTex("y = x").next_to(line_graph, UP).shift(UP * 2).scale(1.5)
        self.play(Create(line_graph), Write(line_text))
        self.wait(1)

        fourier_graphs = []
        term_texts = []

        # 各項の数式を生成
        terms = [
            "y = \\frac{2}{1} \\sin(x)",
            "y = \\frac{2}{1} \\sin(x) - \\frac{2}{2} \\sin(2x)",
            "y = \\frac{2}{1} \\sin(x) - \\frac{2}{2} \\sin(2x) + \\frac{2}{3} \\sin(3x)",
            "y = \\frac{2}{1} \\sin(x) - \\frac{2}{2} \\sin(2x) + \\frac{2}{3} \\sin(3x) - \\frac{2}{4} \\sin(4x)",
            "y = \\frac{2}{1} \\sin(x) - \\frac{2}{2} \\sin(2x) + \\frac{2}{3} \\sin(3x) - \\frac{2}{4} \\sin(4x) + \\frac{2}{5} \\sin(5x)",
            "y = \\frac{2}{1} \\sin(x) - \\frac{2}{2} \\sin(2x) + \\frac{2}{3} \\sin(3x) - \\frac{2}{4} \\sin(4x) + \\frac{2}{5} \\sin(5x) - \\frac{2}{6} \\sin(6x)",
        ]

        for i in range(6):
            y_vals = [fourier_series(x, i+1) for x in x_vals]
            fourier_graphs.append(
                axes.plot_line_graph(
                    x_values=x_vals,
                    y_values=y_vals,
                    line_color=RED,
                )
            )
            term_text = MathTex(terms[i]).to_edge(UP).shift(UP * 2).scale(1.5)
            term_texts.append(term_text)

        # 初期状態のプロット
        current_graph = fourier_graphs[0]
        current_text = term_texts[0]
        self.play(Create(current_graph), Transform(line_text, current_text))
        self.wait(1)
        self.remove(line_text)

        # 順次変形と数式の追加表示
        for i in range(1, 6):
            next_graph = fourier_graphs[i]
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
                line_graph,
            )
        )
        final_text = Text("直線のフーリエ級数展開").next_to(current_text, UP * 3)
        final_form = MathTex(
            "y = \\sum_{n=1}^{\\infty} (-1)^{n+1} \\frac{2}{n} \\sin(nx)"
        ).scale(1.5)

        self.play(Write(final_text))
        self.wait(1)
        self.play(Transform(current_text, final_form))
        self.wait(1)

        self.play(Indicate(current_text))
        self.wait(1)
