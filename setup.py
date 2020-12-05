import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vroom-pkg-mganti", # Replace with your own username
    version="0.1",
    author="Manasi Ganti",
    author_email="manasi.ganti@gmail.com",
    description="pypi package for vroom",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manasi-ganti/project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)