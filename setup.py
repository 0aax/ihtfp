from setuptools import setup


setup(
    name='ihtfp',
    version='0.0.1',
    url='https://github.com/0aax/ihtfp',
    author='Audrey X.',
    author_email='ahx@mit.edu',
    license='MIT',
    py_modules=['ihtfp'],
    entry_points={'console_scripts': ['ihtfp=ihtfp:main']}
)