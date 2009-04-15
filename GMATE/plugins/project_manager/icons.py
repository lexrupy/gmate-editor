# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

"""A widget used to display the file/folder structure of projects."""

import gtk
import gnomevfs

from i18n import err0009

class Icons(object):
    """Retrieves the icons necessary for the ProjectTreeView"""
    def __init__(self, widget):
        """Constructor. """
        if widget is None:
            raise ValueError, err0009
        super(Icons, self).__init__()

        self.__widget = widget
        self.theme = gtk.icon_theme_get_default()
        self.__initialize_icons()

    def retrieve_icon(self, icon_name, stock_substitute=gtk.STOCK_FILE):
        """Retrieves a rendered icon, or a substitution icon."""
        icon = None
        try:
            icon = self.theme.load_icon(icon_name, 16,
                                         gtk.ICON_LOOKUP_USE_BUILTIN)
        except:
            icon = self.__widget.render_icon(
                stock_substitute, gtk.ICON_SIZE_MENU)
        return icon

    def retrieve_file_icon(self, uri):
        """Retrieves a rendered icon based on mime-type and theme."""
        mime_type = gnomevfs.get_mime_type(str(uri))
        icon_name = self.__make_icon_mime_name(mime_type)
        icon = None
        try:
            icon = self.theme.load_icon(icon_name, 16,
                                         gtk.ICON_LOOKUP_USE_BUILTIN)
        except:
            icon = self.file
        return icon

    def __initialize_icons(self):
        """Retrieves and initializes the icons."""
        self.folder = self.retrieve_icon(u'stock_folder', gtk.STOCK_DIRECTORY)
        self.folder_open = self.retrieve_icon(u'stock_open', gtk.STOCK_OPEN)
        self.folder_parent = self.retrieve_icon(u'stock_go_back',
                                                gtk.STOCK_GO_BACK)
        self.file = self.retrieve_icon(u'stock_file')

    def __make_icon_mime_name(self, mime_type):
        """Format a mime-type into an icon name."""
        return "gnome-mime-%s" % mime_type.replace(u'/', u'-')

