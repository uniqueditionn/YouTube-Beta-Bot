import asyncio
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Application
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import register_handlers

app = FastAPI()
bot = Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()
register_handlers(application)

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    await application.update_queue.put(update)
    return {"ok": True}

async def set_webhook():
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(set_webhook())
