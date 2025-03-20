import threading
from fastapi import FastAPI
from routers import user_router, questions_router, stats_router, security_router, room_router, exam_sessions_router
from fastapi.middleware.cors import CORSMiddleware
from helpers import telegram_admin_bot
from contextlib import asynccontextmanager

# Global variable to control the bot thread
bot_thread = None
should_stop = threading.Event()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await telegram_admin_bot.start_bot()
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(stats_router.router)
app.include_router(user_router.router)
app.include_router(questions_router.router)
app.include_router(security_router.router)
app.include_router(room_router.router)
app.include_router(exam_sessions_router.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the game!"}