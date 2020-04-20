from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup

with open('README.md') as fh:
    long_description = fh.read()


def read_version():
    version_contents = {}
    with open(join(dirname(__file__), 'magic_admin', 'version.py')) as fh:
        exec(fh.read(), version_contents)

    return version_contents['VERSION']


def load_readme():
    with open(join(dirname(__file__), 'README.md')) as fh:
        long_description = fh.read()

    return long_description


def load_requirements():
    with open(join(dirname(__file__), 'requirements.txt')) as fh:
        requirements = fh.readlines()

    return requirements


setup(
    name='magic-admin',
    version=read_version(),
    description='Magic Python Library',
    long_description=load_readme(),
    long_description_content_type='text/markdown',
    author='Magic',
    author_email='support@magic.link',
    url='https://magic.link',
    license='MIT',
    keywords='magic python sdk',
    packages=find_packages(
        exclude=[
            'tests',
            'tests.*',
            'testing',
            'testing.*',
            'virtualenv_run',
            'virtualenv_run.*',
        ],
    ),
    zip_safe=False,
    install_requires=load_requirements(),
    python_requires='>=3.6',
    project_urls={
        'Website': 'https://magic.link',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
