from setuptools import setup, find_packages


setup(
    name='wagtail_comments_xtd',
    author='André Karlsson',
    license='GPLv3',
    author_email='andre.karlsson@protractus.se',
    version='0.2.0',
    url='https://github.com/joyider/wagtail_comments_xtd',
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Topic :: Internet :: WWW/HTTP',
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    packages=find_packages(),
    python_requires='>=3',
    install_requires=[
        "wagtail>1.7",
        "Django>=1.8.16",
        "wagtailfontawesome>=1.0.2",
        "django-comments-xtd>=1.6.3"
    ],
)
