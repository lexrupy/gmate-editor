# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import os
import gtksourceview2

USER_HOME_PATH = os.environ['HOME']
GMATE_HOME_PATH = os.path.join(USER_HOME_PATH, '.gmate')
GMATE_PLUGIN_HOME_FOLDER = os.path.join(GMATE_HOME_PATH, 'plugins')
GMATE_PLUGIN_CORE_FOLDER = os.path.join(USER_HOME_PATH, 'projetos/gmate/GMATE/plugins')
GMATE_BACKUP_FOLDER = os.path.join(GMATE_HOME_PATH, 'backup')
GMATE_DATA_FOLDER = os.path.join(USER_HOME_PATH, 'projetos/gmate')

DEFAULT_BORDER_WIDTH = 2

__style_scheme_manager = None
__language_manager = None

def get_style_scheme_manager():
    global __style_scheme_manager
    if __style_scheme_manager == None:
        __style_scheme_manager = gtksourceview2.StyleSchemeManager()
    return __style_scheme_manager

def get_language_manager():
    global __language_manager
    if __language_manager == None:
        __language_manager = gtksourceview2.LanguageManager()
    return __language_manager

