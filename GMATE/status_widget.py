# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import gtk

class StatusWidget(gtk.HBox):
    """
        Generic Box for status information.
        This class it's much more like an Interface, you can create a statusbox
        extending from other Widgets, and implement the methods on_set_document
        and on_disconnect there.
    """
    def __init__(self):
        super(StatusWidget, self).__init__(False, 2)
        self.initialize()

    def initialize(self, current_document):
        """
            Place initialization process overriding this method
        """
        pass

    def on_set_document(self, doc):
        """
            Override this method to capture the event when current document is
            set to StatusBar.
        """
        pass

    def on_disconnect(self):
        """
            Override this method to capture the event when statusbar is
            disconnected
        """

