from __future__ import print_function
from setuptools import setup
# from build_utils import __version__ as VERSION
from build_utils import BuildCommand
from build_utils import PublishCommand
from build_utils import BinaryDistribution
from build_utils import SetGitTag
from build_utils import get_pkg_version


PACKAGE_NAME = 'build_utils'
VERSION = get_pkg_version('build_utils/__init__.py')
BuildCommand.pkg = PACKAGE_NAME
BuildCommand.test = False  # there are no tests
PublishCommand.pkg = PACKAGE_NAME
PublishCommand.version = VERSION
SetGitTag.version = VERSION
README = open('readme.md').read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="Kevin Walchko",
    keywords=['framework', 'python2', 'python3'],
    author_email="walchko@users.noreply.github.com",
    description="Some tools to help build python2/3 source and wheel libraries",
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=['nose', 'twine', 'colorama'],
    url="https://github.com/walchko/{}".format(PACKAGE_NAME),
    long_description=README,
    long_description_content_type='text/markdown',
    packages=[PACKAGE_NAME],
    cmdclass={
        'publish': PublishCommand,
        'make': BuildCommand,
        'git': SetGitTag
    }
)
