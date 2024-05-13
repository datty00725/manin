from manim import *

class EllipseDerivation(Scene):
    def construct(self):
        # 楕円の定義
        text1=Text("楕円の式を求めよう！").scale(0.75)
        text2=Text("2つの線分を足したものは常に等しい").scale(0.75)
        text3=Text("この性質を使いたい").scale(0.75)
        text4=Text("線分の長さを求めなくては！").scale(0.75)
        text2.next_to(text1, DOWN)
        text3.next_to(text2, DOWN)
        text4.next_to(text3, DOWN)

        self.play(Write(text1))
        self.wait(2)
        self.play(Write(text2))
        self.wait(2)
        self.play(Write(text3))
        self.wait(2)
        self.play(Write(text4))
        self.wait()

        first_objects = VGroup(text1,text2,text3,text4)


        self.play(ApplyMethod(first_objects.shift, 3 * UP))
        self.wait()


        self.wait(2)
        text_PF=MathTex(
            "PF = \\sqrt{(x-c)^2+y^2}"
        ).scale(0.75)
        text_PF_prime=MathTex(
            "PF' = \\sqrt{(x+c)^2+y^2}"
        ).scale(0.75)
        text_PF_prime.next_to(text_PF, DOWN)

        self.play(Write(text_PF))
        self.wait(2)
        self.play(Write(text_PF_prime))
        self.wait(2)

        self.play(FadeOut(text1,text3,text4))
        self.play(text2.animate.shift(UP),text_PF.animate.shift(UP*2),text_PF_prime.animate.shift(UP*2))

        definition = MathTex(
            "PF + PF' = 2a"
        ).scale(0.75)  # scaleメソッドを適用してサイズを変更

        # MathTexオブジェクトを配置
    
        self.play(Write(definition))
        self.wait(2)

        # 式変形ステップ1
        step1 = MathTex(
            "\\sqrt{(x-c)^2+y^2} + \\sqrt{(x+c)^2+y^2} = 2a"
        ).scale(0.75).next_to(definition, DOWN)
        self.play(TransformMatchingTex(definition.copy(), step1))
        self.wait(2)

        # 式変形ステップ2
        step2 = MathTex(
            "\\sqrt{(x-c)^2+y^2} = 2a - \\sqrt{(x+c)^2+y^2}"
        ).scale(0.75).next_to(step1, DOWN)
        self.play(TransformMatchingTex(step1.copy(), step2))
        self.wait(2)

        # 両辺を2乗して整理
        step3 = MathTex(
            "a^2 + xc = a \\sqrt{(x+c)^2+y^2}"
        ).scale(0.75).next_to(step2, DOWN)
        self.play(TransformMatchingTex(step2.copy(), step3))
        self.wait(2)

        # 更に両辺を2乗して整理
        final_step = MathTex(
            "\\frac{x^2}{a^2} + \\frac{y^2}{b^2} = 1"
        ).scale(0.75).next_to(step3, DOWN)
        self.play(TransformMatchingTex(step3.copy(), final_step))
        self.wait(2)

        final_text=Text("楕円の式").next_to(final_step, UP)


        # 全体をまとめて表示
        
        

        self.play(
            FadeOut(definition),
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),FadeOut(text2,text_PF,text_PF_prime))
        

        self.play(Write(final_text))

        self.play(final_step.animate.scale(1.5).move_to(ORIGIN)
        )
        self.play( Indicate(final_step, color=YELLOW))
        self.wait(2)