from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Создание экземпляра FastAPI
app = FastAPI()

# Настройка CORS (разрешение кросс-доменных запросов)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение папки со статикой (если есть frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Модель запроса
class Message(BaseModel):
    message: str

# Корневой маршрут
@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>Advisor работает. Отправь POST-запрос на /chat</h1>"

# Обработчик чата
@app.post("/chat")
async def chat(request: Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": request.message}],
            temperature=0.7,
            max_tokens=800,
        )
        reply = response.choices[0].message["content"]
        return {"reply": reply}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
