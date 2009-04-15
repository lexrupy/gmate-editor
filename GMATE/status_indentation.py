# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import gtk
from GMATE.status_widget import StatusWidget
from GMATE import i18n as i

class StatusIndentation(StatusWidget):
    ui = '''
        <ui>
            <popup name="TabIndentSelection">
                <menuitem action="TabWidth2"/>
                <menuitem action="TabWidth3"/>
                <menuitem action="TabWidth4"/>
                <menuitem action="TabWidth8"/>
                <separator/>
                <menuitem action="SoftTabs"/>
            </popup>
        </ui>
        '''

    def initialize(self):
        self.uimanager = gtk.UIManager()
        actiongroup = gtk.ActionGroup('TabIndentSelectionManager')

        actiongroup.add_toggle_actions([('SoftTabs', None, '_Soft Tabs', None,
            i.toggle_soft_tabs, self.toggle_soft_tabs_cb)])
        actiongroup.add_radio_actions([
            ('TabWidth2', None, '2', None, '2', 0),
            ('TabWidth3', None, '3', None, '2', 1),
            ('TabWidth4', None, '4', None, '4', 2),
            ('TabWidth8', None, '8', None, '8', 3)], 0, self.tabwidth_cb)
       # TODO: Set to other default when user use an unknown value (May atualize the label with that value)
       # and launch a popup window (input box) to enter new value
        self.uimanager.insert_action_group(actiongroup, 0)
        self.uimanager.add_ui_from_string(self.ui)
        # TODO: move this string to i18n
        self.button = gtk.Button()
        self.pack_start(self.button, False, False)
        menu = self.uimanager.get_widget('/TabIndentSelection')
        self.button.connect_object("event", self.button_press, menu)
        self.show_all()
        return

    def on_set_document(self, doc):
        self.document = doc.View
        action = self.uimanager.get_widget('/TabIndentSelection/SoftTabs')
        use_spaces = doc.View.get_insert_spaces_instead_of_tabs()
        action.set_active(use_spaces)
        w = doc.View.get_tab_width()
        action = self.uimanager.get_widget('/TabIndentSelection/TabWidth%d' % w)
        if action:
            action.set_active(True)
        width = doc.View.get_tab_width()
        self.button.set_label("%s: %d" % (self.get_tab_style_text(), width))

    def get_tab_style_text(self):
        if self.document.get_insert_spaces_instead_of_tabs():
            return i.soft_tabs
        return i.tab_stops

    def tabwidth_cb(self, action, current):
        width = (2, 2, 4, 8)[action.get_current_value()]
        self.document.set_tab_width(width)
        self.button.set_label("%s: %d" % (self.get_tab_style_text(), width))

    def toggle_soft_tabs_cb(self, action):
        if action.get_active():
            self.document.set_insert_spaces_instead_of_tabs(True)
        width = self.document.get_tab_width()
        self.button.set_label("%s: %d" % (self.get_tab_style_text(), width))

    def button_press(self, widget, event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            widget.popup(None, None, None, event.button, event.time)
            return True
        return False

