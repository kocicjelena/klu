import logging
import time
from celery.result import AsyncResult
from fastapi import Body, FastAPI, Form, Request, WebSocket, Depends, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
#from worker import celery
from worker import get_answer,get_all_dataset_task,get_pick_task,get_dindex_task
import anyio
from ws import WebSocketManagerWithoutSession
from fastapi.responses import Response
from chat import Chat
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import http
import uvicorn

# In a real-world scenario, 
# you would have to load dataset from huggingface
# and particularly here
# go by flow described at Vicuna_unfiltered_train.ipynb:

""" from datasets import load_dataset

data_files = {"train": "train.csv", "test": "test.csv"}
dataset = load_dataset("anon8231489123/ShareGPT_Vicuna_unfiltered", data_files=data_files)
 """
 
# For the purpouses of exercise 
# it is supposed that we have dataset (downloaded).


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

async def is_user_allowed(request: Request):
    # if conditions are not met, return False
    print(request['headers'])
    print(request.client)
    return True


logger = logging.getLogger("uvicorn.access")
async def log_request_middleware(request: Request, call_next):
    logger.debug("middleware: log_request_middleware")
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    try:
        status_phrase = http.HTTPStatus(response.status_code).phrase
    except ValueError:
        status_phrase=""
    logger.info(f'{host}:{port} - "{request.method} {url}" {response.status_code} {status_phrase} {formatted_process_time}ms')
    return response
app.middleware("http")(log_request_middleware)

managerSocket = WebSocketManagerWithoutSession()


def temp():
    d = get_all_dataset_task()
    return d
d = temp()


def temp2(dd):
    ddd = get_dindex_task(dd)
    return ddd

r = temp2(d)


@app.websocket("/ws/chat/{user_id}")
async def chat_endpoint(websocket: WebSocket, user_id: str):
    await managerSocket.connect(websocket, user_id)
    chat = Chat()

    try:
        while True:
            data = await websocket.receive_text()
            chat.add_prompt("human",data)
            
            res = get_pick_task(data, r,d)
            chat.add_prompt("gpt",res)
            conversation = chat.display_conversation()
            await managerSocket.send_message(user_id, str(conversation))
    except Exception as e:
        print(f"WebSocket connection closed: {e}")
    finally:
        managerSocket.disconnect(websocket, user_id)

# TESTING PURPOUSES: the rest of code is for simple BENCHMARK with drill


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})
""" 
@app.post("/dataset", status_code=201)
async def run_first_task(payload = Body(...)):
    task_type = payload["type"]
    task = get_all.apply_async(args=(task_type,))
    return JSONResponse({"task_id": task.id})


@app.get("/dataset/{task_id}", status_code=201)
async def get_dataset(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse({
        "task_id": task_id,
        "task_status": "SUCCESS",
        "task_result": True
    }) """
   
   
@app.post("/chat", status_code=201)
async def run_chat(payload = Body(...)):
    task_type = payload["type"]
    question = payload["quest"]
    task = get_answer.apply_async(args=(task_type,question,))
    return JSONResponse({"task_id": task.id})


@app.get("/chat/{task_id}", status_code=201)
async def get_chat(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse({
        "task_id": task_id,
        "task_status": "SUCCESS",
        "task_result": True
    })
