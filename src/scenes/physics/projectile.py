import os
from manim import *

class ProjectileMotionScene(Scene):
    def construct(self):
        title = Text("Física: Cinemática y Movimiento Parabólico", font_size=30, color=BLUE)
        title.to_edge(UP)
        self.add(title)

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 6, 2],
            axis_config={"include_numbers": True},
        ).scale(0.8).to_edge(DOWN)

        labels = axes.get_axis_labels(x_label="x [m]", y_label="y [m]")
        parabola = axes.plot(lambda x: -0.2 * (x - 4)**2 + 3.2, x_range=[0, 8], color=YELLOW)

        dot = Dot(color=RED).move_to(axes.c2p(0, 0))

        self.play(Create(axes), Write(labels))
        self.play(Create(parabola), run_time=1.5)
        self.play(MoveAlongPath(dot, parabola), run_time=2, rate_func=linear)
        self.wait(1)
