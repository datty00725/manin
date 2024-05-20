from manim import *
import itertools as it
from functools import reduce
import operator as op

class FourierTex(Scene):
    CONFIG = {
        "n_vectors": 50,
        "center_point": ORIGIN,
        "slow_factor": 0.05,
        "n_cycles": None,
        "run_time": 10,
        "tex": r"\rm M",
        "start_drawn": True,
        "path_custom_position": lambda mob: mob,
        "max_circle_stroke_width": 1,
        "tex_class": Tex,
        "tex_config": {
            "fill_opacity": 0,
            "stroke_width": 1,
            "stroke_color": WHITE
        },
        "include_zoom_camera": False,
        "scale_zoom_camera_to_full_screen": False,
        "scale_zoom_camera_to_full_screen_at": 1,
        "zoom_position": lambda mob: mob.scale(0.8).move_to(ORIGIN).to_edge(RIGHT)
    }

    def __init__(self, n_vectors=100, **kwargs):
        super().__init__(**kwargs)
        config = {**self.CONFIG, **kwargs}
        self.n_vectors = config["n_vectors"]
        self.center_point = config["center_point"]
        self.slow_factor = config["slow_factor"]
        self.include_zoom_camera = config["include_zoom_camera"]
        self.scale_zoom_camera_to_full_screen = config["scale_zoom_camera_to_full_screen"]
        self.scale_zoom_camera_to_full_screen_at = config["scale_zoom_camera_to_full_screen_at"]
        self.zoom_position = config["zoom_position"]
        self.tex_config = config["tex_config"]

        self.vector_config = {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.7,
        }
        self.circle_config = {
            "stroke_width": 1,
        }
        self.base_frequency = 1
        self.parametric_function_step_size = 0.001
        self.drawn_path_color = YELLOW
        self.drawn_path_stroke_width = 2
        self.interpolate_config = [0, 1]
        self.zoom_factor = 0.3
        self.zoomed_display_height = 3
        self.zoomed_display_width = 4
        self.image_frame_stroke_width = 1
        self.zoomed_camera_config = {
            "default_frame_stroke_width": 3,
            "cairo_line_width_multiple": 0.05,
        }
        self.zoom_camera_to_full_screen_config = {
            "run_time": 3,
            "func": there_and_back_with_pause,
            "velocity_factor": 1
        }
        self.wait_before_start = None



    def get_freqs(self):
        n = self.n_vectors
        all_freqs = list(range(n // 2, -n // 2, -1))  # 周波数リストを生成
        all_freqs.sort(key=abs)  # 絶対値の昇順にソート
        return all_freqs

    # フーリエ級数を計算するメソッド
    def get_coefficients_of_path(self, path, n_samples=10000, freqs=None):
        if freqs is None:
            freqs = self.get_freqs()
        dt = 1 / n_samples
        ts = np.arange(0, 1, dt)
        samples = np.array([path.point_from_proportion(t) for t in ts])
        samples -= self.center_point
        complex_samples = samples[:, 0] + 1j * samples[:, 1]

        result = []
        for freq in freqs:
            riemann_sum = np.array([
                np.exp(-TAU * 1j * freq * t) * cs
                for t, cs in zip(ts, complex_samples)
            ]).sum() * dt
            result.append(riemann_sum)

        return result

    # "か"文字のパスを取得するメソッド
    def get_paths(self):
        tex_mob = Text("か")  # "か"文字を作成
        tex_mob.scale_to_fit_width(10)  # 幅を10にスケーリング
        paths = tex_mob.family_members_with_points()
        for p in paths:
            p.set_fill(opacity=0)  # 塗りつぶしの透明度を0に設定
            p.set_stroke(WHITE, 1)  # ストロークの色を白、幅を1に設定
        return paths

    def add_vector_clock(self):
        self.vector_clock.add_updater(
            lambda m, dt: m.increment_value(
                self.get_slow_factor() * dt
            )
        )
 
    def get_slow_factor(self):
        return self.slow_factor_tracker.get_value()
 
    def get_vector_time(self):
        return self.vector_clock.get_value()
 
    def get_freqs(self):
        n = self.n_vectors
        all_freqs = list(range(n // 2, -n // 2, -1))
        all_freqs.sort(key=abs)
        return all_freqs
 
    def get_coefficients(self):
        return [complex(0) for _ in range(self.n_vectors)]
 
    def get_color_iterator(self):
        return it.cycle(self.colors)
 
    def get_rotating_vectors(self, freqs=None, coefficients=None):
        vectors = VGroup()
        self.center_tracker = VectorizedPoint(self.center_point)
 
        if freqs is None:
            freqs = self.get_freqs()
        if coefficients is None:
            coefficients = self.get_coefficients()
 
        last_vector = None
        for freq, coefficient in zip(freqs, coefficients):
            if last_vector:
                center_func = last_vector.get_end
            else:
                center_func = self.center_tracker.get_location
            vector = self.get_rotating_vector(
                coefficient=coefficient,
                freq=freq,
                center_func=center_func,
            )
            vectors.add(vector)
            last_vector = vector
        return vectors
 
    def get_rotating_vector(self, coefficient, freq, center_func):
        vector = Vector(RIGHT, **self.vector_config)
        vector.scale(abs(coefficient))
        if abs(coefficient) == 0:
            phase = 0
        else:
            phase = np.log(coefficient).imag
        vector.rotate(phase, about_point=ORIGIN)
        vector.freq = freq
        vector.coefficient = coefficient
        vector.center_func = center_func
        vector.add_updater(self.update_vector)
        return vector
 
    def update_vector(self, vector, dt):
        time = self.get_vector_time()
        coef = vector.coefficient
        freq = vector.freq
        phase = np.log(coef).imag
 
        vector.set_length(abs(coef))
        vector.set_angle(phase + time * freq * TAU)
        vector.shift(vector.center_func() - vector.get_start())
        return vector
 
    def get_circles(self, vectors):
        return VGroup(*[
            self.get_circle(
                vector,
                color=color
            )
            for vector, color in zip(
                vectors,
                self.get_color_iterator()
            )
        ])
 
    def get_circle(self, vector, color=BLUE):
        circle = Circle(color=color, **self.circle_config)
        circle.center_func = vector.get_start
        circle.radius_func = vector.get_length
        circle.add_updater(self.update_circle)
        return circle
 
    def update_circle(self, circle):
        circle.set_width(2 * circle.radius_func())
        circle.move_to(circle.center_func())
        return circle
 
    def get_vector_sum_path(self, vectors, color=YELLOW):
        coefs = [v.coefficient for v in vectors]
        freqs = [v.freq for v in vectors]
        center = vectors[0].get_start()
 
        path = ParametricFunction(
            lambda t: center + reduce(op.add, [
                complex_to_R3(
                    coef * np.exp(TAU * 1j * freq * t)
                )
                for coef, freq in zip(coefs, freqs)
            ]),
            t_min=0,
            t_max=1,
            color=color,
            step_size=self.parametric_function_step_size,
        )
        return path
 
    def get_drawn_path_alpha(self):
        return self.get_vector_time()
 
    def get_drawn_path(self, vectors, stroke_width=None, **kwargs):
        if stroke_width is None:
            stroke_width = self.drawn_path_stroke_width
        path = self.get_vector_sum_path(vectors, **kwargs)
        broken_path = CurvesAsSubmobjects(path)
        broken_path.curr_time = 0
        start, end = self.interpolate_config
 
        def update_path(path, dt):
            alpha = self.get_drawn_path_alpha()
            n_curves = len(path)
            for a, sp in zip(np.linspace(0, 1, n_curves), path):
                b = (alpha - a)
                if b < 0:
                    width = 0
                else:
                    width = stroke_width * interpolate(start, end, (1 - (b % 1)))
                sp.set_stroke(width=width)
            path.curr_time += dt
            return path
 
        broken_path.set_color(self.drawn_path_color)
        broken_path.add_updater(update_path)
        return broken_path
 
    def get_y_component_wave(self,
                             vectors,
                             left_x=1,
                             color=PINK,
                             n_copies=2,
                             right_shift_rate=5):
        path = self.get_vector_sum_path(vectors)
        wave = ParametricFunction(
            lambda t: op.add(
                right_shift_rate * t * LEFT,
                path.function(t)[1] * UP
            ),
            t_min=path.t_min,
            t_max=path.t_max,
            color=color,
        )
        wave_copies = VGroup(*[
            wave.copy()
            for x in range(n_copies)
        ])
        wave_copies.arrange(RIGHT, buff=0)
        top_point = wave_copies.get_top()
        wave.creation = Create(
            wave,
            run_time=(1 / self.get_slow_factor()),
            rate_func=linear,
        )
        cycle_animation(wave.creation)
        wave.add_updater(lambda m: m.shift(
            (m.get_left()[0] - left_x) * LEFT
        ))
 
        def update_wave_copies(wcs):
            index = int(
                wave.creation.total_time * self.get_slow_factor()
            )
            wcs[:index].match_style(wave)
            wcs[index:].set_stroke(width=0)
            wcs.next_to(wave, RIGHT, buff=0)
            wcs.align_to(top_point, UP)
        wave_copies.add_updater(update_wave_copies)
 
        return VGroup(wave, wave_copies)
 
    def get_wave_y_line(self, vectors, wave):
        return DashedLine(
            vectors[-1].get_end(),
            wave[0].get_end(),
            stroke_width=1,
            dash_length=DEFAULT_DASH_LENGTH * 0.5,
        )
 
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
    
    def add_vectors_circles_path(self):
        path = self.get_path()
        self.path_custom_position(path)
        coefs = self.get_coefficients_of_path(path)
        vectors = self.get_rotating_vectors(coefficients=coefs)
        circles = self.get_circles(vectors)
        self.set_decreasing_stroke_widths(circles)
        drawn_path = self.get_drawn_path(vectors)
        if self.start_drawn:
            self.vector_clock.increment_value(1)
        self.add(path)
        self.add(vectors)
        self.add(circles)
        self.add(drawn_path)
 
        self.vectors = vectors
        self.circles = circles
        self.path = path
        self.drawn_path = drawn_path
 
    def run_one_cycle(self):
        time = 1 / self.slow_factor
        self.wait(time)
 
    def set_decreasing_stroke_widths(self, circles):
        mcsw = self.max_circle_stroke_width
        for k, circle in zip(it.count(1), circles):
            circle.set_stroke(width=max(
                mcsw / k,
                mcsw,
            ))
        return circles
 
    def get_path(self):
        tex_mob = self.tex_class(self.tex, **self.tex_config)
        tex_mob.set_height(6)
        path = tex_mob.family_members_with_points()[0]
        return path
 

    def construct(self):
        for i in [400]:
            self.n_vectors = i  # ここでn_vectorsの値を変更

            freqs = self.get_freqs()  # 周波数リストを取得
            paths = self.get_paths()  # パスを取得
            for path in paths:
                for subpath in path.get_subpaths():
                    sp_mob = VMobject()
                    sp_mob.set_points(subpath)
                    coefs = self.get_coefficients_of_path(sp_mob)
                    new_vectors = self.get_rotating_vectors(coefficients=coefs)
                    new_circles = self.get_circles(new_vectors)
                    self.set_decreasing_stroke_widths(new_circles)

                    drawn_path = self.get_drawn_path(new_vectors)
                    drawn_path.clear_updaters()

                    static_vectors = VMobject().become(new_vectors)
                    static_circles = VMobject().become(new_circles)

                    self.play(
                        Transform(vectors, static_vectors, remover=True),
                        Transform(circles, static_circles, remover=True),
                        frame.set_height,
                        frame.move_to, path,
                    )

                    self.add(new_vectors, new_circles)
                    self.vector_clock.set_value(0)
                    self.play(
                        Create(drawn_path),
                        rate_func=linear,
                        run_time=self.time_per_symbol
                    )
                    self.remove(new_vectors, new_circles)
                    self.add(static_vectors, static_circles)

                    vectors = static_vectors
                    circles = static_circles
            self.play(
                FadeOut(vectors),
                FadeOut(circles),
                Restore(frame),
                run_time=2
            )
            self.wait(3)
