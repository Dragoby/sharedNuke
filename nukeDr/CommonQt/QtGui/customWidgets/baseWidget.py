import logging

try:
    from PySide2 import QtWidgets as QtGui
except ImportError:
    from PySide import QtGui


class BaseWidget(QtGui.QWidget):
    def __init__(self):
        super(BaseWidget, self).__init__()

        self.initialized = False

    def __initialize(self):
        """
        This is used to initialize the widget (self) by calling all of the individual initialization methods
        """
        logging.info('Starting initialization of widget')
        logging.info('Initializing interface')
        self.initializeInterface()
        logging.info('Interface initialized')
        logging.info('Initializing defaults')
        self.initializeDefaults()
        logging.info('Defaults initialized')
        logging.info('Initializing signals')
        self.initializeSignals()
        logging.info('Signals initialized')
        self.initialized = True
        logging.info('Initialization of widget complete')

    def initializeInterface(self):
        """
        This is used to add all of the widgets to the main layout and set all interface items. This must be overridden
        """
        raise NotImplementedError('This must be overridden to ensure proper initialization')

    def initializeDefaults(self):
        """
        This will set all of the initial values for all of the widgets and self.  This must be overridden
        """
        raise NotImplementedError('This must be overridden to ensure proper initialization')

    def initializeSignals(self):
        """
        This will connect all of the signals for all widgets and self.  This must be overridden
        """
        raise NotImplementedError('This must be overridden to ensure proper initialization')

    def showEvent(self, event):
        """
        This is overridden to ensure that we initialize the widget before it is shown
        """
        if self.initialized is False:
            self.__initialize()

        super(BaseWidget, self).showEvent(event)
