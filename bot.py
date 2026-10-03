"""
Main Telegram Bot Application with DeepSeek AI Integration
Professional-grade chatbot with multi-turn conversations
"""

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from config import settings
from logger import logger
from telegram_handlers import (
    start_command,
    help_command,
    clear_command,
    model_command,
    settings_command,
    handle_message,
    button_callback,
    error_handler,
)


def main():
    """Start the bot"""
    
    logger.info("=" * 50)
    logger.info("DeepSeek Telegram Bot Starting...")
    logger.info("=" * 50)
    
    # Validate configuration
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not configured!")
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
    
    if not settings.DEEPSEEK_API_KEY:
        logger.error("DEEPSEEK_API_KEY not configured!")
        raise ValueError("DEEPSEEK_API_KEY environment variable is required")
    
    logger.info(f"Configuration loaded successfully")
    logger.info(f"Bot Server: {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    logger.info(f"DeepSeek Model: {settings.MODEL}")
    logger.info(f"Max Tokens: {settings.MAX_TOKENS}")
    
    # Create application
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("model", model_command))
    application.add_handler(CommandHandler("settings", settings_command))
    
    # Add message handler (must be after command handlers)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    logger.info("Handlers registered successfully")
    
    # Start the bot
    logger.info("Starting polling...")
    application.run_polling(allowed_updates=None)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        raise
