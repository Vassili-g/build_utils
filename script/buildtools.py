#!/usr/bin/env python
##############################################################################
# The MIT License (MIT)
#
# Copyright (c) 2017 Kevin J. Walchko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
##############################################################################
# WTF:
# I am breaking this out of my pip package as a script, because I think it might
# work better this way ... we will see.
####
import os
import sys
from colorama import Fore, Back, Style
from shutil import rmtree, copyfileobj
import shutil
from os import path
import urllib
import urllib.request

def update_script():
    """
    This will pull the latest verison from my git repo and keep things current.

    Oh God why are you doing this ... long story, but I hate to have to install
    something before I can use the pip command on a brand new system. This is my
    solution ... let's see how well it works.
    """
    url = "https://raw.githubusercontent.com/walchko/build_utils/master/script/buildtools.py"
    filename = "buildtools.py"
    os.system(f'rm -f {filename}')
    try:
        with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
            copyfileobj(response, out_file)
        print(f">> {response.code}")
        # urllib.request.urlretrieve(url,"buildtools.py")
    except urllib.error.HTTPError as e:
        print(f">> {e}")
    os.system(f'chmod a+x {filename}')

# from psutils
def get_pkg_version(relfile):
    """
    Given a relative path to a file, this searches it and returns the version
    string. The nice thing about this, it doesn't execute any python code when
    it searches. This is an issues during setup when I have C extensions that
    have not been compiled yet, but python code looks for the library (which
    is not built yet).
    import build_utils as bu
    bu.get_pkg_version('build_utils/__init__.py')
    "0.2.0"
    """
    pkg = path.abspath(relfile)
    with open(pkg, 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                ret = eval(line.strip().split(' = ')[1])
                assert ret.count('.') == 2, ret
                for num in ret.split('.'):
                    assert num.isdigit(), ret
                return ret
        raise ValueError("couldn't find version string")

class BuildCommand:
    """Build binaries/packages"""
    pkg = None
    version = None
    test = True     # run tests
    py2 = False     # build python 2 package
    py3 = True      # build python 3 package
    rm_egg = False  # rm egg-info directory
    rm_so = False   # rm shared library, this is for c extensions

    def __init__(self, name):
        self.pkg = name
        self.version = get_pkg_version(f"{self.pkg}/__init__.py")

    def cprint(self, color, msg):
        print(color + msg + Style.RESET_ALL)

    def rmdir(self, folder):
        try:
            rmtree(folder)
            self.cprint(Fore.RED, ">> Deleted Folder {}".format(folder))
        except OSError:
            pass

    def rm(self, file):
        try:
            os.system('rm -f {}'.format(file))
            self.cprint(Fore.RED, ">> Deleted File {}".format(file))
        except OSError:
            pass

    def build(self):
        if not self.pkg or not self.version:
            raise Exception('BuildCommand::pkg is not set')

        print(Fore.BLUE + '+----------------------------------')
        print(f'| Package: {self.pkg}')
        print(f"| Version: {self.version}")
        print('+----------------------------------')
        print('| Python 2: tests & build: {}'.format(self.py2))
        print('| Python 3: tests & build: {}'.format(self.py3))
        print('+----------------------------------\n\n' + Style.RESET_ALL)

        pkg = self.pkg
        self.cprint(Fore.RED, 'Delete dist directory and clean up binary files')
        self.cprint(Fore.RED, '-----------------------------------------------')

        self.rmdir('dist')
        self.rmdir('build')
        self.rmdir('.eggs')
        if self.rm_egg:
            self.rmdir(f'{pkg}.egg-info')
        if self.rm_so:
            self.rm('*.so')
            self.rm(f'{pkg}/*.so')
        self.rm('{}/*.pyc'.format(pkg))
        self.rmdir('{}/__pycache__'.format(pkg))
        self.cprint(Fore.RED, '-----------------------------------------------\n\n')

        if self.test:
            print(Fore.YELLOW + 'Run Nose tests')
            if self.py2:
                ret = os.system("unset PYTHONPATH; python2 -m nose -w tests -v test.py")
                if ret > 0:
                    self.cprint(Fore.WHITE + Back.RED, '<<< Python2 nose tests failed >>>')
                    return
            if self.py3:
                ret = os.system("unset PYTHONPATH; python3 -m nose -w tests -v test.py")
                if ret > 0:
                    self.cprint(Fore.WHITE + Back.RED, '<<< Python3 nose tests failed >>>')
                    return

        print(Style.RESET_ALL + '\nBuilding packages ...')
        print(Fore.WHITE + Back.MAGENTA + '\n>> Python source ----------------------------------------------' + Fore.MAGENTA + Back.RESET)
        os.system("unset PYTHONPATH; python setup.py sdist")
        if self.py2:
            print(Fore.WHITE + Back.CYAN +'\n>> Python 2 Wheel ---------------------------------------------------'+ Fore.CYAN + Back.RESET)
            os.system("unset PYTHONPATH; python2 setup.py bdist_wheel")
        else:
            print(Fore.WHITE + Back.CYAN +'\n*** Skipping Python 2 ***'+Style.RESET_ALL)
        if self.py3:
            print(Fore.WHITE + Back.BLUE + '\n>> Python 3 Wheel ---------------------------------------------------' + Fore.BLUE + Back.RESET)
            os.system("unset PYTHONPATH; python3 setup.py bdist_wheel")
        else:
            print(Fore.WHITE + Back.BLUE +'\n*** Skipping Python 3 ***'+Style.RESET_ALL)

        print("---------------------------------------------------" + Style.RESET_ALL)

    def set_git_tag(self):
        """Set version tag on github"""

        if self.version is None:
            raise Exception("set_git_tag needs version set to something")

        print('Pushing git tags')
        os.system(f'git tag v{self.version}')
        os.system('git push --tags')

    def publish(self):
        """Publish to Pypi"""
        if not self.pkg or not self.version:
            raise Exception('publish: pkg or version is not set')

        print('Publishing to PyPi ...')
        os.system(f"unset PYTHONPATH; twine upload dist/{self.pkg}-{self.version}*")

if __name__ == "__main__":
    update_script()
#     b = BuildCommand("mdh")
#     b.build()
