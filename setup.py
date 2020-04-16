from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()


def load_readme():
    with open(join(dirname(__file__), 'README.md'), 'r') as fh:
        long_description = fh.read()

    return long_description


def load_requirements():
    with open(join(dirname(__file__), 'requirements.txt'), 'r') as fh:
        requirements = fh.readlines()

    return requirements


setup(
    name='magic-admin',
    version='0.0.2',
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
            'examples',
            'examples.*',
            'testing',
            'testing.*',
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
