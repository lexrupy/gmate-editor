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


class StatusPosition(StatusWidget):
    """
        This box holds the current line number
    """
    def initialize(self):
        self.buffer = None
        self.document = None
        self.__changed_id = None
        self.__mark_set_id = None
        self.line_title_label = gtk.Label(i.status_line)
        self.line_position_number = gtk.Label('0')
        self.line_position_number.set_size_request(40, -1)
        self.line_position_number.set_alignment(0.01, 0.5)
        self.column_title_label = gtk.Label(i.status_column)
        self.column_position_number = gtk.Label('0')
        self.column_position_number.set_size_request(25,-1)
        self.column_position_number.set_alignment(0.01, 0.5)
        self.pack_start(self.line_title_label, False, False)
        self.pack_start(self.line_position_number, False, False)
        sep = gtk.VSeparator()
        self.pack_start(sep,False, False, 5)
        self.pack_start(self.column_title_label, False, False)
        self.pack_start(self.column_position_number, False, False)
        self.show_all()


    def on_disconnect(self):
        if self.buffer:
            if self.__changed_id:
                self.buff.disconnect(self.__changed_id)
                self.__changed_id = None
            if self.__mark_set_id:
                self.buff.disconnect(self.__mark_set_id)
                self.__mark_set_id = None


    def on_set_document(self, doc):
        self.on_disconnect()
        self.buff = doc.View.get_buffer()
        self.document = doc.View
        self.__changed_id = self.buff.connect("changed", self.__changed_cb)
        self.__mark_set_id = self.buff.connect("mark-set", self.__mark_set_cb)
        self.__changed_cb(self.buff)


    def __changed_cb(self, buff):
        tabwidth = self.document.get_tab_width()
        iter = buff.get_iter_at_mark(buff.get_insert())
        row = iter.get_line() + 1
        col_offset = iter.get_line_offset()
        iter.set_line_offset(0)
        col = 0
        while not col_offset == iter.get_line_offset():
            if iter.get_char() == '\t':
                col += (tabwidth - (col % tabwidth))
            else:
                col += 1
            iter.forward_char()
        self.line_position_number.set_text(str(row))
        self.column_position_number.set_text(str(col+1))
        return False


    def __mark_set_cb(self, buff, cursoriter, mark):
        self.__changed_cb(buff)
        return False

