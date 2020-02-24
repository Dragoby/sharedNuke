from dr_tools.CommonQt import QtCore


class Processor(QtCore.QObject):

    __globalInstance = None
    __thread = None

    def __init__(self):
        super(Processor, self).__init__()

    @classmethod
    def globalInstance(cls):

        if cls.__globalInstance is None:
            cls.__globalInstance = cls()
            cls.__thread = QtCore.QThread()
            cls.__globalInstance.moveToThread(cls.__thread)
            cls.__thread.start()

        return cls.__globalInstance
