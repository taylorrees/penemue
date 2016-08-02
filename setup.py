try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A tool to stream and store the tweets of a select group of users.',
    'author': 'Taylor Rees',
    'url': 'https://github.com/taylorrees/media-monitor',
    'download_url': 'https://github.com/taylorrees/media-monitor/archive/master.zip',
    'author_email': 'hello@taylorre.es',
    'version': '0.1',
    'install_requires': ['twython', 'pymongo', 'matplotlib', 'textblob', 'beautifulsoup4'],
    'packages': ['media-monitor'],
    'scripts': [],
    'name': 'media-monitor'
}

setup(**config)
