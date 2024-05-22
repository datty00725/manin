# emoji:https://discordapp.com/channels/581738731934056449/1169934985248129044/1169934985248129044

from manim import *

Tex.set_default(
    tex_template=TexTemplate(
        tex_compiler="lualatex",
        output_format=".pdf",
        preamble=r"""
        \usepackage{amsmath}
        \usepackage{amssymb}
        \usepackage{luatexja}
        \usepackage[haranoaji]{luatexja-preset}
    """,
    )
)


class FourierSVG(Scene):
   

    def construct(self):
        def Emoji(text, fmt="svg", res="512"):
            fname = text
            if fmt == "png":
                path = f"../noto-emoji/{fmt}/{res}/emoji_{fname}.{fmt}"
                emoji = ImageMobject(path)
            else:
                path = f"../noto-emoji/{fmt}/emoji_{fname}.{fmt}"
                emoji = SVGMobject(path)
            t = Text(text)
            return emoji.scale_to_fit_width(t.width)

        gros_titre = Emoji("u1f624", "png")
        sub_titre = (
            VGroup(Tex("を円で書く"))
            .arrange(RIGHT)
            .next_to(gros_titre, DOWN)
            .scale(2)
        )

        
        self.add(gros_titre)
        self.play(Create(sub_titre))
        self.wait()

        self.play(
            gros_titre.animate.shift(3.5 * LEFT + 8 * UP).scale(0.3),
            sub_titre.animate.shift(3.5 * LEFT + 9 * UP).scale(0.3),
        )

        