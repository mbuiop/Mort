from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

# ساخت اپلیکیشن
app = FastAPI()

# مسیر فایل‌های استاتیک (در صورت نیاز مثل css/js/img)
# اگر پوشه static نداری، این خط رو کامنت کن
# app.mount("/static", StaticFiles(directory="static"), name="static")

# پیکربندی قالب‌ها (templates)
templates = Jinja2Templates(directory="templates")

# اطمینان از وجود پوشه data
DATA_DIR = "data"
Path(DATA_DIR).mkdir(exist_ok=True)

# فایل‌ها
SITES_FILE = os.path.join(DATA_DIR, "sites.txt")
SIGNALS_FILE = os.path.join(DATA_DIR, "signals.txt")
ANALYSIS_FILE = os.path.join(DATA_DIR, "analysis.txt")

# ایجاد فایل‌های خالی در صورت نبودن
for file_path in [SITES_FILE, SIGNALS_FILE, ANALYSIS_FILE]:
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")

# صفحه اصلی
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# فرم ثبت سایت
@app.get("/sabt/", response_class=HTMLResponse)
async def show_site_form(request: Request):
    return templates.TemplateResponse("sabt.html", {"request": request})

# دریافت اطلاعات فرم و ذخیره سایت
@app.post("/sabt/submit/")
async def submit_site(
    site_name: str = Form(...),
    site_url: str = Form(...),
    description: str = Form(...)
):
    with open(SITES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{site_name}|{site_url}|{description}\n")
    return RedirectResponse(url="/sabt/success", status_code=303)

# صفحه موفقیت پس از ثبت
@app.get("/sabt/success", response_class=HTMLResponse)
async def show_success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

# نمایش سیگنال‌ها
@app.get("/signal/", response_class=HTMLResponse)
async def show_signals(request: Request):
    with open(SIGNALS_FILE, "r", encoding="utf-8") as f:
        signals = f.readlines()
    return templates.TemplateResponse("signal.html", {"request": request, "signals": signals})

# نمایش تحلیل‌ها
@app.get("/tahlil/", response_class=HTMLResponse)
async def show_analysis(request: Request):
    with open(ANALYSIS_FILE, "r", encoding="utf-8") as f:
        analysis = f.read()
    return templates.TemplateResponse("tahlil.html", {"request": request, "analysis": analysis})

# نمایش لیست سایت‌های ثبت‌شده
@app.get("/saet/", response_class=HTMLResponse)
async def show_sites(request: Request):
    with open(SITES_FILE, "r", encoding="utf-8") as f:
        sites = [line.strip().split("|") for line in f if line.strip()]
    return templates.TemplateResponse("saet.html", {"request": request, "sites": sites})

# اجرای سرور فقط اگر مستقیم اجرا شد
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
