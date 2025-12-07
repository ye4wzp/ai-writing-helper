from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-writing-helper",
    version="1.0.0",
    author="ye4wzp",
    description="中文AI文本检测与人性化工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ye4wzp/ai-writing-helper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'jieba>=0.42.1',
        'click>=8.0.0',
        'flask>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'ai-humanizer=cli.main:cli',
        ],
    },
)
