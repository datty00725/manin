from manim import *
import numpy as np

# 設定を変更します
config.pixel_width = 1000
config.pixel_height = 1000
config.frame_height = 10
config.frame_width = 10
config.frame_rate = 60
config.background_color = "#000000"


# フーリエのエピサイクルを描画するクラス
class FourierEpicyclesMObject(VMobject):
    def __init__(
        self,
        complex_points,  # 複素数の点
        num_coefs=None,  # フーリエ係数の数
        speed_factor=1.0,  # 速度の倍率
        circles_color="#06d6a0",  # 円の色
        circles_width=1,  # 円の幅
        circles_opacity=1,  # 円の透明度
        vectors_color="#ef476f",  # ベクトルの色
        vectors_width=4,  # ベクトルの幅
        vectors_opacity=1,  # ベクトルの透明度
        bg_shape_color=GRAY_C,  # 背景形状の色
        bg_shape_stroke_width=1,  # 背景形状の幅
        bg_shape_opacity=1,  # 背景形状の透明度
        path_color=TEAL,  # パスの色
        path_width=4,  # パスの幅
        path_opacity=1,  # パスの透明度
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

    # 背景形状を初期化するメソッド
    def _init_bg_shape(self, color=GRAY_C, stroke_width=1, stroke_opacity=1):
        real_points = list(map(complex_to_R3, self.complex_points))
        self.path = VMobject(
            stroke_color=color, stroke_width=stroke_width, stroke_opacity=stroke_opacity
        ).set_points_as_corners([real_points[-1], *real_points])
        self.add(self.path)
        return self

    # エピサイクルを初期化するメソッド
    def _init_epicycles(self, c_color, c_width, c_opacity, v_color, v_width, v_opacity):
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

    # パスを初期化するメソッド
    def _init_path(self, color, width, opacity):
        self.trace = TracedPath(
            self.epicycles[-1]["vector"].get_end,
            stroke_color=color,
            stroke_width=width,
            stroke_opacity=opacity,
        )
        self.add(self.trace)
        return self

    # エピサイクルを取得するメソッド
    def get_epicycles(self):
        return self.epicycles

    # 円を取得するメソッド
    def get_circles(self):
        return self.circles

    # ベクトルを取得するメソッド
    def get_vectors(self):
        return self.vectors


# フーリエエピサイクルとズームを含むシーン
class FourierZoom(ZoomedScene):
    def construct(self):
        N = 1000
        NumberOfCoeff = 4
        shape = Text("あ")

        # 形状を取得する関数
        def get_shape(shape):
            path = VMobject()
            shape = shape
            for sp in shape.family_members_with_points():
                path.append_points(sp.get_points())
            return path

        path = get_shape(shape)
        complex_points = np.array(
            [
                complex(*path.point_from_proportion(alpha)[:2])
                for alpha in np.arange(0, 1, 1 / N)
            ]
        )
        complex_points = (
            (complex_points - np.mean(complex_points)) / np.max(abs(complex_points)) * 4
        )

        # エピサイクルを作成
        ec = FourierEpicyclesMObject(
            complex_points,
            num_coefs=NumberOfCoeff,
            speed_factor=1,
            circles_color="#118ab2",
            circles_opacity=1,
        )

        self.add(ec)
        self.wait(2)

        # 一番小さい円（実際にパスを描画している円）を取得
        smallest_circle = ec.circles[NumberOfCoeff - 1]

        # ズームを有効にする
        self.activate_zooming()

        # カメラフレームを一番小さい円に移動
        self.zoomed_camera.frame.move_to(smallest_circle)

        # フレームを作成
        self.play(Create(self.zoomed_camera.frame))

        # ズームディスプレイを表示するアニメーション
        self.play(self.get_zoomed_display_pop_out_animation(), run_time=2)
        self.wait(2 * TAU)

        # フレームを削除
        self.play(Uncreate(self.zoomed_camera.frame))
        self.wait()
