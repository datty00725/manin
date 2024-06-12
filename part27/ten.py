from manim import *

Tex.set_default(tex_template=TexTemplate(
    tex_compiler="lualatex",
    output_format=".pdf",
    preamble=r"""
        \usepackage{amsmath}
        \usepackage{amssymb}
        \usepackage{luatexja}
        \usepackage[haranoaji]{luatexja-preset}
    """
))

class FourierTex(Scene):
    def __init__(self, n_vectors=100, **kwargs):
        super().__init__(**kwargs)
        self.n_vectors = n_vectors  # Number of Fourier vectors
        self.center_point = UP * 2  # Center point of the animation
        self.slow_factor = 0.5  # Factor to adjust animation speed

    def get_freqs(self):
        n = self.n_vectors
        all_freqs = list(range(n // 2, -n // 2, -1))  # Generate frequency list
        all_freqs.sort(key=abs)  # Sort by absolute value
        return all_freqs

    def get_coefficients_of_path(self, path, n_samples=10000, freqs=None):
        if freqs is None:
            freqs = self.get_freqs()
        dt = 1 / n_samples
        ts = np.arange(0, 1, dt)
        samples = np.array([path.point_from_proportion(t) for t in ts])
        samples -= self.center_point
        complex_samples = samples[:, 0] + 1j * samples[:, 1]

        return [
            np.array(
                [
                    np.exp(-TAU * 1j * freq * t) * cs
                    for t, cs in zip(ts, complex_samples)
                ]
            ).sum()
            * dt
            for freq in freqs
        ]

    def get_paths(self, text, width):
        tex_mob = Tex(text)  # Create text
        tex_mob.scale_to_fit_width(width)  # Scale to fit width
        paths = tex_mob.family_members_with_points()[0]
        for p in paths:
            p.set_fill(opacity=0)  # Set fill opacity to 0
            p.set_stroke(WHITE, 1)  # Set stroke color to white, width to 1
        return paths

    def construct(self):
        title_texts = ["天上天下", "唯我独尊"]
        positions = [UP * 2, DOWN * 2]

        title = VGroup(
            Tex("天上天下").move_to(UP * 2).scale(2),
            Tex("唯我独尊").move_to(DOWN * 2).scale(2)
        )
        self.play(Write(title))
        self.wait()

        for i, (text, position) in enumerate(zip(title_texts, positions)):
            self.n_vectors = 5  # Change the number of vectors
            ennokazu = Tex("円の数:").scale(2).to_edge(UP)
            cirnum = Tex(str(self.n_vectors)).scale(2).next_to(ennokazu, RIGHT, buff=1)

            self.play(Write(VGroup(ennokazu, cirnum)))
            self.wait()

            freqs = self.get_freqs()
            paths = self.get_paths(text, 10)
            all_vectors_circles = []
            all_dots = []
            all_traces = []

            for path in paths:
                for subpath in path.get_subpaths():
                    sp_mob = VMobject()
                    sp_mob.set_points(subpath)
                    coefs = self.get_coefficients_of_path(
                        sp_mob, n_samples=100, freqs=freqs
                    )

                    vectorsCircles = VGroup()
                    origin = position
                    for i in range(len(freqs)):
                        dummy = Line(
                            start=ORIGIN, end=[np.real(coefs[i]), np.imag(coefs[i]), 0]
                        )
                        circ = Circle(radius=np.abs(coefs[i])).set_stroke(
                            width=1, color=RED
                        )
                        vectorsCircles += VGroup(dummy, circ).shift(
                            origin
                        )
                        origin = dummy.get_end()

                    all_vectors_circles.append(vectorsCircles)

                    dot = always_redraw(
                        lambda vc=vectorsCircles: Dot(
                            vc[-1][0].get_end() if vc[-1][0].has_points() else ORIGIN,
                            radius=0.04, color=GREEN
                        )
                    )
                    trace = VMobject().set_color(YELLOW)
                    trace.start_new_path(vectorsCircles[-1][0].get_end())
                    all_dots.append(dot)
                    all_traces.append(trace)

            self.play(*[DrawBorderThenFill(vc) for vc in all_vectors_circles])
            self.wait()

            for trace, dot in zip(all_traces, all_dots):
                self.add(trace, dot)

            def vectorsUpdater(vc, trace, dt):
                origin = vc[0][0].get_end()
                for i in range(1, len(freqs)):
                    vc[i][0].rotate(
                        2 * PI * dt * freqs[i] * self.slow_factor,
                        about_point=vc[i][0].get_start(),
                    )
                    vc[i].shift(
                        origin - vc[i][0].get_start()
                    )
                    origin = vc[i][0].get_end()
                trace.add_line_to(vc[-1][0].get_end())

            for vc, trace in zip(all_vectors_circles, all_traces):
                vc.add_updater(lambda m, dt, trace=trace: vectorsUpdater(m, trace, dt))
            self.wait(1 / self.slow_factor + 1)
            for vc in all_vectors_circles:
                vc.clear_updaters()
            self.play(*[FadeOut(vc) for vc in all_vectors_circles])

            self.wait(2)

        vmobjects = [m for m in self.mobjects if isinstance(m, VMobject)]
        self.play(FadeOut(VGroup(*vmobjects)))
        self.wait(2)
