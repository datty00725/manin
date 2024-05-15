from manim import *

class FourierCirclesScene(ZoomedScene):
    CONFIG = {
        "n_vectors": 10,
        "big_radius": 2,
        "colors": [
            RED,TEAL
        ],
        "vector_config": {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.7,
        },
        "circle_config": {
            "stroke_width": 1,
        },
        "base_frequency": 1,
        "slow_factor": 0.5,
        "center_point": ORIGIN,
        "parametric_function_step_size": 0.001,
        "drawn_path_color": YELLOW,
        "drawn_path_stroke_width": 2,
        "interpolate_config": [0, 1],
        # Zoom config
        "include_zoom_camera": False,
        "scale_zoom_camera_to_full_screen": False,
        "scale_zoom_camera_to_full_screen_at": 4,
        "zoom_factor": 0.3,
        "zoomed_display_height": 3,
        "zoomed_display_width": 4,
        "image_frame_stroke_width": 1,
        "zoomed_camera_config": {
            "default_frame_stroke_width": 3,
            "cairo_line_width_multiple": 0.05,
        },
        "zoom_position": lambda mob: mob.move_to(ORIGIN),
        "zoom_camera_to_full_screen_config": {
            "run_time": 3,
            "func": there_and_back_with_pause,
            "velocity_factor": 1
        },
        "wait_before_start": None
    }

class AbstractFourierOfTexSymbol(FourierCirclesScene):
    CONFIG = {
        "n_vectors": 50,
        "center_point": ORIGIN,
        "slow_factor": 0.05,
        "n_cycles": None,
        "run_time": 10,
        "tex": r"\rm M",
        "start_drawn": True,
        "add_path": False,
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

class FourierOfTexSymbol(AbstractFourierOfTexSymbol):
    CONFIG = {
        # if start_draw = True the path start to draw
        "start_drawn": True,
        # Tex config
        "tex_class": Tex,
        "tex": r"\Sigma",
        "tex_config": {
            "fill_opacity": 0,
            "stroke_width": 1,
            "stroke_color": WHITE
        },
        # Draw config
        "drawn_path_color": YELLOW,
        "interpolate_config": [0, 1],
        "n_vectors": 50,
        "big_radius": 2,
        "drawn_path_stroke_width": 2,
        "center_point": ORIGIN,
        # Duration config
        "slow_factor": 0.1,
        "n_cycles": None,
        "run_time": 10,
        # colors of circles
        "colors": [
            BLUE_D,
            BLUE_C,
            BLUE_E,
            GREY_BROWN,
        ],
        # circles config
        "circle_config": {
            "stroke_width": 1,
        },
        # vector config
        "vector_config": {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.7,
        },
        "base_frequency": 1,
        # definition of subpaths
        "parametric_function_step_size": 0.001,
    }

class AbstractFourierFromSVG(AbstractFourierOfTexSymbol):
    CONFIG = {
        "n_vectors": 101,
        "run_time": 10,
        "start_drawn": True,
        "file_name": None,
        "svg_config": {
            "fill_opacity": 0,
            "stroke_color": WHITE,
            "stroke_width": 1,
            "height": 7
        }
    }

class FourierFromSVG(AbstractFourierFromSVG):
    CONFIG = {
        # if start_draw = True the path start to draw
        "start_drawn": True,
        # SVG file name
        "file_name": None,
        "svg_config": {
            "fill_opacity": 0,
            "stroke_color": WHITE,
            "stroke_width": 1,
            "height": 7
        },
        # Draw config
        "drawn_path_color": YELLOW,
        "interpolate_config": [0, 1],
        "n_vectors": 50,
        "big_radius": 2,
        "drawn_path_stroke_width": 2,
        "center_point": ORIGIN,
        # Duration config
        "slow_factor": 0.1,
        "n_cycles": None,
        "run_time": 10,
        # colors of circles
        "colors": [
            BLUE_D,
            BLUE_C,
            BLUE_E,
            GREY_BROWN,
        ],
        # circles config
        "circle_config": {
            "stroke_width": 1,
        },
        # vector config
        "vector_config": {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.7,
        },
        "base_frequency": 1,
        # definition of subpaths
        "parametric_function_step_size": 0.001,
    }

class FourierOfPaths(AbstractFourierOfTexSymbol):
    CONFIG = {
        "n_vectors": 100,
        "name_color": WHITE,
        "tex_class": Tex,
        "tex": None,
        "file_name": None,
        "tex_config": {
            "stroke_color": WHITE,
            "fill_opacity": 0,
            "stroke_width": 3,
        },
        "svg_config": {},
        "time_per_symbol": 5,
        "slow_factor": 1 / 5,
        "parametric_function_step_size": 0.01,
        "include_zoom_camera": False,
        "scale_zoom_camera_to_full_screen": False,
    }
# How activate it
class ZoomedActivate(FourierFromSVG):
    CONFIG = {
        "slow_factor": 0.05,
        "n_vectors": 50,
        "n_cycles": 1,
        "file_name": "c_clef",
        "include_zoom_camera": True,
        "zoom_position": lambda zc: zc.to_corner(DR)
    }

class ZoomedConfig(FourierFromSVG):
    CONFIG = {
        "slow_factor": 0.05,
        "n_vectors": 150,
        "n_cycles": 1,
        "file_name": "c_clef",
        "path_custom_position": lambda path: path.shift(LEFT*2),
        "center_point": LEFT*2,
        "circle_config": {
            "stroke_width": 0.5,
            "stroke_opacity": 0.2,
        },
        # Zoom config
        "include_zoom_camera": True,
        "zoom_position": lambda zc: zc.to_edge(RIGHT).set_y(0),
        "zoom_factor": 0.5,
        "zoomed_display_height": 5,
        "zoomed_display_width": 5,
        "zoomed_camera_config": {
            "default_frame_stroke_width": 3,
            "cairo_line_width_multiple": 0.05,
            # What is cairo_line_width_multiple?
            # See here: https://stackoverflow.com/questions/60765530/manim-zoom-not-preserving-line-thickness
        },
    }

class Tsymbol20vectors(FourierOfTexSymbol):
    CONFIG = {
        "n_vectors": 2,
        "run_time": 10, # 10 seconds
        "tex_class": Tex,
        "tex": "T",
    }