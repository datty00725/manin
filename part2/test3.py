from manim import *


class HyperbolaDerivation(Scene):
    def construct(self):
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
        self.play(Indicate(definition),Indicate(text2))
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
            FadeOut(text2, text_PF, text_PF_prime)
        )

        self.play(final_form.animate.scale(2).move_to(ORIGIN+RIGHT))
        final_text = Text("双曲線の式").next_to(final_form, LEFT*2)

        self.play(Write(final_text))
        self.play(Indicate(final_form, color=YELLOW))
        self.wait(1)

        text6=Text("またこの式変形から").next_to(final_text,RIGHT+DOWN*7)
        # 式の定義
        formula1 = MathTex("c^2=a^2+b^2").next_to(text6,DOWN)
        
        formula2 = MathTex("\\Rightarrow c= \\pm \\sqrt{a^2+b^2}").next_to(formula1,DOWN)
        
        

        # 焦点の位置を示す式
        focus_position = MathTex("F(\\sqrt{a^2+b^2}, 0),", "F^\\prime(-\\sqrt{a^2+b^2}, 0)").next_to(formula2,DOWN)

        # アニメーション
        self.play(Write(text6),Write(formula1))
        self.wait(1)
        
        self.play(Write(formula2))
        self.wait(1)
        
        
        # 焦点の位置を示す式のアニメーション
        self.play(Write(focus_position))
        self.wait(4)