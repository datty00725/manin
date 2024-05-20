from manim import *

class FourierTex(Scene):
    def __init__(self, n_vectors=100, **kwargs):
        super().__init__(**kwargs)
        self.n_vectors = n_vectors  # フーリエベクトルの数
        self.center_point = ORIGIN  # アニメーションの中心点
        self.slow_factor = 0.5  # アニメーションの速度を調整する係数

    def get_freqs(self):
        n = self.n_vectors
        all_freqs = list(range(n // 2, -n // 2, -1))  # 周波数リストを生成
        all_freqs.sort(key=abs)  # 絶対値の昇順にソート
        return all_freqs

    # フーリエ級数を計算するメソッド
    # Grant Sanderson（3Blue1Brown）のコードを参考にしています
    def get_coefficients_of_path(self, path, n_samples=10000, freqs=None):
        if freqs is None:
            freqs = self.get_freqs()
        dt = 1 / n_samples
        ts = np.arange(0, 1, dt)
        samples = np.array([
            path.point_from_proportion(t)
            for t in ts
        ])
        samples -= self.center_point
        complex_samples = samples[:, 0] + 1j * samples[:, 1]
 
        return [
            np.array([
                np.exp(-TAU * 1j * freq * t) * cs
                for t, cs in zip(ts, complex_samples)
            ]).sum() * dt for freq in freqs
        ]

    # "T"文字のパスを取得するメソッド
    def get_paths(self):
        tex_mob = Text("か")  # "T"文字を作成
        tex_mob.scale_to_fit_width(10)  # 幅を10にスケーリング
        paths = tex_mob.family_members_with_points()
        for p in paths:
            p.set_fill(opacity=0)  # 塗りつぶしの透明度を0に設定
            p.set_stroke(WHITE, 1)  # ストロークの色を白、幅を1に設定
        return paths

    def construct(self):
        for i in range(24,20+3+2,20):
            self.n_vectors =i  # ここでn_vectorsの値を変更
            #npl = NumberPlane()  # 座標平面を作成
            #npl.add_coordinates()  # 座標を追加
            #self.add(npl)  # 座標平面をシーンに追加

            freqs = self.get_freqs()  # 周波数リストを取得
            paths = self.get_paths()  # パスを取得
            for path in paths:
                for subpath in path.get_subpaths():
                    sp_mob = VMobject()
                    sp_mob.set_points(subpath)
                    coefs = self.get_coefficients_of_path(sp_mob, n_samples=100, freqs=freqs)  # フーリエ係数を計算

                    vectorsCircles = VGroup()  # ベクトルと円のグループを作成
                    #origin = ORIGIN  # 原点を設定
                    for i in range(len(freqs)):
                        print("{:3.0f}: abs = {:5.3f}  Z = {:-5.3f} + {:-5.3f}j".format(
                            freqs[i],
                            np.abs(coefs[i]),
                            np.real(coefs[i]),
                            np.imag(coefs[i])))
                        dummy = Line(
                            start=ORIGIN,
                            end=[np.real(coefs[i]), np.imag(coefs[i]), 0]
                        )  # フーリエ係数に基づくベクトルを作成
                        circ = Circle(radius=np.abs(coefs[i])).set_stroke(width=1, color=RED)  # フーリエ係数に基づく円を作成
                        vectorsCircles += VGroup(dummy, circ).shift(origin)  # ベクトルと円をグループに追加してシフト
                        origin = dummy.get_end()  # 新しい原点を設定

                    self.play(DrawBorderThenFill(vectorsCircles))  # ベクトルと円を描画
                    self.wait()  # 一時停止

                    dot = always_redraw(lambda: Dot(vectorsCircles[-1][0].get_end(), radius=0.04, color=GREEN))  # ドットを常に更新
                    trace = VMobject().set_points([vectorsCircles[-1][0].get_end()]).set_color(YELLOW)  # ドットの軌跡を設定
                    self.add(trace, dot)  # ドットと軌跡をシーンに追加

                    def vectorsUpdater(mobj, dt):
                        origin = mobj[0][0].get_end()  # 初期原点を取得
                        for i in range(1, len(freqs)):
                            mobj[i][0].rotate(2 * PI * dt * freqs[i] * self.slow_factor, about_point=mobj[i][0].get_start())  # ベクトルを回転
                            mobj[i].shift(origin - mobj[i][0].get_start())  # ベクトルをシフト
                            origin = mobj[i][0].get_end()  # 新しい原点を取得
                        trace.add_line_to(mobj[-1][0].get_end())  # トレースにラインを追加

                    vectorsCircles.add_updater(vectorsUpdater)  # アップデータを追加
                    self.wait(1 / self.slow_factor + 1)  # 一時停止
                    vectorsCircles.remove_updater(vectorsUpdater)  # アップデータを削除
                    self.play(FadeOut(vectorsCircles))  # ベクトルと円をフェードアウト
                    self.wait(2)  # 一時停止
                
                # ここでoriginをリセット
                #origin = ORIGIN
