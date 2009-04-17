# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import GMATE
import os
import warnings
import GMATE.configuration as conf
from datetime import datetime


def setup_directories():
    """
        Create the required directories if theh not exists yet.
    """
    directories = [GMATE.GMATE_HOME_PATH, GMATE.GMATE_PLUGIN_HOME_FOLDER,
        GMATE.GMATE_PLUGIN_CORE_FOLDER]
    for d in directories:
        # TODO: Check if directory does not exist. If not create.
#        if not os.exists(d):
#            os.mkdir(d)
        pass


def get_language_for_mime_type(mime):
    """
        Giben a mime type, try to return the language associated with.
    """
    lm = GMATE.get_language_manager()
    lang_ids = lm.get_language_ids()
    for i in lang_ids:
        lang = lm.get_language(i)
        for m in lang.get_mime_types():
            if m == mime:
                return lang
    return None


def to_unicode_or_bust(obj, encoding='utf-8'):
     if isinstance(obj, basestring):
         if not isinstance(obj, unicode):
             obj = unicode(obj, encoding)
     return obj


def not_implemented(func):
    """
        Simple Helper Function to decorate a not implemented function.
        Example:

            @not_implemented
            def some_feature(self):
                pass

    """
    def new_func(*args, **kwargs):
        print "[GMATE] - NotImplementedError: %s function not implemented yet " % func.__name__
    return new_func


def deprecated(function, message):
    """
        This is a function to be used inside other functions to mark them as
        deprecated, and helps the user what to do.
    """
    message = "[GMATE] - Call to a DEPRECATED FUNCTION: \"%s\".\n %s" % (function, message)
    print message

