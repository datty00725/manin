from manim import *


class TaylorSeriesSin(Scene):
    def construct(self):
        gros_titre = Text("テイラー展開").scale(3)
        sub_titre = Text("sin関数編").next_to(gros_titre, 3*DOWN).scale(2)
        title=VGroup(gros_titre,sub_titre)

        self.play(Write(title))
        self.wait()

        self.play(
            title.animate.shift(3.5 * LEFT + 8 * UP).scale(0.3),
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
        term_texts = MathTex("\\sin x"," \\approx x"," - \\frac{x^3}{3!}"," + \\frac{x^5}{5!}"," - \\frac{x^7}{7!} ","+ \\frac{x^9}{9!} + \\cdots").to_edge(UP).shift(UP * 2).scale(1.5)
        

        for i in range(6):
            taylor_graphs.append(
                axes.plot(
                    lambda x, i=i: SINN(2 * x, i),
                    x_range=(-5, 5.1, 0.01),
                    color=RED,
                    discontinuities=[-1.5, 1.5],  # y軸を超える部分をカット
                )
            )
            #term_texts = terms[i].to_edge(UP).shift(UP * 2).scale(1.5)
            #term_texts.append(term_text)

        # 初期状態のプロット
        current_graph = taylor_graphs[0]
        current_text = term_texts[:2]
        self.play(Create(current_graph), Transform(sin_text, current_text))
        self.wait(1)
        #self.remove(sin_text)

        # 順次変形と数式の追加表示
        for i in range(2, 6):
            next_graph = taylor_graphs[i]
            next_text = term_texts[i]
            self.play(
                Transform(current_graph, next_graph), Write(next_text)
            )
            self.wait(1)
            self.remove(current_graph)
            #self.remove(current_text)
            current_graph = next_graph
            #current_text = next_text

        all_objects = VGroup(term_texts)
        self.remove(sin_text)
        self.play(
            all_objects.animate.shift(DOWN * 4),
            FadeOut(
                #current_text,
                current_graph,
                axes,
                sin_graph,
            )
        )
        final_text = Text("sin(x)のテイラー展開").next_to(term_texts, UP * 3)
        final_form = MathTex(
            "\\sin x=\\sum_{n=0}^{\\infty}(-1)^n \\frac{x^{2 n+1}}{(2 n+1)!}"
        ).scale(1.5)

        self.play(Write(final_text))
        self.wait(1)
        self.play(Transform(term_texts, final_form))
        self.wait(1)

        self.play(Indicate(term_texts))
        self.wait(2)
