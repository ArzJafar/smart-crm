# Smart CRM System

یک سیستم مدیریت هوشمند با رابط کاربری مدرن و قابلیت‌های پیشرفته

## ویژگی‌ها

- مدیریت مخاطبین
- مدیریت منابع انسانی
- چت جی‌پی‌تی
- مدیریت فایل‌های تولید
- رابط کاربری مدرن و زیبا
- پشتیبانی از فونت وزیر
- طراحی واکنش‌گرا

## پیش‌نیازها

- Node.js (v14 یا بالاتر)
- Python (v3.8 یا بالاتر)
- npm یا yarn

## نصب و راه‌اندازی

### فرانت‌اند

```bash
cd frontend
npm install
npm start
```

### بک‌اند

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # در ویندوز: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

## ساختار پروژه

```
smart-crm/
├── frontend/          # اپلیکیشن React
├── backend/           # سرور Django
├── static/            # فایل‌های استاتیک
│   ├── fonts/        # فونت‌ها
│   ├── images/       # تصاویر
│   └── css/          # استایل‌ها
└── docs/             # مستندات
```

## API Endpoints

- `/api/contacts` - مدیریت مخاطبین
- `/api/hr` - مدیریت منابع انسانی
- `/api/chatgpt` - چت جی‌پی‌تی
- `/api/production-files` - مدیریت فایل‌ها

## مجوز

این پروژه تحت مجوز MIT منتشر شده است.