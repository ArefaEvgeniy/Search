#!/usr/bin/env python3
"""
Code in file search.py find files and directories on computer by name.
You can use symbols '?' or symbols '*' in name for search.
In search instead symbols '?' can will be any symbol.
In the search, instead of the "?" symbol, there can be any character.
In the search, instead of the "*" symbol, there can be any number of
characters.
Also, the code in the file can find any part of the text in the text
of the found files.
"""

import sys
import os
import re
import time

from PyQt5.QtWidgets import (  # pylint: disable=E0611
    QMainWindow, QWidget, QMessageBox, QPushButton, QComboBox, QTextEdit,
    QLabel, QLineEdit, QCheckBox, QRadioButton, QHBoxLayout, QVBoxLayout,
    QGroupBox, QDesktopWidget, QApplication, QStyleFactory, QFileDialog,
    QSpinBox
)
from PyQt5.QtCore import QTimer, pyqtSignal  # pylint: disable=E0611

import const


class ListDir():
    """
    Class to save paths of files and directories.
    Class work as iterator.
    Read path delete from the class list.
    Unlike an iterator, new paths can be added to the class list.
    """
    def __init__(self, items=None):
        if isinstance(items, (str, int, float)):
            self.items = [items]
        elif isinstance(items, list):
            self.items = items[:]
        else:
            self.items = []

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.items) > 0:
            return self.items.pop()
        else:
            raise StopIteration

    def append(self, directory):
        """
        Method saves new subdirectories and files from input directory.
        The subdirectories are saved first, and then the files.
        Thus, in the next iteration, the files will first be removed from
        the class list and only then the subdirectories will be checked.
        This is done so that at any time the list is of the minimum size
        and there is no memory overflow.
        :param directory: input directory
        """
        try:
            new_objects = os.listdir(directory)
            if new_objects:
                new_objects.sort(reverse=True)
                for name in new_objects:
                    self.items.append(os.path.join(directory, name))
        except PermissionError:
            pass


class Main(QMainWindow):
    """
    Class to show main window with Status Bar
    """
    def __init__(self):
        super().__init__()
        self.field = None
        self.statusbar = None
        self.initUI()

    def initUI(self):  # pylint: disable=C0103
        """
        Init UI: Status Bar, main widget, size and orientation of main window
        """
        self.field = Field(self)
        self.setCentralWidget(self.field)

        self.statusbar = self.statusBar()
        self.field.compareStatusbar[str].connect(self.statusbar.showMessage)

        screen = QDesktopWidget().screenGeometry()
        width = screen.width() / 6 * 5
        height = screen.height() / 6 * 5
        self.resize(width, height)
        self.move(width / 10, height / 10)

        self.setWindowTitle(const.NAME_TITLE)

    def closeEvent(self, event):  # pylint: disable=C0103
        """
        Before close main window ask 'Are you sure to quit?'
        """
        reply = QMessageBox.question(
            self, const.NAME_MESSAGE, const.NAME_QUESTION,
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class Field(QWidget):
    """
    Class of main widget to work
    """
    compareStatusbar = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.counter_result = 0
        self.settings_box = None
        self.find_file_name = None
        self.find_object = None
        self.select_dir = None
        self.find_path = None
        self.find_subdir = None
        self.find_start = None
        self.find_stop = None
        self.list_dir = None
        self.find_file = False
        self.find_dir = False
        self.find_text = False
        self.label_symbols = False
        self.number_symbols = False
        self.label_text = None
        self.file_text = None
        self.start_time = None
        self.pattern_text = None
        self.case_buttons = []
        self.initUI()

    def initUI(self):  # pylint: disable=C0103
        """
        Init UI: Settings Bar and field to show of result
        """
        QApplication.setStyle(QStyleFactory.create('Windows'))
        QApplication.setPalette(QApplication.style().standardPalette())

        self.init_settings()
        self.show_field = QTextEdit()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_list_dir)
        self.timer.start(0.1)

        h_box = QHBoxLayout()
        h_box.addWidget(self.settings_box, 0)
        h_box.addWidget(self.show_field, 3)

        self.setLayout(h_box)

    def keyPressEvent(self, event):  # pylint: disable=C0103
        """
        Analyze events of keys to start search if user introduced text
        for search and pressed "ENTER" key
        :param event: input key event to analyze
        """
        res = None
        if event.key() == const.KEY_ENTER:
            if self.find_object.currentText() == const.VARIANTS_OBJECTS[-1]:
                if self.find_file_name.text() and self.file_text.text():
                    res = True
            else:
                if self.find_file_name.text():
                    res = True
        if res:
            self.start_find()

    def box_find_file(self):
        """
        Init settings to find file
        """
        self.find_file_name = QLineEdit()
        self.find_file_name.textChanged.connect(self.check_input_text)
        self.find_object = QComboBox()
        self.find_object.addItems(const.VARIANTS_OBJECTS)
        self.find_object.activated.connect(self.show_hide_text_settings)

    def box_find_text(self):
        """
        Init settings to find text
        :return: two horizontal boxes of these settings
        """
        self.label_text = QLabel(const.NAME_SEARCH_TEXT)
        self.label_text.setDisabled(True)
        self.file_text = QLineEdit()
        self.file_text.setDisabled(True)
        self.file_text.textChanged.connect(self.check_input_text)
        self.label_symbols = QLabel(const.NAME_SYMBOLS)
        self.label_symbols.setDisabled(True)
        self.number_symbols = QSpinBox()
        self.number_symbols.setDisabled(True)
        self.number_symbols.setMinimum(1)
        self.number_symbols.setFixedWidth(40)

        h_box_1 = QHBoxLayout()
        h_box_1.addWidget(self.label_text)
        h_box_1.addWidget(self.file_text)
        h_box_1.addStretch(1)

        h_box_2 = QHBoxLayout()
        h_box_2.addWidget(self.label_symbols)
        h_box_2.addWidget(self.number_symbols)
        h_box_2.addStretch(1)

        return h_box_1, h_box_2

    def box_select_dir(self):
        """
        Init settings to select directory
        :return: horizontal box of these settings
        """
        label_path = QLabel(const.NAME_SELECT_DIR)
        self.select_dir = QPushButton('+', self)
        self.select_dir.clicked.connect(self.browse_folder)
        self.find_path = QLabel(os.path.abspath(os.curdir))

        self.find_subdir = QCheckBox(const.NAME_FIND_SUBDIR, self)
        self.find_subdir.setChecked(True)

        h_box = QHBoxLayout()
        h_box.addWidget(label_path, 5)
        h_box.addWidget(self.select_dir)

        return h_box

    def box_select_case(self):
        """
        Init settings to ignore of case for search or no
        """
        for name_item in const.VARIANTS_CASE:
            case_button = QRadioButton(name_item)
            self.case_buttons.append(case_button)
        if len(self.case_buttons) > 0:
            self.case_buttons[0].setChecked(True)

    def box_buttons(self):
        """
        Init buttons to start or stop of search
        :return: horizontal box of these buttons
        """
        self.find_start = QPushButton(const.NAME_START, self)
        self.find_start.setFont(const.BOLD_FONT)
        self.find_start.setCheckable(True)
        self.find_start.setDisabled(True)
        self.find_start.clicked.connect(self.start_find)

        self.find_stop = QPushButton(const.NAME_STOP, self)
        self.find_stop.setFont(const.BOLD_FONT)
        self.find_stop.setDisabled(True)
        self.find_stop.clicked.connect(self.get_stop)

        h_box = QHBoxLayout()
        h_box.addStretch(1)
        h_box.addWidget(self.find_start)
        h_box.addWidget(self.find_stop)
        h_box.addStretch(1)

        return h_box

    def init_settings(self):
        """
        Init all settings
        """
        self.settings_box = QGroupBox(const.NAME_SETTINGS)

        self.box_find_file()
        box_text, box_symbols = self.box_find_text()
        box_dir = self.box_select_dir()
        self.box_select_case()
        box_buttons = self.box_buttons()

        v_box = QVBoxLayout()
        v_box.setSpacing(5)
        v_box.addWidget(self.find_file_name)
        v_box.addWidget(self.find_object)
        v_box.addStretch(1)
        v_box.addLayout(box_text)
        v_box.addLayout(box_symbols)
        v_box.addStretch(1)
        v_box.addLayout(box_dir)
        v_box.addWidget(self.find_path)
        v_box.addStretch(1)
        v_box.addWidget(self.find_subdir)
        v_box.addStretch(1)
        for case_button in self.case_buttons:
            v_box.addWidget(case_button)
        v_box.addStretch(10)
        v_box.addLayout(box_buttons)

        self.settings_box.setLayout(v_box)

    def show_hide_text_settings(self):
        """
        Show or hide settings for searching text in a file
        depending on the search mode
        """
        value = not bool(self.find_object.currentText() ==
                         const.VARIANTS_OBJECTS[-1])
        self.label_text.setDisabled(value)
        self.file_text.setDisabled(value)
        self.label_symbols.setDisabled(value)
        self.number_symbols.setDisabled(value)
        self.check_input_text()

    def check_input_text(self):
        """
        Show or hide settings for searching text in a file
        depending on the search mode
        """
        if self.find_object.currentText() == const.VARIANTS_OBJECTS[-1]:
            value = not(self.find_file_name.text() and self.file_text.text())
        else:
            value = not bool(self.find_file_name.text())
        self.find_start.setDisabled(value)

    def browse_folder(self):
        """
        Call dialog window to set directory for search
        Before call need to set timer speed 1 ms, because dialog window
        will not work on speed less than 1 ms.
        After call need to set usual timer speed - 0,1 ms
        """
        self.timer.start(1)
        directory = QFileDialog.getExistingDirectory(self, const.SELECT_DIR,
                                                     self.find_path.text())
        if directory:
            self.find_path.setText(directory)
        self.timer.start(0.1)

    def check_list_dir(self):
        """
        Start process if list for search is not empty
        """
        if self.list_dir:
            self.process()

    def check_file_name(self, value):
        """
        Compare name of file or directory with pattern for search
        :param value: name of file or directory for compare
        :return: True if name and pattern match or False
        """
        res = False
        value = value.split('/')[-1]
        pattern = self.find_file_name.text()
        for item in const.VARIANTS_REPLACE:
            pattern = pattern.replace(item[0], item[1])
        flags = re.I if self.case_buttons[1].isChecked() else 0
        found_value = re.match(pattern, value, flags=flags)
        if found_value:
            if found_value.group(0) == value:
                res = True
        return res

    @staticmethod
    def load_file(file_name, max_symbols):
        """
        Load text from file
        :param file_name: name of file
        :param max_symbols: number symbols to load from file
        :return: return text from file
        """
        try:
            with open(file_name) as open_file:
                res = open_file.read(max_symbols)
        except (EnvironmentError, UnicodeDecodeError):
            res = None
        return res

    def check_text(self, file_name):
        """
        Find pattern in text from input file
        :param file_name: name of input file
        :return: starting index of the matched text or None
        """
        res = None
        max_symbols = int(self.number_symbols.text()) * 1000
        value = self.load_file(file_name, max_symbols)
        if value:
            flags = re.I if self.case_buttons[1].isChecked() else 0
            found_value = re.search(self.pattern_text, value, flags=flags)
            if found_value:
                res = found_value.start()
        return res

    def process(self):
        """
        Process to find file or text.
        One entry in the search list is checked in one cycle and if search is
        successful, a record about this is added to the field with the result.
        This entry is removed from the search list.
        If this entry is a directory and the search in subdirectories
        is enabled, then files and subdirectories from this directory
        are added to the search list.
        If search list is empty, stop search and a record of time search and
        number of result is added to the field with the result.
        """
        res = None
        try:
            next_value = next(self.list_dir)
            if os.path.isdir(next_value) and self.find_subdir.isChecked():
                self.compareStatusbar.emit(next_value)
                self.list_dir.append(next_value)

            if (os.path.isfile(next_value) and self.find_file) or \
                    (os.path.isdir(next_value) and self.find_dir):
                if self.check_file_name(next_value):
                    res = const.RES_FILE.format(next_value)

            elif self.find_text and os.path.isfile(next_value):
                if self.check_file_name(next_value):
                    found_index = self.check_text(next_value)
                    if self.check_text(next_value):
                        res = const.RES_TEXT.format(next_value, found_index)

            if res:
                self.counter_result += 1
                self.show_field.insertPlainText(res)

        except StopIteration:
            self.list_dir = None
            self.find_start.setChecked(False)
            self.find_stop.setDisabled(True)
            self.show_field.insertPlainText('\n' + '-' * 50)
            self.show_field.insertPlainText(const.ACTION_LASTED.format(
                str(round(float(time.time() - self.start_time), 2)),
                str(self.counter_result))
            )

    def start_find(self):
        """
        Search start according to settings (pressed "Search..." buttons
        or pressed "ENTER" key after input name file to search or/and
        text to search)
        """
        self.start_time = time.time()
        self.counter_result = 0
        variants = const.VARIANTS_OBJECTS
        self.show_field.setText('')
        self.find_file = False
        self.find_dir = False
        self.find_text = False
        self.list_dir = ListDir()

        if self.find_object.currentText() in (variants[0], variants[2]):
            self.find_file = True
        if self.find_object.currentText() in (variants[1], variants[2]):
            self.find_dir = True
        if self.find_object.currentText() == variants[-1]:
            self.find_text = True
            self.pattern_text = self.file_text.text()
            for item in const.VARIANTS_REPLACE:
                self.pattern_text = self.pattern_text.replace(item[0], item[1])

        result_text = const.FIRST_LINE_TEXT.format(self.file_text.text()) \
            if self.find_text else ''
        subdirs = const.SUBDIR_ON \
            if self.find_subdir.isChecked() else const.SUBDIR_OFF
        self.show_field.insertPlainText(
            const.FIRST_LINE.format(result_text, self.find_file_name.text(),
                                    self.find_path.text(), subdirs)
        )

        self.list_dir.append(self.find_path.text())
        self.find_stop.setDisabled(False)

        if self.list_dir:
            self.process()
        else:
            self.show_field.insertPlainText('\n' + '-' * 50)
            self.show_field.insertPlainText(const.DIR_EMPTY)

    def get_stop(self):
        """
        Search stop (pressed "STOP" buttons)
        """
        self.list_dir = None
        self.find_start.setChecked(False)
        self.find_stop.setDisabled(True)


if __name__ == '__main__':
    app = QApplication([])
    compare = Main()
    compare.show()
    sys.exit(app.exec_())
