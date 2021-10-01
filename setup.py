import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noid",
    version="1.1.1",
    author="Paul K. Korir",
    author_email="pkorir@ebi.ac.uk, paulkorir@gmail.com",
    description="Mint NOIDs using a CLI or API",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paulkorir/noid",
    packages=setuptools.find_packages(),
    package_data={
      'noid': ['noid.cfg']
    },
    entry_points={
        'console_scripts': [
            'noid=noid.pynoid:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
