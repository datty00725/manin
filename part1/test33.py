from manim import *
import numpy as np  # NumPyをインポート


class EllipseAnimation(Scene):
    def construct(self):
        opte=Text("楕円").scale(5)
        self.play(
            Write(opte)
        )
        self.wait(1)
        self.play(
            FadeOut(opte)
        )
        self.wait(1)
        # 楕円のパラメータ
        a = 6  # 長軸の半分
        c = 4  # 焦点から中心までの距離
        b = np.sqrt(a**2 - c**2)  # 短軸の半分

        # 焦点FとF'
        f = Dot([-c, 0, 0], color=RED)
        f_prime = Dot([c, 0, 0], color=RED)
        label_f_initial = MathTex("F'").next_to(f, DOWN)
        label_f_prime_initial = MathTex("F").next_to(f_prime, DOWN)

        # 点Pの初期表示位置
        p = Dot([a, 0, 0], color=BLUE)

        f.scale(2)
        f_prime.scale(2)
        p.scale(2)

        # 線分PFとPF'の初期状態
        line_pf = Line(p.get_center(), f.get_center(), color=YELLOW)
        line_pf_prime = Line(p.get_center(), f_prime.get_center(), color=YELLOW)

        # 初期状態の描画（点のみ）
        # self.add(f, f_prime, label_f_initial, label_f_prime_initial, p)
        self.play(
            Create(f),
            Create(f_prime),
            Create(p),
            Write(label_f_initial),
            Write(label_f_prime_initial),
        )
        self.wait(1)
        # 点Pの動きを定義
        angle = ValueTracker(0)

        def update_p(mob):
            theta = angle.get_value()
            x = a * np.cos(theta)
            y = b * np.sin(theta)
            mob.move_to([x, y, 0])

        # 線分のアップデートを定義
        line_pf.add_updater(
            lambda mob: mob.become(Line(p.get_center(), f.get_center(), color=YELLOW))
        )
        line_pf_prime.add_updater(
            lambda mob: mob.become(
                Line(p.get_center(), f_prime.get_center(), color=YELLOW)
            )
        )

        # 線分のアニメーションを追加
        self.play(Create(line_pf), Create(line_pf_prime))
        p.add_updater(update_p)
        self.add(p, line_pf, line_pf_prime)
        self.play(
            angle.animate.set_value(2 * PI * 8 + PI / 4),
            run_time=5,
            rate_func=lambda t: t**2,
        )
        self.wait()

        # 線分をフェードアウト
        # self.remove(line_pf, line_pf_prime)  # 動的に更新された線分を削除
        # 現在のPの位置で新しい線分を作成
        # new_line_pf = Line(p.get_center(), f.get_center(), color=YELLOW)
        # new_line_pf_prime = Line(p.get_center(), f_prime.get_center(), color=YELLOW)
        # self.add(new_line_pf, new_line_pf_prime)  # 新しい線分を追加
        # self.play(FadeOut(new_line_pf), FadeOut(new_line_pf_prime), FadeOut(p),run_time=2)

        self.wait()
        # 楕円を表示
        ellipse = Ellipse(width=2 * a, height=2 * b, color=WHITE)
        self.play(Create(ellipse))
        self.wait(1)

        # アップデータを停止
        p.clear_updaters()
        line_pf.clear_updaters()
        line_pf_prime.clear_updaters()

        # 新しい焦点のラベル
        label_f_new = MathTex("F'(-c, 0)").next_to(f, DOWN)
        label_f_prime_new = MathTex("F(c, 0)").next_to(f_prime, DOWN)

        # 点Pのラベル
        label_p = MathTex("P(x, y)").next_to(p, 2 * UP)
        # label_f_new.scale(0.8)

        # 初期ラベルをフェードアウト
        self.play(FadeOut(label_f_initial), FadeOut(label_f_prime_initial))

        # 新しいラベルをフェードイン
        self.play(FadeIn(label_f_new), FadeIn(label_f_prime_new), FadeIn(label_p))

        # オブジェクトをグループ化
        all_objects = VGroup(
            ellipse,
            f,
            f_prime,
            label_f_new,
            label_f_prime_new,
            p,
            line_pf,
            line_pf_prime,
            label_p,
        )

        # グループを上にスライドさせる
        self.play(all_objects.animate.shift(UP * 7))

        self.wait(1)

        # 楕円の定義
        text1 = Text("楕円の式を求めよう！")
        text2 = Text("【2つの線分を足したものは常に等しい】")
        text3 = Text("この性質を使いたい")
        text4 = Text("線分の長さを求めなくては！")
        text2.next_to(text1, DOWN)
        text3.next_to(text2, DOWN)
        text4.next_to(text3, DOWN)

        self.play(Write(text1))
        self.wait(1)
        self.play(Write(text2))
        self.wait(1)
        self.play(Write(text3))
        self.wait(1)
        self.play(Write(text4))
        self.wait()

        first_objects = VGroup(text1, text2, text3, text4)

        self.play(ApplyMethod(first_objects.shift, 2 * UP))
        self.wait()

        self.wait(1)
        text_PF = MathTex("PF = \\sqrt{(x-c)^2+y^2}")
        text_PF_prime = MathTex("PF' = \\sqrt{(x+c)^2+y^2}")
        text_PF.next_to(first_objects, DOWN)
        text_PF_prime.next_to(text_PF, DOWN)

        self.play(Write(text_PF),Write(text_PF_prime))
        

        self.play(FadeOut(text1, text3, text4))
        self.play(
            text_PF.animate.shift(UP),
            text_PF_prime.animate.shift(UP),
        )
        
        definition = MathTex("PF + PF' = 2a").next_to(
            text_PF_prime, DOWN
        )  # scaleメソッドを適用してサイズを変更

        # MathTexオブジェクトを配置

        self.play(Write(definition))
        self.wait()
        self.play(Indicate(definition),Indicate(text2))
        self.wait(1)

        # 式変形ステップ1
        step1 = MathTex("\\sqrt{(x-c)^2+y^2} + \\sqrt{(x+c)^2+y^2} = 2a").next_to(
            definition, DOWN
        )
        self.play(TransformMatchingTex(definition.copy(), step1))
        self.wait(1)

        # 式変形ステップ2
        step2 = MathTex("\\sqrt{(x-c)^2+y^2} = 2a - \\sqrt{(x+c)^2+y^2}").next_to(
            step1, DOWN
        )
        self.play(TransformMatchingTex(step1.copy(), step2))
        self.wait(1)

        # 両辺を2乗して整理
        step3 = MathTex("a^2 + xc = a \\sqrt{(x+c)^2+y^2}").next_to(step2, DOWN)
        self.play(TransformMatchingTex(step2.copy(), step3))
        self.wait(1)

        # 更に両辺を2乗して整理
        final_step = MathTex("\\frac{x^2}{a^2} + \\frac{y^2}{b^2} = 1").next_to(
            step3, DOWN
        )
        self.play(TransformMatchingTex(step3.copy(), final_step))
        self.wait(1)

        

        # 全体をまとめて表示

        self.play(
            FadeOut(definition),
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),
            FadeOut(text2, text_PF, text_PF_prime),
        )

        #self.play(Write(final_text))

        self.play(final_step.animate.scale(2).move_to(ORIGIN+RIGHT))

        final_text = Text("楕円の式").next_to(final_step, LEFT*2)
        self.play(Write(final_text))
        self.play(Indicate(final_step, color=YELLOW))
        self.wait(1)

        #self.play(ApplyMethod(final_step.shift, 2 * RIGHT))
        #self.play(final_text.next_to(final_step, LEFT, buff=0.5))  # buffは間隔です。適宜調整してください。
        text6=Text("またこの式変形から").next_to(final_text,RIGHT+DOWN*7)
        # 式の定義
        formula1 = MathTex("c^2=a^2-b^2").next_to(text6,DOWN)
        formula3 = MathTex("a>b>0").next_to(formula1,DOWN)
        formula2 = MathTex("\\Rightarrow c= \\pm \\sqrt{a^2-b^2}").next_to(formula3,DOWN)
        
        texttt=Text("とすると").next_to(formula3,RIGHT)

        # 焦点の位置を示す式
        focus_position = MathTex("F(\\sqrt{a^2-b^2}, 0),", "F^\\prime(-\\sqrt{a^2-b^2}, 0)").next_to(formula2,DOWN)

        # アニメーション
        self.play(Write(text6),Write(formula1))
        self.wait(1)
        self.play(Write(formula3),Write(texttt))
        self.wait(1)
        self.play(Write(formula2))
        self.wait(1)
        
        
        # 焦点の位置を示す式のアニメーション
        self.play(Write(focus_position))
        self.wait(4)

       

        
