<div dir="rtl">

# Django Mini Library

یک پروژه ساده مدیریت کتابخانه با Django. امکان ثبت و مدیریت کتاب، نویسنده، ناشر و دسته‌بندی را دارد و کاربران می‌توانند ثبت‌نام کنند و کتاب‌ها را به علاقه‌مندی‌هایشان اضافه کنند.

## امکانات

- افزودن، ویرایش، حذف و مشاهده جزئیات کتاب
- حذف گروهی کتاب‌های فیلترشده
- مدیریت نویسندگان، ناشران و دسته‌بندی‌ها
- افزودن سریع نویسنده، ناشر یا دسته‌بندی هنگام ثبت کتاب
- ثبت‌نام، ورود، خروج و تغییر رمز عبور
- لیست علاقه‌مندی‌ها برای هر کاربر
- پنل ادمین Django
- دستور `dummy_data` برای ساخت داده نمونه

## ساختار پروژه

- `library/` : تنظیمات پروژه (settings و urls)
- `books/` : مدل‌ها، ویوها و تمپلیت‌های کتاب‌ها
- `books/management/commands/dummy_data.py` : دستور ساخت داده نمونه
- `accounts/` : ثبت‌نام، ورود و تغییر رمز
- `templates/` : تمپلیت پایه
- `statics/` : فایل‌های CSS
- `ERD.png` : نمودار دیتابیس

## نصب و اجرا

نیازمندی: Python نسخه 3.10 یا بالاتر

**۱. کلون کردن پروژه**

</div>

```bash
git clone <repo-url>
cd django_mini_library
```

<div dir="rtl">

**۲. ساخت و فعال‌سازی محیط مجازی**

</div>

```bash
python -m venv venv
```

<div dir="rtl">

فعال‌سازی در Linux و macOS:

</div>

```bash
source venv/bin/activate
```

<div dir="rtl">

فعال‌سازی در Windows:

</div>

```bash
venv\Scripts\activate
```

<div dir="rtl">

**۳. نصب وابستگی‌ها**

</div>

```bash
pip install -r requirements.txt
```

<div dir="rtl">

**۴. ساخت دیتابیس**

</div>

```bash
python manage.py migrate
```

<div dir="rtl">

**۵. ساخت کاربر ادمین (اختیاری)**

</div>

```bash
python manage.py createsuperuser
```

<div dir="rtl">

**۶. اجرای سرور**

</div>

```bash
python manage.py runserver
```

<div dir="rtl">

سایت روی `http://127.0.0.1:8000/` و پنل ادمین روی `http://127.0.0.1:8000/admin/` در دسترس است.

## ساخت داده نمونه (dummy_data)

برای دیدن سایت با داده تستی از دستور زیر استفاده کنید. این دستور با کتابخانه [Faker](https://faker.readthedocs.io/) و زبان فارسی (`fa_IR`) داده می‌سازد.

</div>

```bash
python manage.py dummy_data
```

<div dir="rtl">

به‌صورت پیش‌فرض این موارد ساخته می‌شود:

| مورد | تعداد |
|------|-------|
| کتاب | ۵۰ |
| نویسنده | ۱۰ |
| ناشر | ۱۰ |
| دسته‌بندی | ۸ |

هر کتاب به‌طور تصادفی نویسنده، ناشر، دسته‌بندی، زبان، قیمت (۵۰ هزار تا ۵۰۰ هزار تومان)، تعداد صفحات (۵۰ تا ۱۰۰۰)، تاریخ انتشار و شابک یکتا می‌گیرد.

### گزینه‌ها

| گزینه | توضیح | پیش‌فرض |
|-------|-------|---------|
| `--books N` | تعداد کتاب‌هایی که ساخته شود | `50` |
| `--clear` | قبل از ساخت، همه داده‌های قبلی (کتاب، نویسنده، ناشر، دسته‌بندی و علاقه‌مندی‌ها) پاک شود | غیرفعال |

### مثال‌ها

ساخت ۲۰۰ کتاب:

</div>

```bash
python manage.py dummy_data --books 200
```

<div dir="rtl">

پاک کردن داده‌های قبلی و ساخت ۱۰۰ کتاب جدید:

</div>

```bash
python manage.py dummy_data --clear --books 100
```

<div dir="rtl">

> **توجه:** گزینه `clear--` همه کتاب‌ها، نویسندگان، ناشران، دسته‌بندی‌ها و علاقه‌مندی‌ها را پاک می‌کند. کاربران پاک نمی‌شوند. اگر دیتابیس واقعی دارید با دقت استفاده کنید.

## اجرای تست‌ها

</div>

```bash
python manage.py test
```

<div dir="rtl">

## نکات مربوط به Migration

فایل‌های `books/migrations/` باید داخل گیت commit شوند. بعد از هر تغییر در `models.py` (حتی تغییر `verbose_name` یا `ordering`) این دستورات را بزنید و فایل جدید را commit کنید:

</div>

```bash
python manage.py makemigrations
python manage.py migrate
```

<div dir="rtl">

برای اطمینان از هماهنگی مدل‌ها و migrationها:

</div>

```bash
python manage.py makemigrations --check --dry-run
```

<div dir="rtl">

## تکنولوژی‌ها

- Python و Django 5
- SQLite
- Faker (برای داده نمونه)

</div>