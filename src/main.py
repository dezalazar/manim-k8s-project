import os
import subprocess
import glob
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI(title="Manim Animation Studio")

QUALITY = os.getenv("MANIM_QUALITY", "-ql")
ENV_NAME = os.getenv("ENVIRONMENT", "Desarrollo (DEV)")

@app.on_event("startup")
def generate_video():
    os.makedirs("/app/media", exist_ok=True)
    cmd = ["manim", QUALITY, "/app/scene.py", "SceneDemo", "-o", "demo.mp4", "--media_dir", "/app/media"]
    print(f"Rendering animation with command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"Manim compilation failed: {result.stderr}")

@app.get("/", response_class=HTMLResponse)
def index():
    return f"""
    <html>
        <head><title>Manim Gallery - {ENV_NAME}</title></head>
        <body style="font-family: sans-serif; text-align: center; background: #1a1a1a; color: #fff; padding-top: 50px;">
            <h2>🎬 Animación Generada con Manim</h2>
            <p><strong>Ambiente:</strong> {ENV_NAME} | <strong>Calidad:</strong> {QUALITY}</p>
            <video width="640" height="360" controls autoplay loop>
              <source src="/video" type="video/mp4">
              Tu navegador no soporta video HTML5.
            </video>
        </body>
    </html>
    """

@app.get("/video")
def get_video():
    files = glob.glob("/app/media/**/*.mp4", recursive=True)
    if files:
        return FileResponse(files[0], media_type="video/mp4")
    return HTMLResponse("Video no encontrado", status_code=404)

@app.get("/health")
def health():
    return {"status": "healthy", "quality": QUALITY, "environment": ENV_NAME}
