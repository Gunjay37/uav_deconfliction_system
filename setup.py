from setuptools import setup, find_packages

setup(
    name="uav-deconfliction-system",
    version="0.1.0",
    description="UAV Strategic Deconfliction System for Shared Airspace",
    author="Your Name",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.3",
        "matplotlib>=3.7.1",
        "plotly>=5.14.0",
        "scipy>=1.10.1",
        "pandas>=2.0.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-cov>=4.1.0",
            "black>=23.3.0",
            "flake8>=6.0.0",
        ],
    },
)