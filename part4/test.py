"""
Commit above which this project is made:
https://github.com/ManimCommunity/manim/tree/3156b9f20aa33f559e6f288d38cfd4a4db456389
"""

import collections

from functions import *
from manim import *

# from manim_fonts import *
from mobjects import Blob, EquilateralTriangle

config.background_color = "#111111"


class VivianiTheorem(Scene):
    def construct(self):
        font_name = "Merienda"  # 'Merienda' が目的のフォント名だと仮定

        title = Text("Viviani Theorem", font=font_name, color=GOLD_E).scale(2)
        underline = Underline(title, color=GOLD_E)

        theorem = Paragraph(
            "For an equilateral triangle, the sum of the distances from any",
            "interior point to the sides, is equal to its altitude.",
            line_spacing=0.8,
            font=font_name,
        ).set_opacity(0.35)

        # タイトルと下線をシーンに追加
        self.add(title, underline)

        # 定理の段落を表示
        theorem.next_to(title, DOWN, buff=0.5)
        self.add(theorem)

        self.wait(0.25)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.play(title.animate.scale(0.5).to_corner(UL, buff=0.25))
        self.wait(0.25)

        theorem.set(width=config.frame_width - 1)
        theorem.next_to(title, DOWN, buff=0.5, aligned_edge=LEFT)
        triangle = EquilateralTriangle(4.5, color=GOLD_E, fill_opacity=0.1)
        triangle.next_to(theorem, DOWN, buff=0.5)

        self.play(FadeIn(theorem))
        self.wait()
        self.play(
            theorem[0][:25].animate(lag_ratio=1).set_opacity(1),
            GrowFromCenter(triangle),
            run_time=3,
        )
        self.wait(0.5)

        dot = Dot(point=triangle.circumcenter)
        perp_line_colors = [RED_C, PINK, BLUE_E]  # ccw starting from right edge
        perp_lines = []
        right_angles = []
        for i, color in zip([2, 0, 1], perp_line_colors):
            line = triangle.get_perpendicular_line_to_edge(
                i, dot.get_center(), color=color
            )
            line.z_index = -1
            right_angle = get_right_angle_to_edge(line, 0.125).match_style(line)
            perp_lines.append(line)
            right_angles.append(right_angle)

        self.play(
            FadeIn(dot),
            AnimationGroup(
                theorem[0][25:].animate(lag_ratio=1).set_opacity(1),
                theorem[1][:13].animate(lag_ratio=1).set_opacity(1),
                lag_ratio=1,
            ),
            run_time=3,
        )
        self.play(*map(Create, perp_lines), run_time=0.75)
        self.play(*map(Create, right_angles), run_time=0.75)

        length_indicators = get_length_indicators(
            perp_lines,
            0.5,
            triangle.get_vertices()[1] + 2 * LEFT,
            fill_opacity=0.25,
            stroke_width=2,
        ).save_state()
        length_indicators.stretch(0.0001, 1, about_edge=DOWN)

        self.play(Restore(length_indicators, run_time=2))
        self.wait(0.5)

        altitude_ref_lines = []
        for i, corner in zip([0, 1], [UR, DR]):
            start = triangle.get_vertices()[i]
            end = length_indicators.get_corner(corner)
            altitude_ref_lines.append(DashedLine(start, end))

        self.play(
            *map(Create, altitude_ref_lines),
            theorem[1][13:].animate(lag_ratio=1).set_opacity(1),
            run_time=3,
        )  # there's something weird about indexing Paragraph or I don't understand it well
        self.wait()

        updater_anims = [
            *map(
                lambda l: UpdateFromFunc(
                    l, lambda l: perp_line_updater(l, triangle, dot)
                ),
                perp_lines,
            ),
            UpdateFromFunc(
                length_indicators, lambda li: length_indicators_updater(li, perp_lines)
            ),
            UpdateFromFunc(
                right_angles[0],
                lambda r: right_angle_updater(right_angles[0], perp_lines[0]),
            ),
            UpdateFromFunc(
                right_angles[1],
                lambda r: right_angle_updater(right_angles[1], perp_lines[1]),
            ),
            UpdateFromFunc(
                right_angles[2],
                lambda r: right_angle_updater(right_angles[2], perp_lines[2]),
            ),
        ]

        def move_dot_along_random_path(blob_center):
            for _ in range(2):
                blob = Blob(triangle.inradius - 0.125, max_scale=0.95, n_samples=15)
                blob.shift(blob_center)
                self.play(
                    dot.animate.move_to(blob.points[0]),
                    *updater_anims,
                    rate_func=linear,
                    run_time=2,
                )
                self.play(
                    MoveAlongPath(dot, blob),
                    *updater_anims,
                    rate_func=linear,
                    run_time=8,
                )

        move_dot_along_random_path(triangle.circumcenter)
        self.play(
            dot.animate.move_to(triangle.get_center()),
            *updater_anims,
            rate_func=linear,
            run_time=2,
        )
        self.wait()

        triangle_copy = triangle.copy()
        edge_triangles = VGroup()
        for i, color in zip([2, 0, 1], perp_line_colors):
            edge_tri = get_triangle_to_edge(
                i, triangle, dot.get_center(), color=color, fill_opacity=0.25
            )
            edge_triangles += edge_tri

        self.add(triangle_copy)
        fade_out_objects = Group(*length_indicators, *altitude_ref_lines)
        self.play(FadeOut(fade_out_objects), run_time=0.5)
        self.play(
            triangle_copy.animate.shift(3 * LEFT),
            Group(triangle, dot, *perp_lines, *right_angles).animate.shift(3 * RIGHT),
        )

        edge_triangles.shift(3 * RIGHT)
        edge_triangles_group = VGroup(*edge_triangles, *perp_lines, *right_angles, dot)

        self.wait(0.5)
        self.play(
            LaggedStart(
                GrowFromPoint(
                    edge_triangles, dot.get_center(), lag_ratio=1, run_time=2
                ),
                triangle.animate.set_opacity(0),
                lag_ratio=0.5,
            )
        )
        self.wait(0.5)

        theorem_group = VGroup(title, theorem)
        theorem_group.save_state()
        triangles_group = VGroup(triangle_copy, edge_triangles_group)
        triangles_group.save_state()

        self.play(
            LaggedStart(
                FadeOut(theorem_group, shift=UP),
                triangles_group.animate.to_edge(UP),
                lag_ratio=1,
            ),
            run_time=3,
        )
        triangle.to_edge(UP)
        self.wait(0.5)

        base_braces = [
            BraceText(mob, "b", label_constructor=Text)
            for mob in [triangle_copy, edge_triangles_group]
        ]
        for brace in base_braces:
            brace.label.scale(0.6)  # ラベルのスケールをここで調整

        h_line = triangle_copy.get_perpendicular_line_to_edge(
            1, triangle_copy.get_vertices()[0], color=triangle_copy.get_color()
        )
        h_ra = get_right_angle_to_edge(h_line, 0.125).match_style(h_line)
        h_text = get_altitude_text(
            h_line, "h", 0.03, 0.65, fill_color=triangle_copy.get_color()
        )
        h0_text, h1_text, h2_text = [
            get_altitude_text(pl, f"h_{pl.edge_index}", 0.03, 0.65, fill_color=col)
            for pl, col in zip(perp_lines, perp_line_colors)
        ]
        h_texts = VGroup(h_text, h0_text, h1_text, h2_text)

        self.play(LaggedStartMap(Create, Group(h_line, h_ra), lag_ratio=1))
        self.wait(0.5)
        self.play(LaggedStartMap(FadeIn, h_texts, lag_ratio=1))
        self.play(
            LaggedStartMap(
                GrowFromCenter, Group(*base_braces), lag_ratio=0, run_time=0.75
            )
        )
        self.wait(0.5)

        shuffled_edge_triangles = collections.deque([*edge_triangles])
        shuffled_edge_triangles.rotate(2)
        shuffled_edge_triangles = list(shuffled_edge_triangles)

        area_left = get_area_text("h", triangle_copy.get_color())
        area_left.next_to(base_braces[0], DOWN)
        area_right = VGroup()

        for index, tri in zip([0, 1, 2], shuffled_edge_triangles):
            area_right += get_area_text(f"h_{index}", tri.get_color())
            area_right += MathTex("+")
        area_right = area_right[:-1]
        area_right.arrange(buff=0.1).next_to(base_braces[1], DOWN)

        equals = MathTex("=")
        area_eqn = VGroup(area_left, equals, area_right).arrange(buff=2)
        area_eqn.next_to(base_braces[0].label, DOWN, 0.5, LEFT)

        self.play(*map(FadeIn, area_eqn[:2]))
        self.wait(0.5)

        edge_triangles_group += h_texts[1:]
        edge_triangles_group.save_state()
        self.play(
            Rotating(
                edge_triangles_group,
                radians=2 * PI / 3,
                about_point=triangle.circumcenter,
                run_time=0.75,
            )
        )
        self.wait(0.5)

        for i in range(3):
            self.play(FadeIn(area_right[2 * i]))
            self.wait(0.5)
            if i != 2:
                self.play(
                    Rotating(
                        edge_triangles_group,
                        radians=-2 * PI / 3,
                        about_point=triangle.circumcenter,
                    ),
                    FadeIn(area_right[2 * i + 1]),
                    run_time=0.75,
                )
            self.wait(0.5)
        self.play(Restore(edge_triangles_group, run_time=0.75))
        self.wait(0.5)
        self.play(area_eqn.animate.arrange(buff=0.25, center=False).move_to(2.5 * DOWN))
        self.wait(0.5)

        half_b = [area_left, *area_right[::2]]
        surr_rects = [
            SurroundingRectangle(hb[0], buff=0.01, stroke_width=1, fill_opacity=0.1)
            for hb in half_b
        ]

        group_to_fade_in = Group(*surr_rects)
        self.play(
            group_to_fade_in.animate.shift(UP), FadeIn(group_to_fade_in), run_time=0.5
        )

        self.wait(0.5)

        for rect, hb in zip(surr_rects, half_b):
            rect.add(hb[0])
            hb.remove(hb[0])

        self.play(
            AnimationGroup(
                FadeOut(Group(*surr_rects), shift=DOWN),
                FadeOut(Group(*base_braces), shift=0.2 * DOWN),
                lag_ratio=0.1,
                run_time=2,
            )
        )
        self.wait(0.25)

        area_eqn_copy = area_eqn.copy()
        area_eqn_copy[2].arrange(buff=0.2, center=False)
        area_eqn_copy.arrange(buff=0.25, center=False)
        area_eqn_copy.move_to(2.5 * DOWN)

        self.play(TransformMatchingShapes(area_eqn, area_eqn_copy, run_time=0.75))
        area_eqn.__dict__ = (
            area_eqn_copy.__dict__
        )  # had to do bcz of a bug in Transform
        self.wait()

        surr_rect_area_eqn = SurroundingRectangle(
            area_eqn, triangle.get_color(), stroke_width=1, fill_opacity=0.1
        )
        self.play(GrowFromEdge(surr_rect_area_eqn, LEFT))
        self.wait(0.5)

        self.play(
            AnimationGroup(
                FadeIn(theorem_group),
                theorem_group.animate.shift(0.25 * UP),
                lag_ratio=0.8,
                run_time=2,
            )
        )
        self.wait(2)
