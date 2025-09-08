import asyncio
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import register_handlers

app = FastAPI()

# Build Telegram application
application = Application.builder().token(BOT_TOKEN).build()
register_handlers(application)

# Webhook route
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return {"ok": True}

# Homepage route (prevents 404)
@app.get("/")
async def home():
    return {"status": "Bot is running!"}

# Set webhook on startup
async def set_webhook():
    await application.bot.delete_webhook()
    await application.bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(set_webhook())
