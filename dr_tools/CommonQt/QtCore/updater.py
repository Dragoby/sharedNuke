from PySide2 import QtCore


class UpdateTimer(QtCore.QObject):

    SECONDS = 'sef'
    MILLISECONDS = 'mil'
    MINUTES = 'min'

    TIME_CONVERSION = {MINUTES: 60000.0,
                       SECONDS: 1000.0,
                       MILLISECONDS: 1.0}

    timerComplete = QtCore.Signal()

    def __init__(self, interval=None, units=None):
        super(UpdateTimer, self).__init__()

        self.updateInterval = interval or 1
        self.updateIntervalUnits = units or self.SECONDS
        self.setTimer(self.updateInterval, self.updateIntervalUnits)
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(lambda: self.timerComplete.emit())

    def setTimer(self, interval, units):
        """
        This will set the duration of the timer and appropriately convert the interval to the given units
        Args:
            interval (int|float): This is the duration in which the timer will run for
            units (str): This is the units that the interval will be processed with ie: sec, min, etc
        """
        self.updateIntervalUnits = units
        self.updateInterval = interval * self.TIME_CONVERSION.get(self.updateIntervalUnits, self.SECONDS)

    @property
    def isRunning(self):
        return self.timer.isActive()

    def start(self):
        """
        This will start the timer
        """
        self.timer.start(self.updateInterval)

    def stop(self):
        """
        This will stop the timer
        """
        self.timer.stop()


class NodeFinder(QtCore.QObject):
    def __init__(self):
        super(NodeFinder, self).__init__()

        self.checkTimer = QtCore.QTimer()

        self.checkTimer.timeout.connect(lambda: self.findNodes(resetTimer=False))

    def findNodes(self, resetTimer=True):

        # anything that calls this should have reset time as true so we dont get a million updates
        # Only when editing is finished this should be reset timer as false ie: editingFinished
        if resetTimer and self.checkTimer.isActive():
            self.checkTimer.start(500)
            return False

        if resetTimer:
            self.checkTimer.start(500)
        else:
            self.checkTimer.stop()

        if resetTimer:
            pass
        # Do update to widget here

