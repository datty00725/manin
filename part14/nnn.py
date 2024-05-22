from manim import *
class BezierSubpaths(Scene):
    def construct(self):
        tex_mob = Text("か")
        paths = tex_mob.family_members_with_points()

        for path in paths:  
            for subpath in path.get_subpaths():
                for point in subpath:
                    dot = Dot(point, color=RED)
                    self.add(dot)

        self.add(tex_mob)
        self.wait(2)