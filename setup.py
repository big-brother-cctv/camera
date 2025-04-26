from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="big-brother-camera",
    version="1.4.10",
    description="Big Brother CCTV camera microservice.",
    author="r-dvl",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=parse_requirements("requirements.txt"),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "big-brother-camera=app:main",
        ],
    },
)
