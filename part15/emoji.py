from manim import *


def Emoji(text, fmt="svg", res="512"):
    fname = "_".join(f"{ord(c):x}" for c in text)
    if fmt=="png":
        path = f"../noto-emoji/{fmt}/{res}/emoji_u{fname}.{fmt}"
        emoji = ImageMobject(path)
    else:
        path = f"../noto-emoji/{fmt}/emoji_u{fname}.{fmt}"
        emoji = SVGMobject(path)
    t = Text(text)
    return emoji.scale_to_fit_width(t.width)

class Test(Scene):
    def construct(self):
        self.add(NumberPlane())
        g = Group()
        image1 = ImageMobject("../noto-emoji-svg/png/u2753.png")
        self.add(image1)
