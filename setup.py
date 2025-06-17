import os
from setuptools import setup, find_packages
from pygameui.version import vernum


def readme():
    fname = "README.md"
    if os.path.exists(fname):
        with open(fname, encoding="utf-8") as f:
            return f.read()
    return ""


setup(
    name="pygameui",
    version=f"{vernum}",
    author="Sackey Ezekiel Etrue",
    author_email="sackeyetrue@gmail.com",
    description="Python Game Development User Interface (Pygame-GUI)",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/djoezeke/pygameui",
    project_urls={
        "Homepage": "https://github.com/djoezeke/pygameui",
        "Documentation": "https://github.com/djoezeke/pygameui#readme",
        "Issues": "https://github.com/djoezeke/pygameui/issues",
        "Release Notes": "https://github.com/djoezeke/pygameui/releases",
        "Source": "https://github.com/djoezeke/pygameui",
    },
    license="MIT",
    packages=find_packages(where="."),
    py_modules=["pygameui"],
    include_package_data=True,
    install_requires=[
        "pygame>=2.0.0",
    ],
    extras_require={
        "dev": ["pytest", "colorama"],
        "docs": ["sphinx"],
    },
    python_requires=">=3.9",
    keywords="game pygame gui development pygameui",
    platforms=["any"],
    classifiers=[
        "Development Status :: 1 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: pygame",
        "Typing :: Typed",
    ],
    zip_safe=False,
)
