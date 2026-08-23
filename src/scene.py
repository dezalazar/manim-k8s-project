import os
from manim import *

class SceneDemo(Scene):
    def construct(self):
        env_name = os.getenv("ENVIRONMENT", "Desarrollo")
        title = Text("Manim en Kubernetes", font_size=36, color=BLUE)
        subtitle = Text(f"Entorno: {env_name}", font_size=24, color=YELLOW)
        subtitle.next_to(title, DOWN)
        
        circle = Circle(radius=1.5, color=GREEN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(1)
        self.play(Transform(title, circle), FadeOut(subtitle))
        self.wait(1)
