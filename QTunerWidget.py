import copy
import os
import sys

from PySide6.QtQuick import QQuickView

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer, QUrl, QObject, Signal, Property


class Rotator(QObject):
    angleChanged = Signal(int)

    def __init__(self):
        QObject.__init__(self)
        self._min_angle = -90
        self._max_angle = 90
        self._angle = self._min_angle

    @Property(int, notify=angleChanged)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        if self._angle != value:
            if value > self._max_angle:
                self._angle = self._max_angle
            elif value < self._min_angle:
                self._angle = self._min_angle
            else:
                self._angle = value
            self.angleChanged.emit(value)


class QTunerWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QTunerWidget, self).__init__(parent)
        qmlFile = QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "main.qml"))
        self._rotator = Rotator()
        self.view = QQuickView()
        self.view.rootContext().setContextProperty("rotate", self._rotator)
        self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.view.setSource(qmlFile)
        print(self.view.errors())
        self.container = self.createWindowContainer(self.view, self)
        self.container.setMinimumSize(300, 175)
        self.container.setMaximumSize(300, 175)
        self.setMinimumSize(300, 175)
        self.setMaximumSize(300, 175)
        self.setFocusPolicy(Qt.TabFocus)

    def Clear(self):
        self.SetAngle(self._rotator._min_angle)

    def Test(self):
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.SetAngle(((self._rotator._angle + 91) % 180) - 90))
        self.timer.setInterval(10)
        self.timer.start()

    def SetAngle(self, angle):
        self._rotator.angle = angle

    def GetAngle(self):
        return self._rotator._angle


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = QTunerWidget()
    form.show()
    sys.exit(app.exec())
