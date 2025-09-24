from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = Path("../").resolve()
WEB_DIR = Path(__file__).resolve().parent

print(PROJECT_DIR)

app = FastAPI(title="Image Region Selector")
img_path = PROJECT_DIR / "awa.jpg"
print(img_path)


# Раздаём статические файлы tgwebapp (index.html, styles.css, script.js)
app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")

# Явный роут для картинки из корня проекта (awa.jpg)
@app.get("/")
async def get_awa():
    
    return FileResponse(str(img_path))