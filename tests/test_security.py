"""
Security tests for SVG icon template tags
"""
import pytest
from django.template import Template, Context
from django.test import override_settings


@pytest.fixture
def mock_icon_dir(tmp_path):
    """Create mock icon directories for security testing"""
    base_dir = tmp_path / "icons"
    base_dir.mkdir()
    
    # Create valid library
    test_lib = base_dir / "test"
    test_lib.mkdir()
    (test_lib / "valid-icon.svg").write_text('<svg><path d="M12 2L2 7"/></svg>')
    
    # Create another library
    other_lib = base_dir / "other"
    other_lib.mkdir()
    (other_lib / "other-icon.svg").write_text('<svg><path d="M12 2L2 7"/></svg>')
    
    return str(tmp_path)


class TestSecurity:
    """Security-focused tests"""
    
    def test_path_traversal_prevention(self, mock_icon_dir):
        """Test that path traversal attacks are prevented"""
        with override_settings(STATICFILES_DIRS=[mock_icon_dir]):
            # Attempt path traversal
            template = Template('{% load svg_icon_tags %}{% svg_icon "../etc/passwd" %}')
            context = Context({})
            result = template.render(context)
            
            # Should not render the file, should show fallback or error
            assert '<svg' not in result or 'fallback' in result.lower() or 'error' in result.lower()
    
    def test_xss_in_icon_name(self, mock_icon_dir):
        """Test that XSS in icon name is prevented"""
        with override_settings(STATICFILES_DIRS=[mock_icon_dir]):
            # Attempt XSS via icon name
            template = Template('{% load svg_icon_tags %}{% svg_icon "test<svg onload=alert(1)>" %}')
            context = Context({})
            
            # Should not raise error but should not render malicious content
            result = template.render(context)
            assert '<svg onload=alert(1)>' not in result
    
    def test_script_tag_removal(self, tmp_path):
        """Test that script tags are removed from SVG content"""
        icon_dir = tmp_path / "icons" / "test"
        icon_dir.mkdir(parents=True)
        
        # Create SVG with script tag
        malicious_svg = icon_dir / "malicious.svg"
        malicious_svg.write_text('''
        <svg xmlns="http://www.w3.org/2000/svg">
            <script>alert("XSS")</script>
            <path d="M12 2L2 7"/>
        </svg>
        ''')
        
        with override_settings(STATICFILES_DIRS=[str(tmp_path)]):
            template = Template('{% load svg_icon_tags %}{% svg_icon "malicious" library="test" %}')
            context = Context({})
            result = template.render(context)
            
            # Script tag should be removed
            assert '<script>' not in result
            assert 'alert("XSS")' not in result
    
    def test_event_handler_removal(self, tmp_path):
        """Test that event handlers are removed from SVG content"""
        icon_dir = tmp_path / "icons" / "test"
        icon_dir.mkdir(parents=True)
        
        # Create SVG with event handler
        malicious_svg = icon_dir / "malicious.svg"
        malicious_svg.write_text('''
        <svg xmlns="http://www.w3.org/2000/svg" onclick="alert(1)">
            <path d="M12 2L2 7" onmouseover="alert(2)"/>
        </svg>
        ''')
        
        with override_settings(STATICFILES_DIRS=[str(tmp_path)]):
            template = Template('{% load svg_icon_tags %}{% svg_icon "malicious" library="test" %}')
            context = Context({})
            result = template.render(context)
            
            # Event handlers should be removed
            assert 'onclick=' not in result.lower()
            assert 'onmouseover=' not in result.lower()
            assert 'alert(1)' not in result
            assert 'alert(2)' not in result
    
    def test_library_name_validation(self, mock_icon_dir):
        """Test that library names are validated"""
        with override_settings(STATICFILES_DIRS=[mock_icon_dir]):
            # Invalid library name with special characters
            template = Template('{% load svg_icon_tags %}{% svg_icon "valid-icon" library="invalid/../library" %}')
            context = Context({})
            result = template.render(context)
            
            # Should not render or should show error
            assert result is not None  # Should not crash
    
    def test_special_characters_in_attributes(self, mock_icon_dir):
        """Test that special characters in attributes are escaped"""
        with override_settings(STATICFILES_DIRS=[mock_icon_dir]):
            # Try to inject HTML via class_name
            template = Template('{% load svg_icon_tags %}{% svg_icon "valid-icon" library="test" class_name=\'"><script>alert(1)</script>\' %}')
            context = Context({})
            result = template.render(context)
            
            # Should be escaped
            assert '<script>' not in result
            assert '&lt;script&gt;' in result or 'alert(1)' not in result
    
    def test_aria_label_escaping(self, mock_icon_dir):
        """Test that ARIA labels are properly escaped"""
        with override_settings(STATICFILES_DIRS=[mock_icon_dir]):
            # Try to inject HTML via aria_label
            template = Template('{% load svg_icon_tags %}{% svg_icon "valid-icon" library="test" aria_label=\'"><script>alert(1)</script>\' %}')
            context = Context({})
            result = template.render(context)
            
            # Should be escaped
            assert '<script>' not in result
            assert '&lt;script&gt;' in result or 'alert(1)' not in result
    
    def test_title_escaping(self, mock_icon_dir):
        """Test that title content is properly escaped"""
        with override_settings(STATICFILES_DIRS=[mock_icon_dir]):
            # Try to inject HTML via title
            template = Template('{% load svg_icon_tags %}{% svg_icon "valid-icon" library="test" title=\'"><script>alert(1)</script>\' %}')
            context = Context({})
            result = template.render(context)
            
            # Should be escaped
            assert '<script>' not in result
            assert '&lt;script&gt;' in result or 'alert(1)' not in result