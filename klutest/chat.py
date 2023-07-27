from fastapi import FastAPI, WebSocket
from typing import List

class Chat:
    def __init__(self):
        self.conversation_history = []

    def add_prompt(self, role, content):
        message = {"content:": content}
        self.conversation_history.append(message)
        
    def display_conversation(self):
        for message in self.conversation_history:
            return self.conversation_history
