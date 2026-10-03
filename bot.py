import logging
import signal
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
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


def main():
    """Start the bot"""
    
    logger.info("=" * 60)
    logger.info("🤖 DeepSeek Telegram Bot - Professional Edition")
    logger.info("=" * 60)
    
    # Validate configuration
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN not configured!")
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
    
    if not settings.DEEPSEEK_API_KEY:
        logger.error("❌ DEEPSEEK_API_KEY not configured!")
        raise ValueError("DEEPSEEK_API_KEY environment variable is required")
    
    logger.info(f"✅ Configuration loaded successfully")
    logger.info(f"🌐 Server: {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    logger.info(f"🤖 Chat Model: {settings.MODEL}")
    logger.info(f"🧠 Reasoning Model: {settings.REASONING_MODEL}")
    logger.info(f"💾 Max History: {settings.MAX_HISTORY}")
    logger.info(f"🧠 Reasoning: {'✅ Enabled' if settings.ENABLE_REASONING else '❌ Disabled'}")
    logger.info("=" * 60)
    
    # Create application
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    logger.info("📝 Registering command handlers...")
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("model", model_command))
    application.add_handler(CommandHandler("reasoning", reasoning_command))
    application.add_handler(CommandHandler("settings", settings_command))
    
    # Add message handler (must be after command handlers)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    logger.info("✅ Handlers registered successfully")
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        logger.info("\n📊 Shutting down gracefully...")
        stats = context_manager.get_stats()
        logger.info(f"📈 Final stats - Active users: {stats['active_users']}, Total messages: {stats['total_messages']}")
        application.stop()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start the bot
    logger.info("\n🚀 Starting polling...")
    logger.info("💬 Bot is ready to receive messages!")
    logger.info("=" * 60)
    
    application.run_polling(allowed_updates=None)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {str(e)}", exc_info=True)
        raise
