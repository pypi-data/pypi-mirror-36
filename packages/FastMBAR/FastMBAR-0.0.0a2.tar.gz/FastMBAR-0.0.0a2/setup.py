from setuptools import setup, find_packages

with open("README.rst", 'r') as file_handle:
    long_description = file_handle.read()

setup(
    name = "FastMBAR",
    version = "0.0.0a2",
    author = "Xinqiang (Shawn) Ding",
    author_email = "xqding@umich.edu",
    description = "A fast solver for large scale MBAR/UWHAM equations",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/xqding/MBAR_PyTorch",
    packages = find_packages(),
    install_requires=['numpy>=1.14.0',
                      'scipy>=1.1.0',
                      'torch>=0.4.0'],
    license = 'MIT',
    classifiers = (
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
