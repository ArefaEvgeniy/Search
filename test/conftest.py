import pytest

import const


@pytest.fixture()
def init_files_directories(tmpdir):
    dir_1 = tmpdir.mkdir('dir_1')
    file_1_dir_1 = dir_1.join('1_1.txt')
    file_1_dir_1.write('Test file "1_1.txt" in subdir "dir_1"')
    file_1 = tmpdir.join('1.txt')
    file_1.write('Test file "1.txt" in main dir')
    file_2 = tmpdir.join('2.csv')
    file_2.write('Test file "2.csv" in main dir')
    dir_2 = tmpdir.mkdir('dir_2')
    file_1_dir_2 = dir_2.join('1.py')
    file_1_dir_2.write('Test file "1.py" in subdir "dir_2"')
    file_2_dir_2 = dir_2.join('2.py')
    file_2_dir_2.write('Test file "2.py" in subdir "dir_2"')
    dir_2_1 = dir_2.mkdir('dir_2_1')
    file_1_dir_2_1 = dir_2_1.join('1_2_1.txt')
    file_1_dir_2_1.write('Test file "1_2_1.txt" in subdir "dir_2_1"')
    dir_2_2 = dir_2.mkdir('dir_2_2')
    dir_2_3 = dir_2.mkdir('dir_2_3')
    file_1_dir_2_3 = dir_2_3.join('1_2_3.txt')
    file_1_dir_2_3.write('Test file "1_2_3.txt" in subdir "dir_2_3"')
    file_2_dir_2_3 = dir_2_3.join('2_2_3.txt')
    file_2_dir_2_3.write('Test file "2_2_3.txt" in subdir "dir_2_3"')
    file_3_dir_2_3 = dir_2_3.join('3_2_3.txt')
    file_3_dir_2_3.write('Test file "3_2_3.txt" in subdir "dir_2_3"')
    dir_2_3_1 = dir_2_3.mkdir('dir_2_3_1')
    dir_2_3_2 = dir_2_3.mkdir('dir_2_3_2')
    file_1_dir_2_3_2 = dir_2_3_2.join('1_2_3_2.py')
    file_1_dir_2_3_2.write('Test file "1_2_3_2.py" in subdir "dir_2_3_2"')

    return tmpdir


values_init_list_dir = ['', [], 1, 1.1, 'a', [1, 'a', [3, 4]], None, {1: 'a'}]

values_check_input_text = [
    ['', '', 0, False],
    ['', 'test_2', 0, False],
    ['test_1', '', 0, True],
    ['test_1', 'test_2', 0, True],
    ['', '', len(const.VARIANTS_OBJECTS) - 1, False],
    ['test_1', '', len(const.VARIANTS_OBJECTS) - 1, False],
    ['', 'test_2', len(const.VARIANTS_OBJECTS) - 1, False],
    ['test_1', 'test_2', len(const.VARIANTS_OBJECTS) - 1, True],
    ['test_1', 'test_2', len(const.VARIANTS_OBJECTS) - 2, True],
    ['test_1', '', len(const.VARIANTS_OBJECTS) - 2, True],
    ['', 'test_2', len(const.VARIANTS_OBJECTS) - 2, False],
    ['', '', len(const.VARIANTS_OBJECTS) - 2, False]
]

values_process = [
    [
        '*', '', True, False, False, True, 18, 10,
        ['1_1.txt', '1.txt', '2.csv', '1.py', '2.py', '1_2_1.txt',
         '1_2_3.txt', '2_2_3.txt', '3_2_3.txt', '1_2_3_2.py']
    ],
    [
        '*', '', True, False, False, False, 5, 2,
        ['1.txt', '2.csv']
    ],
    [
        '*', '', True, False, False, True, 10, None,
        ['1_1.txt', '1.txt', '2.csv', '1.py', '2.py', '1_2_1.txt']
    ],
    [
        '*', '', True, False, False, True, 1, None,
        ['1.txt']
    ],
    [
        '*1*', '', True, True, False, True, 18, 9,
        ['1.txt', 'dir_1', '1_1.txt', '1.py', 'dir_2_1', 'dir_2_3_1',
         '1_2_1.txt', '1_2_3.txt', '1_2_3_2.py']
    ],
    [
        '*1*', '', True, True, False, False, 5, 2,
        ['1.txt', 'dir_1']
    ],
    [
        '2*', 'dir_2', False, False, True, True, 18, 2,
        ['2.py', '28-th symbol', '2_2_3.txt', '33-th symbol']
    ],
    [
        '*', 'Test nothing', False, False, True, True, 18, 0,
        ['']
    ],
]

values_start_find = [
    ['*', '', '1.txt', const.FIRST_LINE, const.RES_FILE],
    ['2.*', '', '', const.FIRST_LINE, ''],
    ['test 1', 'test 2', '', const.FIRST_LINE, ''],
]

values_check_file_name = [
    ['', False, '1.txt', False],
    ['1', False, '1.txt', False],
    ['1.tx', False, '1.txt', False],
    ['.txt', False, '1.txt', False],
    ['1.txtx', False, '1.txt', False],
    ['01.txt', False, '1.txt', False],
    ['1txt', False, '1.txt', False],
    ['?.txt', False, '1.txt', True],
    ['??.txt', False, '1.txt', False],
    ['1.?xt', False, '1.txt', True],
    ['1.?txt', False, '1.txt', False],
    ['?.?x?', True, '1.txt', True],
    ['*', True, '1.txt', True],
    ['1.*', True, '1.txt', True],
    ['*.txt', True, '1.txt', True],
    ['1?.*', True, '1.txt', False],
    ['?1.*', True, '1.txt', False],
    ['?.?*', True, '1.txt', True],
    ['?.*?', True, '1.txt', True],
    ['?.???', True, '1.txt', True],
    ['?.????', True, '1.txt', False],
    ['??.???', True, '1.txt', False],
    ['1.txt', False, '1.txt', True],
    ['1.txt', True, '1.txt', True],
    ['1.TXT', False, '1.txt', False],
    ['1.TXT', True, '1.txt', True],
    ['1.TxT', True, '1.txt', True],
    ['1.tXt', True, '1.txt', True],
    ['1.Txt', False, '1.txt', False],
]

values_load_file = [
    ['1.txt', 1000, 'Test file "1.txt" in main dir'],
    ['1.txt', 5000, 'Test file "1.txt" in main dir'],
    ['1.txt', 10, 'Test file '],
    ['1.txt', 1, 'T'],
    ['1.txt', 0, ''],
    ['1.csv', 100, None],
    [1, 100, None],
    [None, 100, None],
]

values_check_text = [
    ['1.txt', '.*', False, 0],
    ['1_1.txt', '.*', False, None],
    [None, '.*', False, None],
    ['1.txt', '', False, 0],
    ['1.txt', 'Test', False, 0],
    ['1.txt', 'MAIN', False, None],
    ['1.txt', 'MAIN', True, 21],
    ['1.txt', 't', False, 3],
    ['1.txt', 't', True, 0],
    ['1.txt', '"', False, 10],
    ['1.txt', '"', True, 10],
    ['1.txt', 'fIle', True, 5],
    ['1.txt', 'fIle', False, None],
    ['1.txt', 'f.{1}le', False, 5],
    ['1.txt', 'f.*', False, 5],
    ['1.txt', '.*f', False, 0],
    ['1.txt', '"1.txt"', False, 10],
    ['1.txt', r'"1\.txt"', False, 10],
    ['1.txt', '"1..{1}txt"', False, None],
]
