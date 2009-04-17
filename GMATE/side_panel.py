# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import gtk

class SidePanel(gtk.Notebook):

    def __init__(self):
        super(SidePanel, self).__init__()
        # TODO: Implement a Global Close Button for Pannel
        self.set_tab_pos(gtk.POS_BOTTOM)
        self.set_property('can-focus', False)
        self.set_scrollable(True)
        self.set_show_tabs(True)


    def add_tab(self, widget, name, icon=None):
        title = gtk.HBox()
        title.set_border_width(5)
        image = None
        if icon:
            image = gtk.Image()
            image.set_from_stock(icon, gtk.ICON_SIZE_MENU)
            image1 = gtk.Image()
            image1.set_from_stock(icon, gtk.ICON_SIZE_MENU)
            title.pack_start(image1, False, False, 2)
        title.pack_start(gtk.Label(name), False, False, 3)
        # TODO: Here add close button
        box = gtk.VBox()
        box.pack_start(title, False, False, 0)
        box.pack_start(widget, True, True, 0)
        self.append_page(box, image)

