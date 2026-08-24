import os
from manim import *

class VectorTransformScene(LinearTransformationScene):
    def __init__(self, **kwargs):
        super().__init__(
            show_coordinates=True,
            leave_ghost_vectors=True,
            **kwargs
        )

    def construct(self):
        title = Text("Álgebra Lineal: Transformaciones", font_size=32, color=BLUE)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        matrix = [[1, 1], [0, 1]]
        v1 = self.add_vector([1, 0], color=YELLOW)
        v2 = self.add_vector([0, 1], color=GREEN)

        self.wait(0.5)
        self.apply_matrix(matrix)
        self.wait(1)
