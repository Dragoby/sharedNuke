from dr_tools.CommonQt import QtGui, QtCore


class Main(QtGui.BaseWidget):
    def __init__(self):
        super(Main, self).__init__()

        self.masterLayout = QtGui.QVBoxLayout()

    def initializeDefaults(self):
        pass

    def initializeSignals(self):
        pass

    def initializeInterface(self):

        self.setLayout(self.masterLayout)
