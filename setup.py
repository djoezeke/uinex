def readme():
    fname = "README.md"
    if os.path.exists(fname):
        with open(fname, encoding="utf-8") as f:
            return f.read()
    return ""


import os
from setuptools import setup, find_packages
from uinex.version import vernum


def readme():
    fname = "README.md"
    if os.path.exists(fname):
        with open(fname, encoding="utf-8") as f:
            return f.read()
    return ""


setup(
    name="uinex",
    version=f"{vernum}",
    author="Sackey Ezekiel Etrue",
    author_email="sackeyetrue@gmail.com",
    maintainer="Sackey Ezekiel Etrue",
    maintainer_email="sackeyetrue@gmail.com",
    description="Create modern looking GUIs with pygame.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/djoezeke/uinex",
    project_urls={
        "Homepage": "https://github.com/djoezeke/uinex",
        "Documentation": "https://github.com/djoezeke/uinex#readme",
        "Issues": "https://github.com/djoezeke/uinex/issues",
        "Release Notes": "https://github.com/djoezeke/uinex/releases",
        "Source": "https://github.com/djoezeke/uinex",
    },
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pillow>=11.3.0",
        "pygame",
    ],
    extras_require={
        "dev": ["pytest", "build", "twine", "wheel"],
        "docs": [],
    },
    python_requires=">=3.13",
    keywords=[
        "pygame",
        "uinex",
        "game ui",
        "2d",
        "games",
        "development",
        "gui",
        "library",
    ],
    platforms=["any"],
    classifiers=[
        "Framework :: Uinex",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Linux",
        "Operating System :: MacOS",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Typing :: Typed",
    ],
    include_package_data=True,
    zip_safe=False,
)
