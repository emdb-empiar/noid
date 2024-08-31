import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

NOID_VERSION = "1.1.3"

if __name__ == "__main__":
    setuptools.setup(
        name="noid",
        version=NOID_VERSION,
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
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
