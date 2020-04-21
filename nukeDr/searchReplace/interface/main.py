import nuke

from ...CommonQt import QtGui, QtCore
from ..logic import utilities


class Main(QtGui.BaseWidget):

    _globalInstance = None
    requestUpdate = QtCore.Signal(dict)

    def __init__(self):
        super(Main, self).__init__()

        self.masterLayout = QtGui.QVBoxLayout()

        self.topLayout = QtGui.QVBoxLayout()
        self.lowerLayout = QtGui.QVBoxLayout()
        self.upperWidget = QtGui.QWidget()

        self.optionsLayout = QtGui.QHBoxLayout()
        self.searchForLayout = QtGui.QHBoxLayout()

        self.selectionTypeDrop = QtGui.QComboBox()
        self.selectionTypeItem = QtGui.LabeledWidget('Process:', self.selectionTypeDrop)

        self.currentClasses = set()
        self.classLimitDrop = QtGui.QComboBox()
        self.classLimitItem = QtGui.LabeledWidget('Class Limit:', self.classLimitDrop)

        self.currentClass = None
        self.currentKnobs = set()
        self.knobSelectionDrop = QtGui.QComboBox()
        self.knobSelectionItem = QtGui.LabeledWidget('Knob:', self.knobSelectionDrop)
        self.replaceButton = QtGui.QPushButton('Replace')

        self.searchForLine = QtGui.QLineEdit()
        self.useRegexCheck = QtGui.QCheckBox('Use Regex')
        self.caseSensitiveCheck = QtGui.QCheckBox('Case Sensitive')
        self.replaceWithLine = QtGui.QLineEdit()

        self.splitter = QtGui.QSplitter()
        self.infoBox = QtGui.QTextEdit()

        self.blockTimer = False
        self.checkTimer = QtCore.QTimer()
        self.updater = QtCore.UpdateTimer()

    def initializeDefaults(self):
        """
        This will set all of the initial values for all of the widgets
        """
        self.setWindowTitle('Search Replace')
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.selectionTypeDrop.addItems(['All', 'Selected'])

        self.searchForLine.setPlaceholderText('Search For:')
        self.replaceWithLine.setPlaceholderText('Replace With:')
        self.updateControls()

        self.selectionTypeDrop.setStyleSheet("QComboBox { combobox-popup: 0; }");
        self.classLimitDrop.setStyleSheet("QComboBox { combobox-popup: 0; }");
        self.classLimitDrop.setMinimumWidth(100)
        self.knobSelectionDrop.setMinimumWidth(100)
        self.knobSelectionDrop.setStyleSheet("QComboBox { combobox-popup: 0; }");

        # This is here to ensure that the info box is a mono spaced one =====
        font = QtGui.QFont('unexistent')
        font.setStyleHint(QtGui.QFont.Monospace)
        self.infoBox.setFont(font)
        # ====================================================================
        self.infoBox.setReadOnly(True)
        self.caseSensitiveCheck.setChecked(True)

        self.updater.updateInterval = 2
        self.updater.updateIntervalUnits = QtCore.UpdateTimer.SECONDS
        self.updater.start()

    def initializeSignals(self):
        """
        This will connect all of the initial signals.
        """
        self.searchForLine.textChanged.connect(self.processReplace)
        self.replaceWithLine.textChanged.connect(self.processReplace)
        self.selectionTypeDrop.currentIndexChanged.connect(self.processReplace)
        self.classLimitDrop.currentIndexChanged.connect(self.processReplace)
        self.knobSelectionDrop.currentIndexChanged.connect(self.processReplace)
        self.useRegexCheck.stateChanged.connect(self.processReplace)
        self.caseSensitiveCheck.stateChanged.connect(self.processReplace)
        self.searchForLine.editingFinished.connect(lambda: self.processReplace(resetTimer=False))
        self.replaceWithLine.editingFinished.connect(lambda: self.processReplace(resetTimer=False))
        self.checkTimer.timeout.connect(lambda: self.processReplace(resetTimer=False))

        self.replaceButton.pressed.connect(self.replaceValues)

        self.updater.timerComplete.connect(self.updateControls)

    def initializeInterface(self):
        """
        This will add all of the widgets to the layout and set the layout
        """
        self.setLayout(self.masterLayout)

        self.optionsLayout.addWidget(self.selectionTypeItem)
        self.optionsLayout.addWidget(self.classLimitItem)
        self.optionsLayout.addWidget(self.knobSelectionItem)
        self.optionsLayout.addStretch(1)
        self.optionsLayout.addWidget(self.replaceButton)
        self.topLayout.addLayout(self.optionsLayout)

        self.searchForLayout.addWidget(self.searchForLine)
        self.searchForLayout.addWidget(self.caseSensitiveCheck)
        self.searchForLayout.addWidget(self.useRegexCheck)
        self.topLayout.addLayout(self.searchForLayout)

        self.topLayout.addWidget(self.replaceWithLine)
        self.topLayout.addWidget(self.infoBox)
        self.upperWidget.setLayout(self.topLayout)

        self.splitter.addWidget(self.upperWidget)

        self.masterLayout.addWidget(self.splitter)

    def updateControls(self):

        self.selectionTypeDrop.blockSignals(True)
        self.classLimitDrop.blockSignals(True)
        self.knobSelectionDrop.blockSignals(True)
        selected = self.selectionTypeDrop.currentText() == 'Selected'
        nodeData = utilities.getNodeData(selected=selected)
        # This is here so we always have an all option in the class list
        nodeData['All'] = list()

        if nodeData.keys() != self.currentClasses:
            self.currentClasses = list(nodeData.keys())
            self.classLimitDrop.clear()
            self.classLimitDrop.addItems(sorted(self.currentClasses, key=lambda c: utilities.getClassSortIndex(c)))

        if self.classLimitDrop.currentText() != self.currentClass:

            if self.classLimitDrop.currentText() != 'All':
                knobs = nodeData.get(self.classLimitDrop.currentText(), list())
                if self.currentKnobs != set(knobs):
                    self.knobSelectionDrop.clear()
                    self.knobSelectionDrop.addItems(sorted(knobs, key=lambda knob: utilities.getKnobSortIndex(knob)))
            else:
                knobs = set()
                for knobList in nodeData.values():
                    knobs = knobs.union(set(knobList))

                if self.currentKnobs != set(knobs):
                    self.knobSelectionDrop.clear()
                    self.knobSelectionDrop.addItems(sorted(list(knobs),
                                                           key=lambda knob: utilities.getKnobSortIndex(knob)))

            self.currentKnobs = set(knobs)
            self.currentClass = self.classLimitDrop.currentText()

        self.selectionTypeDrop.blockSignals(False)
        self.classLimitDrop.blockSignals(False)
        self.knobSelectionDrop.blockSignals(False)

    def processReplace(self, resetTimer=True):

        # anything that calls this should have reset time as true so we dont get a million updates
        # Only when editing is finished this should be reset timer as false ie: editingFinished
        if self.blockTimer:
            return

        if resetTimer and self.checkTimer.isActive():
            self.checkTimer.start(500)
            return False

        if resetTimer:
            self.checkTimer.start(500)
        else:
            self.checkTimer.stop()

        if self.selectionTypeDrop.currentText() == 'Selected':
            nodes = nuke.selectedNodes()
        else:
            nodes = nuke.allNodes()

        if self.classLimitDrop.currentText() != 'All':
            nodes = [node for node in nodes if node.Class() == self.classLimitDrop.currentText()]

        messageItems = list()

        for node in nodes:
            replacementInfo = utilities.getReplacementInfo(node,
                                                           knobName=str(self.knobSelectionDrop.currentText()),
                                                           searchFor=str(self.searchForLine.text()),
                                                           replaceWith=str(self.replaceWithLine.text()),
                                                           useRegex=self.useRegexCheck.isChecked(),
                                                           caseSensitive=self.caseSensitiveCheck.isChecked())

            original = replacementInfo.get('colouredOriginalValue', None)
            new = replacementInfo.get('colouredNewValue', None)
            error = replacementInfo.get('error', None)
            name = node.name()

            if error:
                messageItem = '{name} - Error: {error}'.format(name=name, error=error)
                messageItems.append(messageItem)
                continue

            if not all([original, new]):
                continue

            space = utilities.SPACE_CHARACTER * len(name)
            messageItem = '{name} - Old: {old}<br>{space} - New: {new}'.format(name=name,
                                                                               old=original,
                                                                               space=space,
                                                                               new=new)
            messageItems.append(messageItem)

        message = '<br><br>'.join(messageItems)
        self.infoBox.setHtml(message)

    def replaceValues(self):

        if self.selectionTypeDrop.currentText() == 'Selected':
            nodes = nuke.selectedNodes()
        else:
            nodes = nuke.allNodes()

        if self.classLimitDrop.currentText() != 'All':
            nodes = [node for node in nodes if node.Class() == str(self.classLimitDrop.currentText())]

        utilities.replaceValues(nodes,
                                [str(self.knobSelectionDrop.currentText())],
                                str(self.searchForLine.text()),
                                str(self.replaceWithLine.text()),
                                self.useRegexCheck.isChecked(),
                                self.caseSensitiveCheck.isChecked())

        self.processReplace()

    @classmethod
    def globalInstance(cls):
        if cls._globalInstance is None:
            cls._globalInstance = cls()

        return cls._globalInstance
