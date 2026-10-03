# 🚀 راهنمای배포

راهنمای جامع برای배포ربات در محیط‌های مختلف

## 📋 فهرست

- [Heroku](#heroku)
- [Railway](#railway)
- [Render](#render)
- [DigitalOcean](#digitalocean)
- [AWS](#aws)
- [Docker Compose](#docker-compose)

---

## ☁️ Heroku

### 1. نصب Heroku CLI
```bash
curl https://cli.heroku.com/install.sh | sh
heroku login
```

### 2. ایجاد اپلیکیشن
```bash
heroku create your-bot-name
```

### 3. تنظیم متغیرهای محیطی
```bash
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set DEEPSEEK_API_KEY=your_key
heroku config:set WEBHOOK_URL=https://your-bot-name.herokuapp.com/webhook
heroku config:set LOG_LEVEL=INFO
```

### 4. Deploy
```bash
git push heroku main
```

### 5. مشاهده لاگ‌ها
```bash
heroku logs --tail
```

---

## 🚂 Railway

### 1. اتصال Repository
- به [railway.app](https://railway.app) بروید
- **New Project** → **Deploy from GitHub repo**
- Repository خود را انتخاب کنید

### 2. تنظیم Environment Variables
در بخش Variables:
```
TELEGRAM_BOT_TOKEN=your_token
DEEPSEEK_API_KEY=your_key
WEBHOOK_URL=https://your-app.railway.app/webhook
```

### 3. Deploy
- Railway خودکار deploy می‌کند

---

## 🎨 Render

### 1. ایجاد New Web Service
- [render.com](https://render.com) → **New +** → **Web Service**
- GitHub repo متصل کنید

### 2. تنظیمات
- **Name**: your-bot-name
- **Runtime**: Python 3.9
- **Build**: `pip install -r requirements.txt`
- **Start**: `python -m uvicorn app:app --host 0.0.0.0`

### 3. Environment Variables
```
TELEGRAM_BOT_TOKEN=your_token
DEEPSEEK_API_KEY=your_key
WEBHOOK_URL=https://your-bot-name.onrender.com/webhook
```

---

## 💧 DigitalOcean

### 1. ایجاد Droplet
```bash
# SSH به droplet
ssh root@your_droplet_ip

# Update system
apt update && apt upgrade -y

# نصب Python و Git
apt install -y python3.9 python3-pip git

# Clone repository
git clone https://github.com/hadedhamzad-tech/deepseek-telegram-bot.git
cd deepseek-telegram-bot

# Virtual environment
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. تنظیم .env
```bash
cp .env.example .env
nano .env
# ویرایش و save کنید
```

### 3. Systemd Service
```bash
sudo nano /etc/systemd/system/deepseek-bot.service
```

```ini
[Unit]
Description=DeepSeek Telegram Bot
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/root/deepseek-telegram-bot
Environment="PATH=/root/deepseek-telegram-bot/venv/bin"
ExecStart=/root/deepseek-telegram-bot/venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable deepseek-bot
sudo systemctl start deepseek-bot
sudo systemctl status deepseek-bot
```

### 4. Nginx Reverse Proxy
```bash
sudo apt install -y nginx
sudo nano /etc/nginx/sites-available/deepseek-bot
```

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/deepseek-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL (Let's Encrypt)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

---

## ☁️ AWS

### با EC2

```bash
# SSH به instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install
sudo yum update -y
sudo yum install python39 -y
git clone https://github.com/hadedhamzad-tech/deepseek-telegram-bot.git
cd deepseek-telegram-bot
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### با ECS + Fargate

1. Create ECR Repository
2. Push Docker image
3. Create ECS Task Definition
4. Create Service
5. Set ALB

---

## 🐳 Docker Compose

### بر روی VPS

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Clone repository
git clone https://github.com/hadedhamzad-tech/deepseek-telegram-bot.git
cd deepseek-telegram-bot

# تنظیم .env
cp .env.example .env
nano .env

# Start services
docker-compose up -d

# لاگ‌ها
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔒 بهترین‌ practices

### 1. Environment Variables
- ❌ هرگز tokens را در کد hardcode نکنید
- ✅ از `.env` استفاده کنید
- ✅ `.env` را در `.gitignore` بگذارید

### 2. Monitoring
```bash
# Health check
curl https://your-domain.com/health

# Stats
curl https://your-domain.com/stats
```

### 3. Logging
```bash
# بررسی لاگ‌ها
docker-compose logs -f bot
tail -f logs/bot.log
```

### 4. SSL/TLS
- ✅ همیشه HTTPS استفاده کنید
- ✅ مطمئن شوید WEBHOOK_URL با HTTPS شروع می‌شود
- ✅ SSL certificate را آپدیت نگه دارید

### 5. Rate Limiting
- محدود کنید requests به DeepSeek API
- استفاده کنید rate limiting middleware
- Handle کنید API errors gracefully

---

## 🐛 Troubleshooting

### Bot not responding
```bash
# بررسی service status
systemctl status deepseek-bot

# لاگ‌ها
journalctl -u deepseek-bot -n 50

# Restart
systemctl restart deepseek-bot
```

### Webhook issues
```bash
# بررسی webhook
curl -X POST https://your-domain.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"update_id": 1}'
```

### API errors
```bash
# بررسی DeepSeek API status
curl -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  https://api.deepseek.com/v1/models
```

---

## 📊 Monitoring و Analytics

### با Sentry (Error Tracking)
```bash
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

### با Prometheus (Metrics)
```bash
pip install prometheus-client
```

---

## 🔄 Auto-Updates

برای بروزرسانی خودکار:

```bash
# Setup cron job
crontab -e

# اضافه کنید:
0 2 * * 0 cd /root/deepseek-telegram-bot && git pull && systemctl restart deepseek-bot
```

---

**آماده است! 🎉**

سوالی دارید؟ Issue بسازید یا تماس بگیرید.
