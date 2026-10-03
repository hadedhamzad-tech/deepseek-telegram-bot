# 🚀 راهنمای Deployment

راهنمای جامع برای deploy کردن ربات بر روی سرورهای مختلف.

## 📋 فهرست

1. [Heroku](#heroku)
2. [Railway](#railway)
3. [Render](#render)
4. [DigitalOcean](#digitalocean)
5. [VPS ایرانی](#vps-ایرانی)
6. [Docker](#docker)

---

## ☁️ Heroku

### پیش‌نیاز‌ها
- Heroku CLI
- حساب Heroku

### مراحل

1. **Login**
```bash
heroku login
```

2. **ایجاد اپلیکیشن**
```bash
heroku create your-bot-name
```

3. **تنظیم متغیرهای محیطی**
```bash
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set DEEPSEEK_API_KEY=your_key
heroku config:set WEBHOOK_URL=https://your-bot-name.herokuapp.com/webhook
heroku config:set LOG_LEVEL=INFO
```

4. **Deploy**
```bash
git push heroku main
```

5. **مشاهده لاگ‌ها**
```bash
heroku logs --tail
```

---

## 🚂 Railway

### مراحل

1. به [railway.app](https://railway.app) بروید
2. **New Project** → **Deploy from GitHub repo**
3. Repository خود را انتخاب کنید
4. تنظیم متغیرهای محیطی در بخش **Variables**
5. Deploy خودکار انجام می‌شود

### Environment Variables
```
TELEGRAM_BOT_TOKEN=your_token
DEEPSEEK_API_KEY=your_key
WEBHOOK_URL=https://your-app.railway.app/webhook
PORT=8000
```

---

## 🎨 Render

### مراحل

1. به [render.com](https://render.com) بروید
2. **New +** → **Web Service**
3. GitHub repo متصل کنید
4. تنظیمات:
   - **Name**: your-bot-name
   - **Runtime**: Python 3.9
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `python -m uvicorn app:app --host 0.0.0.0 --port $PORT`
5. تنظیم Environment Variables

---

## 💧 DigitalOcean

### ایجاد Droplet

1. ایجاد Ubuntu 22.04 Droplet
2. SSH به سرور

### نصب و تنظیم

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.9 python3-pip git nginx

# Clone repository
git clone https://github.com/hadedhamzad-tech/deepseek-telegram-bot.git
cd deepseek-telegram-bot

# Virtual environment
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env
cp .env.example .env
# Edit .env with your credentials
```

### Systemd Service

فایل `/etc/systemd/system/deepseek-bot.service`:

```ini
[Unit]
Description=DeepSeek Telegram Bot
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/ubuntu/deepseek-telegram-bot
Environment="PATH=/home/ubuntu/deepseek-telegram-bot/venv/bin"
ExecStart=/home/ubuntu/deepseek-telegram-bot/venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 8000
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

### Nginx Reverse Proxy

فایل `/etc/nginx/sites-available/deepseek-bot`:

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

### SSL (Let's Encrypt)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

آپدیت Nginx config برای HTTPS

---

## 🖥️ VPS ایرانی

### نصب Python 3.9

```bash
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.9 python3.9-venv python3.9-dev
```

### نصب و راه‌اندازی

```bash
cd /opt
sudo git clone https://github.com/hadedhamzad-tech/deepseek-telegram-bot.git
cd deepseek-telegram-bot

sudo python3.9 -m venv venv
sudo source venv/bin/activate
sudo pip install -r requirements.txt

sudo cp .env.example .env
# Edit .env
```

### تنظیم Supervisor

فایل `/etc/supervisor/conf.d/deepseek-bot.conf`:

```ini
[program:deepseek-bot]
directory=/opt/deepseek-telegram-bot
command=/opt/deepseek-telegram-bot/venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 8000
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=10
stdout_logfile=/var/log/deepseek-bot.log
stderr_logfile=/var/log/deepseek-bot.err
```

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start deepseek-bot
```

---

## 🐳 Docker

### Build

```bash
docker build -t deepseek-telegram-bot .
```

### اجرا

```bash
docker run -p 8000:8000 \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e DEEPSEEK_API_KEY=your_key \
  -e WEBHOOK_URL=https://your-domain.com/webhook \
  deepseek-telegram-bot
```

### Docker Compose

```bash
docker-compose up -d
docker-compose logs -f
```

---

## 🔒 SSL/TLS با Nginx

### تنظیم SSL

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 📊 Monitoring

### بررسی وضعیت

```bash
curl https://your-domain.com/health
curl https://your-domain.com/stats
```

### مشاهده لاگ‌ها

```bash
# Docker
docker logs deepseek-telegram-bot -f

# Systemd
sudo journalctl -u deepseek-bot -f

# File
tail -f logs/bot.log
```

---

## 🔄 Backup و Restore

### Backup

```bash
tar -czf deepseek-bot-backup.tar.gz logs/ .env
```

### Restore

```bash
tar -xzf deepseek-bot-backup.tar.gz
```

---

## ⚡ Performance Tips

1. استفاده از webhook بجای polling
2. Redis برای caching
3. Load balancing برای traffic زیاد
4. CDN برای static files
5. Monitoring و alerting

---

## 🛠️ Troubleshooting

### خطای 502 Bad Gateway
- بررسی Nginx configuration
- مطمئن شوید app در حال اجرا است
- لاگ‌ها را بررسی کنید

### خطای Webhook
- مطمئن شوید HTTPS است
- URL صحیح است
- SSL certificate valid است

### High Memory Usage
- MAX_HISTORY را کاهش دهید
- Context expire timeout را کاهش دهید
- Redis برای caching استفاده کنید

---

**آپدیت شده: اکتبر 2024**
