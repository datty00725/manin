from manim import *

class zoomEcuacion(ZoomedScene):

    def construct(self):
        
        #1:タイトルとManimのロゴ
        titulo1 = Text("ZoomedScene画面の一部を拡大する。").shift(DOWN)
        banner = ManimBanner()
        banner.scale(0.4)
        self.play(Create(titulo1), banner.create())
        self.play(banner.expand())
        self.wait(1)
        self.play(Unwrite(banner))
        
        #2:
        texto1 = Text("ズーム効果は、画面の一部を拡大して移動可能な枠で表示します。")
        texto1.scale(0.75)
        self.play(FadeIn(texto1), run_time=6)
        
        #3:
        texto2=Text("その使用方法を示すために、二次関数を使用します。")
        texto2.scale(0.75)
        self.wait(1)
        self.play(ReplacementTransform(texto1, texto2))
        self.wait(1)
        
        self.play(FadeOut(texto2))
        
        #パラボラの描画
        ax = Axes(
            x_range=[-2, 10, 1],
            y_range=[-2, 22, 1],
            tips = False,
            axis_config={"include_numbers": False},
        )
        cuadricula=number_plane = NumberPlane(
            x_range=[-2, 10, 1],
            y_range=[-2, 22, 1],
            x_length=5,
            y_length=5
        )
        #ax.scale(0.9).shift(DOWN)
        
        y_label = ax.get_y_axis_label("y")
        x_label = ax.get_x_axis_label("x")
        #grid_labels = VGroup(x_label, y_label)
        titulo2 = Title(
            # SyntaxError を防ぐためにスペースを追加
            r"$y=2x^2-12x+20$",
            include_underline=True,
            font_size=40,
        )
        
        
        #描画する関数を定義
        def func(x):
            return 2*x**2-12*x+20
        
        quadratic =  ax.plot(func, color=BLUE)
        quadratic_path=ax.plot(func, x_range=[0, 3], color=BLUE)
        
        grafica=VGroup(quadratic,  ax)
        #grafica.move_to(ORIGIN)
        
        
        self.play(Create(grafica[0]), Unwrite(titulo1))
        self.play(Create(grafica[1]))
        self.wait(2)

        '''self.play(AnimationGroup(*[
            grafica.animate(lag_ratio=0.2, run_time=1.5).shift(DOWN)ç
        ]))'''
        
        #放物線の方程式
        eq = MathTex("y ", " = ", " 2 ", " x ", " ^2 "," -12 ", " x ",  "+20").to_corner(UR).shift(DOWN)
        #eq.add_background_rectangle(opacity=0.7)

        frame_text = Text("フレーム", color=BLUE, font_size=26)
        zoomed_camera_text = Text("ズームフレーム", color=GREEN, font_size=26)

        #self.play(Write(eq))
        
    
        formulaGeneral = MathTex(r"y=ax^2+bx+c", color=TEAL_D)
        formulaGeneral.add_background_rectangle(opacity=0.7)
        VGroup(eq, formulaGeneral).arrange(DOWN).shift(2*UP, 2*RIGHT)
        
        self.play(Write(eq))
        
        self.wait(1)
        texto_explic=Text("方程式の一般形を見てください", font_size=26, color=TEAL_D)
        texto_explic.to_edge(DL)
       
        self.play(Write(texto_explic))
        self.play(FadeIn(formulaGeneral,shift=DOWN))
        self.wait(2)
        self.play(FadeOut(texto_explic))
        self.play(FadeOut(formulaGeneral,shift=UP))
        

        #ズームアニメーションの重要な定義：
    
        #zoomed_camera：拡大したい部分を指すカメラ
        zoomed_camera = self.zoomed_camera
        #zoomed_display：拡大カメラの画像を表示するディスプレイ
        zoomed_display = self.zoomed_display

        #zoomed_camaraのフレーム
        frame = zoomed_camera.frame
        #ディスプレイのフレーム
        frame_zoom = zoomed_display.display_frame
        
        #要素の配置

        #カメラを拡大したい場所に合わせる
        frame.move_to(eq[0])
        
        #ディスプレイを座標の原点に配置する
        zoomed_display.move_to(ORIGIN).shift(2*LEFT, DOWN)
        
        
        #後の作業のためにグラフを移動する
        self.play(grafica.animate.shift(8*UP, LEFT))
        
        #フレームのテキストをフレームに貼り付ける
        frame_text.next_to(frame, UR).add_updater(lambda m: m.next_to(frame, UP))
        
        #フレームとテキストの作成
        self.play(Create(frame), FadeIn(frame_text, shift=UP))
        
        #ズームを開始する
        self.activate_zooming()

        #ズームのディスプレイが表示されるアニメーションを生成
        self.play(self.get_zoomed_display_pop_out_animation())

        #ズームのテキストをディスプレイの横に配置
        zoomed_camera_text.next_to(frame_zoom, RIGHT)
        
        #ズームのテキストを表示
        self.play(FadeIn(zoomed_camera_text, shift=UP))     
        

        #ズームとズームのディスプレイを拡大
        # スケール x y z
        scale_factor1 = [2, 2, 0]
        scale_factor2 = [1, 1, 0]
        self.play(
            frame.animate.scale(scale_factor1),
            zoomed_display.animate.scale(scale_factor2),
        )

        self.wait()

        texto = Text("従属変数", font_size=28).next_to(frame_zoom, DOWN)
        #self.play(ScaleInPlace(zoomed_display, 1.1))
        self.play(Create(texto))
        self.wait()

        texto2 = Text("最高次の係数", font_size=28).next_to(frame_zoom, DOWN)
        self.play(frame.animate.move_to(eq[2]))
        self.play(ReplacementTransform(texto, texto2))
        self.wait()

        texto3 = Text("xの係数", font_size=28).next_to(frame_zoom, DOWN)
        self.play(frame.animate.move_to(eq[5]))
        self.play(ReplacementTransform(texto2, texto3))
        self.wait()

        texto4 = Text("定数項",font_size=28).next_to(frame_zoom, DOWN)
        self.play(frame.animate.move_to(eq[7]))
        self.play(ReplacementTransform(texto3, texto4))
        self.wait()
        
        #ズームを元に戻す
        self.play(Unwrite(zoomed_camera_text), Unwrite(frame_text), Unwrite(texto4))
        self.play(self.get_zoomed_display_pop_out_animation(), rate_func=lambda t: smooth(1 - t))
        self.play(Uncreate(frame_zoom))
        self.wait(1)
        
        
        
        texto5 = Text("定数項の値は、放物線がy軸を切る点を決定します", font_size=30)
        texto5.shift(DOWN)

        self.play(Create(texto5))
        
        self.wait(2)
        
        self.play(FadeOut(texto5))
        
        #点が見えるようにグラフを下げる
        self.play(grafica.animate.shift(8*DOWN, RIGHT))
             
        #交点を作成
        corte_y = [ax.coords_to_point(0, func(0))]
        #描画可能なオブジェクトdotを作成
        dot = Dot(radius=0.07, point=corte_y, color=RED)
    
        self.play(Indicate(dot))
        

        
        
        
        texto6 = Text("y軸との交点", font_size=28, color=TEAL_D).next_to(dot, 2*UP)
        texto6.add_background_rectangle( opacity=0.75)
        self.play(Write(texto6))
        
        self.play(frame.animate.move_to(dot))
        zoomed_display.move_to(ORIGIN).shift(2*RIGHT, DOWN)
        zoomed_display.scale(3)
        self.play(self.get_zoomed_display_pop_out_animation())
        
        self.play(MoveAlongPath(dot, quadratic_path), MoveAlongPath(frame, quadratic_path), run_time=8)
        
        
        self.wait()
        
        texto7 = Text("頂点", color=TEAL_D, font_size=28).next_to(dot,3*UP)
        texto7.add_background_rectangle(opacity=0.75)
        self.play(Write(texto7))
        self.wait()
        self.play(Unwrite(texto6), Unwrite(texto7))
        
        #ズームを元に戻す
        self.play(Unwrite(zoomed_camera_text))
