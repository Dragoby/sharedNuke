from dr_tools.CommonQt import QtGui


class ChannelKnob(QtGui.BaseWidget):
    def __init__(self):
        super(ChannelKnob, self).__init__()

        self.channelSelection = QtGui.QComboBox()

    def initializeInterface(self):
        pass

    def initializeSignals(self):
        pass

    def initializeDefaults(self):
        pass
