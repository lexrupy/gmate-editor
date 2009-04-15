# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

"""Settings manager for Project Manager."""

import os.path
import gconf
import gnomevfs
from GMATE import files
from GMATE.configuration import get_settings

gmate_settings = get_settings()

HOME_URI = str(files.get_user_home_uri())
DEFAULT_TERMINAL = 'file:///usr/bin/gnome-terminal'
DEFAULT_FILEBROWSER = 'file:///usr/bin/nautilus'
DEFAULT_TERMINAL_ARGS = '--working-directory=%s'
DEFAULT_BROWSER_ARGS = '%s'
DEFAULT_FILE_FILTER = ''

class Settings(object):

    def __init__(self):
        self.namespace = 'project_manager'

    def get_string(self, name, default=''):
        return gmate_settings.get_string(name, namespace=self.namespace,
            default=default)

    def set_string(self, name, value):
        return gmate_settings.set_string(name, value, namespace=self.namespace)

    def get_default_encoding(self):
        return gmate_settings.default_file_encoding()

    def get_terminal_arguments(self):
        """Gets the options to pass to the terminal application."""
        return self.get_string('terminal_arguments', DEFAULT_TERMINAL_ARGS)

    def set_terminal_arguments(self, arguments=None):
        """Sets the arguments to pass to the terminal."""
        args = DEFAULT_TERMINAL_ARGS
        if arguments is not None:
            args = arguments
        return self.set_string('terminal_arguments', args)

    def get_browser_arguments(self):
        """Gets the options to pass to the browser application."""
        return self.get_string('browser_arguments', DEFAULT_BROWSER_ARGS)

    def set_browser_arguments(self, arguments=None):
        """Sets the arguments to pass to the browser."""
        args = DEFAULT_BROWSER_ARGS
        if arguments is not None:
            args = arguments
        return self.set_string('browser_arguments', args)

    def get_file_filter(self):
        """Gets the file filter used when displaying files."""
        return self.get_string('file_filter', DEFAULT_FILE_FILTER)

    def set_file_filter(self, arguments=None):
        """Sets the default file filter."""
        args = DEFAULT_FILE_FILTER
        if arguments is not None:
            args = arguments
        return self.set_string('file_filter', args)

    def get_file_browser(self):
        """Gets the default file browser."""
        return self.get_string('file_browser', DEFAULT_FILEBROWSER)

    def set_file_browser(self, arguments=None):
        """Sets the default file browser."""
        args = DEFAULT_FILEBROWSER
        if arguments is not None:
            args = arguments
        return self.set_string('file_browser', args)

    def get_terminal(self):
        """Gets the default terminal application."""
        return self.get_string('terminal', DEFAULT_TERMINAL)

    def set_terminal(self, arguments=None):
        """Sets the default terminal application."""
        args = DEFAULT_TERMINAL
        if arguments is not None:
            args = arguments
        return self.set_string('terminal', args)

    def get_repository(self):
        uri = self.get_string('repository', HOME_URI)
        file_info = gnomevfs.get_file_info(uri)
        try:
            if files.is_dir(file_info):
                file_uri = gnomevfs.URI(uri)
        except:
            file_uri = files.get_user_home_uri()
        return file_uri

    def set_repository(self, arguments=None):
        args = files.get_user_home_uri()
        if arguments is not None:
            args = arguments
        return self.set_string('repository', str(args))

