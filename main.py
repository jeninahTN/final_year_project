from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
from app.data import get_monitored_crops, get_crop_detail
from app.prediction import prediction_service
from pydantic import BaseModel
from typing import List

from pathlib import Path

app = FastAPI(title="Market Pulse")

# Setup paths
BASE_DIR = Path(__file__).resolve().parent

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    crops = get_monitored_crops()
    return templates.TemplateResponse("index.html", {"request": request, "title": "Dashboard", "crops": crops})

@app.get("/detail/{crop}/{region}", response_class=HTMLResponse)
async def read_detail(request: Request, crop: str, region: str):
    detail = get_crop_detail(crop, region)
    return templates.TemplateResponse("detail.html", {"request": request, "title": f"{detail['name']} in {detail['region']}", "detail": detail})

@app.get("/offline", response_class=HTMLResponse)
async def read_offline(request: Request):
    return templates.TemplateResponse("offline.html", {"request": request, "title": "Offline Access"})

@app.get("/help", response_class=HTMLResponse)
async def read_help(request: Request):
    return templates.TemplateResponse("help.html", {"request": request, "title": "Help & Support"})

@app.get("/ussd", response_class=HTMLResponse)
async def read_ussd(request: Request):
    return templates.TemplateResponse("ussd.html", {"request": request, "title": "USSD Service"})

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title": "Login"})

class PredictionRequest(BaseModel):
    features: List[float]

@app.post("/predict")
async def predict_price(request: PredictionRequest):
    prediction = prediction_service.predict(request.features)
    if prediction is not None:
        return {"predicted_price": prediction}
    else:
        return {"error": "Prediction failed"}, 500
