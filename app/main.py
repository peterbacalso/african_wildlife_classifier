from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from pathlib import Path
from io import BytesIO
from fastai.vision import (
    defaults,
    open_image,
    load_learner
)
import torch
import aiohttp

app = FastAPI()

defaults.device = torch.device('cpu')
learner = load_learner(".")

def predict_image(data, is_file=True):
    img = open_image(data if is_file else BytesIO(data))
    _,_,losses = learner.predict(img)
    return {
        "predictions": sorted(
            zip(learner.data.classes, map(float, losses)),
            key=lambda p: p[1],
            reverse=True
        )
    }

async def get_bytes_from_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    return predict_image(file.file)

@app.post("/classify-url")
async def classify_url(*, url: str = Form(...)):
    bytes = await get_bytes_from_url(url)
    return predict_image(data=bytes, is_file=False)

@app.get("/")
async def form():
    html_content = """
        <form action="/upload" method="post" enctype="multipart/form-data">
            Select image to upload:
            <input type="file" name="file">
            <input type="submit" value="Upload Image">
        </form>
        Or submit a URL:
        <form action="/classify-url" method="post">
            <input type="url" name="url">
            <input type="submit" value="Fetch and analyze image">
        </form>
    """
    return HTMLResponse(content=html_content, status_code=200)



