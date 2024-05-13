from manim import *
import numpy as np
from math import *


def projection_point_sur_droite(point, droite):
    produit_scalaire = np.dot(point - droite[0], droite[1] - droite[0])
    norme = np.linalg.norm(droite[1] - droite[0])
    return droite[0] + produit_scalaire / norme**2 * (droite[1] - droite[0])


class Viviani(Scene):
    def construct(self):

        gros_titre = Text("ヴィヴィアーニの定理", weight=BOLD, color=YELLOW).shift(UP)
        gros_titre.scale(1.6)
        # annee = Text("1649", weight=BOLD, color=RED)
        # annee.next_to(gros_titre, DOWN, buff=1).scale(1.6)

        self.add(gros_titre)
        self.wait()

        self.play(
            gros_titre.animate.shift(3.5 * LEFT + 2 * UP).scale(0.5),
            # FadeOut(annee)
        )

        hyp1 = Text(
            "(1) 正三角形",
        )
        hyp2 = Text(
            "(2) 三角形内の任意の点",
        )

        group_hyp = VGroup(hyp1, hyp2).scale(0.5).set_opacity(0.2)
        group_hyp.arrange(DOWN, center=False, aligned_edge=LEFT)
        group_hyp.move_to(3 * LEFT + UP)
        self.add(group_hyp)

        triangle = Triangle(fill_color=GOLD, fill_opacity=0.2).scale(2.5)
        triangle.set_color(GOLD).move_to(3 * RIGHT)
        A, B, C = triangle.get_vertices()

        self.play(
            hyp1.animate(lag_ratio=1).set_opacity(1),
            GrowFromCenter(VGroup(triangle)),
            run_time=2,
        )
        self.wait(0.5)

        G = triangle.get_center_of_mass() + UP + 0.2 * RIGHT
        G_point = Dot(point=G)

        self.play(
            hyp1.animate.set_opacity(0.2),
            hyp2.animate(lag_ratio=1).set_opacity(1),
            Create(G_point),
            run_time=2,
        )
        self.add_foreground_mobject(G_point)
        self.wait(0.5)

        # self.play(
        #     hyp2.animate.set_opacity(0.2)
        # )

        # bloc principal (triangle + rectangles animés)
        A, B, C = triangle.get_vertices()
        perp2 = always_redraw(
            lambda: Line(
                G_point.get_center(),
                Dot(
                    point=projection_point_sur_droite(G_point.get_center(), [A, B])
                ).get_center(),
                color=BLUE,
            )
        )
        perp1 = always_redraw(
            lambda: Line(
                G_point.get_center(),
                Dot(
                    point=projection_point_sur_droite(G_point.get_center(), [B, C])
                ).get_center(),
                color=PINK,
            )
        )
        perp3 = always_redraw(
            lambda: Line(
                G_point.get_center(),
                Dot(
                    point=projection_point_sur_droite(G_point.get_center(), [A, C])
                ).get_center(),
                color=GREEN,
            )
        )
        perps = [perp1, perp2, perp3]

        right_angle1 = always_redraw(
            lambda: RightAngle(
                Line(B, C),
                Line(
                    G_point.get_center(),
                    Dot(
                        point=projection_point_sur_droite(G_point.get_center(), [B, C])
                    ).get_center(),
                ),
                quadrant=(1, -1),
                length=0.1,
                color=PINK,
            )
        )
        right_angle2 = always_redraw(
            lambda: RightAngle(
                Line(A, B),
                Line(
                    G_point.get_center(),
                    Dot(
                        point=projection_point_sur_droite(G_point.get_center(), [A, B])
                    ).get_center(),
                ),
                quadrant=(1, -1),
                length=0.1,
                color=BLUE,
            )
        )
        right_angle3 = always_redraw(
            lambda: RightAngle(
                Line(A, C),
                Line(
                    G_point.get_center(),
                    Dot(
                        point=projection_point_sur_droite(G_point.get_center(), [A, C])
                    ).get_center(),
                ),
                quadrant=(1, -1),
                length=0.1,
                color=GREEN,
            )
        )
        right_angles = [right_angle1, right_angle2, right_angle3]

        # Construction des jauges rectangulaires à droite
        rectangle1 = always_redraw(
            lambda: Rectangle(
                width=0.5,
                height=Line(
                    G_point.get_center(),
                    Dot(
                        point=projection_point_sur_droite(G_point.get_center(), [B, C])
                    ).get_center(),
                ).get_length(),
                color=PINK,
                fill_color=PINK,
                fill_opacity=0.2,
            ).next_to(C + 0.5 * RIGHT, aligned_edge=DL)
        )
        rectangle2 = always_redraw(
            lambda: Rectangle(
                width=0.5,
                height=Line(
                    G_point.get_center(),
                    Dot(
                        point=projection_point_sur_droite(G_point.get_center(), [A, B])
                    ).get_center(),
                ).get_length(),
                color=BLUE,
                fill_color=BLUE,
                fill_opacity=0.2,
            ).next_to(rectangle1.get_top() + LEFT * 0.5, aligned_edge=DOWN)
        )
        rectangle3 = always_redraw(
            lambda: Rectangle(
                width=0.5,
                height=Line(
                    G_point.get_center(),
                    Dot(
                        point=projection_point_sur_droite(G_point.get_center(), [A, C])
                    ).get_center(),
                ).get_length(),
                color=GREEN,
                fill_color=GREEN,
                fill_opacity=0.2,
            ).next_to(rectangle2.get_top() + LEFT * 0.5, aligned_edge=DOWN)
        )

        # Construction des jauges rectangulaires à gauche
        rectangle1_copie = always_redraw(
            lambda: Rectangle(
                width=0.5,
                height=Line(
                    G_point.get_center(),
                    Dot(
                        point=projection_point_sur_droite(G_point.get_center(), [B, C])
                    ).get_center(),
                ).get_length(),
                color=PINK,
                fill_color=PINK,
                fill_opacity=0.2,
            ).next_to(B + 5.5 * LEFT + 0.5 * UP, aligned_edge=DL)
        )
        rectangle2_copie = always_redraw(
            lambda: Rectangle(
                width=0.5,
                height=Line(
                    G_point.get_center(),
                    Dot(
                        point=projection_point_sur_droite(G_point.get_center(), [A, B])
                    ).get_center(),
                ).get_length(),
                color=BLUE,
                fill_color=BLUE,
                fill_opacity=0.2,
            ).next_to(B + 4.1 * LEFT + 0.5 * UP, aligned_edge=DL)
        )
        rectangle3_copie = always_redraw(
            lambda: Rectangle(
                width=0.5,
                height=Line(
                    G_point.get_center(),
                    Dot(
                        point=projection_point_sur_droite(G_point.get_center(), [A, C])
                    ).get_center(),
                ).get_length(),
                color=GREEN,
                fill_color=GREEN,
                fill_opacity=0.2,
            ).next_to(B + 2.7 * LEFT + 0.5 * UP, aligned_edge=DL),
        )
        symbole_add = Text("+")
        symbole_add.scale(1.5)
        symbole_add2 = Text("+")
        symbole_add2.scale(1.5)

        self.play(
            FadeOut(VGroup(hyp1, hyp2)),
            Create(VGroup(perp1, right_angle1)),
        )
        self.play(ReplacementTransform(perp1.copy(), rectangle1_copie))

        self.wait()

        self.play(
            Create(VGroup(perp2, right_angle2)),
        )
        self.play(ReplacementTransform(perp2.copy(), rectangle2_copie))

        self.wait()

        self.play(
            Create(VGroup(perp3, right_angle3)),
        )
        self.play(ReplacementTransform(perp3.copy(), rectangle3_copie))
        #theoreme = Paragraph(
        #    "Alors la somme des distances aux côtés du triangle NE dépend PAS du point choisi !",
        #    "Elle est toujours égale à la hauteur du triangle",
        #    line_spacing=1,
        #)

        #theoreme.move_to(2.9 * DOWN + 0.1 * RIGHT)
        #theoreme.scale(0.55)
        #theoreme.set_opacity(0.2)

        #self.add(theoreme)
        self.wait()
        #self.play(
        #    theoreme[0][0:42].animate(lag_ratio=1).set_opacity(1),
        #    FadeIn(
        #        VGroup(
        #            symbole_add.next_to(B + 4.8 * LEFT + 0.5 * UP, aligned_edge=DL),
        #            symbole_add2.next_to(B + 3.4 * LEFT + 0.5 * UP, aligned_edge=DL),
        #        ),
        #        shift=DOWN,
        #    ),
        #    run_time=2,
        #)
        self.play(
            Circumscribe(
                VGroup(
                    rectangle1_copie,
                    symbole_add,
                    rectangle2_copie,
                    symbole_add2,
                    rectangle3_copie,
                ),
                time_width=3,
            ),
            #Circumscribe(theoreme[0][5:42], time_width=3),
            run_time=1.5,
        )
        #self.play(theoreme[0][42:].animate(lag_ratio=1).set_opacity(1), run_time=1.5)

        rectangles = [rectangle1, rectangle2, rectangle3]
        self.wait(0.5)
        line1 = DashedLine(Dot(A), Dot(rectangle3.get_top() - RIGHT * 0.25))
        line2 = DashedLine(Dot(C), Dot(rectangle1.get_bottom() - RIGHT * 0.25))
        self.play(
            Create(line1),
            Create(line2),
            #theoreme[1].animate(lag_ratio=1).set_opacity(1),
            run_time=2,
        )
        self.play(
            ReplacementTransform(perp1.copy(), rectangle1),
            ReplacementTransform(perp2.copy(), rectangle2),
            ReplacementTransform(perp3.copy(), rectangle3),
        )

        self.play(G_point.animate.shift(DOWN * 0.75), run_time=2)
        self.play(G_point.animate.shift(LEFT), run_time=2)
        self.play(G_point.animate.shift(0.8 * RIGHT + UP * 1.75), run_time=2)
        self.play(
            G_point.animate.move_to(triangle.get_center_of_mass() + RIGHT * 0.7),
            run_time=2,
        )
        self.wait(2)

        self.remove_foreground_mobject(G_point)
        self.play(
            FadeOut(
                *perps,
                *right_angles,
                *rectangles,
                line1,
                line2,
                gros_titre,
                #theoreme,
                rectangle1_copie,
                rectangle2_copie,
                rectangle3_copie,
                symbole_add,
                symbole_add2,
                triangle,
                G_point
            ),
            run_time=1,
        )
        self.wait()

        demonstration = Text("証明").scale(1.4)
        self.play(Create(demonstration))
        self.wait(1)
        self.play(FadeOut(demonstration))

        triangle = Triangle(fill_color=GOLD, fill_opacity=0.2).scale(2.5)
        triangle.set_color(GOLD)
        triangle.move_to(ORIGIN)
        A, B, C = triangle.get_vertices()
        G = triangle.get_center_of_mass() + UP + 0.2 * RIGHT
        G_point = Dot(point=G)
        triangle_2 = triangle.copy()

        perp1 = Line(
            G_point.get_center(),
            Dot(
                point=projection_point_sur_droite(G_point.get_center(), [A, B])
            ).get_center(),
            color=BLUE,
        )
        perp2 = Line(
            G_point.get_center(),
            Dot(
                point=projection_point_sur_droite(G_point.get_center(), [B, C])
            ).get_center(),
            color=PINK,
        )
        perp3 = Line(
            G_point.get_center(),
            Dot(
                point=projection_point_sur_droite(G_point.get_center(), [A, C])
            ).get_center(),
            color=GREEN,
        )
        construction_somme_distance = [perp1, perp2, perp3]

        right_angle1 = RightAngle(
            Line(A, B),
            Line(
                G_point.get_center(),
                Dot(
                    point=projection_point_sur_droite(G_point.get_center(), [A, B])
                ).get_center(),
            ),
            quadrant=(1, -1),
            length=0.1,
            color=BLUE,
        )
        right_angle2 = RightAngle(
            Line(B, C),
            Line(
                G_point.get_center(),
                Dot(
                    point=projection_point_sur_droite(G_point.get_center(), [B, C])
                ).get_center(),
            ),
            quadrant=(1, -1),
            length=0.1,
            color=PINK,
        )
        right_angle3 = RightAngle(
            Line(A, C),
            Line(
                G_point.get_center(),
                Dot(
                    point=projection_point_sur_droite(G_point.get_center(), [A, C])
                ).get_center(),
            ),
            quadrant=(1, -1),
            length=0.1,
            color=GREEN,
        )
        right_angles = [right_angle1, right_angle2, right_angle3]
        tout = VGroup(triangle, *construction_somme_distance, *right_angles, G_point)
        self.add(tout)
        self.wait()
        self.play(
            triangle_2.animate.shift(LEFT * 3 + UP * 1.5),
            tout.animate.shift(RIGHT * 3 + UP * 1.5),
            run_time=2.5,
        )

        self.play(Indicate(triangle_2))

        legende = Text(
            "面積(", ")", "=", " 面積(", ")", "+", " 面積(", ")", "+", " 面積(", ")"
        )
        legende.scale(1)

        legende[0].next_to(triangle_2, 5.5 * DOWN, aligned_edge=DL)
        petit_triangle_gauche = triangle_2.copy().scale(0.1).next_to(legende[0], RIGHT)
        legende[1].next_to(petit_triangle_gauche, RIGHT)
        self.play(
            FadeIn(legende[0], shift=LEFT),
            ReplacementTransform(triangle_2.copy(), petit_triangle_gauche),
            FadeIn(legende[1], shift=RIGHT),
        )

        self.play(Indicate(tout))
        G_point_coord = [G_point.get_x(), G_point.get_y(), 0]
        A, B, C = triangle.get_vertices()
        triangle_a = Polygon(
            B, C, G_point_coord, color=PINK, fill_color=PINK, fill_opacity=0.2
        )
        triangle_b = Polygon(
            A, C, G_point_coord, color=GREEN, fill_color=GREEN, fill_opacity=0.2
        )
        triangle_c = Polygon(
            A, B, G_point_coord, color=BLUE, fill_color=BLUE, fill_opacity=0.2
        )

        self.add_foreground_mobject(G_point)

        self.play(
            VGroup(triangle_c, perp1, right_angle1).animate.shift(0.1 * LEFT),
            VGroup(triangle_b, perp3, right_angle3).animate.shift(0.1 * RIGHT),
            VGroup(triangle_a, perp2, right_angle2).animate.shift(0.1 * DOWN),
            FadeOut(triangle),
            FadeOut(G_point),
            run_time=1.5,
        )

        legende[2].next_to(legende[1], buff=0.2)
        self.play(Write(legende[2]))

        legende[3:4].next_to(legende[2], buff=0.2)
        petit_triangle_a = triangle_a.copy().scale(0.2).next_to(legende[3], RIGHT)
        legende[4].next_to(petit_triangle_a, RIGHT)
        self.play(
            FadeIn(legende[3:4], shift=LEFT),
            ReplacementTransform(triangle_a.copy(), petit_triangle_a),
            FadeIn(legende[4], shift=RIGHT),
            run_time=1.5,
        )

        legende[5:7].next_to(legende[4], buff=0.2)
        petit_triangle_c = triangle_c.copy().scale(0.2).next_to(legende[6], RIGHT)
        legende[7].next_to(petit_triangle_c, RIGHT)
        self.play(
            FadeIn(legende[5:7], shift=LEFT),
            ReplacementTransform(triangle_c.copy(), petit_triangle_c),
            FadeIn(legende[7], shift=RIGHT),
            run_time=1.5,
        )

        legende[8:10].next_to(legende[7], buff=0.2)
        petit_triangle_b = triangle_b.copy().scale(0.2).next_to(legende[9], RIGHT)
        legende[10].next_to(petit_triangle_b, RIGHT)
        self.play(
            FadeIn(legende[8:10], shift=LEFT),
            ReplacementTransform(triangle_b.copy(), petit_triangle_b),
            FadeIn(legende[10], shift=RIGHT),
            run_time=1.5,
        )

        self.wait(1.5)

        aire = MathTex("\dfrac{1}{2}", "b", "h")
        aire.set_color_by_tex_to_color_map({"h": GOLD})
        aire.next_to(legende[2], LEFT)

        self.play(Circumscribe(VGroup(legende[0:2], petit_triangle_gauche)), run_time=1)

        hauteur = Line(
            triangle_2.get_vertices()[0],
            projection_point_sur_droite(
                triangle_2.get_vertices()[0],
                [triangle_2.get_vertices()[1], triangle_2.get_vertices()[2]],
            ),
            color=GOLD,
        )
        hauteur_legende = MathTex("h").next_to(hauteur.get_center(), RIGHT).scale(0.6)
        hauteur_angle = RightAngle(
            hauteur,
            Line(triangle_2.get_vertices()[1], triangle_2.get_vertices()[2]),
            length=0.2,
            quadrant=(-1, 1),
        )
        hauteur_angle.set_color(GOLD)
        base = Brace(
            Line(triangle_2.get_vertices()[1], triangle_2.get_vertices()[2]),
            sharpness=1,
        )
        base_legende = base.get_tex("b").scale(0.6)
        self.play(
            FadeIn(VGroup(hauteur, hauteur_legende, hauteur_angle), shift=LEFT),
            FadeIn(VGroup(base, base_legende), shift=UP),
            run_time=1.5,
        )

        self.play(
            ReplacementTransform(
                VGroup(
                    triangle_2.copy(),
                    legende[0:2],
                    petit_triangle_gauche,
                    base,
                    base_legende,
                    hauteur.copy(),
                    hauteur_legende.copy(),
                ),
                aire,
            )
        )

        # self.play(
        #     Write(MathTex("h_a", color=PINK).scale(0.6).next_to(perp2.get_midpoint(), 0.9*RIGHT)),
        #     Write(MathTex("h_c", color=BLUE).scale(0.6).next_to(perp1.get_midpoint(), 0.1*LEFT+DOWN)),
        #     Write(MathTex("h_b", color=GREEN).scale(0.6).next_to(perp3.get_midpoint(), 0.12*RIGHT+DOWN))
        # )

        self.wait()

        ha = MathTex("h_a", color=PINK)
        ha.scale(0.6).next_to(perp2.get_midpoint(), 0.9 * RIGHT)
        hb = MathTex("h_b", color=BLUE)
        hb.scale(0.6).next_to(perp1.get_midpoint(), 0.1 * LEFT + DOWN)
        hc = MathTex("h_c", color=GREEN)
        hc.scale(0.6).next_to(perp3.get_midpoint(), 0.2 * RIGHT + 0.95 * DOWN)

        egal = MathTex("=")
        aire_droite = MathTex(
            "\dfrac{1}{2}",
            "b",
            "h_a",
            "+",
            "\dfrac{1}{2}",
            "b",
            "h_b",
            "+",
            "\dfrac{1}{2}",
            "b",
            "h_c",
        )
        aire_droite.set_color_by_tex_to_color_map(
            {"h_a": PINK, "h_b": BLUE, "h_c": GREEN}
        )
        aire_droite.next_to(legende[2], RIGHT)

        self.play(Circumscribe(VGroup(legende[3:5], petit_triangle_a)))
        base = Brace(
            Line(triangle_a.get_vertices()[0], triangle_a.get_vertices()[1]),
            direction=[0, -1, 0],
            sharpness=1,
        )
        base_legende = base.get_tex("b").scale(0.6)
        self.play(Write(ha), FadeIn(VGroup(base, base_legende), shift=UP), run_time=1.5)
        self.play(
            ReplacementTransform(
                VGroup(
                    legende[3:5],
                    petit_triangle_a,
                    triangle_a.copy(),
                    base,
                    base_legende,
                    ha.copy(),
                ),
                aire_droite[0:3],
            )
        )

        self.wait()

        self.play(Circumscribe(VGroup(legende[6:8], petit_triangle_c)))
        base = Brace(
            Line(triangle_c.get_vertices()[0], triangle_c.get_vertices()[1]),
            direction=[-1, 0.6, 0],
            sharpness=1,
        )
        base_legende = base.get_tex("b").scale(0.6)
        self.play(
            Write(hb), FadeIn(VGroup(base, base_legende), shift=RIGHT), run_time=1.5
        )
        self.play(
            ReplacementTransform(
                VGroup(
                    legende[6:8],
                    petit_triangle_c,
                    triangle_c.copy(),
                    base,
                    base_legende,
                    hb.copy(),
                ),
                aire_droite[4:7].next_to(legende[5], RIGHT),
            )
        )

        self.wait()

        self.play(Circumscribe(VGroup(legende[9:11], petit_triangle_b)))
        base = Brace(
            Line(triangle_b.get_vertices()[0], triangle_b.get_vertices()[1]),
            direction=[1, 0.6, 0],
            sharpness=1,
        )
        base_legende = base.get_tex("b").scale(0.6)
        self.play(
            Write(hc), FadeIn(VGroup(base, base_legende), shift=LEFT), run_time=1.5
        )
        self.play(
            ReplacementTransform(
                VGroup(
                    legende[9:11],
                    petit_triangle_b,
                    triangle_b.copy(),
                    base,
                    base_legende,
                    hc.copy(),
                ),
                aire_droite[8:11].next_to(legende[8], RIGHT),
            )
        )

        self.wait()

        demi_b = [aire[:2], aire_droite[0:2], aire_droite[4:6], aire_droite[8:10]]
        encadrement = []
        for text in demi_b:
            encadrement.append(
                SurroundingRectangle(
                    text, buff=0.01, fill_color=YELLOW, fill_opacity=0.2, stroke_width=1
                )
            )
        self.play(FadeIn(*encadrement, lag_ratio=0.2))
        self.play(FadeOut(*encadrement, *demi_b, shift=DOWN))

        formule = VGroup(
            aire[2],
            legende[2],
            aire_droite[2:3],
            legende[5],
            aire_droite[6:7],
            legende[8],
            aire_droite[10],
        )
        conclusion = MathTex("h", "=", "h_a", "+", "h_b", "+", "h_c")
        conclusion.set_color_by_tex_to_color_map(
            {"h": GOLD, "h_a": PINK, "h_b": BLUE, "h_c": GREEN}
        )
        conclusion.next_to(legende[2], RIGHT)
        self.play(ReplacementTransform(formule, conclusion))
        self.play(Circumscribe(conclusion, time_width=2, FadeOut=False))
        self.wait(3)
        self.clear()
