try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A tool to stream and store the tweets of a select group of users.',
    'author': 'Taylor Rees',
    'url': 'https://github.com/taylorrees/penemue',
    'download_url': 'https://github.com/taylorrees/penemue/archive/master.zip',
    'author_email': 'hello@taylorre.es',
    'version': '0.1',
    'install_requires': ['twython', 'pymongo'],
    'packages': ['penemue'],
    'scripts': [],
    'name': 'penemue'
}

setup(**config)
