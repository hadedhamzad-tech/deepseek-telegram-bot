from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from contextlib import asynccontextmanager
import json
from config import settings
from logger import logger
from user_context import context_manager
from telegram_handlers import (
    start_command, help_command, clear_command, reasoning_command,
    model_command, settings_command, handle_message, button_callback, error_handler
)

app_instance = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global app_instance
    
    logger.info("=" * 60)
    logger.info("🤖 DeepSeek Telegram Bot - FastAPI")
    logger.info("=" * 60)
    
    try:
        app_instance = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        
        app_instance.add_handler(CommandHandler("start", start_command))
        app_instance.add_handler(CommandHandler("help", help_command))
        app_instance.add_handler(CommandHandler("clear", clear_command))
        app_instance.add_handler(CommandHandler("reasoning", reasoning_command))
        app_instance.add_handler(CommandHandler("model", model_command))
        app_instance.add_handler(CommandHandler("settings", settings_command))
        app_instance.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app_instance.add_handler(CallbackQueryHandler(button_callback))
        app_instance.add_error_handler(error_handler)
        
        await app_instance.initialize()
        logger.info("✅ Bot initialized")
        
        if settings.WEBHOOK_URL:
            await app_instance.bot.set_webhook(url=settings.WEBHOOK_URL)
            logger.info(f"✅ Webhook set: {settings.WEBHOOK_URL}")
        
    except Exception as e:
        logger.error(f"❌ Initialization failed: {str(e)}")
        raise
    
    yield
    
    logger.info("Shutting down...")
    if app_instance:
        await app_instance.stop()
    logger.info("✅ Shutdown complete")


app = FastAPI(
    title="DeepSeek Telegram Bot",
    description="Professional Telegram bot with DeepSeek AI and reasoning",
    version="2.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    return {
        "status": "online",
        "bot": "DeepSeek Telegram Bot",
        "version": "2.0.0"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/webhook")
async def webhook(request: Request):
    global app_instance
    try:
        data = await request.json()
        update = Update.de_json(data, app_instance.bot)
        if update:
            await app_instance.process_update(update)
        return {"ok": True}
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return {"ok": False, "error": str(e)}


@app.get("/stats")
async def stats():
    return context_manager.stats()
