# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import gtk
import GMATE
from GMATE import i18n as i
from GMATE.document import Document
from GMATE.file_manager import GnomeFileManager as FileManager


class TabTitle(gtk.HBox):

    def __init__(self):
        super(TabTitle, self).__init__()
        self.set_homogeneous(False)
        self.set_spacing(3)
        self.icon = gtk.Image()
        self.__doc = None
        # Default document Icon
        self.icon.set_from_stock(gtk.STOCK_DND, gtk.ICON_SIZE_MENU)
        self.title_label = gtk.Label(i.untitled)
        self.close_btn = gtk.Button()
        self.close_btn.connect("clicked", self.__close)
        self.__add_close_icon(self.close_btn)
        self.pack_end(self.title_label, True, True)
        self.pack_start(self.close_btn, False, False,0)
        return self.show_all()

    # Public Methods ===========================================================
    def set_modified(self, modified):
        """
            Defines the title of document as Modified changing the icon look.
        """
        if modified:
            self.close_img.set_from_file(GMATE.GMATE_DATA_FOLDER + '/images/dirty.png')
        else:
            self.close_img.set_from_file(GMATE.GMATE_DATA_FOLDER + '/images/close.png')
        return

    def set_title(self, title):
        """
            Set the title of tab with the given text
        """
        self.title_label.set_text(title)
        return

    def get_title(self):
        """
            Return current title text shown in tab
        """
        return self.title_label.get_text()

    def set_doc(self, doc):
        """
            Defines the document related to this tab, so when click at close
            button Gmate Knows what document to close.
        """
        self.__doc = doc

    # Private Methods ===========================================================
    def __add_close_icon(self, button):
        box = gtk.HBox(False, 0)
        self.close_img = gtk.Image()
        self.close_img.show()
        self.close_img.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        self.set_modified(False)
        button.set_relief(gtk.RELIEF_NONE)
        settings = button.get_settings()
        (w,h) = gtk.icon_size_lookup_for_settings(settings, gtk.ICON_SIZE_MENU)
        button.set_size_request(w + 4, h + 4)
        box.pack_start(self.close_img, True, False, 0)
        button.add(box)
        box.show()
        return

    def __close(self, widget):
        # TODO: when close the last document, create a new empty document
        # And if the current document is a new umodified document, just ignore
        #self.statusbar.disconnect_all()
        if self.__doc:
            self.__doc.close()


class DocumentManager(object):
    """
        This class manage documents of Gmate, it is responsible by create, load
        and save documents.
    """

    def __init__(self, window, notebook, status_bar):
        self.documents = []
        self.new_document_count = 0
        self.window = window
        self.status_bar = status_bar
        self.notebook = notebook


    # Public Methods ===========================================================
    def new_document(self, language='none'):
        """
            Create a New document with the given language
        """
        self.new_document_count += 1
        return self.__create_document(language)


    def load_document(self, uri, encoding='utf-8'):
        """
            Load the document from URI with given encoding
            If you are a plugin developer, please use GmateEditor.open_uri
            instead
        """
        doc = self.get_document_by_uri(uri)
        if not doc:
            language = 'none'
            doc =  self.__create_document(language)
            self.file_manager = FileManager()
            self.file_manager.open_file(doc, uri, encoding)
        return doc


    def save_document(self, document):
        """
            Save the given document to file
        """
        return self.file_manager.save_file(document)


    def get_document_by_uri(self, uri):
        """
            Look at open document list and return the document if it's already
            open or None if not.
        """
        for doc in self.documents:
            if doc.get_uri() == uri:
                return doc
        return None

    def get_notebook(self):
        """
            Return the GtkNotebook Component used in DocumentManager
        """
        return self.notebook

    # Private Methods ==========================================================

    def __create_document(self, language):
        """
            Create a new document with the given language
        """
        title = TabTitle()
        doc = Document(self.window, title, language)

        title_text = i.new_document_title % self.new_document_count
        doc.set_title(title_text)

        self.notebook.append_page(doc, title)
        # Add to list of documents
        self.documents.append(doc)
        doc.document_manager = self
        return doc

