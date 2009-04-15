# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008 Alexandre da Silva / Carlos Antonio da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import os
import gnomevfs
from datetime import datetime


def get_file_info(uri):
    """Return the File information if uri exists"""
    if uri is not None and gnomevfs.exists(uri):
        return gnomevfs.get_file_info(uri)
    return False

def is_uri_dir(uri):
    """Checks if given uri is a dir"""
    file_info = get_file_info(uri)
    if file_info:
        return is_dir(file_info)
    return False

def is_dir(file_info):
    """Checks to see if the file is a directory."""
    if file_info is not None:
        return file_info.type == gnomevfs.FILE_TYPE_DIRECTORY
    return False

def is_file(file_info):
    """Checks to see if the file is a directory."""
    if file_info is not None:
        return file_info.type != gnomevfs.FILE_TYPE_DIRECTORY
    return False

def is_hidden(file_info):
    """Checks to see if the file is hidden."""
    if file_info is not None:
        return file_info.name.startswith(u'.') or file_info.name.endswith(u'~')
    return False

def is_hidden_dir(file_info):
    """Checks to see if the file is a hidden directory."""
    return is_dir(file_info) and is_hidden(file_info)

def is_hidden_file(file_info):
    """Checks to see if the file is a hidden file."""
    return not is_dir(file_info) and is_hidden(file_info)

def is_visible_dir(file_info):
    """Checks to see if the file is a visible directory."""
    return is_dir(file_info) and not is_hidden(file_info)

def is_visible_file(file_info):
    """Checks to see if the file is a visible file."""
    return not is_dir(file_info) and not is_hidden(file_info)

def get_user_home_uri():
    """Gets a URI pointing to the user's home directory '~'."""
    return gnomevfs.URI(u'file://%s' % os.path.expanduser(u'~'))

def get_mime_type(uri):
    """Gets the mime type of given file uri"""
    return gnomevfs.get_mime_type(uri)

def get_path_from_uri(uri):
    return gnomevfs.get_local_path_from_uri(uri)

def get_last_modification(uri):
    """Gigen a file uri return the last modification date"""
    file_info = get_file_info(uri)
    if file_info:
        return datetime.fromtimestamp(file_info.mtime)

