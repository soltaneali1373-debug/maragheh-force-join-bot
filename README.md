# ربات Force Join مراغه آنلاین

این نسخه یک ربات اختصاصی ساده برای Force Join است.

## امکانات
- بررسی عضویت کاربر در `@MaraghehOnline_Com`
- دکمه عضویت در کانال
- دکمه «عضو شدم»
- بررسی مجدد عضویت با Bot API
- پیام خوش‌آمدگویی فارسی
- آماده اجرا روی VPS/سرور یا Docker

## نکته مهم
ربات را باید در کانال `@MaraghehOnline_Com` به عنوان Administrator اضافه کنید تا بتواند عضویت کاربران دیگر را با `getChatMember` بررسی کند.

## راه‌اندازی
1. در @BotFather یک ربات بسازید و توکن بگیرید.
2. ربات را در کانال مراغه آنلاین به عنوان ادمین اضافه کنید.
3. فایل `.env.example` را به `.env` تبدیل کنید و `BOT_TOKEN` را وارد کنید.
4. نصب:
   ```bash
   pip install -r requirements.txt
   ```
5. اجرا:
   ```bash
   python bot.py
   ```

## اجرای Docker
```bash
docker build -t maragheh-force-join .
docker run -d --restart unless-stopped   -e BOT_TOKEN="توکن_ربات"   -e CHANNEL="@MaraghehOnline_Com"   -e CHANNEL_URL="https://t.me/MaraghehOnline_Com"   maragheh-force-join
```

توکن را داخل فایل یا چت عمومی منتشر نکنید.
