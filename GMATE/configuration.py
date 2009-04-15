# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import gtk
import gconf
import os
import pango
import GMATE

GTK_POS = [gtk.POS_TOP]

class Settings(object):

    def __init__(self):
        super(Settings, self).__init__()
        self.base = '/apps/gmate'
        self.client = gconf.client_get_default()
        self.client.add_dir(self.base, gconf.CLIENT_PRELOAD_NONE)

    def __get_path(self, *args):
        value_list = list(args)
        value_list.insert(0,self.base)
        path = filter(lambda x: x is not None, value_list)
        path = tuple(path)
        return os.path.join(*path)

    # Default Settings Manipulation Methods ====================================
    def get_string(self, name, namespace=None, default=None):
        path = self.__get_path(namespace, name)
        val = self.client.get(path)
        if val is not None:
            return val.get_string()
        if default:
            self.set_string(name, default)
        return default

    def set_string(self, name, value, namespace=None):
        path = self.__get_path(namespace, name)
        self.client.set_string(path, value)
        return value

    def get_integer(self, name, namespace=None, default=None):
        path = self.__get_path(namespace, name)
        val = self.client.get(path)
        if val is not None:
            return val.get_int()
        if default:
            self.set_integer(name, default, namespace=namespace)
        return default

    def set_integer(self, name, value, namespace=None):
        path = os.path.join(self.base, name)
        self.client.set_int(path, value)
        return value

    # Configuration Methods ====================================================

    def default_file_encoding(self):
        return self.get_string('default_file_encoding', default='utf-8')

    def tab_position(self):
        index = self.get_integer('tab_position', default=0)
        return GTK_POS[index]

    def editor_font(self):
        #font_desc = 'Monospace 10'
        #path = os.path.join(self.base, 'editor_font')
        #val = self.client.get(path)
        #if val:
        #    font_desc =  val.get_string()
        font_desc = self.get_string('editor_font')
        # If No Configuration, use by default, the gnomne monospace font
        if font_desc == None:
            mono_font_path = '/desktop/gnome/interface/monospace_font_name'
            val = self.client.get(mono_font_path)
            if val:
                font_desc = val.get_string()
        return pango.FontDescription(font_desc)

    def editor_indent_width(self):
        return self.get_integer('editor_indent_width', default=4)

    def editor_tab_width(self):
        return self.get_integer('editor_tab_width', default=4)

    def editor_margin_pos(self):
        return self.get_integer('editor_margin_pos', default=80)

    def get_style_scheme(self):
        scheme = self.get_string('style_scheme', default='classic')
        return GMATE.get_style_scheme_manager().get_scheme(scheme)

    def get_last_window_bounds(self):
        path = self.__get_path('window_bounds')
        val = self.client.get(path)
        values = [10, 10, 670, 480]
        if val is not None:
            values = map(lambda x: x.get_int(), val.get_list(gconf.VALUE_INT))
        else:
            self.client.set_list(path, gconf.VALUE_INT, values)
        return values

    def set_last_window_bounds(self, bounds):
        path = self.__get_path('window_bounds')
        self.client.set_list(path, gconf.VALUE_INT, bounds)
        return

__settings = None

def get_settings():
    global __settings
    if __settings is None:
        __settings = Settings()
    return __settings


#close_btn_xpm_data = [
#    "9 9 3 1",
#    " 	c None",
#    ".	c #5A5A5A",
#    "+	c #484848",
#    "         ",
#    "  .   .  ",
#    " .+. .+. ",
#    "  .+.+.  ",
#    "   .+.   ",
#    "  .+.+.  ",
#    " .+. .+. ",
#    "  .   .  ",
#    "         "]
#mod_btn_xpm_data = [
#    "9 9 3 1",
#    " 	c None",
#    ".	c #5A5A5A",
#    "+	c #484848",
#    "         ",
#    "   ...   ",
#    "  .+++.  ",
#    " .+++++. ",
#    " .++.++. ",
#    " .+++++. ",
#    "  .+++.  ",
#    "   ...   ",
#    "         "]

