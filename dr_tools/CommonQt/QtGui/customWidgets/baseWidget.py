try:
    from PySide2 import QtWidgets as QtGui
except ImportError:
    from PySide import QtGui


class BaseWidget(QtGui.QWidget):
    def __init__(self):
        super(BaseWidget, self).__init__()

        self.initialized = False

    def initialize(self):
        self.initializeInterface()
        self.initializeDefaults()
        self.initializeSignals()
        self.initialized = True

    def initializeInterface(self):
        raise NotImplementedError('This must be overridden to ensure proper initialization')

    def initializeDefaults(self):
        raise NotImplementedError('This must be overridden to ensure proper initialization')

    def initializeSignals(self):
        raise NotImplementedError('This must be overridden to ensure proper initialization')

    def showEvent(self, event):

        if self.initialized is False:
            self.initialize()

        super(BaseWidget, self).showEvent(event)
