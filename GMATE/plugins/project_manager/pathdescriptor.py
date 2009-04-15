# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

"""A description of a found path within the ProjectTreeView"""

import os.path
from i18n import err0007, err0008

class PathDescriptor(object):
    """Describes the location of a file within the ProjectTreeView."""
    def __init__(self, uri, isdir=False):
        """Constructor."""
        self.__uri = uri
        self.__tree_iter = None
        self.__isdir = isdir

    def get_uri(self):
        """Gets a URI pointing to a location on the file system."""
        return self.__uri

    def get_name(self):
        """Gets the display name."""
        return self.__uri.short_name

    def get_iter(self):
        """Gets an iterator from the TreeView."""
        return self.__tree_iter

    def set_iter(self, tree_iter):
        """Sets an iter from the TreeView."""
        self.__tree_iter = tree_iter

    def is_dir(self):
        """Gets whether the descriptor corresponds with a directory."""
        return self.__isdir

