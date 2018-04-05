from PySide import QtCore, QtGui
import traceback
import nuke
import nukescripts


PANEL = None
STRING_KNOBS = ['file', 'label', 'proxy']


class MySearchReplace(QtGui.QWidget):

    baseSelectItem = 'Select One'

    def __init__(self, parent=None):
        super(MySearchReplace, self).__init__(parent)

        self.masterLayout = QtGui.QVBoxLayout()
        self.controlLayout = QtGui.QHBoxLayout()
        self.optionsLayout = QtGui.QHBoxLayout()

        self.nodeSelectionLabel = QtGui.QLabel('Selection Type')
        self.nodeSelection = QtGui.QComboBox()
        self.classLimitLabel = QtGui.QLabel('Class Limit')
        self.classLimit = QtGui.QComboBox()
        self.executeReplace = QtGui.QPushButton('Replace')
        self.search = QtGui.QLineEdit()
        self.replace = QtGui.QLineEdit()

        self.infoBox = QtGui.QTextEdit()

        self.setLayout(self.masterLayout)
        self.constructLayout()
        self.setInitialValues()
        self.updateClasses()

    def constructLayout(self):

        self.controlLayout.addWidget(self.nodeSelectionLabel)
        self.controlLayout.addWidget(self.nodeSelection)
        self.controlLayout.addWidget(self.classLimitLabel)
        self.controlLayout.addWidget(self.classLimit)
        self.controlLayout.addWidget(self.executeReplace)
        self.controlLayout.addStretch(0)

        self.masterLayout.addLayout(self.controlLayout)
        self.masterLayout.addWidget(self.search)
        self.masterLayout.addWidget(self.replace)
        self.masterLayout.addWidget(self.infoBox)
        self.masterLayout.addStretch(0)

    def setInitialValues(self):

        self.nodeSelection.addItems(['All', 'Selected'])
        self.search.setPlaceholderText('Search')
        self.replace.setPlaceholderText('Replace')
        self.infoBox.setReadOnly(True)
        self.infoBox.setFont(QtGui.QFont('Consolas', 10))

        self.search.textChanged.connect(self.populateInfo)
        self.replace.textChanged.connect(self.populateInfo)
        self.classLimit.currentIndexChanged.connect(self.populateInfo)

        nuke.addOnCreate(lambda: QtCore.QTimer.singleShot(0, self.updateClasses))
        nuke.addOnDestroy(lambda: QtCore.QTimer.singleShot(0, self.updateClasses))

    def updateClasses(self):

        nodes = nuke.allNodes()
        classes = set()

        for node in nodes:
            classes.add(node.Class())

        classes = sorted(list(classes))
        classes.insert(0, self.baseSelectItem)

        self.classLimit.clear()
        self.classLimit.addItems(classes)

    def populateInfo(self):

        classLimit = str(self.classLimit.currentText())
        if classLimit != self.baseSelectItem:
            nodes = nuke.allNodes(classLimit)
        else:
            nodes = nuke.allNodes()
        infoItems = dict()
        for node in nodes:
            nodeItems = dict()
            stringKnobs = findStringKnobs(node)
            for knob, value in stringKnobs.iteritems():
                    if str(self.search.text()) in value:
                        nodeItems[knob] = ['Old: {oldVal}'.format(oldVal=value),
                                           'New: {newVal}'.format(newVal=value.replace(str(self.search.text()),
                                                                                       str(self.replace.text())))]
            if nodeItems:
                infoItems[node.fullName()] = nodeItems

        spacer = max([len(name) for name in infoItems.keys()]) + 1
        space = ' ' * spacer
        message = ''

        for node, value in infoItems.iteritems():

            for idx, values in enumerate(value.values()):
                if idx == 0:
                    smallSpace = ' ' * (spacer - len(node))
                    message += '{name}{smallSpace}{oldVal}\n{space}{newVal}\n'.format(name=node,
                                                                                      smallSpace=smallSpace,
                                                                                      oldVal=values[0],
                                                                                      space=space,
                                                                                      newVal=values[1])
                else:
                    message += '{space}{oldVal}\n{space}{newVal}\n'.format(oldVal=values[0],
                                                                           space=space,
                                                                           newVal=values[1])

            message += '\n\n'

        self.infoBox.setText(message)


def findStringKnobs(node):

    knobs = dict()
    for knob in STRING_KNOBS:

        if not hasKnob(node, knob):
            continue
        knobVal = node[knob].toScript()
        if isinstance(knobVal, str):
            knobs[knob] = knobVal

    return knobs


def hasKnob(node, knob):

    try:
        node[knob]
    except NameError:
        return False
    except StandardError:
        traceback.print_exc()

    return True


def start():

    print __name__
    nukescripts.panels.registerWidgetAsPanel('{0}.MySearchReplace'.format(__name__), 'Search Replace',
                                             'com.thefoundry.NukeTestWindow', True)

