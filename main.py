from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем ключ из переменной окружения
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Разрешаем CORS (для доступа с фронта)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель запроса
class ChatRequest(BaseModel):
    message: str

# Обработка запроса на /chat
@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": req.message}],
            temperature=0.7,
            max_tokens=800,
        )
        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}
