from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="china_map_generator",
    version="0.1.0",
    author="Map Generator Team",
    author_email="",
    description="中国地图和8000公里范围地图生成器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'matplotlib',
        'cartopy',
    ],
    entry_points={
        'console_scripts': [
            'china-map-generator=main:main',
        ],
    },
)