from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from contextlib import asynccontextmanager
import json
from config import settings
from logger import logger
from user_context import context_manager
from telegram_handlers import (
    start_command,
    help_command,
    clear_command,
    model_command,
    reasoning_command,
    settings_command,
    handle_message,
    button_callback,
    error_handler,
)

# Global application instance
app_instance: Application = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage FastAPI app lifecycle"""
    global app_instance
    
    logger.info("=" * 60)
    logger.info("🤖 DeepSeek Telegram Bot - Starting FastAPI...")
    logger.info("=" * 60)
    
    try:
        # Create Telegram Application
        app_instance = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        
        # Add handlers
        logger.info("📝 Registering handlers...")
        app_instance.add_handler(CommandHandler("start", start_command))
        app_instance.add_handler(CommandHandler("help", help_command))
        app_instance.add_handler(CommandHandler("clear", clear_command))
        app_instance.add_handler(CommandHandler("model", model_command))
        app_instance.add_handler(CommandHandler("reasoning", reasoning_command))
        app_instance.add_handler(CommandHandler("settings", settings_command))
        app_instance.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app_instance.add_handler(CallbackQueryHandler(button_callback))
        app_instance.add_error_handler(error_handler)
        
        # Initialize application
        await app_instance.initialize()
        logger.info("✅ Telegram Application initialized successfully")
        
        # Set webhook
        if settings.WEBHOOK_URL:
            await app_instance.bot.set_webhook(url=settings.WEBHOOK_URL)
            logger.info(f"🔗 Webhook set to {settings.WEBHOOK_URL}")
        
        logger.info(f"🚀 FastAPI running on {settings.SERVER_HOST}:{settings.SERVER_PORT}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize bot: {str(e)}", exc_info=True)
        raise
    
    yield
    
    # Shutdown
    logger.info("\n📊 Shutting down application...")
    stats = context_manager.get_stats()
    logger.info(f"📈 Final stats - Active users: {stats['active_users']}, Total messages: {stats['total_messages']}")
    if app_instance:
        await app_instance.stop()
    logger.info("✅ Application shut down successfully")


# Create FastAPI app
app = FastAPI(
    title="DeepSeek Telegram Bot",
    description="Professional Telegram bot powered by DeepSeek AI with reasoning capabilities",
    version="2.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "online",
        "bot": "DeepSeek Telegram Bot",
        "version": "2.0.0",
        "webhook_url": settings.WEBHOOK_URL,
        "model": settings.MODEL,
        "reasoning_enabled": settings.ENABLE_REASONING
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "bot": "DeepSeek Telegram Bot",
        "version": "2.0.0"
    }


@app.post("/webhook")
async def webhook(request: Request):
    """Handle Telegram webhook updates"""
    global app_instance
    
    try:
        # Get update data
        data = await request.json()
        logger.debug(f"Received update: {json.dumps(data)[:200]}")
        
        # Create Update object
        update = Update.de_json(data, app_instance.bot)
        
        # Process update
        if update:
            await app_instance.process_update(update)
            logger.debug("Update processed successfully")
        
        return {"ok": True}
        
    except Exception as e:
        logger.error(f"❌ Error processing webhook: {str(e)}", exc_info=True)
        return {"ok": False, "error": str(e)}


@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    """Alternative webhook endpoint for Telegram"""
    return await webhook(request)


@app.get("/stats")
async def get_stats():
    """Get bot statistics"""
    stats = context_manager.get_stats()
    return {
        **stats,
        "model": settings.MODEL,
        "reasoning_model": settings.REASONING_MODEL,
        "max_tokens": settings.MAX_TOKENS,
        "reasoning_max_tokens": settings.REASONING_MAX_TOKENS,
        "temperature": settings.TEMPERATURE
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"🚀 Starting FastAPI server on {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    
    uvicorn.run(
        "app:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=False,
        log_level=settings.LOG_LEVEL.lower()
    )
