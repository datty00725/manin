from manim import *


class FourierEpicyclesMObject(VMobject):
    def __init__(
        self,
        complex_points,
        num_coefs=None,
        speed_factor=1.0,
        circles_color="#06d6a0",
        circles_width=1,
        circles_opacity=1,
        vectors_color="#ef476f",
        vectors_width=4,
        vectors_opacity=1,
        bg_shape_color=GRAY_C,
        bg_shape_stroke_width=1,
        bg_shape_opacity=1,
        path_color=TEAL,
        path_width=4,
        path_opacity=1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.complex_points = complex_points
        self.N = len(self.complex_points)
        self.K = num_coefs if num_coefs is not None else self.N
        self.speed_factor = 0.1 * speed_factor * self.N
        self.circles = VGroup()
        self.vectors = VGroup()
        self._init_bg_shape(bg_shape_color, bg_shape_stroke_width, bg_shape_opacity)
        self._init_epicycles(
            circles_color,
            circles_width,
            circles_opacity,
            vectors_color,
            vectors_width,
            vectors_opacity,
        )
        self._init_path(path_color, path_width, path_opacity)

    def _init_bg_shape(self, color=GRAY_C, stroke_width=1, stroke_opacity=1):
        # バックグラウンドの形状を初期化
        real_points = list(map(complex_to_R3, self.complex_points))
        self.path = VMobject(
            stroke_color=color, stroke_width=stroke_width, stroke_opacity=stroke_opacity
        ).set_points_as_corners([real_points[-1], *real_points])
        self.add(self.path)
        return self

    def _init_epicycles(self, c_color, c_width, c_opacity, v_color, v_width, v_opacity):
        # エピサイクルを初期化
        def create_one_epicycle(radius, angle):
            circle = Circle(
                radius=radius,
                stroke_color=c_color,
                stroke_width=c_width,
                stroke_opacity=c_opacity,
            )
            vector = Line(
                ORIGIN,
                circle.get_right(),
                stroke_color=v_color,
                stroke_width=v_width,
                stroke_opacity=v_opacity,
            )
            return VDict([("circle", circle), ("vector", vector)]).rotate(angle)

        fft = np.fft.fft(self.complex_points) / self.N
        self.epicycles = VGroup(VDict([("vector", Dot(radius=0))]))
        for i, k in enumerate([int(i / 2) * (-1) ** i for i in range(1, self.K + 1)]):
            epicycle = create_one_epicycle(radius=abs(fft[k]), angle=np.angle(fft[k]))
            epicycle.set(previous=self.epicycles[i]["vector"].get_end)
            epicycle.set(speed=TAU * k / self.N)
            epicycle.move_to(epicycle.previous())
            epicycle.add_updater(
                lambda e, dt: e.move_to(e.previous()).rotate(
                    e.speed * dt * self.speed_factor
                )
            )
            self.epicycles.add(epicycle)
            self.circles.add(epicycle["circle"])
            self.vectors.add(epicycle["vector"])
        self.add(self.epicycles)
        return self

    def _init_path(self, color, width, opacity):
        # トレースパスを初期化
        self.trace = TracedPath(
            self.epicycles[-1]["vector"].get_end,
            stroke_color=color,
            stroke_width=width,
            stroke_opacity=opacity,
        )
        self.add(self.trace)
        return self

    def get_epicycles(self):
        return self.epicycles

    def get_circles(self):
        return self.circles

    def get_vectors(self):
        return self.vectors


class Pi(ZoomedScene):
    CONFIG = {
        # エピサイクルの数。この値を増やすと、描画される図形がより精密になります。
        "n_vectors": 4,
        # アニメーション全体の実行時間（秒単位）。この値を増やすと、アニメーションがゆっくりと実行されます。
        "run_time": 4,
        # アニメーションの速度。この値を増やすと、アニメーションが速くなります。
        "slow_factor": 0.5,
        # ズームの倍率。この値を増やすと、ズームインの度合いが強くなります。
        "zoom_factor": 0.3,
        # ズームされた表示の高さ。この値を増やすと、表示が大きくなります。
        "zoomed_display_height": 5,
        # ズームされた表示の幅。この値を増やすと、表示が広くなります。
        "zoomed_display_width": 5,
        # ズームフレームの枠線の幅。この値を増やすと、枠線が太くなります。
        "image_frame_stroke_width": 1,
        "zoomed_camera_config": {
            # ズームカメラフレームの枠線の幅。この値を増やすと、枠線が太くなります。
            "default_frame_stroke_width": 3,
            # カイロラインの幅の倍率。この値を増やすと、線が太くなります。
            "cairo_line_width_multiple": 0.05,
        },
    }

    def construct(self):
        # シーンの構築
        N = 1000
        shape = Text("あ")

        def get_shape(shape):
            # 形状からパスを取得
            path = VMobject()
            for sp in shape.family_members_with_points():
                path.append_points(sp.get_points())
            return path

        path = get_shape(shape)
        # パスのポイントを複素数配列に変換
        complex_points = np.array(
            [
                complex(*path.point_from_proportion(alpha)[:2])
                for alpha in np.arange(0, 1, 1 / N)
            ]
        )
        # パスを正規化
        complex_points = (
            (complex_points - np.mean(complex_points)) / np.max(abs(complex_points)) * 4
        )

        # フォーリエエピサイクルオブジェクトを作成
        ec = FourierEpicyclesMObject(
            complex_points,
            num_coefs=self.CONFIG["n_vectors"],
            speed_factor=self.CONFIG["slow_factor"],
            circles_color="#118ab2",
            circles_opacity=1,
        )
        

        # ズームカメラの設定
        self.activate_zooming(animate=False)
        zoomed_camera_frame = self.zoomed_camera.frame
        zoomed_display = self.zoomed_display
        zoomed_display_frame = zoomed_display.display_frame

        zoomed_camera_frame.set_width(2)
        zoomed_camera_frame.move_to(ec.get_epicycles()[-1]["vector"].get_end())

        # 位置を変更する例
        zoomed_display.shift(DOWN)  # 下にシフト
        # zoomed_display.move_to(ORIGIN)  # 中央に移動
        # zoomed_display.to_corner(UR)  # 右上の角に移動
        # zoomed_display.to_edge(LEFT)  # 左端に移動

        zoomed_display.set_height(3)

        # ズームディスプレイフレームを作成して表示
        #self.play(Create(zoomed_display_frame))
        #self.play(FadeIn(zoomed_display))

        self.play(Create(ec))
        # ズームカメラフレームがエピサイクルの終点を追従するようにアップデート
        zoomed_camera_frame.add_updater(
            lambda mob: mob.move_to(ec.get_epicycles()[-1]["vector"].get_end())
        )

        # アニメーションを実行
        self.wait(4 * TAU)

        # アップデーターを削除し、ズームディスプレイをフェードアウト
        #zoomed_camera_frame.remove_updater(
        #    lambda mob: mob.move_to(ec.get_epicycles()[-1]["vector"].get_end())
        #)
        self.play(FadeOut(zoomed_display), FadeOut(zoomed_display_frame))
