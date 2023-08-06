from setuptools import setup, find_packages

setup(
    name='hiku',
    version='0.5.0rc2',
    description='Library to implement Graph APIs',
    author='Vladimir Magamedov',
    author_email='vladimir@magamedov.com',
    url='https://github.com/vmagamedov/hiku',
    packages=find_packages(exclude=['test*']),
    include_package_data=True,
    license='BSD',
    install_requires=[],
)
