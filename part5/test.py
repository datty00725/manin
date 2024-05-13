from manim import *

class PlaneIn3D(ThreeDScene):
    def construct(self):
        # 座標軸を作成
        axes = ThreeDAxes()

        # 平面の方程式 y = -x + 2 を3D空間で表現
        # この場合、z = 0 として、xy平面に平面を配置します。
        plane = Surface(
            axis_1=[1, 1, 0],  # 平面の向き
            axis_2=[0, 0, 1],
            color=BLUE,
            u_range=(-5, 5),
            v_range=(-5, 5)
        ).shift(2*UP)  # y軸に沿って平面を上にシフト

        # シーンにオブジェクトを追加
        self.add(axes, plane)

        # カメラの視点を設定
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)

        # シーンを表示するためのアニメーション
        self.begin_ambient_camera_rotation(rate=0.1)  # カメラをゆっくり回転させる
        self.wait(5)
        self.stop_ambient_camera_rotation()  # カメラの回転を停止
        self.wait(2)

# ファイルを実行するためのコマンド:
# manim -p -ql plane_in_3d.py PlaneIn3D
