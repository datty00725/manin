from manim import *
import numpy as np  # NumPyをインポート


class HyperbolaScene(Scene):
    def construct(self):
        opte = Text("双曲線").scale(5)
        self.play(Write(opte), run_time=2)
        self.wait(1)
        self.play(FadeOut(opte), run_time=2)
        self.wait(1)
        
        a = 2  # 実軸の半分、以前より大きく
        b = 3  # 焦点から中心までの距離、小さくして開きを狭める
        c = np.sqrt(a**2 + b**2)  # 虚軸の半分

        # 焦点FとF'
        f = Dot([c, 0, 0], color=RED)
        f_prime = Dot([-c, 0, 0], color=RED)
        label_f_initial = MathTex("F").next_to(f, DOWN)
        label_f_prime_initial = MathTex("F'").next_to(f_prime, DOWN)

        # θの値を追跡するValueTracker
        theta_tracker = ValueTracker(np.pi / 3)

        # 点Pの更新関数
        def update_p(mob):
            theta = theta_tracker.get_value()
            p_x = a / np.cos(theta)
            p_y = b * np.tan(theta)
            mob.move_to([p_x, p_y, 0])

        # 点Qの更新関数
        def update_q(mob):
            theta = theta_tracker.get_value()
            q_x = -a / np.cos(theta)  # x座標を反転して左側の双曲線に合わせる
            q_y = b * np.tan(theta)
            mob.move_to([q_x, q_y, 0])

        # 点Pの初期位置
        p = Dot(color=BLUE)
        p.add_updater(update_p)

        q = Dot(color=BLUE).add_updater(update_q)

        f.scale(2)
        f_prime.scale(2)
        p.scale(2)
        q.scale(2)

        # 線分PFとPF'の初期状態
        line_pf = Line(p.get_center(), f.get_center(), color=YELLOW)
        line_pf_prime = Line(p.get_center(), f_prime.get_center(), color=YELLOW)

        line_qf = Line(q.get_center(), f.get_center(), color=YELLOW)
        line_qf_prime = Line(q.get_center(), f_prime.get_center(), color=YELLOW)

        self.play(
            Create(f),
            Create(f_prime),
            Create(p),
            Create(q),
            Write(label_f_initial),
            Write(label_f_prime_initial),
        )
        self.wait(1)

        line_pf.add_updater(
            lambda m: m.become(Line(p.get_center(), f.get_center(), color=YELLOW))
        )

        line_pf_prime.add_updater(
            lambda m: m.become(Line(p.get_center(), f_prime.get_center(), color=YELLOW))
        )

        line_qf.add_updater(
            lambda m: m.become(Line(q.get_center(), f.get_center(), color=YELLOW))
        )
        line_qf_prime.add_updater(
            lambda m: m.become(Line(q.get_center(), f_prime.get_center(), color=YELLOW))
        )

        self.play(
            Create(line_pf),
            Create(line_pf_prime),
            Create(line_qf),
            Create(line_qf_prime),
        )

        self.add(p, q, line_pf, line_pf_prime, line_qf, line_qf_prime)
        self.play(
            theta_tracker.animate.set_value(-PI / 3), run_time=5, rate_func=linear
        )
        self.wait(1)

        self.wait()

        # 双曲線を表示するParametricFunctionのt_range調整
        # 右側の双曲線（主軸がx軸に沿う）
        hyperbola_right = ParametricFunction(
            lambda t: np.array([a * np.cosh(t), b * np.sinh(t), 0]),
            t_range=np.array([-3, 3, 0.01]),
            color=WHITE,
        )

        # 左側の双曲線（主軸がx軸に沿う）
        hyperbola_left = ParametricFunction(
            lambda t: np.array(
                [-a * np.cosh(t), b * np.sinh(t), 0]
            ),  # x座標の符号を反転
            t_range=np.array([-3, 3, 0.01]),
            color=WHITE,
        )

        self.play(Create(hyperbola_left), Create(hyperbola_right))
        self.wait(1)

        p.clear_updaters()
        line_pf.clear_updaters()
        line_pf_prime.clear_updaters()
        q.clear_updaters()
        line_qf.clear_updaters()
        line_qf_prime.clear_updaters()

        # 新しい焦点のラベル
        label_f_new = MathTex("F'(-c, 0)").next_to(f, RIGHT)
        label_f_prime_new = MathTex("F(c, 0)").next_to(f_prime, LEFT)

        # 点Pのラベル
        label_p = MathTex("P(x, y)").next_to(p, LEFT)
        label_q = MathTex("Q(-x, y)").next_to(q, RIGHT)
        # label_f_new.scale(0.8)

        # 初期ラベルをフェードアウト
        self.play(FadeOut(label_f_initial), FadeOut(label_f_prime_initial))

        # 新しいラベルをフェードイン
        self.play(
            FadeIn(label_f_new),
            FadeIn(label_f_prime_new),
            FadeIn(label_p),
            FadeIn(label_q),
        )

        # オブジェクトをグループ化
        all_objects = VGroup(
            hyperbola_left,
            hyperbola_right,
            f,
            f_prime,
            label_f_new,
            label_f_prime_new,
            p,
            line_pf,
            line_pf_prime,
            label_p,
            q,
            line_qf,
            line_qf_prime,
            label_q,
        )

        # グループを上にスライドさせる
        self.play(all_objects.animate.shift(UP * 9))

        self.wait(1)

        text1 = Text("双曲線の式を求めることはできるか？")
        text2 = Text("【2点からの距離の差が一定】")
        text3 = Text("この性質を使うんだ")
        text4 = Text("じゃあまず線分の長さを求めなくては！")
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

        self.play(Write(text_PF), Write(text_PF_prime))

        self.play(FadeOut(text1, text3, text4))
        self.play(
            text_PF.animate.shift(UP),
            text_PF_prime.animate.shift(UP),
        )
        # 双曲線の定義
        definition = MathTex("|PF - PF'| = 2a").next_to(text_PF_prime, DOWN)
        self.play(Write(definition))
        self.play(Indicate(definition), Indicate(text2))
        self.wait(2)

        # 式の説明
        explanation = MathTex(
            "|\\sqrt{(x-c)^2+y^2} - \\sqrt{(x+c)^2+y^2}| = 2a"
        ).next_to(definition, DOWN)
        self.play(TransformMatchingTex(definition.copy(), explanation))
        self.wait(2)

        # 式変形ステップ1
        step1 = MathTex("\\sqrt{(x-c)^2+y^2} = \\pm 2a + \\sqrt{(x+c)^2+y^2}").next_to(
            explanation, DOWN
        )
        self.play(TransformMatchingTex(explanation.copy(), step1))
        self.wait(2)

        # 両辺を2乗して整理
        step2 = MathTex("a^2 + xc = \\pm \\sqrt{(x+c)^2+y^2}").next_to(step1, DOWN)
        self.play(TransformMatchingTex(step1.copy(), step2))
        self.wait(2)

        # 更に両辺を2乗して整理
        step3 = MathTex("(c^2-a^2) x^2 - a^2 y^2 = a^2(c^2-a^2)").next_to(step2, DOWN)
        self.play(TransformMatchingTex(step2.copy(), step3))
        self.wait(2)

        # b^2を導入
        step4 = MathTex("b^2 x^2 - a^2 y^2 = a^2 b^2").next_to(step3, DOWN)

        self.play(TransformMatchingTex(step3.copy(), step4))
        self.wait(2)

        final_form = MathTex("\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1").next_to(
            step4, DOWN
        )

        self.play(TransformMatchingTex(step4.copy(), final_form))
        self.wait(1)

        # 全体をまとめて表示
        self.play(
            FadeOut(definition),
            FadeOut(explanation),
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),
            FadeOut(step4),
            FadeOut(text2, text_PF, text_PF_prime),
        )

        self.play(final_form.animate.scale(2).move_to(ORIGIN + RIGHT))
        final_text = Text("双曲線の式").next_to(final_form, LEFT * 2)

        self.play(Write(final_text))
        self.play(Indicate(final_form, color=YELLOW))
        self.wait(1)

        text6 = Text("またこの式変形から").next_to(final_text, RIGHT + DOWN * 7)
        # 式の定義
        formula1 = MathTex("c^2=a^2+b^2").next_to(text6, DOWN)

        formula2 = MathTex("\\Rightarrow c= \\pm \\sqrt{a^2+b^2}").next_to(
            formula1, DOWN
        )

        # 焦点の位置を示す式
        focus_position = MathTex(
            "F(\\sqrt{a^2+b^2}, 0),", "F^\\prime(-\\sqrt{a^2+b^2}, 0)"
        ).next_to(formula2, DOWN)

        # アニメーション
        self.play(Write(text6), Write(formula1))
        self.wait(1)

        self.play(Write(formula2))
        self.wait(1)

        # 焦点の位置を示す式のアニメーション
        self.play(Write(focus_position))
        self.wait(4)
