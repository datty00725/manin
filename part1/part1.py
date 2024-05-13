from manim import *

from manim import *

class NumberLineAndEllipse(Scene):
    def construct(self):
        # 数直線を作成
        number_line = NumberLine(x_range=[-5, 5, 1], length=10, color=BLUE, include_numbers=True)
        
        # 数直線をシーンに追加
        self.play(Create(number_line))
        
        # 楕円を定義
        ellipse = Ellipse(width=4.0, height=2.0, color=GREEN).shift(DOWN*2)
        
        # 楕円をシーンに追加
        self.play(Create(ellipse))
        
        # 点Pを定義し、楕円の右端に配置
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
        
        # 点Pのアップデータを削除
        dot.remove_updater(update_dot_pos)
