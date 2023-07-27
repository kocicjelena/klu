from fastapi import WebSocket
from requests import Session
#from fastapi_contrib.sessions import FastAPISessionMaker, Session
#from fastapi_sessions import SessionMiddleware, Session, EncryptedCookieStorage
#from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
#from fastapi_sessions import Session
from typing import List

class WebSocketManagerWithoutSession:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)

    async def send_message(self, user_id: str, message: str):
        if user_id in self.active_connections:
            for websocket in self.active_connections[user_id]:
                await websocket.send_text(message) 
  