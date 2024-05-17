from manim import *
import itertools as it
from functools import reduce
import operator as op
class FourierCirclesScene(ZoomedScene):
    def __init__(self, n_vectors=10, big_radius=2, colors=None, vector_config=None, 
                 circle_config=None, base_frequency=1, slow_factor=0.5, center_point=ORIGIN, 
                 parametric_function_step_size=0.001, drawn_path_color=YELLOW, 
                 drawn_path_stroke_width=2, interpolate_config=None, include_zoom_camera=False, 
                 scale_zoom_camera_to_full_screen=False, scale_zoom_camera_to_full_screen_at=4, 
                 zoom_factor=0.3, zoomed_display_height=3, zoomed_display_width=4, 
                 image_frame_stroke_width=1, zoomed_camera_config=None, zoom_position=None, 
                 zoom_camera_to_full_screen_config=None, wait_before_start=None, **kwargs):
        
        if colors is None:
            colors = [BLUE_D, BLUE_C, BLUE_E, GREY_BROWN]
        if vector_config is None:
            vector_config = {
                "buff": 0,
                "max_tip_length_to_length_ratio": 0.25,
                "tip_length": 0.15,
                "max_stroke_width_to_length_ratio": 10,
                "stroke_width": 1.7,
            }
        if circle_config is None:
            circle_config = {"stroke_width": 1}
        if interpolate_config is None:
            interpolate_config = [0, 1]
        if zoomed_camera_config is None:
            zoomed_camera_config = {
                "default_frame_stroke_width": 3,
                "cairo_line_width_multiple": 0.05,
            }
        if zoom_position is None:
            zoom_position = lambda mob: mob.move_to(ORIGIN)
        if zoom_camera_to_full_screen_config is None:
            zoom_camera_to_full_screen_config = {
                "run_time": 3,
                "func": there_and_back_with_pause,
                "velocity_factor": 1,
            }

        self.n_vectors = n_vectors
        self.big_radius = big_radius
        self.colors = colors
        self.vector_config = vector_config
        self.circle_config = circle_config
        self.base_frequency = base_frequency
        self.slow_factor = slow_factor
        self.center_point = center_point
        self.parametric_function_step_size = parametric_function_step_size
        self.drawn_path_color = drawn_path_color
        self.drawn_path_stroke_width = drawn_path_stroke_width
        self.interpolate_config = interpolate_config
        self.include_zoom_camera = include_zoom_camera
        self.scale_zoom_camera_to_full_screen = scale_zoom_camera_to_full_screen
        self.scale_zoom_camera_to_full_screen_at = scale_zoom_camera_to_full_screen_at
        self.zoom_factor = zoom_factor
        self.zoomed_display_height = zoomed_display_height
        self.zoomed_display_width = zoomed_display_width
        self.image_frame_stroke_width = image_frame_stroke_width
        self.zoomed_camera_config = zoomed_camera_config
        self.zoom_position = zoom_position
        self.zoom_camera_to_full_screen_config = zoom_camera_to_full_screen_config
        self.wait_before_start = wait_before_start

        super().__init__(**kwargs)

class CustomAnimationExample(FourierCirclesScene):
    def __init__(self, **kwargs):
        kwargs["n_vectors"] = 200
        kwargs["slow_factor"] = 0.2
        super().__init__(**kwargs)
        self.fourier_symbol_config = {
            "stroke_width": 0,
            "fill_opacity": 0,
            "height": 4,
            "fill_color": WHITE
        }
        self.circle_config.update({
            "stroke_width": 1,
            "stroke_opacity": 0.3,
        })

    def construct(self):
        t_symbol = Text("T", **self.fourier_symbol_config)
        c_clef_symbol = SVGMobject("c_clef", **self.fourier_symbol_config)
        c_clef_symbol.match_height(t_symbol)
        # set gradient
        for mob in [t_symbol, c_clef_symbol]:
            mob.set_sheen(0, UP)
            mob.set_color(color=[BLACK, GRAY, WHITE])
        group = VGroup(t_symbol, c_clef_symbol).arrange(RIGHT, buff=0.1)
        # set paths
        path1 = t_symbol.family_members_with_points()[0]
        path2 = c_clef_symbol.family_members_with_points()[0]
        # path 1 config
        coefs1 = self.get_coefficients_of_path(path1)
        vectors1 = self.get_rotating_vectors(coefficients=coefs1)
        circles1 = self.get_circles(vectors1)
        drawn_path1 = self.get_drawn_path(vectors1)
        # path 2 config
        coefs2 = self.get_coefficients_of_path(path2)
        vectors2 = self.get_rotating_vectors(coefficients=coefs2)
        circles2 = self.get_circles(vectors2)
        drawn_path2 = self.get_drawn_path(vectors2)
        # text definition
        text = Text("Thanks for watch!")
        text.scale(1.5)
        text.next_to(group, DOWN)
        # all elements together
        all_mobs = VGroup(group, text)
        # set mobs to remove
        vectors1_to_fade = vectors1.copy()
        circles1_to_fade = circles1.copy()
        vectors1_to_fade.clear_updaters()
        circles1_to_fade.clear_updaters()
        vectors2_to_fade = vectors2.copy()
        circles2_to_fade = circles2.copy()
        vectors2_to_fade.clear_updaters()
        circles2_to_fade.clear_updaters()

        self.play(
            *[
                GrowArrow(arrow)
                for vg in [vectors1_to_fade, vectors2_to_fade]
                for arrow in vg
            ],
            *[
                Create(circle)
                for cg in [circles1_to_fade, circles2_to_fade]
                for circle in cg
            ],
            run_time=2.5,
        )
        self.remove(
            *vectors1_to_fade,
            *circles1_to_fade,
            *vectors2_to_fade,
            *circles2_to_fade,
        )
        self.add(
            vectors1,
            circles1,
            drawn_path1.set_color(RED),
            vectors2,
            circles2,
            drawn_path2.set_color(BLUE),
        )
        self.add_vector_clock()

        # wait one cycle
        self.wait(1 / self.slow_factor)
        self.bring_to_back(t_symbol, c_clef_symbol)
        self.play(
            t_symbol.set_fill, None, 1,
            c_clef_symbol.set_fill, None, 1,
            run_time=3
        )
        self.wait()
        # move camera
        self.play(
            self.camera_frame.set_height, all_mobs.get_height() * 1.2,
            self.camera_frame.move_to, all_mobs.get_center()
        )
        self.wait(0.5)
        self.play(
            Write(text)
        )
        self.wait(10)
