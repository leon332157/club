## python setup.py py2exe --windows

from distutils.core import setup
import py2exe  # http://starship.python.net/crew/theller/py2exe/

setup(name='webcam-watcher',
      scripts=['webcam-watcher.py'],
      data_files=[('.', ['webcam-watcher.ini', 'retrieving.png', 'error.png', 'cam.png', 'README.txt'])
                  ]
      )

import os

os.system(r'deltree /y build')
os.system(r'deltree /y dist\webcam-watcher\tcl')
os.system(r'del dist\webcam-watcher\_imagingtk.pyd')
# ~ os.system(r'del dist\webcam-watcher\_tkinter.pyd')
# ~ os.system(r'del dist\webcam-watcher\tcl83.dll')
# ~ os.system(r'del dist\webcam-watcher\tk83.dll')
os.system(r'del dist\webcam-watcher\win32api.pyd')
