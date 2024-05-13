from manim import *
# HELPERS FOR COMPLEX SCENES, you can always create your own :)
def get_horizontal_line_to_graph(axes, function, x, width, color):
    result = VGroup()
    line = DashedLine(
        start=axes.c2p(0, function.underlying_function(x)),
        end=axes.c2p(x, function.underlying_function(x)),
        stroke_width=width,
        stroke_color=color,
    )
    dot = Dot().set_color(color).move_to(axes.c2p(x, function.underlying_function(x)))
    result.add(line, dot)
    return result


def get_arc_lines_on_function(
    graph, plane, dx=1, line_color=WHITE, line_width=1, x_min=None, x_max=None
):

    dots = VGroup()
    lines = VGroup()
    result = VGroup(dots, lines)

    x_range = np.arange(x_min, x_max, dx)
    colors = color_gradient([BLUE_B, GREEN_B], len(x_range))

    for x, color in zip(x_range, colors):
        p1 = Dot().scale(0.7).move_to(plane.input_to_graph_point(x, graph))
        p2 = Dot().scale(0.7).move_to(plane.input_to_graph_point(x + dx, graph))
        dots.add(p1, p2)
        dots.set_fill(colors, opacity=0.8)

        line = Line(
            p1.get_center(),
            p2.get_center(),
            stroke_color=line_color,
            stroke_width=line_width,
        )
        lines.add(line)

    return result


from manim import *

class Derivatives(Scene):
    def construct(self):
        k = ValueTracker(-3)  # Tracking the end values of stuff to show

        # Adding Mobjects for the first plane
        plane1 = NumberPlane(x_range=[-3, 4, 1], y_range=[-8, 9, 2])\
            .add_coordinates()\
            .shift(LEFT * 3.5)

        func1 = always_redraw(
            lambda: plane1.get_graph(lambda x: (1 / 3) * x ** 3)
        )