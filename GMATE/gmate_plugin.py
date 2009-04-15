# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

BUILTIN_PLUGIN          = -1
TEXT_MANIPULATION_PLUGIN=  0
LANGUAGE_PLUGIN         =  1
INTERFACE_HELPER_PLUGIN =  2

from GMATE.configuration import get_settings

settings = get_settings()

class GMatePlugin(object):
    plugin_type = None

    def __init__(self, window, uimanager):
        self.window = window
        self.uimanager = uimanager
        self.menu_merge_id = None

    def finalize(self):
        if self.menu_merge_id:
            self.uimanager.remove_ui(self.menu_merge_id)
        self.teardown()


    # Public Helper Methods ====================================================
    # These methods are Helpers to DRY with frequent tasks
    # DO NOT Override unless you know what you are doing

    def get_current_document(self):
        self.window.get_active_document()

    def get_current_buffer(self):
        document = get_current_document()
        if document:
            return document.buffer
        return None

    def get_current_view(self):
        document = get_current_document()
        if document:
            return document.view
        return None

    def get_current_buffer_view(self):
        document = get_current_document()
        if document:
            return (document.buffer, document.view)
        return (None, None)

    def add_gmate_menu_ui(self, str_ui, action_group):
        if self.uimanager:
            self.uimanager.insert_action_group(action_group, -1)
            self.menu_merge_id = self.uimanager.add_ui_from_string(str_ui)
        return

    def get_current_encoding(self):
        doc = self.get_current_document()
        if doc:
            return doc.encoding
        return settings.default_file_encoding()

    def get_current_file_path(self):
        return self.window.get_current_document_path()


    # Public Plugin API ========================================================
    # Override these methods in your plugin to get functionality

    def setup(self):
        """Startup Method"""
        return False

    def document_activate(self, document=None):
        """Triggered when a document is activated, tab has changed to here"""
        return True

    def document_desactivate(self, document=None):
        """Triggered when document is desactiveted (Tab has changed)"""
        return True

    def document_close(self, document=None):
        """Triggered when document is being to close"""
        return True

    def configure(self):
        """When on plugin configuration screen a on click on configure button
           this method will be called"""
        return None

    def about(self):
        """When on plugin configuration screen a on click on about button
           this method will be called"""
        return None

    def help(self):
        """When on plugin configuration screen a on click on help button
           this method will be called"""
        return None

    def teardown(self):
        """Finalization method, do filalization needed here"""
        pass

