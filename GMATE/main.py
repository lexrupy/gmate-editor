# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information


import gtk
import editor

class Gmate(object):

    def __init__(self):
        self.editor = editor.GmateEditor()
        self.editor.show()

    def run(self, file_uri=None):
        if file_uri:
            self.editor.open_uri(file_uri)
        else:
            self.editor.new_document()
        gtk.main()

