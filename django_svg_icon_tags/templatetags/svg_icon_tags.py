"""
Django Template Tags for SVG Icons
===================================

A secure and flexible template tag library for rendering SVG icons
from multiple icon libraries.

Author: Your Name
Version: 1.0.0
License: MIT
"""
import re
import logging
from functools import lru_cache
from pathlib import Path
from typing import Optional, Dict, Any

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.cache import cache as django_cache
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()
logger = logging.getLogger(__name__)

# ============================================================================
# Security Patterns - Prevent XSS and Path Traversal
# ============================================================================

_ICON_NAME_PATTERN = re.compile(r'^[\w\-\.]+$')
_LIBRARY_PATTERN = re.compile(r'^[a-z0-9\-_]+$')
_XML_DECLARATION_PATTERN = re.compile(r'^<\?xml[^>]*\?>\s*')
_SCRIPT_TAG_PATTERN = re.compile(
    r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>',
    re.IGNORECASE | re.DOTALL
)
_EVENT_HANDLER_PATTERN = re.compile(r'on\w+\s*=', re.IGNORECASE)

_FALLBACK_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<circle cx="12" cy="12" r="10"></circle>
<line x1="12" y1="8" x2="12" y2="12"></line>
<line x1="12" y1="16" x2="12.01" y2="16"></line>
</svg>'''

_USE_DJANGO_CACHE = not settings.DEBUG
_CACHE_TIMEOUT = getattr(settings, 'SVG_ICON_CACHE_TIMEOUT', 60 * 60 * 24 * 30)


def _sanitize_svg_content(content: str) -> str:
    """Basic SVG sanitization for defense-in-depth."""
    content = _XML_DECLARATION_PATTERN.sub('', content)
    content = _SCRIPT_TAG_PATTERN.sub('', content)
    content = _EVENT_HANDLER_PATTERN.sub('', content)
    return content.strip()


@lru_cache(maxsize=256)
def _get_cached_svg_content(filepath: str, mtime: float) -> Optional[str]:
    """Read and sanitize SVG content with LRU caching."""
    try:
        path = Path(filepath)
        if not path.exists() or not path.is_file():
            logger.warning(f"SVG file not found: {filepath}")
            return None
        
        content = path.read_text(encoding='utf-8').strip()
        
        if not content.startswith('<svg') and 'xmlns="http://www.w3.org/2000/svg"' not in content:
            logger.warning(f"Invalid SVG structure: {filepath}")
            return None
        
        return _sanitize_svg_content(content)
    
    except (OSError, UnicodeDecodeError) as e:
        logger.error(f"Failed to read SVG file {filepath}: {e}")
        return None


def _find_icon_path(name: str, library: Optional[str] = None) -> Optional[str]:
    """Locate icon file with library support."""
    if library:
        if not _LIBRARY_PATTERN.match(library):
            logger.warning(f"Invalid library name: {library}")
            return None
        search_path = f"icons/{library}/{name}.svg"
    else:
        search_path = f"icons/{name}.svg"
    
    if not _ICON_NAME_PATTERN.match(name):
        logger.warning(f"Invalid icon name: {name}")
        return None
    
    found = finders.find(search_path)
    if found:
        return found
    
    if settings.STATICFILES_DIRS:
        for static_dir in settings.STATICFILES_DIRS:
            full_path = Path(static_dir) / search_path
            if full_path.exists() and full_path.is_file():
                return str(full_path)
    
    return None


def _render_as_img(
    name: str,
    library: Optional[str],
    class_name: str,
    aria_label: Optional[str],
    title: Optional[str],
    width: Optional[str],
    height: Optional[str],
    extra_attrs: Optional[Dict[str, Any]]
) -> str:
    """Render icon as <img> tag."""
    from django.templatetags.static import static
    
    path_parts = ["icons"]
    if library:
        path_parts.append(library)
    path_parts.append(f"{name}.svg")
    static_url = static("/".join(path_parts))
    
    attrs = {
        'src': static_url,
        'alt': aria_label or title or '',
        'class': class_name.strip() if class_name else None,
        'width': width,
        'height': height,
        'aria-hidden': 'true' if not (aria_label or title) else None,
    }
    
    SAFE_ATTRS = {'loading', 'decoding', 'fetchpriority', 'style'}
    if extra_attrs:
        for key, val in extra_attrs.items():
            if key.startswith('data-') or key in SAFE_ATTRS:
                if val is not None:
                    attrs[key] = str(val)
    
    attr_str = ' '.join(
        f'{k}="{escape(str(v))}"' 
        for k, v in attrs.items() 
        if v is not None and v != ''
    )
    
    return mark_safe(f'<img {attr_str}>')


def _process_inline_svg(
    svg_content: str,
    class_name: str,
    aria_label: Optional[str],
    title: Optional[str],
    width: Optional[str],
    height: Optional[str],
    fill: Optional[str],
    stroke: Optional[str],
    extra_attrs: Optional[Dict[str, Any]]
) -> str:
    """Inject attributes into SVG with escaping."""
    inject_attrs = {}
    
    if class_name:
        inject_attrs['class'] = class_name.strip()
    if width:
        inject_attrs['width'] = str(width)
    if height:
        inject_attrs['height'] = str(height)
    if fill:
        inject_attrs['fill'] = fill
    if stroke:
        inject_attrs['stroke'] = stroke
    
    if aria_label:
        inject_attrs['aria-label'] = aria_label
        inject_attrs['role'] = 'img'
        inject_attrs['focusable'] = 'false'
    
    SAFE_SVG_ATTRS = {
        'viewBox', 'preserveAspectRatio', 'style', 
        'fill-rule', 'clip-rule', 'stroke-width',
        'stroke-linecap', 'stroke-linejoin'
    }
    if extra_attrs:
        for key, val in extra_attrs.items():
            if key in SAFE_SVG_ATTRS and val is not None:
                inject_attrs[key] = str(val)
    
    if title and not aria_label:
        safe_title = escape(title)
        svg_start = svg_content.find('<svg')
        if svg_start != -1:
            first_close = svg_content.find('>', svg_start)
            if first_close != -1:
                svg_content = (
                    svg_content[:first_close + 1] +
                    f'<title>{safe_title}</title>' +
                    svg_content[first_close + 1:]
                )
    
    if inject_attrs:
        attr_str = ' '.join(
            f'{escape(k)}="{escape(str(v))}"' 
            for k, v in inject_attrs.items()
        )
        svg_content = svg_content.replace('<svg', f'<svg {attr_str}', 1)
    
    return mark_safe(svg_content)


def _get_fallback(use_fallback: bool, message: str = "") -> str:
    """Return fallback icon or debug comment."""
    if settings.DEBUG and not use_fallback:
        logger.debug(f"SVG Icon Error: {message}")
        return mark_safe(f'<!-- SVG ICON ERROR: {escape(message)} -->')
    
    if not use_fallback:
        return ''
    
    logger.warning(f"Using fallback icon: {message}")
    return mark_safe(_FALLBACK_SVG)


@register.simple_tag
def svg_icon(
    name: str,
    library: Optional[str] = None,
    class_name: str = "",
    aria_label: Optional[str] = None,
    title: Optional[str] = None,
    width: Optional[str] = None,
    height: Optional[str] = None,
    fill: Optional[str] = None,
    stroke: Optional[str] = None,
    extra_attrs: Optional[Dict[str, Any]] = None,
    inline: bool = True,
    fallback: bool = True,
) -> str:
    """
    Render SVG icon with multi-library support.
    
    Args:
        name: Icon filename without extension
        library: Library namespace (e.g., "bootstrap", "heroicons-outline")
        class_name: CSS classes
        aria_label: ARIA label for accessibility
        title: Visual title
        width: Width attribute
        height: Height attribute
        fill: Fill color
        stroke: Stroke color
        extra_attrs: Additional attributes (whitelist validated)
        inline: Render as inline SVG (True) or <img> tag (False)
        fallback: Show fallback on error
        
    Returns:
        Safe HTML string containing the icon
    """
    if not name or not isinstance(name, str):
        return _get_fallback(fallback, "Invalid icon name")
    
    if ":" in name and library is None:
        parts = name.split(":", 1)
        if len(parts) == 2:
            lib_part, name_part = parts
            if _LIBRARY_PATTERN.match(lib_part) and _ICON_NAME_PATTERN.match(name_part):
                library, name = lib_part, name_part
    
    icon_path = _find_icon_path(name, library)
    if not icon_path:
        msg = f"Icon '{name}'"
        if library:
            msg += f" in library '{library}'"
        msg += " not found"
        return _get_fallback(fallback, msg)
    
    file_mtime = Path(icon_path).stat().st_mtime
    
    if _USE_DJANGO_CACHE:
        cache_key = f"svg_icon:{library or 'default'}:{name}:{file_mtime}"
        svg_content = django_cache.get(cache_key)
        if svg_content is None:
            svg_content = _get_cached_svg_content(icon_path, file_mtime)
            if svg_content:
                django_cache.set(cache_key, svg_content, _CACHE_TIMEOUT)
    else:
        svg_content = _get_cached_svg_content(icon_path, file_mtime)
    
    if not svg_content:
        return _get_fallback(fallback, f"Error processing icon '{name}'")
    
    if not inline:
        return _render_as_img(
            name, library, class_name, aria_label, title,
            width, height, extra_attrs
        )
    
    return _process_inline_svg(
        svg_content, class_name, aria_label, title,
        width, height, fill, stroke, extra_attrs
    )


@register.filter
def svg_icon_simple(name: str) -> str:
    """Simplified filter for common use cases."""
    return svg_icon(name, class_name="icon")


@register.inclusion_tag('svg_icon_tags/icon.html')
def icon(
    name: str,
    size: str = "md",
    color: str = "current",
    library: Optional[str] = None,
    rotate: Optional[str] = None,
    flip: Optional[str] = None,
    spin: bool = False,
    pulse: bool = False,
) -> Dict[str, str]:
    """
    Inclusion tag with Tailwind-friendly presets and animations.
    
    Args:
        name: Icon name
        size: Size preset (xs, sm, md, lg, xl, 2xl, 3xl, 4xl)
        color: Color preset
        library: Library name
        rotate: Rotation angle (e.g., "90", "180", "270")
        flip: Flip direction ("horizontal" or "vertical")
        spin: Enable spinning animation
        pulse: Enable pulsing animation
        
    Returns:
        dict: Context for icon.html template
    """
    size_map = {
        'xs': 'w-3 h-3',
        'sm': 'w-4 h-4',
        'md': 'w-5 h-5',
        'lg': 'w-6 h-6',
        'xl': 'w-8 h-8',
        '2xl': 'w-10 h-10',
        '3xl': 'w-12 h-12',
        '4xl': 'w-16 h-16',
    }
    
    color_map = {
        'current': 'text-current',
        'primary': 'text-primary-600',
        'secondary': 'text-secondary-600',
        'success': 'text-success-600',
        'danger': 'text-danger-600',
        'warning': 'text-warning-600',
        'info': 'text-info-600',
        'gray': 'text-gray-500',
        'light': 'text-gray-400',
        'dark': 'text-gray-800',
        'brand-blue': 'text-blue-600',
        'brand-green': 'text-green-600',
    }
    
    classes = [
        size_map.get(size, 'w-5 h-5'),
        color_map.get(color, 'text-current'),
    ]
    
    # Add rotation classes
    if rotate:
        classes.append(f'rotate-{rotate}')
    
    # Add flip classes
    if flip == 'horizontal':
        classes.append('scale-x-[-1]')
    elif flip == 'vertical':
        classes.append('scale-y-[-1]')
    
    # Add animation classes
    if spin:
        classes.append('animate-spin')
    if pulse:
        classes.append('animate-pulse')
    
    return {
        'icon_name': name,
        'library': library,
        'class_name': ' '.join(classes),
    }