"""
Django SVG Icon Template Tags
==============================

A secure and flexible Django template tag library for rendering SVG icons
from multiple icon libraries (Bootstrap Icons, Heroicons, etc.)

Features:
- ✅ Multi-library support
- ✅ Security hardening (XSS protection, path traversal prevention)
- ✅ Performance optimization (caching)
- ✅ Accessibility (ARIA labels, titles)
- ✅ Tailwind CSS friendly
- ✅ Comprehensive error handling

Quick Start:
    pip install django-svg-icon-tags
    
    # In settings.py
    INSTALLED_APPS = [
        ...,
        'django_svg_icon_tags',
    ]
    
    # In template
    {% load svg_icon_tags %}
    {% svg_icon "home" library="heroicons-solid" %}
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__license__ = "MIT"