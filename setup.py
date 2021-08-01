from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='ihtfp',
    version='0.1',
    description="Mood tracker using IHTFP meanings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/0aax/ihtfp',
    author='Audrey X.',
    author_email='ahx@mit.edu',
    license='MIT',

    packages = find_packages(),
    package_data={'ihtfp': ['data/*.json']},
    entry_points ={'console_scripts': ['ihtfp=ihtfp.ihtfp:main']},

    install_requires=['numpy', 'matplotlib'],
    zip_safe = False
)