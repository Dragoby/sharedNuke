try:
    from PySide2.QtGui import  *
    from PySide2.QtWidgets import  *
except ImportError:
    from PySide.QtGui import *

from .customWidgets.baseWidget import BaseWidget
from .customWidgets.labeledWidget import LabeledWidget