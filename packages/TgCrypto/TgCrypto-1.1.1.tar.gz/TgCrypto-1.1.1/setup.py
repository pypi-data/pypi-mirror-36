# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import re

from setuptools import setup, Extension, find_packages

# PyPI doesn't like raw html
with open("README.rst", encoding="utf-8") as f:
    readme = re.sub(r"\.\. \|.+\| raw:: html(?:\s{4}.+)+\n\n", "", f.read())
    readme = re.sub(r"\|header\|", "|logo|\n\n|description|", readme)

setup(
    name="TgCrypto",
    version="1.1.1",
    description="Fast Telegram Crypto Library for Python",
    long_description=readme,
    url="https://github.com/pyrogram",
    download_url="https://github.com/pyrogram/tgcrypto/releases/latest",
    author="Dan Tès",
    author_email="admin@pyrogram.ml",
    license="LGPLv3+",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords="fast pyrogram telegram crypto mtproto api client library python",
    project_urls={
        "Tracker": "https://github.com/pyrogram/tgcrypto/issues",
        "Community": "https://t.me/PyrogramChat",
        "Source": "https://github.com/pyrogram/tgcrypto",
        "Documentation": "https://docs.pyrogram.ml",
    },
    python_requires="~=3.4",
    packages=find_packages(),
    zip_safe=False,
    ext_modules=[
        Extension(
            "tgcrypto",
            sources=[
                "tgcrypto/tgcrypto.c",
                "tgcrypto/aes256.c",
                "tgcrypto/ige256.c",
                "tgcrypto/ctr256.c"
            ]
        )
    ]
)
