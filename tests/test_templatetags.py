"""
Unit tests for SVG icon template tags
"""
import pytest
from django.template import Template, Context
from django.test import override_settings


@pytest.fixture
def mock_icon_file(tmp_path):
    """Create a mock SVG icon file for testing"""
    icon_dir = tmp_path / "icons" / "test"
    icon_dir.mkdir(parents=True)
    
    icon_file = icon_dir / "test-icon.svg"
    icon_file.write_text('<svg xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>')
    
    return str(tmp_path)


class TestSvgIconTag:
    """Test the svg_icon template tag"""
    
    def test_basic_icon_rendering(self, mock_icon_file):
        """Test basic icon rendering"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% svg_icon "test-icon" library="test" %}')
            context = Context({})
            result = template.render(context)
            
            assert '<svg' in result
            assert 'test-icon.svg' in result or 'path d=' in result
    
    def test_icon_with_library_syntax(self, mock_icon_file):
        """Test icon rendering with library:name syntax"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% svg_icon "test:test-icon" %}')
            context = Context({})
            result = template.render(context)
            
            assert '<svg' in result
    
    def test_icon_with_custom_classes(self, mock_icon_file):
        """Test icon with custom CSS classes"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% svg_icon "test-icon" library="test" class_name="w-6 h-6 text-blue-500" %}')
            context = Context({})
            result = template.render(context)
            
            assert 'w-6' in result
            assert 'h-6' in result
            assert 'text-blue-500' in result
    
    def test_icon_as_img_tag(self, mock_icon_file):
        """Test icon rendering as img tag"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% svg_icon "test-icon" library="test" inline=False %}')
            context = Context({})
            result = template.render(context)
            
            assert '<img' in result
            assert 'src=' in result
    
    def test_icon_with_aria_label(self, mock_icon_file):
        """Test icon with ARIA label"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% svg_icon "test-icon" library="test" aria_label="Test Icon" %}')
            context = Context({})
            result = template.render(context)
            
            assert 'aria-label="Test Icon"' in result
            assert 'role="img"' in result
            assert 'focusable="false"' in result
    
    def test_icon_with_title(self, mock_icon_file):
        """Test icon with title element"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% svg_icon "test-icon" library="test" title="Test Title" %}')
            context = Context({})
            result = template.render(context)
            
            assert '<title>Test Title</title>' in result
    
    def test_icon_with_dimensions(self, mock_icon_file):
        """Test icon with custom width and height"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% svg_icon "test-icon" library="test" width="100" height="50" %}')
            context = Context({})
            result = template.render(context)
            
            assert 'width="100"' in result
            assert 'height="50"' in result


class TestIconInclusionTag:
    """Test the icon inclusion tag"""
    
    def test_basic_icon(self, mock_icon_file):
        """Test basic icon inclusion tag"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% icon "test-icon" library="test" %}')
            context = Context({})
            result = template.render(context)
            
            assert '<svg' in result
    
    def test_icon_with_size_preset(self, mock_icon_file):
        """Test icon with size preset"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% icon "test-icon" library="test" size="lg" %}')
            context = Context({})
            result = template.render(context)
            
            # lg preset is w-6 h-6
            assert 'w-6' in result
            assert 'h-6' in result
    
    def test_icon_with_color_preset(self, mock_icon_file):
        """Test icon with color preset"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% icon "test-icon" library="test" color="primary" %}')
            context = Context({})
            result = template.render(context)
            
            assert 'text-primary-600' in result
    
    def test_icon_with_spin_animation(self, mock_icon_file):
        """Test icon with spin animation"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% icon "test-icon" library="test" spin=True %}')
            context = Context({})
            result = template.render(context)
            
            assert 'animate-spin' in result
    
    def test_icon_with_rotate(self, mock_icon_file):
        """Test icon with rotation"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% icon "test-icon" library="test" rotate="90" %}')
            context = Context({})
            result = template.render(context)
            
            assert 'rotate-90' in result
    
    def test_icon_with_flip_horizontal(self, mock_icon_file):
        """Test icon with horizontal flip"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% icon "test-icon" library="test" flip="horizontal" %}')
            context = Context({})
            result = template.render(context)
            
            assert 'scale-x-[-1]' in result
    
    def test_icon_with_flip_vertical(self, mock_icon_file):
        """Test icon with vertical flip"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{% icon "test-icon" library="test" flip="vertical" %}')
            context = Context({})
            result = template.render(context)
            
            assert 'scale-y-[-1]' in result


class TestSvgIconFilter:
    """Test the svg_icon_simple filter"""
    
    def test_svg_icon_filter(self, mock_icon_file):
        """Test svg_icon_simple filter"""
        with override_settings(STATICFILES_DIRS=[mock_icon_file]):
            template = Template('{% load svg_icon_tags %}{{ "test-icon"|svg_icon_simple }}')
            context = Context({})
            result = template.render(context)
            
            assert '<svg' in result
            assert 'class="icon"' in result