# -*- coding: utf-8 -*-
# Eddt is a directory browsing plugin written in Python for the Gnome text
# editor, gedit.
#
# Copyright (C) 2006 Michael Diolosa <michael@mbrio.org>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.

"""Eddt is a directory browsing plugin written in Python for the Gnome text
editor, gedit.

"""

__all__ = (u'EddtPlugin', u'ProjectExplorer')

import gtk

from projectexplorer import ProjectExplorer
from projecttreeview import ProjectTreeView
from i18n import msg0005
from treecellmenu import TreeCellMenu

from GMATE.gmate_plugin import GMatePlugin

class ProjectManager(GMatePlugin):

    def setup(self):
        self.DATA_KEY = 'GMateProjectManagerPlugin'
        self.__create_ui()
        self.window.set_data(self.DATA_KEY, self.__project_explorer)

    def teardown(self):
        self.__destroy_ui()
        self.window.set_data(self.DATA_KEY, None)

    def __create_ui(self):
        """Creates all UI elements needed by ProjectExplorer."""
        vbox = gtk.VBox()

        # Create the viewable area of the file browser
        self.__view_port = gtk.ScrolledWindow()
        self.__view_port.set_policy(gtk.POLICY_AUTOMATIC,
                                   gtk.POLICY_AUTOMATIC)
        # Create the tree view and add it to the viewable area
        self.__tree_view = ProjectTreeView()
        self.__project_explorer = ProjectExplorer(self.window, self.__tree_view)
        self.__tree_view.connect('button_press_event',
                                self.__on_treeview_button_press_event)
        self.__project_explorer.set_repository()
        self.__view_port.add(self.__tree_view)
        # Create the toolbar
        hbox = gtk.HBox()
        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_ICONS)
        toolbar.set_icon_size(gtk.ICON_SIZE_MENU)
        back = gtk.ToolButton(gtk.STOCK_GO_UP)
        back.connect('clicked', self.__on_back_clicked)
        toolbar.insert(back, 0)
        toolbar.insert(gtk.SeparatorToolItem(), 1)
        refresh = gtk.ToolButton(gtk.STOCK_REFRESH)
        refresh.connect('clicked', self.__on_refresh_clicked)
        toolbar.insert(refresh, 2)
        hbox.pack_start(toolbar, True, True, 0)
        vbox.pack_start(hbox, False, False, 0)
        vbox.pack_start(self.__view_port, True, True, 0)

        # Setup the create the buttons for:
        # New File, New Folder
        # ----------------------------------------------------------------------
        hbox1 = gtk.VBox()
        toolbar_actions = gtk.Toolbar()
        toolbar_actions.set_style(gtk.TOOLBAR_ICONS)
        toolbar_actions.set_icon_size(gtk.ICON_SIZE_MENU)
        new_file = gtk.ToolButton(gtk.STOCK_NEW)
        new_file.connect('clicked', self.__on_new_file_clicked_cb)
        toolbar_actions.insert(new_file, 0)
        new_dir = gtk.ToolButton(gtk.STOCK_OPEN) # TODO: use a custom icon
        new_dir.connect('clicked', self.__on_new_dir_clicked_cb)
        toolbar_actions.insert(new_dir, 1)
        hbox1.pack_start(gtk.HSeparator(), True, True, 0)
        hbox1.pack_start(toolbar_actions, True, True, 0)
        vbox.pack_end(hbox1, False, False, 0)
        # ----------------------------------------------------------------------
        vbox.show_all()
        # Attach the project explorer to GMate's side panel
        self.__side_panel = self.window.get_side_panel()
        self.__side_panel.add_tab(vbox, msg0005, gtk.STOCK_HARDDISK)


    def __destroy_ui(self):
        """Removes all UI elements created by ProjectExplorer."""
        # Remove the viewable area from Gedit's side panel
        self.__side_panel.remove_item(self.__view_port)

        # Empty class's properties
        self.__tree_view = None
        self.__side_panel = None

        self.__view_port.destroy()
        self.__view_port = None

    def __on_refresh_clicked(self, widget):
        self.__project_explorer.refresh()

    def __on_back_clicked(self, widget):
        self.__project_explorer.navigate_to_parent()

    def __on_new_file_clicked_cb(self, widget):
        # TODO: implement
        print self.__project_explorer.get_repository()

    def __on_new_dir_clicked_cb(self, widget):
        # TODO: implement
        print self.__project_explorer.get_repository()


    def __on_treeview_button_press_event(self, widget, event):
        """Display a menu based on what item was right clicked."""
        # Display the menu when right clicked
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)

            # Get the path of the item clicked we'll need this to retrieve the
            # corresponding PathDescriptor
            path = self.__tree_view.get_path_at_pos(x, y)

            if path is not None:
                # Get the PathDescriptor of the item clicked for use when
                # opening up the menu
                path_iter = self.__tree_view.get_model().get_iter(path[0])
                desc = self.__tree_view.get_model().get_value(path_iter, 0)

                # Display the menu based on the PathDescriptor
                menu = TreeCellMenu(self.__project_explorer)
                menu.display(desc, event)

    def get_project_root(self):
        """
            Return the current project root. This is usefull to other plugin
            interation
            returns: gnomevfs.URI
        """
        return self.__tree_view.get_repository()

