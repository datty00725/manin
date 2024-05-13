from manim import *

class NumberLineAndEllipse(Scene):
    def construct(self):
        # 2次元平面（xy平面）の作成
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            axis_config={"color": BLUE},
        )

        # 平面をシーンに追加
        self.play(Create(axes))
        self.wait(1)  # 平面が表示された後の一時停止

        # 点F(-1, 0)と点F'(1, 0)の定義
        point_f = Dot(axes.c2p(-1, 0), color=RED)
        point_f_prime = Dot(axes.c2p(1, 0), color=GREEN)
        
        # 点のラベルを定義
        label_f = MathTex("F").next_to(point_f, DOWN)
        label_f_prime = MathTex("F'").next_to(point_f_prime, DOWN)

        # 点とラベルをシーンに追加
        self.play(FadeIn(point_f), FadeIn(point_f_prime), Write(label_f), Write(label_f_prime))
        self.wait(1)  # 点が表示された後の一時停止

        # 楕円の定義
        ellipse = Ellipse(width=4.0, height=2.0, color=GREEN).move_to(axes.c2p(0, 0))

        # 楕円をシーンに追加
        self.play(Create(ellipse))
        self.wait(1)  # 楕円が表示された後の一時停止
       
        # 楕円上の点Pを定義し、楕円の右端に配置
        dot = Dot(color=RED).move_to(ellipse.get_right())
        
        # 点Pをシーンに追加
        self.play(FadeIn(dot))
        
        # ValueTrackerを定義。これは、0から1までの値を追跡します。
        value_tracker = ValueTracker(0)
        
        # 点Pの位置を更新する関数。ValueTrackerの値に応じて楕円上の位置を変更します。
        def update_dot_pos(mob):
            # ValueTrackerの値を取得
            t = value_tracker.get_value()
            # 楕円上の点の位置を計算
            point = ellipse.point_from_proportion(t)
            # 点Pの位置を更新
            mob.move_to(point)
        
        # 点Pにアップデータを追加
        dot.add_updater(update_dot_pos)
        
        # ValueTrackerの値をアニメーション。これにより、点Pが楕円の周りを動きます。
        self.play(value_tracker.animate.set_value(1), run_time=5, rate_func=linear)
        self.wait()
        # 点Fと点F'のラベルを消す
        self.play(FadeOut(label_f), FadeOut(label_f_prime))
        self.wait()
        self.play(value_tracker.animate.set_value(1), run_time=5, rate_func=linear)

        # 点Pのアップデータを削除
        dot.remove_updater(update_dot_pos)