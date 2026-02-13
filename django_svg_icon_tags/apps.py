"""
Django App Configuration for SVG Icon Tags
"""
from django.apps import AppConfig


class SvgIconTagsConfig(AppConfig):
    """App configuration for django-svg-icon-tags"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_svg_icon_tags'
    verbose_name = 'SVG Icon Tags'
    
    def ready(self):
        """Initialize app when ready"""
        pass