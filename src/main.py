import os
import glob
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI(title="Portal Educativo Manim")

QUALITY = os.getenv("MANIM_QUALITY", "-ql")
ENV_NAME = os.getenv("ENVIRONMENT", "Desarrollo (DEV)")

CATALOG = {
    "matematica": {
        "title": "Matemática",
        "description": "Transformaciones lineales, cálculo y geometría analítica.",
        "file": "/app/scenes/math/vectors.py",
        "scene": "VectorTransformScene",
        "id": "matematica"
    },
    "fisica": {
        "title": "Física",
        "description": "Cinemática, vectores de fuerza y leyes de Newton.",
        "file": "/app/scenes/physics/projectile.py",
        "scene": "ProjectileMotionScene",
        "id": "fisica"
    },
    "ti": {
        "title": "Tecnología de la Información",
        "description": "Estructuras de datos, árboles binarios y redes.",
        "file": "/app/scenes/it/binary_tree.py",
        "scene": "BinaryTreeScene",
        "id": "ti"
    }
}

@app.on_event("startup")
def compile_initial_scenes():
    os.makedirs("/app/media", exist_ok=True)
    for key, item in CATALOG.items():
        media_out = f"/app/media/{key}"
        os.makedirs(media_out, exist_ok=True)
        cmd = ["manim", QUALITY, item["file"], item["scene"], "-o", f"{key}.mp4", "--media_dir", media_out]
        print(f"Compilando {item['title']}...")
        subprocess.run(cmd, check=False)

@app.get("/", response_class=HTMLResponse)
def index():
    cards = ""
    for k, v in CATALOG.items():
        cards += f"""
        <div style="background:#262626; border-radius:10px; padding:20px; width:300px; margin:15px; box-shadow:0 4px 6px rgba(0,0,0,0.3); text-align:left;">
            <h3 style="color:#60a5fa; margin-top:0;">{v['title']}</h3>
            <p style="color:#d1d5db; font-size:14px; min-height:45px;">{v['description']}</p>
            <video width="100%" height="180" controls style="border-radius:6px; background:#000;">
                <source src="/video/{k}" type="video/mp4">
            </video>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Portal Educativo - Manim Studio</title>
    </head>
    <body style="font-family:sans-serif; background:#121212; color:#fff; margin:0; padding:20px;">
        <header style="text-align:center; padding:20px 0; border-bottom:1px solid #333;">
            <h1>📚 Portal Educativo Multimedia</h1>
            <p style="color:#9ca3af;">Ambiente: <span style="color:#34d399; font-weight:bold;">{ENV_NAME}</span> | Render: <span style="color:#fbbf24;">{QUALITY}</span></p>
        </header>
        <main style="display:flex; flex-wrap:wrap; justify-content:center; padding:30px 10px;">
            {cards}
        </main>
    </body>
    </html>
    """

@app.get("/video/{category}")
def get_video(category: str):
    if category not in CATALOG:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    files = glob.glob(f"/app/media/{category}/**/*.mp4", recursive=True)
    if files:
        return FileResponse(files[0], media_type="video/mp4")
    return HTMLResponse("Video en renderizado...", status_code=202)

@app.get("/health")
def health():
    return {"status": "healthy", "environment": ENV_NAME, "quality": QUALITY, "categories": list(CATALOG.keys())}
