# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import gtk

from GMATE import i18n as i
from GMATE.status_widget import StatusWidget

from GMATE.status_position import StatusPosition
from GMATE.status_keyboard import StatusKeyboard
from GMATE.status_language import StatusLanguage
from GMATE.status_indentation import StatusIndentation



class StatusBar(gtk.HBox):
    """
        The StatusBar Object
    """
    # TODO: Polish the status bar combobox to  be smaller with a hack to GtkRc
    def __init__(self):
        super(StatusBar, self).__init__(False, 0)
        # store components
        self.__status_widgets = []
        self.set_homogeneous(False)
        self.set_spacing(2)
        # Add Default Status Widgets
        self.position = StatusPosition()
        self.language = StatusLanguage()
        self.tab_indent = StatusIndentation()
        self.status_keyb = StatusKeyboard()
        self.status_keyb.set_size_request(60,-1)
        self.status_text = gtk.Statusbar()
        self.status_text.set_has_resize_grip(False)
        self.add_status(self.position, sep=False)
        self.add_status(self.language)
        self.add_status(self.tab_indent)
        self.add_status(self.status_text, True, True, sep=False)
        self.add_status(self.status_keyb, False, True, sep=False)
        self.show_all()

    def add_status(self, child, expand=False, fill=False, padding=0, sep=True):
        if sep:
            sep = gtk.VSeparator()
            self.pack_start(sep,False, False, 3)
        self.pack_start(child, expand, fill, padding)
        # Add The StatusBox to the StatusBox List
        self.__status_widgets.append(child)
        return False

    def set_document(self, document):
        for widget in self.__status_widgets:
            if hasattr(widget, "on_set_document"):
                widget.on_set_document(document)

#        self.buffer = view.get_buffer()
#        self.current_lang.set_buffer(self.buffer)
#        self.current_tab_indent.set_document(view)
#        self.keyb_status.set_document(view)
#        self.position_status.set_document(view)
        return False

    def disconnect_all(self):
        for widget in self.__status_widgets:
            if hasattr(widget, "on_disconnect"):
                widget.on_disconnect()

