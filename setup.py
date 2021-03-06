import codecs
import os
from platform import python_version

from setuptools import find_packages, setup

PACKAGE_NAME = "textx-gen-vscode"
VERSION = "0.1.3"
AUTHOR = "Daniel Elero"
AUTHOR_EMAIL = "danixeee@gmail.com"
DESCRIPTION = "a VS Code extension generator"
KEYWORDS = "textX DSL python domain specific languages VS Code"
LICENSE = "MIT"
URL = "https://github.com/danixeee/textx-gen-vscode"

packages = find_packages()

print("packages:", packages)

README = codecs.open(
    os.path.join(os.path.dirname(__file__), "README.md"), "r", encoding="utf-8"
).read()

ci_require = [
    "bandit==1.6.2",
    "pytest==5.3.2",
    "pytest-cov==2.8.1",
    "pytest-azurepipelines==0.8.0",
]

dev_require = ["bandit==1.6.2"]

tests_require = ["coverage==5.0.1", "pytest==5.3.2", "pytest-cov==2.8.1"]

if python_version().startswith("3.6"):  # For python 3.6
    ci_require.append("black")
    dev_require.append("black")


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    keywords=KEYWORDS,
    license=LICENSE,
    packages=packages,
    include_package_data=True,
    install_requires=["click", "jinja2>=2", "textx>=2", "textx-gen-coloring>=0.1.2"],
    entry_points={"textx_generators": ["vscode_gen = textx_gen_vscode:vscode_gen"]},
    extras_require={"ci": ci_require, "dev": dev_require, "test": tests_require},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
