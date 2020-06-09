from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from io import BytesIO
from fastai.vision import (
    defaults,
    open_image,
    load_learner
)
import torch
import aiohttp
import asyncio

path = Path(__file__).parent
defaults.device = torch.device('cpu')
learner = load_learner(".")

app = FastAPI()
app.mount("/static", StaticFiles(directory=path/"static"), name="static")

def predict_image(data, is_file=True):
    img = open_image(data if is_file else BytesIO(data))
    prediction = learner.predict(img)[0]
    return {'result': str(prediction)}

async def get_bytes_from_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

@app.post("/analyze")
async def create_upload_file(file: UploadFile = File(...)):
    return predict_image(file.file)

@app.post("/classify-url")
async def classify_url(*, url: str = Form(...)):
    bytes = await get_bytes_from_url(url)
    return predict_image(data=bytes, is_file=False)

@app.get('/')
async def homepage():
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())



