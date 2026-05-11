import os
from src import interface_core
from src import interface_gui

dir = os.path.dirname(__file__)
cwd = os.getcwd()

if dir != cwd:
    os.chdir(dir)

interface_gui.begin_interface()
exit(0)