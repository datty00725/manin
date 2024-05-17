# SVGから行けるかなと思ったけど無理

import random
import numpy as np
import manim as mn
from svgpathtools import svg2paths,parse_path

def integrate(func, a, b, *, dx=0.01):
    return sum(func(x) * dx for x in np.arange(a, b, dx))

class SVGPath(mn.VMobject):
    def __init__(self, path_str, *, num_points=500, **kwargs):
        self.path = parse_path(path_str)
        self.num_points = num_points
        super().__init__(**kwargs)

    def point(self, alpha):
        z = self.path.point(alpha)
        return np.array([z.real, z.imag, 0])

    def generate_points(self):
        step = 1 / self.num_points
        points = [self.point(x) for x in np.arange(0, 1, step)]
        self.start_new_path(points[0])
        self.add_points_as_corners(points[1:])
        self.add_line_to(self.point(1))
        self.flip(mn.RIGHT)
        self.center()
        return self

class Epicycle(mn.VMobject):
    def __init__(self, path, coeff_start, coeff_end=None, *, num_points=500, **kwargs):
        self.num_points = num_points
        if coeff_end is None:
            coeff_end = int(np.ceil(coeff_start / 2))
            coeff_start = coeff_end - coeff_start
        self.coeffs = self.gen_fourier_coeffs(path, coeff_start, coeff_end)
        super().__init__(**kwargs)

    def generate_points(self):
        step = 1 / self.num_points
        points = [self.point(x) for x in np.arange(0, 1, step)]
        self.start_new_path(points[0])
        self.add_points_as_corners(points[1:])
        self.add_line_to(points[0])
        return self

    def point(self, alpha):
        z = sum(radius * np.exp(alpha * speed * mn.TAU * 1j) for speed, radius in self.coeffs.items())
        return np.array([z.real, z.imag, 0])

    def gen_fourier_coeffs(self, path, start, end):
        def point(alpha):
            pt = path.point_from_proportion(alpha) - path.get_center()
            return complex(pt[0], pt[1])

        return {i: integrate(lambda x: point(x) * np.exp(x * -i * mn.TAU * 1j), 0, 1) for i in range(start, end)}

    def draw_circles(self, alpha, whole_mobject=None, **kwargs):
        if whole_mobject is None:
            whole_mobject = self.copy()

        self.submobjects.clear()
        self.pointwise_become_partial(whole_mobject, 0, alpha)
        speeds_and_radii = sorted(self.coeffs.items(), key=lambda x: abs(x[1]), reverse=True)

        z = 0
        for speed, radius in speeds_and_radii:
            circ = mn.Circle(**kwargs)
            circ.scale(abs(radius))
            circ.move_to([z.real, z.imag, 0])
            self.add(circ)
            z += radius * np.exp(alpha * speed * mn.TAU * 1j)

        return self

    def animate_circles(self, **kwargs):
        class Draw(mn.Animation):
            def interpolate_submobject(self, submobject, starting_submobject, alpha):
                submobject.draw_circles(alpha, starting_submobject, **kwargs)

        return Draw(self)

class EpicCycle(mn.Scene):
    def construct(self):
        # SVGファイルのパス
        svg_path = "music_symbols.svg"  # SVGファイルのパスを指定

        # SVGファイルからパスを読み込む
        paths, attributes = svg2paths(svg_path)
        path_str = str(paths[0])

        # SVGPathオブジェクトを作成
        path = SVGPath(path_str).scale(1.75)
        path.set_color(mn.RED).set_opacity(0.5)
        self.add(path)

        for num_coeffs in range(2, 105 + 1, 260):
            ep = Epicycle(path, num_coeffs)
            ep_copy = ep.copy().draw_circles(0, color=mn.BLUE)

            text = mn.Tex(f"Cycles: {num_coeffs}").to_edge(mn.UP).shift(mn.LEFT)
            self.play(mn.FadeIn(mn.VGroup(ep_copy, text)), run_time=0.75)
            self.wait(1)
            self.play(mn.FadeOut(ep_copy))
            self.remove(ep_copy)

            ep.clear_points()
            ep.submobjects.clear()

            self.play(ep.animate_circles(color=mn.BLUE), run_time=10, rate_func=mn.linear)
            self.play(mn.FadeOut(mn.VGroup(ep, text)))

