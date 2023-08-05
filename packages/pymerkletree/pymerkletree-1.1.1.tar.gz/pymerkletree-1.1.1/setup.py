from setuptools import find_packages
from setuptools import setup

long_description = (
    "This project is adapted from the pymerkletools of Tierion. "
    "It includes a `MerkleTree` class for creating Merkle trees, "
    "generating merkle proofs, and verification of merkle proofs."
)


setup(
    name="pymerkletree",
    version='1.1.1',
    description='Simple Merkle Tree',
    long_description=long_description,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    url='https://github.com/aliciawyy/pymerkletools',
    author='Alice Wang, Eder Santana',
    author_email="rainingilove@gmail.com",
    keywords='merkle tree, blockchain',
    license="MIT",
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=["pysha3==1.0.2"],
    extras_require={
        "test": ["pytest==3.6.1", "pytest-cov==2.5.1"]
    }
)
