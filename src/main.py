import os
import subprocess
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI(title="Manim Animation Studio")

QUALITY = os.getenv("MANIM_QUALITY", "-ql")  # -ql para dev (rápido), -qh para prod

MANIM_SCRIPT = """
from manim import *

class SceneDemo(Scene):
    def construct(self):
        title = Text("Manim en Kubernetes", font_size=40, color=BLUE)
        subtitle = Text(f"Entorno: {os.getenv('ENVIRONMENT', 'Local')}", font_size=24, color=YELLOW)
        subtitle.next_to(title, DOWN)
        
        circle = Circle(radius=1.5, color=GREEN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(1)
        self.play(Transform(title, circle), FadeOut(subtitle))
        self.wait(1)
"""

@app.on_event("startup")
def generate_video():
    with open("scene.py", "w") as f:
        f.write(MANIM_SCRIPT)
    # Compilar video al arrancar
    subprocess.run(["manim", QUALITY, "scene.py", "SceneDemo", "-o", "demo.mp4", "--media_dir", "./media"], check=True)

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
        <head><title>Manim Gallery</title></head>
        <body style="font-family: sans-serif; text-align: center; background: #1a1a1a; color: #fff; padding-top: 50px;">
            <h2>🎬 Animación Generada con Manim</h2>
            <video width="640" height="360" controls autoplay loop>
              <source src="/video" type="video/mp4">
              Tu navegador no soporta video HTML5.
            </video>
        </body>
    </html>
    """

@app.get("/video")
def get_video():
    video_path = "./media/videos/scene/480p15/demo.mp4" if QUALITY == "-ql" else "./media/videos/scene/1080p60/demo.mp4"
    if not os.path.exists(video_path):
        # Fallback de búsqueda recursiva
        for root, _, files in os.walk("./media"):
            for file in files:
                if file.endswith(".mp4"):
                    return FileResponse(os.path.join(root, file), media_type="video/mp4")
    return FileResponse(video_path, media_type="video/mp4")

@app.get("/health")
def health():
    return {"status": "healthy", "quality": QUALITY}
