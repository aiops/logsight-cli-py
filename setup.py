from setuptools import find_packages, setup

VERSION = '0.0.41'


with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='logsight-cli-py',
    version=VERSION,
    description='Logsight CLI Python',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Jorge Cardoso',
    author_email='jorge.cardoso.pt@gmail.com',
    url="https://github.com/aiops/logsight-cli-py",
    project_urls={
        "Documentation": "https://github.com/aiops/logsight-cli-py/",
        "Source": "https://github.com/aiops/logsight-cli-py",
        "Tracker": "https://github.com/aiops/logsight-cli-py/issues",
    },
    license='unlicense',
    packages=find_packages(exclude=("test",)),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=[
        "logsight-sdk-py",
        "click",
        "prettytable",
        "tqdm",
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "logsight = logsight_cli.logsight_cli:main",
        ]
    }
)
