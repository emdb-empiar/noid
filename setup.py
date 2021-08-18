import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noid",
    version="1.0.0.a1",
    author="Yinlin Chen, Tingting Jiang, Lee Hunter, Jim Tuttle, Paul K. Korir",
    author_email="ylchen@vt.edu, virjtt03@vt.edu, whunter@vt.edu, jjt@vt.edu, paulkorir@gmail.com",
    description="Mint NOID",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vt-digital-libraries-platform/NOID-mint",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'noid=noid.pynoid:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
