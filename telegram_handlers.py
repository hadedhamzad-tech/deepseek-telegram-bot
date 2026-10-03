from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from deepseek_client import get_deepseek_client
from user_context import context_manager
from logger import logger
from config import settings


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    
    welcome_message = (
        f"👋 سلام {user.first_name}!\n\n"
        "🤖 خوش‌آمدید به ربات هوش مصنوعی DeepSeek\n\n"
        "✨ توانایی‌های من:\n"
        "• 💬 پاسخ‌های هوشمند و دقیق\n"
        "• 🧠 استدلال عمیق برای مسائل پیچیده\n"
        "• 📚 یادآوری تاریخچه گفتگو\n"
        "• 🔄 گفتگوهای چند‌نوبتی سلس‌الاتصال\n\n"
        "📋 دستورات:\n"
        "/help - راهنمای کامل\n"
        "/reasoning - فعال کردن حالت استدلال\n"
        "/clear - پاک کردن تاریخچه\n"
        "/model - تغییر مدل\n"
        "/settings - تنظیمات"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🆘 راهنما", callback_data="help"),
            InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings")
        ],
        [
            InlineKeyboardButton("🧠 استدلال", callback_data="reasoning"),
            InlineKeyboardButton("🤖 مدل", callback_data="model")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "📚 **راهنمای استفاده**\n\n"
        "**دستورات دستیاب:**\n"
        "/start - شروع\n"
        "/help - این پیام\n"
        "/reasoning - فعال/غیرفعال کردن استدلال عمیق\n"
        "/clear - پاک کردن تاریخچه گفتگو\n"
        "/model - تغییر مدل AI\n"
        "/settings - مشاهده تنظیمات\n\n"
        "**نحوه استفاده:**\n"
        "1️⃣ پیام یا سوال خود را بنویسید\n"
        "2️⃣ من با استفاده از DeepSeek به شما پاسخ می‌دهم\n"
        "3️⃣ می‌توانید صحبت را ادامه دهید (تاریخچه حفظ می‌شود)\n\n"
        "**حالت‌های پاسخ:**\n"
        "• 🚀 **سریع**: پاسخ فوری و دقیق\n"
        "• 🧠 **استدلال**: تفکر عمیق برای مسائل پیچیده\n\n"
        "**مدل‌های موجود:**\n"
        "• deepseek-chat - برای گفتگوهای سریع\n"
        "• deepseek-reasoner - برای تفکر عمیق"
    )
    
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clear command - clear conversation history"""
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    
    user_context = context_manager.get_context(user_id, username)
    user_context.clear_history()
    
    logger.info(f"User {user_id} cleared conversation history")
    
    await update.message.reply_text(
        "✅ تاریخچه گفتگو پاک شد\n"
        "می‌توانیم از ابتدا شروع کنیم!"
    )


async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /model command - change AI model"""
    keyboard = [
        [InlineKeyboardButton("⚡ deepseek-chat", callback_data="model_chat")],
        [InlineKeyboardButton("🧠 deepseek-reasoner", callback_data="model_reasoner")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 کدام مدل را می‌خواهید استفاده کنید؟",
        reply_markup=reply_markup
    )


async def reasoning_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /reasoning command - toggle reasoning mode"""
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    
    user_context = context_manager.get_context(user_id, username)
    user_context.reasoning_enabled = not user_context.reasoning_enabled
    
    status = "✅ فعال" if user_context.reasoning_enabled else "❌ غیرفعال"
    
    await update.message.reply_text(
        f"🧠 حالت استدلال {status} شد"
    )


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /settings command"""
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    
    user_context = context_manager.get_context(user_id, username)
    
    settings_text = (
        "⚙️ **تنظیمات شما**\n\n"
        + user_context.get_context_summary() + "\n\n"
        f"💾 تعداد پیام‌های ذخیره شده: {len(user_context.chat_history)}/{user_context.max_history}"
    )
    
    await update.message.reply_text(settings_text, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages - main AI interaction"""
    user = update.effective_user
    message_text = update.message.text
    
    logger.info(f"User {user.id} ({user.username}): {message_text[:100]}")
    
    # Show typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )
    
    try:
        # Get user context
        user_context = context_manager.get_context(user.id, user.username or "Unknown")
        
        # Add user message to history
        user_context.add_message("user", message_text)
        
        # Get AI client
        ai_client = get_deepseek_client()
        
        # Get conversation history
        messages = user_context.get_messages()
        
        # Determine if we should use reasoning
        use_reasoning = user_context.reasoning_enabled and settings.ENABLE_REASONING
        
        if use_reasoning:
            # Show thinking indicator
            thinking_msg = await update.message.reply_text(
                "🧠 درحال تفکر عمیق..."
            )
            
            # Use reasoning model
            thinking, response = ai_client.reasoning_chat(
                message_text,
                history=messages[:-1]  # Exclude current message from history
            )
            
            # Delete thinking message
            await thinking_msg.delete()
            
            # Add response to history
            user_context.add_message("assistant", response)
            
            # Send thinking process if available
            if thinking and len(thinking) > 0:
                thinking_preview = thinking[:300] + "..." if len(thinking) > 300 else thinking
                await update.message.reply_text(
                    f"💭 **فرآیند تفکر:**\n{thinking_preview}",
                    parse_mode="Markdown"
                )
        else:
            # Use regular chat model
            response = ai_client.chat(
                message_text,
                history=messages[:-1]  # Exclude current message from history
            )
            
            # Add response to history
            user_context.add_message("assistant", response)
        
        # Send response (split if too long)
        if len(response) > 4000:
            for i in range(0, len(response), 4000):
                chunk = response[i:i+4000]
                await update.message.reply_text(chunk)
            logger.info(f"Sent response in {(len(response) // 4000) + 1} chunks")
        else:
            await update.message.reply_text(response)
        
        logger.info(f"Response sent successfully (length: {len(response)})")
        
    except Exception as e:
        error_msg = f"❌ خطا: {str(e)}"
        logger.error(f"Error processing message from user {user.id}: {str(e)}")
        await update.message.reply_text(error_msg)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    user_context = context_manager.get_context(user_id, username)
    
    if query.data == "help":
        await help_command(update, context)
    elif query.data == "settings":
        await settings_command(update, context)
    elif query.data == "reasoning":
        user_context.reasoning_enabled = not user_context.reasoning_enabled
        status = "✅ فعال" if user_context.reasoning_enabled else "❌ غیرفعال"
        await query.edit_message_text(f"🧠 حالت استدلال {status} شد")
    elif query.data == "model":
        await model_command(update, context)
    elif query.data == "model_chat":
        user_context.model = "deepseek-chat"
        await query.edit_message_text("✅ مدل به deepseek-chat تغییر یافت")
    elif query.data == "model_reasoner":
        user_context.model = "deepseek-reasoner"
        await query.edit_message_text("✅ مدل به deepseek-reasoner تغییر یافت")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ یک خطای غیرمنتظره رخ داد. لطفاً دوباره تلاش کنید."
        )
