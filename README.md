# Django SVG Icon Tags

[![PyPI version](https://badge.fury.io/py/django-svg-icon-tags.svg)](https://badge.fury.io/py/django-svg-icon-tags)
[![Python Version](https://img.shields.io/pypi/pyversions/django-svg-icon-tags.svg)](https://pypi.org/project/django-svg-icon-tags/)
[![Django Versions](https://img.shields.io/pypi/djversions/django-svg-icon-tags.svg)](https://pypi.org/project/django-svg-icon-tags/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)



---

## مقدمه

`django_svg_icon_tags` یک پکیج کامل و امن برای رندر کردن آیکون‌های SVG در پروژه‌های Django است که از چندین کتابخانه آیکون محبوب (Bootstrap Icons، Heroicons و آیکون‌های سفارشی) پشتیبانی می‌کند.

این پکیج با ارائه راه‌حلی ساده و قدرتمند، به شما امکان می‌دهد به راحتی آیکون‌های زیبا و تعاملی را در تمپلیت‌های Django خود استفاده کنید.

---

## ویژگی‌ها

✅ **پشتیبانی چندکتابخانه‌ای** - استفاده همزمان از کتابخانه‌های مختلف آیکون  
✅ **امنیت بالا** - محافظت در برابر حملات XSS و Path Traversal  
✅ **کش هوشمند** - بهینه‌سازی عملکرد با سیستم کشینگ پیشرفته  
✅ **دسترسی‌پذیری** - پشتیبانی کامل از ARIA labels و عنوان‌ها  
✅ **یکپارچه‌سازی Tailwind CSS** - پیش‌تنظیمات اندازه و رنگ آماده  
✅ **انیمیشن‌های داخلی** - چرخش، وارونه کردن، چرخش پیوسته و ضربان  
✅ **رندرینگ انعطاف‌پذیر** - پشتیبانی از رندرینگ داخلی و تگ `<img>`  
✅ **مستندات کامل** - مثال‌های عملی و راهنمایی جامع  

---


## نصب

### نصب با استفاده از pip

```bash

# نصب آخرین نسخه

pip install django-svg-icon-tags

# نصب مستقیم از گیت‌هاب

pip install git+https://github.com/reza-bayat/django-svg-icon-tags.git

# نصب با کلون مخزن

git clone https://github.com/reza-bayat/django-svg-icon-tags.git
cd django-svg-icon-tags
pip install -e .

```


## پیکربندی

### گام ۱: اضافه کردن به INSTALLED_APPS

```python

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
		
    # ... سایر اپ‌های شما
    'django_svg_icon_tags',  # ✅ اضافه کردن پکیج
]

```

### گام ۲: تنظیمات استاتیک
```python
# settings.py

# تنظیمات استاتیک (الزامی)

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# تنظیمات کش (اختیاری اما توصیه می‌شود)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "svg_icon_cache",
        "TIMEOUT": 60 * 60 * 24 * 30,  # 30 روز
    }
}

# تنظیمات زمان بازنشانی کش آیکون‌ها (اختیاری)

SVG_ICON_CACHE_TIMEOUT = 60 * 60 * 24 * 30  # 30 روز

# برای محیط تولید با ترافیک بالا - استفاده از Redis

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#         "TIMEOUT": 60 * 60 * 24 * 30,
#     }
# }
 
```

# جمع‌آوری فایل‌های استاتیک (برای محیط تولید)
```bash
python manage.py collectstatic
```


## لود کردن تگ‌ها در تمپلیت

```python

{% load svg_icon_tags %}

```


## سه روش استفاده
### روش ۱: تگ اصلی svg_icon (کامل‌ترین)

```python

{# آیکون پایه با کتابخانه مشخص #}
{% svg_icon "home" library="heroicons-solid" %}

{# با سینتکس کوتاه کتابخانه #}
{% svg_icon "bootstrap:arrow-up" %}

{# با کلاس‌های سفارشی #}
{% svg_icon "search" library="heroicons-outline" class_name="w-6 h-6 text-blue-500 hover:text-blue-700" %}

{# با ابعاد مشخص #}
{% svg_icon "logo" library="custom" width="120" height="40" fill="#3b82f6" %}

{# با دسترسی‌پذیری (ARIA label) #}
{% svg_icon "home" library="heroicons-solid" aria_label="صفحه اصلی" %}

{# با عنوان (تولتیپ) #}
{% svg_icon "info" library="heroicons-outline" title="اطلاعات بیشتر" %}

```


### روش ۲: تگ icon (ساده‌تر با پیش‌تنظیمات)

```python
{# آیکون با اندازه و رنگ پیش‌فرض #}
{% icon "home" library="heroicons-solid" %}

{# تغییر اندازه #}
{% icon "search" library="heroicons-outline" size="lg" %}
{% icon "settings" library="heroicons-outline" size="xl" %}

{# تغییر رنگ #}
{% icon "check" library="heroicons-solid" color="success" %}
{% icon "x" library="heroicons-solid" color="danger" %}
{% icon "info" library="heroicons-outline" color="info" %}

{# ترکیب اندازه و رنگ #}
{% icon "star" library="heroicons-solid" size="2xl" color="warning" %}
```


### روش ۳: فیلتر svg_icon_simple (سریع‌ترین)

```python
{# استفاده به صورت فیلتر #}
{{ "home"|svg_icon_simple }}
{{ "search"|svg_icon_simple }}
```

## مثال‌های ساده

```python
{# مثال ۱: آیکون ساده #}
{% load svg_icon_tags %}
{% svg_icon "home" library="heroicons-solid" %}

{# مثال ۲: آیکون با کلاس‌های Tailwind #}
{% svg_icon "search" library="heroicons-outline" class_name="w-6 h-6 text-gray-500 hover:text-gray-700" %}

{# مثال ۳: آیکون با ابعاد مشخص #}
{% svg_icon "logo" library="custom" width="120" height="40" %}

{# مثال ۴: آیکون با دسترسی‌پذیری #}
{% svg_icon "bell" library="heroicons-outline" aria_label="اعلان‌ها" %}

{# مثال ۵: آیکون با عنوان #}
{% svg_icon "question-mark-circle" library="heroicons-outline" title="راهنما" %}
```

## پارامترهای پیشرفته

### انیمیشن‌ها و تبدیل‌ها

```python
{# آیکون چرخان (برای لودینگ) #}
{% icon "arrow-path" library="heroicons-outline" spin=True size="lg" color="primary" %}

{# آیکون با ضربان #}
{% icon "exclamation-circle" library="heroicons-outline" pulse=True size="lg" color="warning" %}

{# آیکون چرخان 90 درجه #}
{% icon "arrow-up" library="heroicons-outline" rotate="90" size="sm" color="gray" %}

{# آیکون وارونه افقی #}
{% icon "arrow-left" library="heroicons-outline" flip="horizontal" size="sm" color="gray" %}

{# آیکون وارونه عمودی #}
{% icon "arrow-up" library="heroicons-outline" flip="vertical" size="sm" color="gray" %}

{# ترکیب چند افکت #}
{% icon "arrow-path" library="heroicons-outline" spin=True rotate="45" size="xl" color="brand-blue" %}
```

## رندرینگ به صورت <img> (برای کش مرورگر)

```python
{# آیکون به صورت تگ img #}
{% svg_icon "logo" library="custom" inline=False width="200" height="50" %}

{# با ویژگی‌های اضافه #}
{% svg_icon "avatar" library="custom" inline=False class_name="rounded-full" 
           extra_attrs={'loading': 'lazy', 'decoding': 'async'} %}

{# با alt text برای دسترسی‌پذیری #}
{% svg_icon "logo" library="custom" inline=False aria_label="لوگوی شرکت" %}
```

## پارامترهای کامل svg_icon
## پارامترهای کامل icon
## مپ‌های اندازه و رنگ

```python
# اندازه‌های پیش‌فرض (Tailwind CSS)
size_map = {
    'xs': 'w-3 h-3',    # 12px
    'sm': 'w-4 h-4',    # 16px
    'md': 'w-5 h-5',    # 20px
    'lg': 'w-6 h-6',    # 24px
    'xl': 'w-8 h-8',    # 32px
    '2xl': 'w-10 h-10', # 40px
    '3xl': 'w-12 h-12', # 48px
    '4xl': 'w-16 h-16', # 64px
}

# رنگ‌های پیش‌فرض (Tailwind CSS)
color_map = {
    'current': 'text-current',      # رنگ والد
    'primary': 'text-primary-600',  # آبی
    'secondary': 'text-secondary-600', # خاکستری
    'success': 'text-success-600',  # سبز
    'danger': 'text-danger-600',    # قرمز
    'warning': 'text-warning-600',  # نارنجی
    'info': 'text-info-600',        # آبی روشن
    'gray': 'text-gray-500',        # خاکستری
    'light': 'text-gray-400',       # خاکستری روشن
    'dark': 'text-gray-800',        # خاکستری تیره
    'brand-blue': 'text-blue-600',  # آبی برند
    'brand-green': 'text-green-600', # سبز برند
}
```

## مثال ۱: منوی ناوبری

```html
{% load svg_icon_tags %}

<nav class="bg-white shadow">
  <div class="max-w-7xl mx-auto px-4">
    <div class="flex justify-between h-16">
      <div class="flex">
        <div class="flex-shrink-0 flex items-center">
          {% svg_icon "logo" library="custom" width="120" height="40" %}
        </div>
        
        <div class="hidden md:ml-6 md:flex md:space-x-8">
          <a href="/" class="border-blue-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
            {% icon "home" library="heroicons-solid" size="sm" color="primary" %}
            <span class="mr-2">خانه</span>
          </a>
          
          <a href="/products" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
            {% icon "shopping-bag" library="heroicons-outline" size="sm" color="gray" %}
            <span class="mr-2">محصولات</span>
          </a>
          
          <a href="/blog" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
            {% icon "newspaper" library="heroicons-outline" size="sm" color="gray" %}
            <span class="mr-2">بلاگ</span>
          </a>
          
          <a href="/contact" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
            {% icon "chat-alt" library="heroicons-outline" size="sm" color="gray" %}
            <span class="mr-2">تماس</span>
          </a>
        </div>
      </div>
      
      <div class="flex items-center">
        <button class="bg-gray-100 p-2 rounded-full text-gray-400 hover:text-gray-500 mr-4">
          {% icon "search" library="heroicons-outline" size="lg" color="gray" %}
        </button>
        
        <div class="relative mr-4">
          <button class="bg-gray-100 p-2 rounded-full text-gray-400 hover:text-gray-500">
            {% icon "bell" library="heroicons-outline" size="lg" color="gray" %}
          </button>
          <span class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-500 ring-2 ring-white"></span>
        </div>
        
        <div class="relative">
          <button class="flex items-center max-w-xs bg-gray-100 rounded-full focus:outline-none">
            <span class="sr-only">باز کردن منوی کاربر</span>
            <img class="h-8 w-8 rounded-full" src="https://ui-avatars.com/api/?name=علی+رضایی&background=0D8ABC&color=fff" alt="علی رضایی">
          </button>
        </div>
      </div>
      
      <div class="-mr-2 flex md:hidden">
        <button class="bg-gray-100 inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-200">
          <span class="sr-only">باز کردن منوی اصلی</span>
          {% icon "menu" library="heroicons-outline" size="lg" color="gray" %}
        </button>
      </div>
    </div>
  </div>
</nav>
```

## مثال ۲: فرم ورود با آیکون‌ها

```html
{% load svg_icon_tags %}

<div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
  <div class="max-w-md w-full space-y-8">
    <div>
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        ورود به حساب کاربری
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        یا
        <a href="#" class="font-medium text-blue-600 hover:text-blue-500">
          ایجاد حساب جدید
        </a>
      </p>
    </div>
    
    <form class="mt-8 space-y-6" action="#" method="POST">
      <input type="hidden" name="remember" value="true">
      
      <div class="rounded-md shadow-sm -space-y-px">
        <div class="relative">
          <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
            {% icon "envelope" library="heroicons-outline" size="sm" color="gray" %}
          </div>
          <input id="email-address" name="email" type="email" autocomplete="email" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm text-left pr-10" placeholder="آدرس ایمیل">
        </div>
        
        <div class="relative">
          <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
            {% icon "lock-closed" library="heroicons-outline" size="sm" color="gray" %}
          </div>
          <input id="password" name="password" type="password" autocomplete="current-password" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm text-left pr-10" placeholder="رمز عبور">
        </div>
      </div>
      
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <input id="remember-me" name="remember-me" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
          <label for="remember-me" class="mr-2 block text-sm text-gray-900">
            مرا به خاطر بسپار
          </label>
        </div>
        
        <div class="text-sm">
          <a href="#" class="font-medium text-blue-600 hover:text-blue-500">
            رمز عبور خود را فراموش کرده‌اید؟
          </a>
        </div>
      </div>
      
      <div>
        <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
          <span class="absolute right-0 inset-y-0 flex items-center pr-3">
            {% icon "arrow-right" library="heroicons-outline" size="sm" color="white" class="opacity-0 group-hover:opacity-100 transition-opacity" %}
          </span>
          ورود به سیستم
        </button>
      </div>
    </form>
    
    <div class="mt-6">
      <div class="relative">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-300"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-2 bg-gray-50 text-gray-500">یا ورود با</span>
        </div>
      </div>
      
      <div class="mt-6 grid grid-cols-2 gap-3">
        <button class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
          {% svg_icon "google" library="bootstrap" class_name="w-5 h-5 ml-2" %}
          Google
        </button>
        
        <button class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
          {% svg_icon "github" library="bootstrap" class_name="w-5 h-5 ml-2" %}
          GitHub
        </button>
      </div>
    </div>
  </div>
</div>
```


## مثال ۳: کارت محصول

```html
{% load svg_icon_tags %}

<div class="max-w-sm bg-white rounded-lg shadow-md overflow-hidden transition-transform hover:scale-105">
  <div class="h-48 bg-gray-200 flex items-center justify-center">
    <span class="text-gray-500">تصویر محصول</span>
  </div>
  
  <div class="p-4">
    <div class="flex justify-between items-start">
      <div>
        <h3 class="text-lg font-medium text-gray-900">لپ‌تاپ گیمینگ</h3>
        <p class="mt-1 text-sm text-gray-500">پردازنده Intel i7، 16GB RAM، RTX 3060</p>
      </div>
      <button class="text-gray-400 hover:text-red-500 transition-colors" aria-label="افزودن به علاقه‌مندی‌ها">
        {% icon "heart" library="heroicons-outline" size="lg" color="gray" %}
      </button>
    </div>
    
    <div class="mt-3 flex items-baseline">
      <span class="text-2xl font-bold text-gray-900">۲۵,۰۰۰,۰۰۰</span>
      <span class="mr-1 text-gray-600">تومان</span>
      
      <div class="flex items-center mr-4 text-yellow-400">
        {% icon "star" library="heroicons-solid" size="xs" color="warning" %}
        <span class="mr-1 text-sm text-gray-600">4.8</span>
        <span class="text-xs text-gray-500">(124)</span>
      </div>
    </div>
    
    <div class="mt-4 flex space-x-2 space-x-reverse">
      <button class="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md flex items-center justify-center transition-colors">
        {% icon "cart-plus" library="bootstrap" size="sm" color="white" class="ml-2" %}
        افزودن به سبد
      </button>
      
      <button class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md flex items-center justify-center transition-colors" aria-label="مشاهده جزئیات">
        {% icon "eye" library="heroicons-outline" size="sm" color="gray" %}
      </button>
    </div>
    
    <div class="mt-4 flex flex-wrap gap-2">
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
        {% icon "truck" library="bootstrap" size="xs" color="success" class="ml-1" %}
        ارسال رایگان
      </span>
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
        {% icon "shield-check" library="heroicons-outline" size="xs" color="brand-blue" class="ml-1" %}
        گارانتی 18 ماهه
      </span>
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
        {% icon "clock" library="heroicons-outline" size="xs" color="purple" class="ml-1" %}
        موجود در انبار
      </span>
    </div>
  </div>
</div>
```

## مثال ۴: استفاده در حلقه‌ها
```html
{% load svg_icon_tags %}

<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
  {% for category in categories %}
    <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div class="flex items-center mb-4">
        {% icon category.icon_name library="heroicons-outline" size="2xl" color="primary" %}
        <h3 class="text-xl font-bold mr-3">{{ category.name }}</h3>
      </div>
      <p class="text-gray-600">{{ category.description }}</p>
      <a href="{{ category.get_absolute_url }}" class="mt-4 inline-flex items-center text-blue-600 hover:text-blue-800">
        مشاهده محصولات
        {% icon "arrow-right" library="heroicons-outline" size="sm" color="blue" class="mr-2" %}
      </a>
    </div>
  {% endfor %}
</div>
```


## مثال ۵: استفاده با شرایط

```html
{% load svg_icon_tags %}

<div class="flex items-center">
  {% if user.is_authenticated %}
    <span class="text-green-600 font-medium">
      {% icon "check-circle" library="heroicons-solid" size="sm" color="success" class="ml-1" %}
      وارد شده‌اید
    </span>
  {% else %}
    <span class="text-red-600 font-medium">
      {% icon "x-circle" library="heroicons-solid" size="sm" color="danger" class="ml-1" %}
      وارد نشده‌اید
    </span>
  {% endif %}
</div>

<div class="mt-4">
  {% if product.in_stock %}
    <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
      {% icon "check" library="heroicons-solid" size="xs" color="success" class="ml-1" %}
      موجود در انبار
    </span>
  {% else %}
    <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800">
      {% icon "x" library="heroicons-solid" size="xs" color="danger" class="ml-1" %}
      ناموجود
    </span>
  {% endif %}
</div>
```


## مثال ۶: دکمه‌های اکشن با انیمیشن
```html
{% load svg_icon_tags %}

<div class="flex space-x-4 space-x-reverse">
  {# دکمه لودینگ #}
  <button class="btn btn-primary" disabled>
    {% icon "arrow-path" library="heroicons-outline" spin=True size="sm" color="white" %}
    در حال بارگذاری...
  </button>
  
  {# دکمه موفقیت #}
  <button class="btn btn-success">
    {% icon "check-circle" library="heroicons-solid" size="sm" color="white" %}
    تأیید
  </button>
  
  {# دکمه خطا #}
  <button class="btn btn-danger">
    {% icon "x-circle" library="heroicons-solid" size="sm" color="white" %}
    لغو
  </button>
  
  {# دکمه هشدار #}
  <button class="btn btn-warning">
    {% icon "exclamation-triangle" library="heroicons-solid" size="sm" color="white" pulse=True %}
    هشدار
  </button>
</div>
```


## مثال ۷: لیست انتخاب‌ها با آیکون

```html
{% load svg_icon_tags %}

<div class="space-y-2">
  {% for item in items %}
    <label class="flex items-center p-3 bg-white rounded-lg border hover:border-blue-500 cursor-pointer">
      <input type="radio" name="option" value="{{ item.id }}" class="form-radio h-5 w-5 text-blue-600">
      <span class="mr-3">
        {% if item.icon %}
          {% icon item.icon library="heroicons-outline" size="lg" color="gray" %}
        {% else %}
          {% icon "document" library="heroicons-outline" size="lg" color="gray" %}
        {% endif %}
      </span>
      <div>
        <div class="font-medium text-gray-900">{{ item.title }}</div>
        <div class="text-sm text-gray-600">{{ item.description }}</div>
      </div>
    </label>
  {% endfor %}
</div>
```

## مثال ۸: داشبورد مدیریت
```html
{% load svg_icon_tags %}

<div class="min-h-screen bg-gray-50">
  <header class="bg-white shadow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">پیشخوان مدیریت</h1>
      
      <div class="flex items-center space-x-4 space-x-reverse">
        <button class="p-2 text-gray-400 hover:text-gray-500 rounded-full bg-gray-100">
          {% icon "bell" library="heroicons-outline" size="lg" color="gray" %}
        </button>
        
        <div class="relative">
          <button class="flex items-center max-w-xs bg-gray-100 rounded-full focus:outline-none">
            <img class="h-8 w-8 rounded-full" src="https://ui-avatars.com/api/?name=مدیر+سیستم&background=0D8ABC&color=fff" alt="مدیر سیستم">
          </button>
        </div>
      </div>
    </div>
  </header>
  
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              {% icon "cash" library="heroicons-outline" size="2xl" color="primary" %}
            </div>
            <div class="mr-5">
              <p class="text-sm font-medium text-gray-500 truncate">فروش امروز</p>
              <p class="mt-1 text-3xl font-semibold text-gray-900">۱۲۷,۵۰۰,۰۰۰</p>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-5 py-3">
          <div class="text-sm">
            <span class="text-green-500 font-medium">↑ 12.5%</span>
            <span class="text-gray-500 mr-1">نسبت به دیروز</span>
          </div>
        </div>
      </div>
      
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              {% icon "shopping-cart" library="heroicons-outline" size="2xl" color="success" %}
            </div>
            <div class="mr-5">
              <p class="text-sm font-medium text-gray-500 truncate">سفارشات جدید</p>
              <p class="mt-1 text-3xl font-semibold text-gray-900">42</p>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-5 py-3">
          <div class="text-sm">
            <span class="text-green-500 font-medium">↑ 8%</span>
            <span class="text-gray-500 mr-1">نسبت به هفته گذشته</span>
          </div>
        </div>
      </div>
      
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              {% icon "user-group" library="heroicons-outline" size="2xl" color="warning" %}
            </div>
            <div class="mr-5">
              <p class="text-sm font-medium text-gray-500 truncate">مشتریان جدید</p>
              <p class="mt-1 text-3xl font-semibold text-gray-900">18</p>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-5 py-3">
          <div class="text-sm">
            <span class="text-red-500 font-medium">↓ 3%</span>
            <span class="text-gray-500 mr-1">نسبت به ماه گذشته</span>
          </div>
        </div>
      </div>
      
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              {% icon "eye" library="heroicons-outline" size="2xl" color="info" %}
            </div>
            <div class="mr-5">
              <p class="text-sm font-medium text-gray-500 truncate">بازدیدها</p>
              <p class="mt-1 text-3xl font-semibold text-gray-900">3,245</p>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-5 py-3">
          <div class="text-sm">
            <span class="text-green-500 font-medium">↑ 24%</span>
            <span class="text-gray-500 mr-1">نسبت به روز گذشته</span>
          </div>
        </div>
      </div>
    </div>
  </main>
</div>
```


## مشکل: آیکون نمایش داده نمی‌شود (خالی است)

```python
# بررسی تنظیمات استاتیک
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# تست دستی آدرس آیکون
curl http://localhost:8000/static/icons/bootstrap/home.svg

# بررسی کنسول مرورگر برای خطاهای 404
```


## مشکل: کش قدیمی آیکون‌ها

```python
# پاک کردن کش در کنسول Django
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()  # پاک کردن تمام کش

# یا فقط کش آیکون‌ها
>>> cache.delete_pattern('svg_icon:*')
```

## مشکل: آیکون‌ها در محیط تولید نمایش داده نمی‌شوند

```bash
# جمع‌آوری فایل‌های استاتیک
python manage.py collectstatic --clear

# بررسی دسترسی‌ها
chmod -R 755 static/

# بررسی تنظیمات Nginx/Apache
# مطمئن شوید فایل‌های استاتیک سرو می‌شوند
```


