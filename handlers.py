from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, CallbackQueryHandler, filters
from downloader import download_audio, download_video
from utils import clean_file

def register_handlers(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.add_handler(CallbackQueryHandler(handle_button))

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    keyboard = [
        [InlineKeyboardButton("🎵 Music", callback_data=f"audio|{url}")],
        [InlineKeyboardButton("🎬 Video", callback_data=f"video|{url}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose format:", reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice, url = query.data.split("|")

    msg = await query.message.reply_text(f"Downloading {choice}... Please wait.")

    try:
        if choice == "audio":
            file_path = await download_audio(url)
        else:
            file_path = await download_video(url)

        await query.message.reply_document(open(file_path, "rb"))
        clean_file(file_path)
        await msg.delete()
    except Exception as e:
        await query.message.reply_text(f"Error: {str(e)}")
