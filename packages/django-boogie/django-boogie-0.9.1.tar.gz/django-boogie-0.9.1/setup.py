import sys;

from setuptools import setup, find_packages

sys.path.append('src')

setup(
    name='django-boogie',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    setup_requires='setuptools >= 30.3',
)
