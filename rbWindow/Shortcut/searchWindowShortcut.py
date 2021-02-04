import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from fontParts.world import *
from uitestcode import menuWindow

menuWindow.popSearchWindow(menuWindow)