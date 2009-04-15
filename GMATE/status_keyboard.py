# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import gtk
from GMATE import i18n as i

class StatusKeyboard(gtk.Statusbar):
    """
        Displays the current status of Keyboard
    """
    def __init__(self):
        super(StatusKeyboard, self).__init__()#False, 2)
        self.__signal_id = None
        self.document = None
        self.context_id = None
        #self.status_label = gtk.Label(i.keyb_mode_insert)
        self.set_text(i.keyb_mode_insert)
        #self.pack_start(self.status_label, False, False)
        self.show_all()


    def on_set_document(self, doc):
        self.on_disconnect()
        self.document = doc.View
        self.__signal_id = doc.View.connect("toggle-overwrite", self.__toggle_cb)
        mode = [i.keyb_mode_overrite, i.keyb_mode_insert][doc.View.get_overwrite()==False]
        #self.status_label.set_text(mode)
        self.set_text(mode)


    def on_disconnect(self):
        if self.__signal_id and self.document:
            #self.document.disconnect(self.__signal_id)
            self.__signal_id = None

    def set_text(self, text):
        if self.context_id:
            self.pop(self.context_id)
        self.context_id = self.get_context_id(text)
        self.push(self.context_id, text)


    def __toggle_cb(self, widget=None):
        if not self.document.get_overwrite():
            mode = i.keyb_mode_overrite
        else:
            mode = i.keyb_mode_insert
        self.status_label.set_text(mode)
        return False

