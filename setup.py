from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="github_repo_diff",
    version="0.0.1",
    description="A simple tool to get percentage differences across GitHub Forks",  # Optional
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wason1797/github-repo-diff",  # Optional
    author="Wladymir Brborich",
    author_email="Wasonlol1797@hotmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="GitHub, diff, asyncio",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
    install_requires=["aiofiles", "httpx", "prettytable", "tqdm"],
    entry_points={  # Optional
        "console_scripts": [
            "compare-forks=github_repo_diff.scripts:entry_point",
        ],
    },
    project_urls={  # Optional
        "Bug Reports": "https://github.com/Wason1797/github-repo-diff/issues",
        "Source": "https://github.com/Wason1797/github-repo-diff",
    },
)
