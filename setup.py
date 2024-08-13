from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in erpkenema/__init__.py
from erpkenema import __version__ as version

setup(
	name="erpkenema",
	version=version,
	description="ERP System for kenema Pharmacies Enterprise",
	author="TechEthio IT Solution plc",
	author_email="dev@techethio.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
