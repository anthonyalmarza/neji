from neji import __version__
import errno
import os
import sys
from setuptools import setup, find_packages


def file_name(rel_path):
    dir_path = os.path.dirname(__file__)
    return os.path.join(dir_path, rel_path)


def read(rel_path):
    with open(file_name(rel_path)) as f:
        return f.read()


def readlines(rel_path):
    with open(file_name(rel_path)) as f:
        ret = f.readlines()
    return ret


def mkdir_p(path):
    "recreate mkdir -p functionality"
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

share_path = os.path.join(
    os.path.dirname(sys.executable),
    'share/neji'
)

mkdir_p(share_path)

setup(
    author="Anthony Almarza",
    author_email="anthony.almarza@gmail.com",
    name="neji",
    packages=find_packages(),
    version=__version__,
    url="https://github.com/anthonyalmarza/neji",
    download_url=(
        "https://github.com/anthonyalmarza/neji/tarball/"
        "v"+__version__+"-beta"
    ),
    description="Making the twisted web a little bit easier",
    # long_description=read('docs/long_desc.rst'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords=["twisted", "async", "web framework"],
    scripts=['scripts/ng', ],
    install_requires=readlines('requirements'),
    extras_require={
        'mongo': ['pymongo', ],
        'redis': ['redis', ]
    }
)
