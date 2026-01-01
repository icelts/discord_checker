from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from app.checker import process_tokens
import json
import os

app = FastAPI()

@app.get("/")
async def index():
    with open("static/frontend.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/upload/")
async def upload_files(background_tasks: BackgroundTasks,
                       token_file: UploadFile = File(...),
                       proxy_file: UploadFile = File(...)):
    os.makedirs("tmp", exist_ok=True)
    token_path = f"tmp/tokens.txt"
    proxy_path = f"tmp/proxies.txt"
    with open(token_path, "wb") as f:
        f.write(await token_file.read())
    with open(proxy_path, "wb") as f:
        f.write(await proxy_file.read())
    background_tasks.add_task(process_tokens, token_path, proxy_path)
    return {"status": "检测任务已启动，请稍候查看结果"}

@app.get("/download/{result_type}")
async def download_result(result_type: str):
    path = f"result/{result_type}.txt"
    return FileResponse(path, media_type="text/plain", filename=f"{result_type}.txt")

@app.get("/progress")
async def get_progress():
    try:
        with open("result/progress.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"done": 0, "total": 0, "stats": {}}
