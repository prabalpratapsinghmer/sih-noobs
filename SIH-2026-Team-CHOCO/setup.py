"""Setup script for SIH26184 - Predictive Analytics Framework."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="sih26184",
    version="1.0.0",
    author="SIH Team",
    author_email="team@sih.gov.in",
    description="Predictive Analytics Framework for Cybercrime Complaints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sih26184/cybercrime-prediction",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sih-train-atm=models.spatio_temporal.train:main",
            "sih-train-mule=models.mule_detection.train:main",
            "sih-serve=api.main:main",
            "sih-synthesize=models.utils.data_synthesis:main",
        ],
    },
)
