import io  # for python2
from os import path
from setuptools import setup, find_packages
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
from version import __version__ as version

WORKING_DIR = path.abspath(path.dirname(__file__))

# Get long description from README.md
with io.open(path.join(WORKING_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# read requirements.txt and load into list
REQUIREMENTS_TXT = parse_requirements(
    path.join(WORKING_DIR, "requirements.txt"), session='my_session')
REQUIREMENTS = [str(r.req) for r in REQUIREMENTS_TXT]

setup(
    author='Dave Gallant',
    author_email='davegallant@gmail.com',
    description='Improved Color Kafka',
    entry_points={
        'console_scripts': [
            'ickafka=ickafka.app:main',
        ],
    },
    install_requires=REQUIREMENTS,
    keywords=['kafka', 'pygments'],
    license='Apache License, Version 2.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    name='ickafka',
    packages=find_packages(),
    url='https://github.com/davegallant/ickafka',
    version=version,
)
