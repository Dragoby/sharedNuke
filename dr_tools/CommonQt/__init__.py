try:
    from PySide2 import QtCore
    from PySide2 import *
except ImportError:
    from PySide import QtCore
    from PySide import *

del globals()['QtGui']
del globals()['QtWidgets']

from . import QtGui
