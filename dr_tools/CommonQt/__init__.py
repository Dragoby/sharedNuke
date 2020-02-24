try:
    from PySide2 import *
except ImportError:
    from PySide import QtCore
    from PySide import *

del globals()['QtGui']
del globals()['QtWidgets']
del globals()['QtCore']

from . import QtGui
from . import QtCore
