from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.rst')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, 'runtest', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='runtest',
    version=version['__version__'],
    description=('Numerically tolerant end-to-end test library for scientific codes.'),
    long_description=long_description,
    author='Radovan Bast',
    author_email='radovan.bast@uit.no',
    url='https://github.com/bast/runtest',
    license='MPL-2.0',
    packages=['runtest'],
#   no dependencies
#   install_requires=[
#       'dependency==1.2.3',
#   ],
#   no scripts
#   scripts=['bin/a-script'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
    )
