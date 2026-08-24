import os
from manim import *

class BinaryTreeScene(Scene):
    def construct(self):
        title = Text("IT: Árbol Binario de Búsqueda (BST)", font_size=30, color=BLUE)
        title.to_edge(UP)
        self.add(title)

        def make_node(val, pos):
            c = Circle(radius=0.4, color=WHITE, fill_opacity=1, fill_color=BLACK).move_to(pos)
            t = Text(str(val), font_size=22).move_to(pos)
            return VGroup(c, t)

        root = make_node("50", UP * 1.5)
        left = make_node("30", LEFT * 2 + UP * 0.2)
        right = make_node("70", RIGHT * 2 + UP * 0.2)

        edge1 = Line(root.get_bottom(), left.get_top(), color=GRAY)
        edge2 = Line(root.get_bottom(), right.get_top(), color=GRAY)

        self.play(FadeIn(root))
        self.play(Create(edge1), FadeIn(left))
        self.play(Create(edge2), FadeIn(right))
        self.wait(1)
