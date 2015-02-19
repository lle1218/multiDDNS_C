try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
		'description': 'multiDDNS_C Project',
		'author': 'stefan',
		'url': '',
		'download_url': '',
		'author_email': 'tianle1218@126.com',
		'version': '0.1',
		'install_requires': ['nose'],
		'package': ['ddns'],
		'scrips': [],
		'name': 'multiDDNS_C',
}

setup(**config)
