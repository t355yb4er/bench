from setuptools import find_packages, setup
from bench import FRAPPE_VERSION, set_frappe_version
import bench, VERSION
from bench.config.site_config import get_site_config

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

setup(
	name= get_site_config,
	description='CLI to manage Multi-tenant deployments for Frappe apps',
	author='Frappe Technologies',
	author_email='info@frappe.io',
	version=VERSION,
	packages=find_packages(),
	python_requires='~=3.6',
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
	entry_points='''
[console_scripts]
bench=bench.cli:cli
''',
)
