# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import gtk
from GMATE.status_widget import StatusWidget
from GMATE import get_style_scheme_manager, get_language_manager

class StatusLanguage(StatusWidget):
    """Status Box for show and change the current language"""

    def initialize(self):
        # Get the List Of Languages
        self.buffer = None
        self.langs = gtk.ListStore(str, str)
        self.langs.set_sort_column_id(1, gtk.SORT_ASCENDING)
        lm = get_language_manager()
        for l in lm.get_language_ids():
            lang = lm.get_language(l)
            if not lang.get_hidden():
                self.langs.append([l, lang.get_name()])
        # TODO: Move None to i18n
        self.langs.append(['none', "None"])
        self.language_combo = gtk.ComboBox(self.langs)
        # TODO: Polish the status bar combobox to  be smaller with a hack to GtkRc
        self.language_combo.set_property("height-request", 30)
        self.language_combo.set_focus_on_click(False)
        self.language_combo.set_wrap_width(4)
        cell = gtk.CellRendererText()
        self.language_combo.pack_start(cell, True)
        self.language_combo.add_attribute(cell, 'text', 1)
        # TODO: Need to set the current active language
        # self.language_combo.set_active()
        self.language_combo.connect('changed', self.__combo_changed)

        self.pack_start(self.language_combo, False, False)
        self.show_all()


    def on_set_document(self, doc):
        self.buffer = doc.View.get_buffer()
        lang = self.buffer.get_language()
        lang_id = 'none'
        if lang:
            lang_id = lang.get_id()
        iter = self.langs.get_iter_first()
        index = 0
        while self.langs.get_value(iter, 0) != lang_id:
            try:
                iter = self.langs.iter_next(iter)
                index += 1
            except: index = 0
        self.language_combo.set_active(index)


    def __combo_changed(self, combo):
        if self.buffer:
            index, model = combo.get_active(), combo.get_model()
            if index >= 0:
                language = model[index][0]
                lang = get_language_manager().get_language(language)
                if lang:
                    self.buffer.set_language(lang)

