from setuptools import setup, find_packages

with open('tcpping2/__init__.py') as fp:
    for line in fp:
        if line.startswith('__version__'):
            __version__ = line.split('=')[1].strip(" \"'\r\n")
            break
    else:
        from tcpping2 import __version__


def read_long_description():
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except(IOError, ImportError, RuntimeError):
        return ""


setup(
    name='tcpping2',
    version=__version__,
    author='Anton Tuchak',
    author_email='anton.tuchak@gmail.com',
    long_description=read_long_description(),
    url='https://github.com/atuchak/tcpping',
    description='Non-privileged TCP ping implementation using raw socket.',
    license='MIT',
    keywords='non-privileged python tcp ping',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "Topic :: System"
    ]
)
