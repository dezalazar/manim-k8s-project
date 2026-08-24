import os
from manim import *

class VectorTransformScene(Scene):
    def construct(self):
        title = Text("Álgebra Lineal: Transformaciones", font_size=30, color=BLUE)
        title.to_edge(UP)
        self.add(title)

        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.4}
        )

        v1 = Vector([2, 1], color=YELLOW)
        v2 = Vector([-1, 2], color=GREEN)
        v1_label = Text("v1", font_size=20, color=YELLOW).next_to(v1.get_end(), RIGHT)
        v2_label = Text("v2", font_size=20, color=GREEN).next_to(v2.get_end(), UP)

        matrix = [[1, 1], [0, 1]]

        self.play(Create(grid), run_time=1)
        self.play(GrowArrow(v1), Write(v1_label), GrowArrow(v2), Write(v2_label))
        self.wait(0.5)

        # Aplicar transformación de corte (shear)
        self.play(
            grid.animate.apply_matrix(matrix),
            v1.animate.apply_matrix(matrix),
            v2.animate.apply_matrix(matrix),
            v1_label.animate.move_to(v1.get_end() + RIGHT * 0.3),
            v2_label.animate.move_to(v2.get_end() + UP * 0.3),
            run_time=2
        )
        self.wait(1)
