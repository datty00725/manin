# Based on the code found here:
# https://github.com/Flundrahn/Manim-Fourier-Project
#
# I have added some improvements such as getting the Fourier
# coefficients using the FFT and sampling SVG paths segment by segment
# rather than the default which samples the whole SVG path uniformly.
#
# Original 3Blue1Brown video link: https://youtu.be/r6sGWTCMz2k

#%%
from manim import *
import itertools as it

# config.use_opengl_renderer = True

#%%
class FourierSceneAbstract(Scene):
    def __init__(self):
        super().__init__()
        self.fourier_symbol_config = {
            "stroke_width": 1,
            "fill_opacity": 1,
            "height": 4,
        }
        self.vector_config = {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.4
        }
        self.circle_config = {
            "stroke_width": 1,
            "stroke_opacity": 0.3
        }
        self.n_vectors = 40
        self.cycle_seconds = 5
        self.center_point = ORIGIN
        # self.slow_factor = 0.25
        self.parametric_func_step = 0.001
        self.max_circle_stroke_width = 1
        self.drawn_path_stroke_width = 2
        self.drawn_path_interpolation_config = [0, 1]
        self.path_n_samples = 10000
        self.colors = [
            GREY,
            LIGHT_GREY,
            DARK_GREY,
            '#B8860B' # darkgoldenrod
        ]

    def setup(self):
        super().setup()
        self.vector_clock = ValueTracker()
        # self.slow_factor_tracker = ValueTracker(self.slow_factor)
        self.add(self.vector_clock)

    def start_vector_clock(self):
        '''This updates vector_clock to follow the add_updater
        parameter dt'''
        self.vector_clock.add_updater(
            lambda t, dt: t.increment_value(dt / self.cycle_seconds)
        )

    def stop_vector_clock(self):
        self.vector_clock.remove_updater(self.start_vector_clock)

    def get_freqs(self):
        freqs = list(np.arange(self.n_vectors // 2
                               , -self.n_vectors // 2
                               , -1))
        freqs.sort(key=abs)
        return freqs

    def get_points(self, path):
        '''This samples points of individual path segments that make
        up the SVG which is much more efficient and produces more
        detailed circle drawings with fewer vectors. The tradeoff
        is that the number of path samples will not be exactly
        equal to ``self.path_n_samples``.'''
        subpaths = CurvesAsSubmobjects(path)
        dt = len(subpaths) / self.path_n_samples
        t_range = np.arange(0, 1, dt)
        
        points = []
        for subpath in subpaths:
            subpoints = np.array([subpath.point_from_proportion(t) for t in t_range])
            points.append(subpoints)

        # Flatten the list of points
        points = np.vstack(points)
        
        return points


    def get_fourier_coeffs(self, path):
        points = self.get_points(path)
        points -= self.center_point
        # np.savetxt('./points_ce.txt', points)
        # com = path.get_center_of_mass()
        complex_points = points[:, 0] + 1j * points[:, 1]

        # Use FFT
        n = points.shape[0]
        dt = 1 / n
        coefficients = np.fft.fft(complex_points) * dt
        raw_freqs = np.fft.fftfreq(n, dt)
        inds = np.abs(raw_freqs).argsort(kind='stable')
        coefficients = coefficients[inds]
        coefficients = coefficients[:self.n_vectors]

        # print(coefficients[0])

        # coefficients = [
        #     np.sum(np.array([
        #         c_point * np.exp(-TAU * 1j * freq * t) * dt
        #         for t, c_point in zip(t_range, complex_points)
        #         ]))
        #     for freq in self.freqs
        # ]
        return coefficients

    def get_color_iterator(self):
        return it.cycle(self.colors)

    def get_fourier_vectors(self, path):
        coefficients = self.get_fourier_coeffs(path)
        freqs = self.get_freqs()

        vectors = VGroup()
        v_is_first_vector = True
        for coef, freq in zip(coefficients, freqs):
            v = Vector([np.real(coef), np.imag(coef)], **self.vector_config)
            if v_is_first_vector:
                center_func = VectorizedPoint(self.center_point).get_location # Function to center position at tip of last vector
                v_is_first_vector = False
            else:
                center_func = last_v.get_end
            v.center_func = center_func
            last_v = v
            v.freq = freq
            v.coef = coef
            v.phase = np.angle(coef)
            v.shift(v.center_func() - v.get_start())
            v.set_angle(v.phase)
            vectors.add(v)
        return vectors

    def update_vectors(self, vectors):
            for v in vectors:
                time = self.vector_clock.get_value()
                v.shift(v.center_func() - v.get_start())
                v.set_angle(v.phase + time * v.freq * TAU)  # NOTE Rotate() did not work here for unknown reason, probably related to how manin handles updaters

    def get_circles(self, vectors):
        circles = VGroup()
        color_it = self.get_color_iterator()
        for v in vectors:
            c = Circle(radius = v.get_length()
                       , color=next(color_it)
                       , **self.circle_config)
            c.center_func = v.get_start
            c.move_to(c.center_func())
            circles.add(c)
        return circles

    def update_circles(self, circles):
        for c in circles:
            c.move_to(c.center_func())

    def get_drawn_path(self, vectors):

        def fourier_series_func(t):
            fss = np.sum(np.array([
                v.coef * np.exp(TAU * 1j * v.freq * t)
                for v in vectors
            ]))
            real_fss = np.array([np.real(fss), np.imag(fss), 0])
            return real_fss

        t_range = np.array([0, 1, self.parametric_func_step])
        vector_sum_path = ParametricFunction(fourier_series_func, t_range = t_range)
        broken_path = CurvesAsSubmobjects(vector_sum_path)
        broken_path.stroke_width = 0
        broken_path.start_width = self.drawn_path_interpolation_config[0]
        broken_path.end_width = self.drawn_path_interpolation_config[1]
        return broken_path

    def update_path(self, broken_path):
        alpha = self.vector_clock.get_value()
        n_curves = len(broken_path)
        alpha_range = np.linspace(0, 1, n_curves)
        for a, subpath in zip(alpha_range, broken_path):
            b = (alpha - a)
            if b < 0:
                width = 0
            else:
                width = self.drawn_path_stroke_width * interpolate(broken_path.start_width, broken_path.end_width, (1 - (b % 1)))
            subpath.set_stroke(width=width)


class FourierOfSVG(FourierSceneAbstract):
    def __init__(self):
        super().__init__()
        self.file_name = 'A'
        self.n_vectors = 250
        self.parametric_func_step = 2.5e-4
        self.cycle_seconds = 60.
        self.start_drawn = True
        self.fourier_symbol_config = {
            "stroke_width": 0
            , "fill_opacity": 0
            , 'height': 6
            }
        self.drawn_path_config = {
            'color': YELLOW
            , 'stroke_width': 1
            }
        self.circle_config = {
            "stroke_width": 1,
            "stroke_opacity": 1
            }

    def get_symbol(self):
        symbol = SVGMobject(self.file_name)
        return symbol

    def get_path(self):
        symbol = self.get_symbol()
        path = symbol.family_members_with_points()[0]
        path.set(**self.fourier_symbol_config)
        return path

    def get_points(self, path):
        '''This samples points of individual path segments that make
           up the SVG which is much more efficient and produces more
           detailed circle drawings with fewer vectors. The tradeoff
           is that the number of path samples will not be exactly
           equal to ``self.path_n_samples``.'''
        subpaths = CurvesAsSubmobjects(path)
        dt = len(subpaths) / self.path_n_samples
        t_range = np.arange(0, 1, dt)
        points = []
        for subpath in subpaths:
            subpoints = np.array([subpath.point_from_proportion(t)
                                  for t in t_range])
            if points == []:
                points = subpoints
            else:
                points = np.append(points, subpoints, axis=0)

        return points

    def add_objects(self):
        path = self.get_path()
        vectors = self.get_fourier_vectors(path)
        circles = self.get_circles(vectors)
        drawn_path = self.get_drawn_path(vectors)
        drawn_path.set(**self.drawn_path_config)
        drawn_path.add_updater(self.update_path)
        if self.start_drawn:
            self.vector_clock.increment_value(1)

        # self.add(path) # Uncomment to show original SVG path
        self.add(vectors)
        self.add(circles)
        self.add(drawn_path)

        vectors.add_updater(self.update_vectors)
        circles.add_updater(self.update_circles)
        self.start_vector_clock()

    def run_one_cycle(self):
        time = self.cycle_seconds
        self.wait(time)

    def construct(self):
        self.add_objects()
        self.run_one_cycle()


class FourierOfFourier(FourierOfSVG):
    def __init__(self):
        super().__init__()
        self.file_name = 'music_symbols.svg'
        self.n_vectors = 360


class FourierOfOhio(FourierOfSVG):
    def __init__(self):
        super().__init__()
        self.file_name = 'Ohio'

class FourierOfGreatLakes(FourierOfSVG):
    def __init__(self):
        super().__init__()
        self.file_name = 'Great_Lakes'
        self.n_vectors = 300
