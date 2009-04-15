# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

"""A context menu widget for ProjectTreeView"""

import os
import sys
import gtk
import gnomevfs
from icons import Icons
from i18n import err0005, menu0001, menu0003, menu0007, menu0008, menu0009,\
                 menu0010, menu0011, menu0002
from GMATE import files

class TreeCellMenu(gtk.Menu):
    """A context menu widget for ProjectTreeView."""

    def __init__(self, project_explorer):
        """Constructor."""
        if project_explorer is None:
            raise ValueError, err0005
        super(TreeCellMenu, self).__init__()
        self.__project_explorer = project_explorer

    def display(self, desc, event):
        uri = desc.get_uri()
        if not gnomevfs.exists(uri):
            return
        file_info = gnomevfs.get_file_info(uri)
        is_dir = files.is_dir(file_info)
        icon_manager = Icons(self)
        if is_dir:
            pixbuf = icon_manager.retrieve_icon(u'stock_folder',
                                                gtk.STOCK_DIRECTORY)
            self.__appendMenuItem(label=menu0001, pixbuf=pixbuf,
                callback=lambda a: self.__set_repository(uri))
            pixbuf = None
        else:
            self.__appendMenuItem(stock=gtk.STOCK_OPEN,
                callback=lambda a: self.__open_file(uri))

        if is_dir:
            self.__appendSeperator()
            pixbuf = icon_manager.retrieve_icon(gtk.STOCK_NEW, gtk.STOCK_NEW)
            self.__appendMenuItem(label=menu0003, pixbuf=pixbuf,
                callback=lambda a: self.__create_file_in(uri))
            self.__appendMenuItem(label=menu0010, pixbuf=pixbuf,
                callback=lambda a: self.__create_folder_in(uri))
            self.__appendSeperator()
            pixbuf = None

            if gnomevfs.exists(uri) and uri.is_local:
                pixbuf = None
                if icon_manager.theme.has_icon(u'gnome-terminal'):
                    pixbuf = icon_manager.theme.load_icon(u'gnome-terminal',
                        16, gtk.ICON_LOOKUP_USE_BUILTIN)
                self.__appendMenuItem(label=menu0011, pixbuf=pixbuf,
                    callback=lambda a: self.__open_terminal(uri))
                pixbuf = icon_manager.retrieve_icon(u'stock_open',
                                                    gtk.STOCK_OPEN)
                self.__appendMenuItem(label=u'Browse...', pixbuf=pixbuf,
                    callback=lambda a: self.__open_file_browser(uri))
                self.__appendSeperator()
        self.__appendMenuItem(stock=gtk.STOCK_CUT, sensitive=False)
        self.__appendMenuItem(stock=gtk.STOCK_COPY, sensitive=False)
        if is_dir:
            self.__appendMenuItem(stock=gtk.STOCK_PASTE, sensitive=False)
        self.__appendSeperator()
        self.__appendMenuItem(menu0008, sensitive=False)
        self.__appendSeperator()
        self.__appendMenuItem(stock=gtk.STOCK_DELETE,
            callback=lambda a: self.__unlink(uri))
        pixbuf = None
        if icon_manager.theme.has_icon(u'gconf-editor'):
            pixbuf = icon_manager.theme.load_icon(u'gconf-editor',
                16, gtk.ICON_LOOKUP_USE_BUILTIN)
        self.__appendSeperator()
        self.__appendMenuItem(label=menu0002, pixbuf=pixbuf,
            callback=lambda a: self.__display_settings())
        pixbuf = None
        icon_manager = None
        self.popup(None, None, None, event.button, event.time)

    def __appendMenuItem(self, label=None, stock=None, pixbuf=None, callback=None,
                         sensitive=True):
        m = None
        if stock is not None:
            m = gtk.ImageMenuItem(stock)
        elif pixbuf is not None:
            m = gtk.ImageMenuItem(label)
            icon = gtk.Image()
            icon.set_from_pixbuf(pixbuf)
            m.set_image(icon)
        else:
            m = gtk.MenuItem(label)
        if not sensitive:
            m.set_property(u'sensitive', False)
        if callback is not None:
            m.connect("activate", callback)
        self.append(m)
        m.show()

    def __appendSeperator(self):
        m = gtk.SeparatorMenuItem()
        self.append(m)
        m.show()

    def __set_repository(self, uri):
        self.__project_explorer.set_repository(uri)

    def __open_file(self, uri):
        self.__project_explorer.open_file(uri)

    def __unlink(self, uri):
        self.__project_explorer.unlink(uri)

    def __create_folder_in(self, uri):
        self.__project_explorer.create_folder_in(uri)

    def __create_file_in(self, uri):
        self.__project_explorer.create_file_in(uri)

    def __open_terminal(self, uri):
        self.__project_explorer.open_terminal(uri)

    def __open_file_browser(self, uri):
        self.__project_explorer.open_file_browser(uri)

    def __display_settings(self):
        self.__project_explorer.display_settings()

