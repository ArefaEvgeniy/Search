#!/usr/bin/env python3
"""
Constants from file const.py used in main files compare.py and utils.py
"""

from PyQt5.QtGui import QFont


NAME_TITLE = 'Search...'
NAME_MESSAGE = 'Message'
NAME_QUESTION = 'Are you sure to quit?'
NAME_SETTINGS = 'Settings'
NAME_FIND_SUBDIR = 'search in subdirectories'
NAME_START = 'Search...'
NAME_STOP = 'STOP'
NAME_SELECT_DIR = 'Directory for search:'
NAME_SEARCH_TEXT = 'Search text in file:'
NAME_SYMBOLS = 'First thousand symbols to search:'

SELECT_DIR = 'Select directory for search'
FIRST_LINE = 'Result of search {0}"{1}" by on path "{2}"{3}:\n'
FIRST_LINE_TEXT = '"{0}" in files '
ACTION_LASTED = '\nThe action lasted {0} seconds. Found: {1}'
DIR_EMPTY = '\nThe directory for search is empty.'
SUBDIR_ON = ' and on subdirs'
SUBDIR_OFF = ''
RES_FILE = '\n{0}'
RES_TEXT = '\n{0}  -  {1}-th symbol'
KEY_ENTER = 16777220

CASE_SENSITIVE = 'case sensitive'
CASE_IGNORE = 'ignore case'

VARIANTS_OBJECTS = ['Find file', 'Find directory', 'Find file or directory',
                    'Find text in file']
VARIANTS_CASE = [CASE_SENSITIVE, CASE_IGNORE]
VARIANTS_REPLACE = (('.', r'\.'), ('?', '.{1}'), ('*', '.*'))

BOLD_FONT = QFont()
BOLD_FONT.setBold(True)
