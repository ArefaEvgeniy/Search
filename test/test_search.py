import os
import time
import pytest

from PyQt5.QtWidgets import QDesktopWidget

import conftest
import search
import const


class TestListDir():

    @staticmethod
    @pytest.mark.parametrize('value', conftest.values_init_list_dir)
    def test_init(value):
        list_dir = search.ListDir(value)

        if not isinstance(value, (list, str, int, float)) or value == []:
            assert list_dir.items == []
            with pytest.raises(StopIteration):
                next(list_dir)

        elif isinstance(value, list):
            value.reverse()
            for item in value:
                assert item == next(list_dir)
            with pytest.raises(StopIteration):
                next(list_dir)

        else:
            assert list_dir.items == [value]
            assert next(list_dir) == value
            with pytest.raises(StopIteration):
                next(list_dir)

    @staticmethod
    def test_iter():
        list_dir = search.ListDir()
        assert list_dir == iter(list_dir)

        list_dir = search.ListDir([1, 2, 3])
        assert list_dir == iter(list_dir)

    @staticmethod
    def test_next():
        list_dir = search.ListDir()
        with pytest.raises(StopIteration):
            next(list_dir)

        value = [1, 2, 3, 'a', 'b']
        list_dir = search.ListDir(value)
        value.reverse()
        for item in value:
            assert item == next(list_dir)
        with pytest.raises(StopIteration):
            next(list_dir)

    @staticmethod
    def test_append(init_files_directories):
        list_dir = search.ListDir()
        list_dir.append(init_files_directories)
        assert len(list_dir.items) == 4
        for index in range(2):
            assert list_dir.items[index].split('/')[-1] in ('dir_1', 'dir_2')
        for index in range(2, 4):
            assert list_dir.items[index].split('/')[-1] in ('1.txt', '2.csv')

        list_dir.append(init_files_directories.join('dir_2'))
        assert len(list_dir.items) == 9
        for index in range(2):
            assert list_dir.items[index].split('/')[-1] in ('dir_1', 'dir_2')
        for index in range(2, 4):
            assert list_dir.items[index].split('/')[-1] in ('1.txt', '2.csv')
        for index in range(4, 7):
            assert list_dir.items[index].split('/')[-1] \
                   in ('dir_2_1', 'dir_2_2', 'dir_2_3')
        for index in range(7, 9):
            assert list_dir.items[index].split('/')[-1] in ('1.py', '2.py')


class TestMain():

    @staticmethod
    def test_initUI(qtbot):
        main_widget = search.Main()
        screen = QDesktopWidget().screenGeometry()
        assert main_widget.windowTitle() == const.NAME_TITLE
        assert main_widget.width() == int(screen.width() / 6 * 5)
        assert main_widget.height() == int(screen.height() / 6 * 5)


class TestField():

    @staticmethod
    def test_initUI(qtbot):
        main_widget = search.Main()
        widget = search.Field(main_widget)
        assert widget.counter_result == 0
        assert widget.find_file_name.text() == ''
        assert widget.find_object.currentText() == const.VARIANTS_OBJECTS[0]
        assert widget.find_path.text() == os.path.abspath(os.curdir)
        assert widget.find_subdir.isChecked() is True
        assert widget.list_dir is None
        assert widget.find_file is False
        assert widget.find_dir is False
        assert widget.find_text is False
        assert widget.label_symbols.text() == const.NAME_SYMBOLS
        assert widget.number_symbols.text() == '1'
        assert widget.label_text.text() == const.NAME_SEARCH_TEXT
        assert widget.file_text.text() == ''
        assert widget.start_time is None
        assert widget.pattern_text is None
        assert len(widget.case_buttons) == 2
        assert widget.case_buttons[0].text() == const.CASE_SENSITIVE
        assert widget.case_buttons[1].text() == const.CASE_IGNORE

    @staticmethod
    def test_show_hide_text_settings():
        main_widget = search.Main()
        widget = search.Field(main_widget)
        assert widget.find_object.currentText() == const.VARIANTS_OBJECTS[0]
        assert widget.label_text.isEnabled() is False
        assert widget.file_text.isEnabled() is False
        assert widget.label_symbols.isEnabled() is False
        assert widget.number_symbols.isEnabled() is False

        widget.find_object.setCurrentIndex(len(const.VARIANTS_OBJECTS)-1)
        widget.show_hide_text_settings()
        assert widget.find_object.currentText() == const.VARIANTS_OBJECTS[-1]
        assert widget.label_text.isEnabled() is True
        assert widget.file_text.isEnabled() is True
        assert widget.label_symbols.isEnabled() is True
        assert widget.number_symbols.isEnabled() is True

        widget.find_object.setCurrentIndex(len(const.VARIANTS_OBJECTS) - 2)
        widget.show_hide_text_settings()
        assert widget.find_object.currentText() == const.VARIANTS_OBJECTS[-2]
        assert widget.label_text.isEnabled() is False
        assert widget.file_text.isEnabled() is False
        assert widget.label_symbols.isEnabled() is False
        assert widget.number_symbols.isEnabled() is False

    @staticmethod
    @pytest.mark.parametrize('values', conftest.values_check_input_text)
    def test_check_input_text(values):
        main_widget = search.Main()
        widget = search.Field(main_widget)
        assert widget.find_object.currentText() == const.VARIANTS_OBJECTS[0]
        assert widget.find_file_name.text() == ''
        assert widget.file_text.text() == ''
        assert widget.find_start.isEnabled() is False

        widget.find_file_name.setText(values[0])
        widget.file_text.setText(values[1])
        widget.find_object.setCurrentIndex(values[2])

        widget.check_input_text()
        assert widget.find_start.isEnabled() is values[-1]

    @staticmethod
    @pytest.mark.parametrize('values', conftest.values_check_file_name)
    def test_check_file_name(values):
        main_widget = search.Main()
        widget = search.Field(main_widget)
        widget.find_file_name.setText(values[0])
        widget.case_buttons[1].setChecked(values[1])
        assert widget.check_file_name(values[2]) == values[-1]

    @staticmethod
    @pytest.mark.parametrize('values', conftest.values_load_file)
    def test_load_file(values, init_files_directories):
        main_widget = search.Main()
        widget = search.Field(main_widget)
        full_name = os.path.join(str(init_files_directories), str(values[0]))
        assert widget.load_file(full_name, values[1]) == values[-1]

    @staticmethod
    @pytest.mark.parametrize('values', conftest.values_check_text)
    def test_check_text(values, init_files_directories):
        main_widget = search.Main()
        widget = search.Field(main_widget)
        full_name = os.path.join(str(init_files_directories), str(values[0]))
        widget.pattern_text = values[1]
        widget.case_buttons[1].setChecked(values[2])
        assert widget.check_text(full_name) == values[-1]

    @staticmethod
    @pytest.mark.parametrize('values', conftest.values_process)
    def test_process(values, init_files_directories):
        main_widget = search.Main()
        widget = search.Field(main_widget)
        assert widget.list_dir is None
        assert widget.show_field.toPlainText() == ''
        assert widget.find_stop.isEnabled() is False

        widget.start_time = time.time()
        widget.find_file_name.setText(values[0])
        widget.pattern_text = values[1]
        widget.list_dir = search.ListDir()
        widget.list_dir.append(str(init_files_directories))
        widget.find_stop.setDisabled(False)
        widget.find_file = values[2]
        widget.find_dir = values[3]
        widget.find_text = values[4]
        widget.find_subdir.setChecked(values[5])

        for index in range(values[6]):
            widget.process()

        result = widget.show_field.toPlainText()

        for item in values[-1]:
            assert item in result

        if values[-2] is not None:
            assert 'Found: {}'.format(values[-2]) in result
            assert widget.list_dir is None
            assert widget.find_stop.isEnabled() is False
        else:
            assert widget.list_dir is not None
            assert widget.find_stop.isEnabled() is True

    @staticmethod
    @pytest.mark.parametrize('values', conftest.values_start_find)
    def test_start_find(values, init_files_directories):
        main_widget = search.Main()
        widget = search.Field(main_widget)
        assert widget.list_dir is None
        assert widget.show_field.toPlainText() == ''

        widget.find_file_name.setText(values[0])
        widget.file_text.setText(values[1])
        widget.find_path.setText(str(init_files_directories))

        widget.start_find()
        res_1 = values[-2].format('', values[0], str(init_files_directories),
                                  const.SUBDIR_ON)
        full_name = os.path.join(str(init_files_directories), values[2])
        res_2 = values[-1].format(full_name) if values[-1] else values[-1]
        assert widget.list_dir is not None
        assert widget.show_field.toPlainText() == res_1 + res_2

    @staticmethod
    def test_get_stop(qtbot, mocker, init_files_directories):
        main_widget = search.Main()
        widget = search.Field(main_widget)

        def mock_check_input_text(self):
            widget.find_start.setDisabled(False)

        def mock_start_find(self):
            widget.start_time = time.time()
            widget.list_dir = search.ListDir()
            widget.list_dir.append(str(init_files_directories))
            widget.find_start.setChecked(True)
            self.find_stop.setDisabled(False)

        mocker.patch('search.Field.check_input_text', mock_check_input_text)
        mocker.patch('search.Field.start_find', mock_start_find)
        assert widget.list_dir is None
        assert widget.show_field.toPlainText() == ''
        assert widget.find_start.isEnabled() is False
        assert widget.find_start.isChecked() is False
        assert widget.find_stop.isEnabled() is False

        widget.check_input_text()
        assert widget.find_start.isEnabled() is True
        assert widget.find_start.isChecked() is False
        assert widget.find_stop.isEnabled() is False

        widget.start_find()
        assert widget.list_dir is not None
        assert widget.find_start.isEnabled() is True
        assert widget.find_start.isChecked() is True
        assert widget.find_stop.isEnabled() is True

        widget.get_stop()
        assert widget.list_dir is None
        assert widget.find_start.isEnabled() is True
        assert widget.find_start.isChecked() is False
        assert widget.find_stop.isEnabled() is False
