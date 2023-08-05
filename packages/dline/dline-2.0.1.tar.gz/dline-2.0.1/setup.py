# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()[:-1]

setup(
    name='dline',
    version='2.0.1',
    description='A feature-rich terminal discord client',
    long_description=readme,
    author='Nat Osaka',
    author_email='natthetupper@gmail.com',
    url='https://github.com/NatTupper/dline',
    license='gpl-3.0',
    keywords=['discord', 'discord.py', 'chat client', 'ncurses'],
    packages=[
        'dline', 'dline.client', 'dline.commands',
        'dline.input', 'dline.ui', 'dline.utils'
    ],
    install_requires=requirements,
    dependency_links=['https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Communications :: Chat'
    ],
    entry_points={
        'console_scripts': ['dline=dline.__main__:main']
    },
    include_package_data=True,
    zip_safe=False
)
