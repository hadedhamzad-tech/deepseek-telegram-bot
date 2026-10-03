# 🤖 DeepSeek Telegram Bot - Professional Edition

ربات تلگرام حرفه‌ای و قدرتمند با هوش مصنوعی DeepSeek، توانایی استدلال عمیق و پاسخ‌های هوشمند.

## ✨ ویژگی‌های اصلی

### 🧠 توانایی‌های هوش مصنوعی
- **مدل Chat**: پاسخ‌های سریع و دقیق برای اکثر سوالات
- **مدل Reasoner**: استدلال عمیق برای مسائل پیچیده و تحلیلی
- **حافظه مکالمه**: یادآوری تاریخچه گفتگو برای تعاملات بهتر
- **تغییر مدل**: انتخاب بین حالات مختلف پاسخ

### 🔧 ویژگی‌های فنی
- FastAPI برای webhook و production deployment
- Polling برای توسعه محلی
- مدیریت context کاربران
- Logging جامع و فایل‌های لاگ
- تنظیمات کامل و قابل تغییر
- پشتیبانی از Docker و Docker Compose
- معماری ماژولار و آسان برای توسعه

## 📋 دستورات دستیاب

| دستور | توضیح |
|-------|-------|
| `/start` | شروع ربات و مشاهده منوی اصلی |
| `/help` | نمایش راهنمای کامل |
| `/reasoning` | فعال/غیرفعال کردن حالت استدلال عمیق |
| `/clear` | پاک کردن تاریخچه گفتگو |
| `/model` | تغییر مدل AI (chat یا reasoner) |
| `/settings` | مشاهده تنظیمات فعلی |

## 🚀 شروع سریع

### نیازمندی‌ها
- Python 3.8+
- API Key از [DeepSeek Platform](https://platform.deepseek.com)
- Telegram Bot Token از [@BotFather](https://t.me/BotFather)

### نصب

1. **Clone Repository**
```bash
git clone https://github.com/hadedhamzad-tech/deepseek-telegram-bot.git
cd deepseek-telegram-bot
```

2. **ایجاد Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# یا
venv\Scripts\activate  # Windows
```

3. **نصب Dependencies**
```bash
pip install -r requirements.txt
```

4. **کانفیگ محیطی**
```bash
cp .env.example .env
# .env را با اطلاعات واقعی کامل کن
```

5. **اجرای ربات**
```bash
python bot.py
```

## ⚙️ تنظیمات

### متغیرهای محیطی

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_token

# DeepSeek API
DEEPSEEK_API_KEY=your_key
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
WEBHOOK_URL=https://your-domain.com/webhook  # For production

# Models
MAX_TOKENS=2000
TEMPERATURE=0.7
MODEL=deepseek-chat
REASONING_MODEL=deepseek-reasoner
REASONING_MAX_TOKENS=8000

# Features
ENABLE_REASONING=true
ENABLE_CONTEXT=true
MAX_HISTORY=20

# Logging
LOG_LEVEL=INFO
```

## 📁 ساختار پروژه

```
deepseek-telegram-bot/
├── config.py                 # Configuration management
├── logger.py                 # Logging setup
├── deepseek_client.py        # DeepSeek API client
├── user_context.py           # User context management
├── telegram_handlers.py      # Telegram command handlers
├── bot.py                    # Main bot (polling)
├── app.py                    # FastAPI webhook app
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose
├── DEPLOYMENT.md             # Deployment guide
├── LICENSE                   # MIT License
└── README.md                 # This file
```

## 🎯 حالت‌های کار

### Polling (توسعه محلی)
```bash
python bot.py
```
- مناسب برای توسعه و تست
- ربات مستقیماً تغییرات را بررسی می‌کند

### Webhook (Production)
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```
- مناسب برای سرور و production
- بدون تاخیر در دریافت پیام‌ها
- قابل scale کردن

## 🐳 Docker

### Build و اجرا
```bash
docker build -t deepseek-telegram-bot .
docker run -p 8000:8000 --env-file .env deepseek-telegram-bot
```

### Docker Compose
```bash
docker-compose up --build
```

## 📊 API Endpoints

### Health Check
```
GET /health
```
پاسخ: `{"status": "healthy", "bot": "DeepSeek Telegram Bot", "version": "2.0.0"}`

### Root
```
GET /
```
معلومات کلی ربات

### Webhook
```
POST /webhook
```
دریافت آپدیت‌های تلگرام

### Statistics
```
GET /stats
```
معلومات آماری (تعداد کاربران فعال، پیام‌های کل)

## 🔐 امنیت

- API keys در فایل `.env` (غیرفعال در Git)
- HTTPS برای webhook
- Rate limiting برای API
- Exception handling برای تمام درخواست‌ها

## 🛠️ توسعه و ویرایش

### اضافه کردن دستور جدید

در `telegram_handlers.py`:
```python
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("پاسخ")
```

در `bot.py` یا `app.py`:
```python
application.add_handler(CommandHandler("mycommand", my_command))
```

### اضافه کردن Feature جدید

1. تعریف در `config.py`
2. پیاده‌سازی در ماژول مربوطه
3. استفاده در `telegram_handlers.py`

## 📚 مستندات بیشتر

- [Deployment Guide](DEPLOYMENT.md) - راهنمای deployment برای VPS/Render/Railway/Heroku
- [DeepSeek API Docs](https://platform.deepseek.com/api-docs)
- [python-telegram-bot Docs](https://python-telegram-bot.readthedocs.io/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

## 🐛 Troubleshooting

### خطای "Invalid bot token"
- بررسی کنید TELEGRAM_BOT_TOKEN صحیح است
- مطمئن شوید token از @BotFather دریافت کرده‌اید

### خطای "DeepSeek API error"
- بررسی کنید DEEPSEEK_API_KEY صحیح است
- اتصال اینترنت را بررسی کنید
- حد مجاز API را بررسی کنید

### خطای "Connection timeout"
- timeout را افزایش دهید
- اتصال VPN را بررسی کنید
- وضعیت سرور DeepSeek را بررسی کنید

## 📈 Performance Tips

- استفاده از webhook بجای polling برای production
- فعال کردن Redis برای caching
- محدود کردن MAX_HISTORY برای کاهش استفاده از حافظه
- استفاده از reasoning فقط برای مسائل پیچیده

## 📝 License

MIT License - آزادانه استفاده، اصلاح و توزیع کنید

## 🤝 مشارکت

پذیراندن PR و Issues از سایر توسعه‌دهندگان!

## 📞 ارتباط

- Issues: [GitHub Issues](https://github.com/hadedhamzad-tech/deepseek-telegram-bot/issues)
- Email: haded.hamzad@gmail.com

---

<div align="center">

**ساخته شده با ❤️ استفاده از DeepSeek API**

⭐ اگر پروژه برایت مفید بود، لطفاً ستاره بدهید!

</div>
