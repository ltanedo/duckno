from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="duckno",
    version="0.1.0",
    author="ltanedo",
    author_email="ltanedo@users.noreply.github.com",
    description="Treat DuckDB as a tiny NoSQL-style key/value store",
    url="https://github.com/ltanedo/duckno",
    license="MIT",
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    py_modules=["duckno"],
    install_requires=["duckdb"],
    keywords=["duckdb", "nosql", "key-value", "kv-store", "database", "storage"],
    classifiers=["Development Status :: 3 - Alpha", "Intended Audience :: Developers", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent", "Programming Language :: Python :: 3", "Programming Language :: Python :: 3.8", "Programming Language :: Python :: 3.9", "Programming Language :: Python :: 3.10", "Programming Language :: Python :: 3.11", "Programming Language :: Python :: 3.12", "Topic :: Software Development :: Libraries :: Python Modules", "Topic :: Utilities"],
    project_urls={"Bug Reports": "https://github.com/ltanedo/duckno/issues","Source": "https://github.com/ltanedo/duckno","Documentation": "https://github.com/ltanedo/duckno#readme"},
    long_description=long_description,
    packages=find_packages(),
)
