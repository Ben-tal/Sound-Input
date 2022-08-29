import copy
import json
# import queue
# import re
import pyautogui
import sys
import sounddevice as sd
import time as tm
import keyboard
import mouse
import numpy as np
import scipy
from PySide6.QtCore import Signal, QTimer, QEvent, QCoreApplication
# import threading
# from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import QMediaDevices
# from PySide6.QtMultimedia import *
# from PySide6.QtSensors import *
# from PySide6.QtWidgets import *
# from PySide6.QtSerialPort import *
from PySide6.QtWidgets import *
from ui_main import Ui_MainWindow
# import numpy as np
from QTunerWidget import QTunerWidget
from ui_start import Ui_Form

ALL_NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", ]
ALL_NOTES_SORTED = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", ]
NOTE_ANGLE = {"C": 30, "C#": 40, "D": 50, "D#": 60, "E": 70, "F": 90, "F#": 100, "G": 110, "G#": 120, "A": 130,
              "A#": 140, "B": 150}
# ALL_NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", ]
# General settings that can be changed by the user
SAMPLE_FREQ = 44100  # sample frequency in Hz
WINDOW_SIZE = 2 ** 12  # window size of the DFT in samples
WINDOW_STEP = 2 ** 12  # step size of window
NUM_HPS = 5  # max number of harmonic product spectrums
POWER_THRESH = 1e-6  # tuning is activated if the signal power exceeds this threshold
CONCERT_PITCH = 440  # defining a1
WHITE_NOISE_THRESH = 0.2  # everything under WHITE_NOISE_THRESH*avg_energy_per_freq is cut off

WINDOW_T_LEN = WINDOW_SIZE / SAMPLE_FREQ  # length of the window in seconds
SAMPLE_T_LENGTH = 1 / SAMPLE_FREQ  # length between two samples in seconds
DELTA_FREQ = SAMPLE_FREQ / WINDOW_SIZE  # frequency step width of the interpolated DFT
OCTAVE_BANDS = [50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600]

HANN_WINDOW = np.hanning(WINDOW_SIZE)

TYPE_TO_INDEX = {"Keyboard": 3, "Mouse Move": 1, "Mouse Click": 2}


def find_closest_note(pitch):
    """
  This function finds the closest note for a given pitch
  Parameters:
    pitch (float): pitch given in hertz
  Returns:
    closest_note (str): e.g. a, g#, ..
    closest_pitch (float): pitch of the closest note in hertz
  """
    i = int(np.round(np.log2(pitch / CONCERT_PITCH) * 12))
    closest_note = ALL_NOTES[i % 12] + str(4 + (i + 9) // 12)
    closest_pitch = CONCERT_PITCH * 2 ** (i / 12)
    return closest_note, closest_pitch


class StartWindow(QWidget):
    CLOSED_SIGNAL = Signal()

    def __init__(self):
        super(StartWindow, self).__init__(None)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Sound")
        self._settings = {}
        self._table = None
        self.tuner = QTunerWidget()
        self.last_time = None
        self.last_note = None
        self.ui.Layout_IM.addWidget(self.tuner)
        self.inputUpdateTimer = QTimer()
        self.inputUpdateTimer.timeout.connect(self.UpdateAudioInputInfo)
        self.inputUpdateTimer.start(2000)
        self.ui.comboBox.currentIndexChanged.connect(lambda index: self.ChangeInputDevice(index))
        self.hide()
        self.modifiers = []
        self.currentSoundInput = None
        self._WINDOW_SAMPLE = [0 for _ in range(WINDOW_SIZE)]
        self._NOTE_BUFFER = ["1", "2"]
        self.ui.pushButton.clicked.connect(lambda: self.close())
        font = self.ui.label.font()
        font.setPointSize(16)
        self.ui.label.setFont(font)
        self.raise_()
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

    def Set(self, settings: dict):
        self._settings = settings
        if not self._table:
            self._table = QTableWidget()
            self._table.setColumnCount(3)
            self._table.setHorizontalHeaderLabels(["Type", "Key", "Value"])
            self._table.horizontalHeader().setStretchLastSection(True)
            self.SetTable()
            self.ui.verticalLayout.addWidget(self._table)
        else:
            self._table.setRowCount(0)
            self._table.clearContents()
            self.SetTable()

    def SetTable(self):
        for _key, (_type, _value) in self._settings.items():
            self._table.insertRow(self._table.rowCount())
            self._table.setItem(self._table.rowCount() - 1, 0, QTableWidgetItem(_type))
            self._table.setItem(self._table.rowCount() - 1, 1, QTableWidgetItem(_key))
            self._table.setItem(self._table.rowCount() - 1, 2, QTableWidgetItem(_value))

    def hideEvent(self, arg__1):
        super(StartWindow, self).hideEvent(arg__1)
        # if self.currentSoundInput:
        #     self.currentSoundInput.close()
        # self.CLOSED_SIGNAL.emit()

    def closeEvent(self, arg__1):
        self.ui.comboBox.clear()
        self.ui.comboBox.setPlaceholderText("Input Devices")
        if self.currentSoundInput:
            self.currentSoundInput.close()
        self.currentSoundInput = None
        self.ui.label.clear()
        self.tuner.Clear()
        self.CLOSED_SIGNAL.emit()
        super(StartWindow, self).closeEvent(arg__1)

    def UpdateAudioInputInfo(self):

        # audioInput = QMediaDevices.audioInputs()
        ll = sd.query_hostapis(0).get("devices")
        # print(sd.query_hostapis(0))
        # print([i for i in audioInput])
        audioInput = sd.query_devices()
        l = []
        for p, i in enumerate(audioInput):
            if i["max_input_channels"] > 0 and p in ll:
                l.append((p, i))
        audioInput = l
        if len(audioInput) < self.ui.comboBox.count():
            for i in range(len(audioInput), len(audioInput) - self.ui.comboBox.count()):
                self.ui.comboBox.removeItem(i)
        for i, AudioDevice in enumerate(audioInput):
            if i >= self.ui.comboBox.count():
                self.ui.comboBox.addItem(f"{AudioDevice[0]}, {AudioDevice[1]['name']}")
            else:
                self.ui.comboBox.setItemText(i, f"{AudioDevice[0]}, {AudioDevice[1]['name']}")
            self.ui.comboBox.setItemData(i, int(AudioDevice[0]), Qt.UserRole + 1)

    def callback(self, indata, frames, time, status):
        def ReleaseLastKey():
            last_key = self._settings.get(self.last_note)
            if not last_key:
                return
            if last_key[0] == "Mouse Click":
                pyautogui.mouseUp(button=last_key[1])
            elif last_key[0] == "Keyboard":
                pyautogui.keyUp(last_key[1].lower())

        def HandleNote(note):
            _ = self._settings.get(note, None)
            if not _:
                return
            if _[0] == "Mouse Click":
                if self.last_note and self.last_note != note:
                    ReleaseLastKey()
                    mouse.press(_[1].lower())
                    self.last_note = note
                elif not self.last_note:
                    mouse.press(_[1].lower())
                    self.last_note = note
                self.last_time = tm.time()
            elif _[0] == "Mouse Move":
                movePos = eval(_[1])
                pyautogui.move(movePos[0], movePos[1], movePos[2],)
            elif _[0] == "Keyboard":
                if self.last_note and self.last_note != note:
                    ReleaseLastKey()
                    pyautogui.keyDown(_[1].lower())
                    self.last_note = note
                elif not self.last_note:
                    pyautogui.keyDown(_[1].lower())
                    self.last_note = note
                self.last_time = tm.time()

        def callback(indata, frames, time, status):
            # define static variables

            if self.last_time and tm.time() - self.last_time > 0.1 and self.last_note:
                ReleaseLastKey()
                self.last_note = None
            elif self.last_note:
                last_key = self._settings.get(self.last_note)
                if last_key[0] == "Mouse Click" and mouse.is_pressed(last_key[1]):
                    pyautogui.mouseDown(button=last_key[1].lower())
                elif last_key[0] == "Keyboard" and keyboard.is_pressed(last_key[1]):
                    pyautogui.keyDown(last_key[1].lower())

            if status:
                return
            if any(indata):
                self._WINDOW_SAMPLE = np.concatenate((self._WINDOW_SAMPLE, indata[:, 0]))  # append new samples
                self._WINDOW_SAMPLE = self._WINDOW_SAMPLE[len(indata[:, 0]):]  # remove old samples

                # skip if signal power is too low
                signal_power = (np.linalg.norm(self._WINDOW_SAMPLE, ord=2) ** 2) / len(self._WINDOW_SAMPLE)
                if signal_power < POWER_THRESH:
                    print("No Input")
                    return

                # avoid spectral leakage by multiplying the signal with a hann window
                hann_samples = self._WINDOW_SAMPLE * HANN_WINDOW
                magnitude_spec = abs(scipy.fftpack.fft(hann_samples)[:len(hann_samples) // 2])

                # supress mains hum, set everything below 62Hz to zero
                for i in range(int(62 / DELTA_FREQ)):
                    magnitude_spec[i] = 0

                # calculate average energy per frequency for the octave bands
                # and suppress everything below it
                for j in range(len(OCTAVE_BANDS) - 1):
                    ind_start = int(OCTAVE_BANDS[j] / DELTA_FREQ)
                    ind_end = int(OCTAVE_BANDS[j + 1] / DELTA_FREQ)
                    ind_end = ind_end if len(magnitude_spec) > ind_end else len(magnitude_spec)
                    avg_energy_per_freq = (np.linalg.norm(magnitude_spec[ind_start:ind_end], ord=2) ** 2) / (
                            ind_end - ind_start)
                    avg_energy_per_freq = avg_energy_per_freq ** 0.5
                    for i in range(ind_start, ind_end):
                        magnitude_spec[i] = magnitude_spec[i] if magnitude_spec[
                                                                     i] > WHITE_NOISE_THRESH * avg_energy_per_freq else 0

                # interpolate spectrum
                mag_spec_ipol = np.interp(np.arange(0, len(magnitude_spec), 1 / NUM_HPS),
                                          np.arange(0, len(magnitude_spec)),
                                          magnitude_spec)
                mag_spec_ipol = mag_spec_ipol / np.linalg.norm(mag_spec_ipol, ord=2)  # normalize it

                hps_spec = copy.deepcopy(mag_spec_ipol)

                # calculate the HPS
                for i in range(NUM_HPS):
                    tmp_hps_spec = np.multiply(hps_spec[:int(np.ceil(len(mag_spec_ipol) / (i + 1)))],
                                               mag_spec_ipol[::(i + 1)])
                    if not any(tmp_hps_spec):
                        break
                    hps_spec = tmp_hps_spec

                max_ind = np.argmax(hps_spec)
                max_freq = max_ind * (SAMPLE_FREQ / WINDOW_SIZE) / NUM_HPS

                closest_note, closest_pitch = find_closest_note(max_freq)
                max_freq = round(max_freq, 1)
                closest_pitch = round(closest_pitch, 1)

                self._NOTE_BUFFER.insert(0, closest_note)  # note that this is a ringbuffer
                self._NOTE_BUFFER.pop()

                if self._NOTE_BUFFER.count(self._NOTE_BUFFER[0]) == len(self._NOTE_BUFFER) and (
                        63 < closest_pitch < 1050):
                    print(f"Closest note: {closest_note} {max_freq}/{closest_pitch}")
                    HandleNote(closest_note)
                    return closest_note
                else:
                    print(f"Closest note: ...")
            else:
                print('no input')

        _note = callback(indata, frames, time, status)
        if _note:
            self.tuner.SetAngle(NOTE_ANGLE.get(_note[:-1]) - 90)
            if self.ui.label.text() != _note:
                self.SetNote(_note)

    def SetNote(self, _note):
        self.ui.label.setText(_note)
        if _note in self._settings.keys():
            self._table: QTableWidget
            # self._table.item(1, 2).setBackground(QColor(125, 125, 125))

    def ClearTuner(self):
        self.tuner.SetAngle(-90)

    def ChangeInputDevice(self, index):

        if self.currentSoundInput:
            self.currentSoundInput.close(True)
        self.currentSoundInput = sd.InputStream(channels=1, device=self.ui.comboBox.itemData(index, Qt.UserRole + 1),
                                                samplerate=SAMPLE_FREQ, blocksize=WINDOW_STEP,
                                                callback=self.callback)
        self.currentSoundInput.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(parent=None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Sound")
        self.ui.frame.hide()
        self.ui.frame_3.hide()
        self.ComboChange()
        self.ui.NoteComboBox.currentIndexChanged.connect(lambda: self.ui.comboBox.setEnabled(True))
        self.ui.comboBox.setCurrentIndex(-1)
        self.ui.comboBox.currentIndexChanged.connect(self.ComboChange)
        self.ui.comboBox.setDisabled(True)
        self.HideAllFrames()
        self.ui.Slider.valueChanged.connect(lambda: self.ui.ValueSlider.setValue(self.ui.Slider.value()))
        self.ui.ValueSlider.valueChanged.connect(lambda: self.ui.Slider.setValue(self.ui.ValueSlider.value()))
        self.GenerateAllNotesBetween("C1", "C6")
        # for i in range(2, 7):
        #     for NOTE in ALL_NOTES_SORTED:
        #         self.ui.NoteComboBox.addItem(NOTE + str(i))
        self.ui.Add.clicked.connect(self.Add)
        self.ui.label.hide()

        # self.ui.label.setPixmap(
        #     QPixmap("1.png").scaled(self.ui.label.width(), self.ui.label.height(), Qt.KeepAspectRatio))
        # self.ui.label.setAlignment(Qt.AlignCenter)
        self.ui.Export.clicked.connect(self.Export)
        self.ui.Import.clicked.connect(self.Import)
        self.ui.keySequence.keySequenceChanged.connect(self.KeySeq)
        self.StartWindow = StartWindow()
        self.StartWindow.CLOSED_SIGNAL.connect(lambda: self.show())
        self.ui.Start.clicked.connect(self.Start)

    def GenerateAllNotesBetween(self, _from, _to):
        note_f, scale_f = _from[:-1], _from[-1]
        note_t, scale_t = _to[:-1], _to[-1]
        # print(note_f, scale_f)
        # print(note_t, scale_t)
        final = []
        for i in ALL_NOTES_SORTED[ALL_NOTES_SORTED.index(note_f):]:
            self.ui.NoteComboBox.addItem(i + scale_f)
            final.append(i + scale_f)
        for i in range(int(scale_f) + 1, int(scale_t)):
            for NOTE in ALL_NOTES_SORTED:
                self.ui.NoteComboBox.addItem(NOTE + str(i))
        for i in ALL_NOTES_SORTED[:ALL_NOTES_SORTED.index(note_t) + 1]:
            self.ui.NoteComboBox.addItem(i + scale_t)
        return final

    def _ValidateInScale(self, _list):
        octave = int(_list[0][-1])
        i = ALL_NOTES_SORTED.index(_list[0][:-1])
        for note in _list:
            if ALL_NOTES_SORTED[i] + str(octave) != note:
                return False
            i += 1
            if i == len(ALL_NOTES_SORTED):
                octave += 1
                i = i % len(ALL_NOTES_SORTED)
        return True

    def Start(self):
        self.StartWindow.Set(self.GetTableInfo())
        self.StartWindow.show()
        self.hide()

    def KeySeq(self, keySequence: QKeySequence):
        keys = (keySequence.toString().split(", "))
        if len(keys) > 1:
            self.ui.keySequence.setKeySequence(QKeySequence(keys[0]))
            return

    def GetTableInfo(self):
        _dict = {}
        for row in range(self.ui.table.rowCount()):
            # item(row, 0) Returns the item for the given row and column if one has been set; otherwise returns nullptr.
            # self.ui.table.item(row, column).setTextAlignment(Qt.AlignCenter)
            _type = self.ui.table.item(row, 0).text()
            _key = self.ui.table.item(row, 1).text()
            _value = self.ui.table.item(row, 2).text()
            _dict.update({_key: (_type, _value)})
        return _dict

    def Export(self):
        # rowCount() This property holds the number of rows in the table
        _dict = self.GetTableInfo()
        name = QFileDialog.getSaveFileName(None, "Export", "export", "*.json")[0]
        if not name:
            return
        with open(name, 'w+') as f:
            json.dump(_dict, f)

    def Import(self):
        name = QFileDialog.getOpenFileName(None, "Import", "", "*.json")[0]
        if not name:
            return
        with open(name, 'r') as f:
            _dict = json.load(f)
        self.ui.table.clearContents()
        self.ui.table.setRowCount(0)
        for key, value in _dict.items():
            self.SetNewTableRow(value[0], key, value[1])

    def CheckNoteExist(self):
        for row in range(self.ui.table.rowCount()):
            if self.ui.table.item(row, 1).text() == self.ui.NoteComboBox.currentText():
                return True
        return False

    def Add(self):
        note = self.ui.NoteComboBox.currentText()
        if self.CheckNoteExist():
            QMessageBox.warning(self, "Warning", "This note already exist")
            return
        index = self.ui.comboBox.currentIndex()
        data = ""
        if index == 0:
            # Mouse
            duration = 0.05
            value = self.ui.Slider.value()
            position_Y = 0
            position_X = 0
            if self.ui.comboBox_2.currentText() == "Up":
                position_Y = -value
            elif self.ui.comboBox_2.currentText() == "Down":
                position_Y = value
            elif self.ui.comboBox_2.currentText() == "Left":
                position_X = -value
            elif self.ui.comboBox_2.currentText() == "Right":
                position_X = value
            data = str((position_X, position_Y, duration))
        elif index == 1:
            # Mouse Click
            data = self.ui.comboBox_3.currentText().split(" ")[0].lower()
        elif index == 2:
            # Keyboard
            data = self.ui.keySequence.keySequence().toString()
        else:
            return
        self.SetNewTableRow(self.ui.comboBox.currentText(), note, data)

    def SetNewTableRow(self, *args):
        self.ui.table.insertRow(self.ui.table.rowCount())
        for i, arg in enumerate(args):
            self.ui.table.setItem(self.ui.table.rowCount() - 1, i, QTableWidgetItem(arg))

    def HideAllFrames(self):
        self.ui.frame.hide()
        self.ui.frame_3.hide()
        self.ui.frame_5.hide()

    def ComboChange(self):
        self.HideAllFrames()
        if self.ui.comboBox.currentText() == "Mouse Move":
            self.ui.frame.show()
        elif self.ui.comboBox.currentText() == "Keyboard":
            self.ui.frame_3.show()
        elif self.ui.comboBox.currentText() == "Mouse Click":
            self.ui.frame_5.show()
        else:
            return


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
