import signal
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import settings
from logger import logger
from user_context import context_manager
from telegram_handlers import (
    start_command, help_command, clear_command, reasoning_command,
    model_command, settings_command, handle_message, button_callback, error_handler
)


def main():
    logger.info("=" * 60)
    logger.info("🤖 DeepSeek Telegram Bot - Professional Edition")
    logger.info("=" * 60)
    
    if not settings.TELEGRAM_BOT_TOKEN or not settings.DEEPSEEK_API_KEY:
        logger.error("Missing required environment variables")
        raise ValueError("TELEGRAM_BOT_TOKEN and DEEPSEEK_API_KEY are required")
    
    logger.info(f"Model: {settings.MODEL}")
    logger.info(f"Reasoning: {'Enabled' if settings.ENABLE_REASONING else 'Disabled'}")
    
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("reasoning", reasoning_command))
    app.add_handler(CommandHandler("model", model_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_error_handler(error_handler)
    
    def signal_handler(sig, frame):
        logger.info("Shutting down...")
        stats = context_manager.stats()
        logger.info(f"Stats: {stats}")
        app.stop()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("🚀 Bot started - Polling...")
    app.run_polling(allowed_updates=None)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
