import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cnf_process",
    version="0.0.1",
    author="Henry He",
    author_email="hehenry14@gmail.com",
    description="A small package that convert a string of boolean expression into sympy object in the conjunctive "
                "normal form",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hehenry14/cnf_process",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)