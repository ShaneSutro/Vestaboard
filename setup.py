import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Vestaboard",
    version="0.4.0",
    author="Shane Sutro",
    author_email="shane@shanesutro.com",
    description="A Vestaboard Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SonicRift/Vestaboard.git",
    packages=setuptools.find_packages(),
    license="MIT",
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)