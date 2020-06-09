FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install torch_nightly -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html
RUN pip install fastai python-multipart aiohttp aiofiles

COPY export.pkl export.pkl
COPY ./app /app
