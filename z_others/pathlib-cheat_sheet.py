# -*- coding: utf-8 -*-
"""
Pathlib - cheat-sheet

@author: mdp18js
"""

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


