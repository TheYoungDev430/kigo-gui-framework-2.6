# kigo/android/lifecycle.py
from kigo.qt.backend import QtCore
from kigo.android.platform import is_android


class AndroidLifecycle(QtCore.QObject):
    paused = QtCore.Signal()
    resumed = QtCore.Signal()

    def __init__(self, app):
        super().__init__()
        self.app = app

        if is_android():
            app.applicationStateChanged.connect(self._on_state)

    def _on_state(self, state):
        if state == QtCore.Qt.ApplicationState.ApplicationSuspended:
            self.paused.emit()
        elif state == QtCore.Qt.ApplicationState.ApplicationActive:
            self.resumed.emit()