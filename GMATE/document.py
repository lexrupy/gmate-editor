# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information


import os
import gtksourceview2 as sw
from gnomevfs import get_local_path_from_uri
from gtk import ScrolledWindow
import GMATE
from GMATE import plugin_system as plugin
from GMATE.configuration import get_settings
from GMATE import i18n as i

settings = get_settings()

class Document(ScrolledWindow):

    def __init__(self, window, tab_title, language=None):
        super(Document, self).__init__()
        self.__initialize_properties()
        self.__window = window
        self.__document_manager = window.DocumentManager
        self.__notebook = self.__document_manager.get_notebook()
        self.__tab_title = tab_title
        #self.__notebook = window.DocumentManager.get_notebook()
        self.__language = language
        self.__configure_buffer()
        self.__tab_title.set_doc(self)
        self.__configure_view()
        self.add(self.View)
        self.show_all()
        return


    # Public Methods ===========================================================

    def save(self):
        # TODO: Test if is a new document
        if self.__is_untitled:
            from GMATE.dialogs import retrieve_new_file_name
            filename = retrieve_new_file_name()
        else:
            if self.__document_manager.save_document(self):
                self.Buffer.set_modified(False)
                return True
        return False

    def close(self):
        # TODO: Put Here all tests about current document before close
        can_close = True
        if can_close:
            plugin.trigger_method('close_document', self)
            # Remove reference from document manager
            for d in self.__document_manager.documents:
                if d == self:
                    self.__document_manager.documents.remove(d)
                    break
            # Destroy the page
            page_num = self.__notebook.page_num(self)
            del self.Buffer
            self.Buffer = None
            self.View.destroy()
            self.View = None
            self.Buffer = None
            self.destroy()
            self = None
        return


    def get_buffer_view(self):
        return (self.Buffer, self.View)


    def set_title(self, title):
        if self.__tab_title:
            self.__tab_title.set_title(title)
        return


    def get_tab_title(self):
        return self.__tab_title.get_title()


    def set_language(self, language):
        lang = None
        if language is None: return
        if isinstance(language, sw.Language):
            lang = language
        else:
            lang = GMATE.get_language_manager().get_language(language)
        if lang:
            self.Buffer.set_language(lang)

    def get_filename(self):
        return self.__filename

    def set_filename(self, fname):
        self.__filename = fname
        title = os.path.basename(fname)
        self.set_title(title)

        return

    def get_uri(self):
        return self.__uri

    def set_uri(self, uri):
        self.__uri = uri
        return

    # Private Methods ==========================================================
    def __initialize_properties(self):
        self.__document_manager = None
        self.__modified = False
        self.__last_modified_time = None
        self.__is_untouched = True
        self.__is_untitled = True
        # Reference to Tab Title Object, so We can change the title on tab
        self.__filename = None
        self.__uri = None
        self.View = sw.View()
        self.Buffer = sw.Buffer()


    def __configure_buffer(self):
        self.Buffer.set_style_scheme(settings.get_style_scheme())
        if self.__language:
            lang = GMATE.get_language_manager().get_language(self.__language)
            if lang:
                self.Buffer.set_language(lang)
        self.Buffer.connect('changed', self.__buffer_changed_cb)
        self.Buffer.connect('modified-changed', self.__buffer_modified_changed_cb)
        # Signals
        #"highlight-updated" def callback(textbuffer, start, end, user_param1, ...)
        #"source-mark-updated" def callback(textbuffer, textmark, user_param1, ...)
        #"apply-tag" def callback(textbuffer, texttag, start, end, user_param1, ...)
        #"begin-user-action" ef callback(textbuffer, user_param1, ...)
        #"delete-range" def callback(textbuffer, start, end, user_param1, ...)
        #"end-user-action" def callback(textbuffer, user_param1, ...)
        #"insert-child-anchor" def callback(textbuffer, iter, anchor, user_param1, ...)
        #"insert-pixbuf" def callback(textbuffer, iter, pixbuf, user_param1, ...)
        #"insert-text" def callback(textbuffer, iter, text, length, user_param1, ...)
        #"mark-deleted" def callback(textbuffer, textmark, user_param1, ...)
        #"mark-set" def callback(textbuffer, iter, textmark, user_param1, ...)
        #"remove-tag" def callback(textbuffer, texttag, start, end, user_param1, ...)


    def __configure_view(self):
        # Set the configured font
        self.View.modify_font(settings.editor_font())
        # TODO: Get a Per-Language tab width configuration
        self.View.set_tab_width(settings.editor_tab_width())
        self.View.set_indent_width(settings.editor_indent_width())
        # TODO: First Read this from configuratin, after make a menu in status
        # bar for Selection
        self.View.set_auto_indent(True)
        self.View.set_insert_spaces_instead_of_tabs(True)
        self.View.set_show_right_margin(True)
        self.View.set_right_margin_position(settings.editor_margin_pos())
        # Smart Home and end, moves to the first no-blanc char before start and
        # end of line
        self.View.set_smart_home_end(True)
        # Indent Current Selection when press tab key
        self.View.set_indent_on_tab(True)
        self.View.set_highlight_current_line(True)
        self.View.set_buffer(self.Buffer)
        self.View.set_show_line_numbers(True)
        # TODO: Connect View Events
        return


    # Callbacks ----------------------------------------------------------------
    def __buffer_changed_cb(self, buff):
        self.__can_redo = buff.can_redo()
        self.__can_undo = buff.can_undo()


    def __buffer_modified_changed_cb(self, buff):
        self.__tab_title.set_modified(buff.get_modified())
        self.__is_untouched = buff.get_modified()

