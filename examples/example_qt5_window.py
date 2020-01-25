""" Example for PyQt5 windows with pysg scene graph renderer."""
import sys
import time

import numpy as np
from PyQt5 import QtOpenGL, QtWidgets, QtCore


class WindowInfo:
    def __init__(self):
        self.size = (0, 0)
        self.mouse = (0, 0)
        self.wheel = 0
        self.time = 0
        self.ratio = 1.0
        self.viewport = (0, 0, 0, 0)
        self.keys = np.full(256, False)
        self.old_keys = np.copy(self.keys)

    def key_down(self, key):
        return self.keys[key]

    def key_pressed(self, key):
        return self.keys[key] and not self.old_keys[key]

    def key_released(self, key):
        return not self.keys[key] and self.old_keys[key]


class ExampleWindow(QtOpenGL.QGLWidget):
    def __init__(self, size, title):
        fmt = QtOpenGL.QGLFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        fmt.setSwapInterval(1)
        fmt.setSampleBuffers(True)
        fmt.setDepthBufferSize(24)

        super(ExampleWindow, self).__init__(fmt, None)
        self.setFixedSize(size[0], size[1])
        self.move(QtWidgets.QDesktopWidget().rect().center() - self.rect().center())
        self.setWindowTitle(title)

        self.start_time = time.process_time()
        self.example = lambda: None
        self.ex = None

        self.wnd = WindowInfo()
        self.wnd.viewport = (0, 0) + (size[0] * self.devicePixelRatio(), size[1] * self.devicePixelRatio())
        self.wnd.ratio = size[0] / size[1]
        self.wnd.size = size

    def keyPressEvent(self, event):
        # Quit when ESC is pressed
        if event.key() == QtCore.Qt.Key_Escape:
            QtCore.QCoreApplication.instance().quit()

        self.wnd.keys[event.nativeVirtualKey() & 0xFF] = True

    def keyReleaseEvent(self, event):
        self.wnd.keys[event.nativeVirtualKey() & 0xFF] = False

    def mouseMoveEvent(self, event):
        self.wnd.mouse = (event.x(), event.y())

    def wheelEvent(self, event):
        self.wnd.wheel += event.angleDelta().y()

    def paintGL(self):
        if self.ex is None:
            self.ex = self.example()
        self.wnd.time = time.process_time() - self.start_time
        self.ex.update()
        self.wnd.old_keys = np.copy(self.wnd.keys)
        self.wnd.wheel = 0
        self.update()


def run_example(example):
    """ Execute example with PyQt5 window.

    Important! Route all exceptions to exception hook.
    Otherwise only error is shown in PyQt.
    See https://stackoverflow.com/questions/18740884/preventing-pyqt-to-silence-exceptions-occurring-in-slots
    """
    def exception_hook(exctype, value, traceback):
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys._excepthook = sys.excepthook
    sys.excepthook = exception_hook

    app = QtWidgets.QApplication([])
    widget = ExampleWindow(example.WINDOW_SIZE, getattr(example, 'WINDOW_TITLE', example.__name__))
    example.wnd = widget.wnd
    widget.example = example
    widget.show()
    app.exec_()
    del app


class Example:
    WINDOW_SIZE = (1280, 720)
    wnd = None  # type: WindowInfo

    def update(self):
        raise NotImplementedError()
