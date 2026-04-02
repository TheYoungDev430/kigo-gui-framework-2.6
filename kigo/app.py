# SPDX-License-Identifier: Zlib
# kigo/app.py

from __future__ import annotations
import sys
import time

from kigo.qt.backend import QtCore, QtWidgets, IS_ANDROID
from kigo.android import AndroidLifecycle, is_android


class App:
    """
    Base application class for Kigo.

    - Desktop: PyQt6
    - Android: PySide6
    - Touch-friendly
    - Lifecycle-aware
    """

    def __init__(self, *, dev: bool = False):
        self.dev = dev
        self._last_time = time.perf_counter()

        # ----------------------------------
        # Qt Application
        # ----------------------------------
        self.qt_app = QtWidgets.QApplication.instance()
        if self.qt_app is None:
            self.qt_app = QtWidgets.QApplication(sys.argv)

        # ----------------------------------
        # Android lifecycle
        # ----------------------------------
        self.lifecycle = None
        if is_android():
            self.lifecycle = AndroidLifecycle(self.qt_app)
            self.lifecycle.paused.connect(self.on_pause)
            self.lifecycle.resumed.connect(self.on_resume)

        # ----------------------------------
        # Frame update timer
        # ----------------------------------
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._tick)

    # --------------------------------------------------
    # App lifecycle (override in subclasses)
    # --------------------------------------------------
    def on_start(self):
        """
        Called once when the app starts.
        Override this to build UI.
        """
        pass

    def on_pause(self):
        """
        Android only: app moved to background.
        Override if needed.
        """
        if self.dev:
            print("[Kigo] App paused")

    def on_resume(self):
        """
        Android only: app returned to foreground.
        Override if needed.
        """
        if self.dev:
            print("[Kigo] App resumed")

    def update(self, dt: float):
        """
        Called every frame.
        Override for animations, logic, physics.
        """
        pass

    # --------------------------------------------------
    # Internal loop
    # --------------------------------------------------
    def _tick(self):
        now = time.perf_counter()
        dt = now - self._last_time
        self._last_time = now
        self.update(dt)

    # --------------------------------------------------
    # Run
    # --------------------------------------------------
    def run(self, fps: int = 60):
        """
        Start the application.
        """
        self.on_start()

        interval_ms = int(1000 / max(1, fps))
        self._timer.start(interval_ms)

        if self.dev:
            backend = "PySide6" if IS_ANDROID else "PyQt6"
            platform = "Android" if is_android() else "Desktop"
            print(f"[Kigo] Running on {platform} using {backend}")

        return self.qt_app.exec()
