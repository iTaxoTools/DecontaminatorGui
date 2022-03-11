"""The setup module for Taxi3Gui"""

# Always prefer setuptools over distutils
from setuptools import setup, find_namespace_packages
import pathlib

# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='taxi3-gui',
    version='0.0.1',
    description='A Qt GUI for Taxi3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Patmanidis Stefanos',
    author_email='stefanpatman91@gmail.com',
    package_dir={'': 'src'},
    packages=find_namespace_packages(
        include=('itaxotools*',),
        where='src',
    ),
    python_requires='>=3.8.6, <4',
    install_requires=[
        'pyside6>=6.1.1, <6.2.0',
        'itaxotools-common==0.2.2',
        ],
    extras_require={
        'dev': ['pyinstaller>=4.5.1'],
    },
    entry_points={
        'console_scripts': [
            'taxi3-gui = itaxotools.taxi3_gui:run',
        ]
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    include_package_data=True,
)
