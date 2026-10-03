from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from config import settings
from deepseek_client import deepseek_client
from user_context import context_manager
from logger import logger


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"👋 سلام {user.first_name}!\n\n"
        "🤖 من ربات هوش مصنوعی DeepSeek هستم.\n\n"
        "✨ توانایی‌ها:\n"
        "• 💬 پاسخ‌های هوشمند\n"
        "• 🧠 استدلال عمیق\n"
        "• 📚 یادآوری تاریخچه\n"
        "• ⚙️ تنظیمات سفارشی\n\n"
        "برای راهنما /help را بزن."
    )
    keyboard = [
        [InlineKeyboardButton("🆘 راهنما", callback_data="help"),
         InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings")],
        [InlineKeyboardButton("🧠 استدلال", callback_data="reasoning")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📚 **راهنما**\n\n"
        "/start - شروع\n"
        "/help - راهنما\n"
        "/clear - پاک کردن سابقه\n"
        "/reasoning - استدلال عمیق\n"
        "/model - تغییر مدل\n"
        "/settings - تنظیمات\n\n"
        "**حالت استدلال** برای مسائل پیچیده بهتر است!"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    context_manager.clear_context(user_id)
    await update.message.reply_text("✅ سابقه گفتگو پاک شد.")


async def reasoning_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_ctx = context_manager.get_context(user_id, update.effective_user.username or "Unknown")
    user_ctx.reasoning_enabled = not user_ctx.reasoning_enabled
    status = "فعال" if user_ctx.reasoning_enabled else "غیرفعال"
    await update.message.reply_text(f"🧠 حالت استدلال: {status}")


async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ Chat (سریع)", callback_data="model_chat")],
        [InlineKeyboardButton("🧠 Reasoner (عمیق)", callback_data="model_reasoner")]
    ]
    await update.message.reply_text(
        "🤖 کدام مدل را انتخاب می‌کنید؟",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_ctx = context_manager.get_context(user_id, update.effective_user.username or "Unknown")
    text = (
        f"⚙️ **تنظیمات**\n\n"
        f"👤 نام: {user_ctx.username}\n"
        f"💬 تعداد پیام‌ها: {len(user_ctx.chat_history)}\n"
        f"🧠 استدلال: {'✅ فعال' if user_ctx.reasoning_enabled else '❌ غیرفعال'}\n"
        f"🤖 مدل: {user_ctx.model}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    user_ctx = context_manager.get_context(user.id, user.username or "Unknown")
    
    logger.info(f"User {user.id}: {text[:50]}")
    user_ctx.add_message("user", text)
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    
    try:
        history = user_ctx.get_messages()[:-1]
        
        if user_ctx.reasoning_enabled and settings.ENABLE_REASONING:
            thinking, response = deepseek_client.reasoning_chat(text, history=history)
            if thinking:
                preview = thinking[:250] + "..." if len(thinking) > 250 else thinking
                await update.message.reply_text(f"💭 فرآیند تفکر:\n{preview}")
            user_ctx.add_message("assistant", response)
            if len(response) > 4000:
                for i in range(0, len(response), 4000):
                    await update.message.reply_text(response[i:i+4000])
            else:
                await update.message.reply_text(response)
        else:
            response = deepseek_client.chat(text, history=history)
            user_ctx.add_message("assistant", response)
            if len(response) > 4000:
                for i in range(0, len(response), 4000):
                    await update.message.reply_text(response[i:i+4000])
            else:
                await update.message.reply_text(response)
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        await update.message.reply_text(f"❌ خطا: {str(e)}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "help":
        await help_command(update, context)
    elif query.data == "settings":
        await settings_command(update, context)
    elif query.data == "reasoning":
        await reasoning_command(update, context)
    elif query.data == "model":
        await model_command(update, context)
    elif query.data == "model_chat":
        user_id = update.effective_user.id
        context_manager.get_context(user_id).model = "deepseek-chat"
        await query.edit_message_text("✅ مدل به Chat تغییر یافت")
    elif query.data == "model_reasoner":
        user_id = update.effective_user.id
        context_manager.get_context(user_id).model = "deepseek-reasoner"
        await query.edit_message_text("✅ مدل به Reasoner تغییر یافت")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}")
