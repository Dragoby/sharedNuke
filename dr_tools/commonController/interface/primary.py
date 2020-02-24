from dr_tools.CommonQt import QtGui, QtCore


class Main(QtGui.BaseWidget):
    def __init__(self):
        super(Main, self).__init__()

        self.masterLayout = QtGui.QVBoxLayout()

        self.classSelectionDrop = QtGui.QComboBox()
        self.classSelectionItem = QtGui.LabeledWidget('Class:', self.classSelectionDrop)

        self.knobSelectionDrop = QtGui.QComboBox()
        self.knobSelectionItem = QtGui.LabeledWidget('Knob:', self.knobSelectionDrop)

    def initializeDefaults(self):
        pass

    def initializeInterface(self):
        pass

    def initializeSignals(self):
        pass
