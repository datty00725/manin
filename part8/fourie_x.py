from manim import *

class FourierSeriesLine(Scene):
    def construct(self):
        # タイトルの設定
        title = Text("フーリエ級数展開")
        title.scale(3)

        self.play(Write(title))
        self.wait()

        self.play(
            title.animate.shift(3.5 * LEFT + 3.5 * UP).scale(0.3),
        )

        # 座標軸の設定
        axes = Axes(
            x_range=[-2*PI, 2*PI, PI/2],
            y_range=[-2*PI, 2*PI, PI/2],
            x_length=10,
            y_length=6,
            axis_config={"color": BLACK},
            tips=False,
        ).shift(DOWN * 1.5)

        self.play(Create(axes))

        # フーリエ級数の定義
        def fourier_series(x, n_terms):
            result = 0
            for n in range(1, n_terms + 1):
                result += (-1)**(n + 1) * (2 / n) * np.sin(n * x)
            return result

        x_vals = np.linspace(-2 * PI, 2 * PI, 200)
        y_vals = [fourier_series(x, 1) for x in x_vals]

        series_graph = axes.plot_line_graph(
            x_values=x_vals,
            y_values=y_vals,
            line_color=RED
        )

        self.add(series_graph)

        # 項数を増やしながらフーリエ級数を描画
        for n in range(2, 6):
            new_y_vals = [fourier_series(x, n) for x in x_vals]
            new_series_graph = axes.plot_line_graph(
                x_values=x_vals,
                y_values=new_y_vals,
                line_color=RED
            )
            self.play(Transform(series_graph, new_series_graph), run_time=0.5)

        final_y_vals = [x for x in x_vals]
        final_series_graph = axes.plot_line_graph(
            x_values=x_vals,
            y_values=final_y_vals,
            line_color=BLUE
        )

        # 最終的に直線 y = x を表示
        self.play(Transform(series_graph, final_series_graph), run_time=2)
        self.wait()
