from manim import *

class WriteUnicodeCharacter(Scene):
    def construct(self):
        # Use a font that supports the character 𰻞 (U+30EDE)
        character = Text("𰻞", font="Noto Sans CJK JP", font_size=144)
        self.play(Write(character))
        self.wait(2)
