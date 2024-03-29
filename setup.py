"""The setup module for DecontaminatorGui"""

# Always prefer setuptools over distutils
from setuptools import setup, find_namespace_packages
from pathlib import Path

# Get the long description from the README file
here = Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='decontaminator-gui',
    version='0.0.1',
    description='A Qt GUI for Decontaminator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Patmanidis Stefanos',
    author_email='stefanpatman91@gmail.com',
    package_dir={'': 'src'},
    packages=find_namespace_packages(
        include=('itaxotools*',),
        where='src',
    ),
    python_requires='>=3.10.2, <4',
    install_requires=[
        'itaxotools-common==0.2.4',
        'pyside6>=6.1.1',
        'decontaminator',
        'Genesubsetselector',
        'SCaFoSpy',
    ],
    extras_require={
        'dev': [
            'pyinstaller>=4.5.1',
            'flake8>=4.0.0',
            'isort>=5.9.0'
        ],
    },
    entry_points={
        'console_scripts': [
            'decontaminator-gui = itaxotools.decontaminator_gui:run',
        ]
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
    ],
    include_package_data=True,
)
