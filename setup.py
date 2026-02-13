"""
Setup script for django-svg-icon-tags package
"""
import os
from setuptools import setup, find_packages

# Read README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
def read_requirements(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="django-svg-icon-tags",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Secure and flexible Django template tags for SVG icons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/reza-bayat/django-svg-icon-tags",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'django_svg_icon_tags': [
            'templates/svg_icon_tags/*.html',
            'templatetags/*.py',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-django>=4.5.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
        ],
    },
    keywords="django svg icons template tags bootstrap heroicons",
    project_urls={
        "Bug Tracker": "https://github.com/reza-bayat/django-svg-icon-tags/issues",
        "Documentation": "https://github.com/reza-bayat/django-svg-icon-tags#readme",
        "Source Code": "https://github.com/reza-bayat/django-svg-icon-tags",
    },
)