# -*- coding: utf-8 -*-
"""
Pathlib - cheat-sheet

@author: mdp18js
"""
#https://www.freecodecamp.org/news/how-to-use-pathlib-module-in-python/
#https://realpython.com/python-pathlib/#find-the-last-modified-file

def tree(directory):
    print(f'+ {directory}')
    for path in sorted(directory.rglob('*')):
        depth = len(path.relative_to(directory).parts)
        spacer = '    ' * depth
        print(f'{spacer}+ {path.name}')

tree(pathlib.Path.cwd())

#In Python 3.6 and later it is recommended to use os.fspath() instead of str() if you need to do an explicit conversion. This is a little safer as it will raise an error if you accidently try to convert an object that is not pathlike.

#https://stackoverflow.com/questions/54401973/pythons-pathlib-get-parents-relative-path
import pathlib
>>> path = pathlib.Path(r'C:\users\user1\documents\importantdocuments')
>>> homedir = pathlib.Path(r'C:\users\user1')
>>> str(path.relative_to(homedir))
'documents\\importantdocuments'

#https://towardsthecloud.com/get-relative-path-python

from pathlib import Path
#Getting the home directory
path = Path.home() / 'data' / 'file.txt'
#Getting the current working directory
Path.cwd()
#Working with file names and suffixes
Path('/path/file.suffix').name
Path('/path/file.suffix').stem
Path('/path/file.suffix').suffix

Path(dir_input).is_dir()
Path(dir_input).is_file()

#Making directories
path = Path.home() / 'python-file-paths'
path.mkdir()
path = Path.home() / 'python-file-paths' / 'foo' / 'bar'
path.mkdir(parents=True) # will create parent folders 
path = Path.home() / 'python-file-paths' / 'foo' / 'bar'
path.mkdir(parents=True, exist_ok=True) # will create parent folders and if they do exist the error will be ignored
path = Path.home() / 'python-file-paths' / 'foo' / 'bar' / 'baz.file'
path.parent.mkdir(parents=True, exist_ok=True)

#Reading from text files
path = Path.home() / 'python-file-paths'/ 'samples.data'
data = path.read_text()

#Finding many files recursively
path = Path().home()
paths = [p for p in path.glob('**/*.py') if p.is_file()]

#Finding all directories
path = Path().home()
dirs = [p.name for p in path.iterdir() if p.is_dir()]

#Finding all directories recursively
path = Path().home()
paths = [p for p in path.glob('**/*') if p.is_dir()]

#Remove dirs
from shutil import rmtree
from pathlib import Path
path = Path.home() / 'python-file-paths'
rmtree(path)

#Remove files 
from pathlib import Path
path = Path.home() / 'python-file-paths' / 'data.txt'
path.unlink(missing_ok=True)


p = PurePath('/etc/passwd')
p.is_relative_to('/etc')
True
p.is_relative_to('/usr')
False

p = PurePosixPath('/etc/passwd')
p.relative_to('/')
PurePosixPath('etc/passwd')
p.relative_to('/etc')
PurePosixPath('passwd')
p.relative_to('/usr')



