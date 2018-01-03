from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = [line.strip() for line in f]

setup(
    name = 'Exchanges',
    version = '0.0.1',
    author = 'Victor Reyes',
    author_email = 'vreyes@protonmail.com',
    description = '',
    long_description = open('README.rst').read(),
    license = "GPL",
    url = 'https://github.com/vreyesd/Exchanges',
    packages = find_packages(),
    install_requires=install_requires,
    python_requires='>=3'
)
