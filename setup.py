import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='Forex Form Finder Toolkit',
    version='1.0.0',
    author="Evan Shamal",
    author_email="evan@ishamal.ru",
    description="The library designed to help you find any pattern on market",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )
