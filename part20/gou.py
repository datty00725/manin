from manim import *

class DisplayUnicodeImage(Scene):
    def construct(self):
        # Load the image file containing the Unicode character
        image = ImageMobject("unicode_char.png")
        self.play(FadeIn(image))
        self.wait(2)
