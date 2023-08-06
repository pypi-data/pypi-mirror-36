# egegsignals - Software for processing electrogastroenterography signals.

# Copyright (C) 2013 -- 2018 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup
import os
from egegsignals import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="egegsignals",
    version=__version__,
    description="Package for processing EGG/EGEG signals",

    author="Aleksandr Popov",
    author_email="aleneus@gmail.com",

    keywords="electrophysiology " +
    "electrogastrography " +
    "electrogastroenterography " +
    "biomedical signal processing",

    url="https://bitbucket.org/aleneus/egegsignals",

    license="GPLv3",

    long_description=read('README'),

    packages=['egegsignals'],

    install_requires=[
        'numpy>=1.14.0',
        'scipy>=1.0.0',
        'nose>=1.3.7',
        'dsplab>=0.33.0',
    ],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
