from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates configuration
templates = Jinja2Templates(directory="templates")

# Ensure data directory exists
DATA_DIR = "data"
Path(DATA_DIR).mkdir(exist_ok=True)

# File paths
SITES_FILE = os.path.join(DATA_DIR, "sites.txt")
SIGNALS_FILE = os.path.join(DATA_DIR, "signals.txt")
ANALYSIS_FILE = os.path.join(DATA_DIR, "analysis.txt")

# Initialize files if they don't exist
for file_path in [SITES_FILE, SIGNALS_FILE, ANALYSIS_FILE]:
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/sabt/", response_class=HTMLResponse)
async def show_site_form(request: Request):
    return templates.TemplateResponse("sabt.html", {"request": request})

@app.post("/sabt/submit/")
async def submit_site(
    site_name: str = Form(...),
    site_url: str = Form(...),
    description: str = Form(...)
):
    with open(SITES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{site_name}|{site_url}|{description}\n")
    
    return RedirectResponse(url="/sabt/success", status_code=303)

@app.get("/sabt/success", response_class=HTMLResponse)
async def show_success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@app.get("/signal/", response_class=HTMLResponse)
async def show_signals(request: Request):
    with open(SIGNALS_FILE, "r", encoding="utf-8") as f:
        signals = f.readlines()
    return templates.TemplateResponse("signal.html", {"request": request, "signals": signals})

@app.get("/tahlil/", response_class=HTMLResponse)
async def show_analysis(request: Request):
    with open(ANALYSIS_FILE, "r", encoding="utf-8") as f:
        analysis = f.read()
    return templates.TemplateResponse("tahlil.html", {"request": request, "analysis": analysis})

@app.get("/saet/", response_class=HTMLResponse)
async def show_sites(request: Request):
    with open(SITES_FILE, "r", encoding="utf-8") as f:
        sites = [line.strip().split("|") for line in f.readlines() if line.strip()]
    return templates.TemplateResponse("saet.html", {"request": request, "sites": sites})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)