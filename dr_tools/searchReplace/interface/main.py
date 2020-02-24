from dr_tools.CommonQt import QtGui, QtCore


class Main(QtGui.BaseWidget):
    def __init__(self):
        super(Main, self).__init__()

        self.masterLayout = QtGui.QVBoxLayout()

        self.topLayout = QtGui.QVBoxLayout()
        self.lowerLayout = QtGui.QVBoxLayout()
        self.upperWidget = QtGui.QWidget()

        self.optionsLayout = QtGui.QHBoxLayout()
        self.searchForLayout = QtGui.QHBoxLayout()

        self.selectionTypeDrop = QtGui.QComboBox()
        self.selectionTypeItem = QtGui.LabeledWidget('Select:', self.selectionTypeDrop)
        self.classLimitDrop = QtGui.QComboBox()
        self.classLimitItem = QtGui.LabeledWidget('Class:', self.classLimitDrop)
        self.knobSelectionDrop = QtGui.QComboBox()
        self.knobSelectionItem = QtGui.LabeledWidget('Knob:', self.knobSelectionDrop)
        self.replaceButton = QtGui.QPushButton('Replace')

        self.searchForLine = QtGui.QLineEdit()
        self.useRegexCheck = QtGui.QCheckBox('Use Regex')
        self.replaceWithLine = QtGui.QLineEdit()

        self.splitter = QtGui.QSplitter()
        self.infoBox = QtGui.QTextEdit()
        self.progressBar = QtGui.QProgressBar()

    def initializeDefaults(self):

        self.setWindowTitle('Search Replace')
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.selectionTypeDrop.addItems(['All', 'Selected'])
        self.progressBar.setMaximumHeight(20)

        self.searchForLine.setPlaceholderText('Search For:')
        self.replaceWithLine.setPlaceholderText('Replace With:')

    def initializeSignals(self):
        pass

    def initializeInterface(self):

        self.setLayout(self.masterLayout)

        self.optionsLayout.addWidget(self.selectionTypeItem)
        self.optionsLayout.addWidget(self.classLimitItem)
        self.optionsLayout.addWidget(self.knobSelectionItem)
        self.optionsLayout.addStretch(1)
        self.optionsLayout.addWidget(self.replaceButton)
        self.topLayout.addLayout(self.optionsLayout)

        self.searchForLayout.addWidget(self.searchForLine)
        self.searchForLayout.addWidget(self.useRegexCheck)
        self.topLayout.addLayout(self.searchForLayout)

        self.topLayout.addWidget(self.replaceWithLine)
        self.topLayout.addWidget(self.infoBox)
        self.upperWidget.setLayout(self.topLayout)

        self.splitter.addWidget(self.upperWidget)
        self.splitter.addWidget(self.progressBar)

        self.masterLayout.addWidget(self.splitter)
