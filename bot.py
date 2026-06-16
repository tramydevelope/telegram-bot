#!/usr/bin/env python3
import logging
import pandas as pd
import os
import json
import hashlib
from datetime import datetime
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
    BotCommand,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN chua duoc cau hinh!")

print(f"✅ Bot started with token: {BOT_TOKEN[:20]}...")

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Chào mừng bạn đến với bot kiếm tiền!\n\n"
        "Hãy nhấn /help để xem hướng dẫn.",
        parse_mode="Markdown"
    )

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 **HƯỚNG DẪN SỬ DỤNG BOT**\n\n"
        "/start - Menu chính\n"
        "/profile - Xem hồ sơ\n"
        "/invite - Lấy link mời bạn\n"
        "/withdraw - Rút tiền",
        parse_mode="Markdown"
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Exception while handling update: {context.error}")

async def post_init(application: Application):
    await application.bot.set_my_commands([
        BotCommand("start", "Bắt đầu / Menu chính"),
        BotCommand("help", "Xem danh sách lệnh"),
        BotCommand("profile", "Hồ sơ & số dư"),
        BotCommand("invite", "Lấy link mời bạn"),
        BotCommand("withdraw", "Rút tiền"),
    ])

def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_error_handler(error_handler)
    
    print(f"╔{'═'*38}")
    print(f"║  🤖 BOT TELEGRAM - KIẾM TIỀN")
    print(f"║  Status: RUNNING 24/7")
    print(f"╚{'═'*38}")
    
    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=__import__("telegram").Update.ALL_TYPES,
    )

if __name__ == "__main__":
    main()