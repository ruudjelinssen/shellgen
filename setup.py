import os
import shellgen

from setuptools import setup


DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(DIR, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'shellgen',
    version = shellgen.__version__,
    author = 'Ruud Linssen',
    author_email = 'r.p.j.linssen@gmail.com',
    description = ('Tool for generating reverse shells.'),
    long_description = long_description,
    url = 'https://github.com/ruudjelinssen/shellgen',
    license = 'MIT',
    keywords = 'reverse shell pentest bash',
    packages = ['shellgen'],
    package_data = {'shellgen': ['shells/*.shell']},
    classifiers=[
        'Topic :: Utilities',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            'shellgen=shellgen.shellgen:main'
        ],
    },
)
