# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information
# Based on snap-open v1.1.5


import gtk, gtk.glade
import os, os.path, gobject
import i18n as i
from GMATE.gmate_plugin import GMatePlugin

# set this to true for gedit versions before 2.16
pre216_version = False

max_result = 50

ui_str='''<ui>
<menubar name="MenuBar">
    <menu action="Search">
        <menuitem name="GoToFile" action="GoToFile"/>
    </menu>
</menubar>
</ui>'''

# essential interface
class GoToFile(GMatePlugin):
    def setup(self):
        self._encoding = self.get_current_encoding()
        self._rootdir = "file://" + os.getcwd()
        self._show_hidden = False
        self._liststore = None;
        self._init_glade()
        self.add_menu()

    def add_menu(self):
        actions = [('GoToFile', gtk.STOCK_OPEN, i.menu_gotofile , '<Control>t',
            i.menu_gotofile_desc, self.show_go_to_file_dialog_cb)]
        action_group = gtk.ActionGroup("GoToFileActions")
        action_group.add_actions(actions)
        self.add_gmate_menu_ui(ui_str, action_group)

    # UI DIALOGUES
    def _init_glade(self):
        self._gotofile_glade = gtk.glade.XML(os.path.dirname(__file__) + "/gotofile.glade")
        #setup window
        self._gotofile_window = self._gotofile_glade.get_widget("GoToFileWindow")
        self._gotofile_window.connect("key-release-event", self.on_window_key)
        self._gotofile_window.set_transient_for(self.window)
        #setup buttons
        self._gotofile_glade.get_widget("ok_button").connect("clicked", self.open_selected_item)
        self._gotofile_glade.get_widget("cancel_button").connect("clicked", lambda a: self._gotofile_window.hide())
        #setup entry field
        self._glade_entry_name = self._gotofile_glade.get_widget("entry_name")
        self._glade_entry_name.connect("key-release-event", self.on_pattern_entry)
        #setup list field
        self._hit_list = self._gotofile_glade.get_widget("hit_list")
        self._hit_list.connect("select-cursor-row", self.on_select_from_list)
        self._hit_list.connect("button_press_event", self.on_list_mouse)
        self._liststore = gtk.ListStore(str, str, str)
        self._hit_list.set_model(self._liststore)
        column = gtk.TreeViewColumn("Name" , gtk.CellRendererText(), markup=0)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column2 = gtk.TreeViewColumn("File", gtk.CellRendererText(), markup=1)
        column2.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        self._hit_list.append_column(column)
        self._hit_list.append_column(column2)
        self._hit_list.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

    #mouse event on list
    def on_list_mouse(self, widget, event):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            self.open_selected_item(event)

    #key selects from list (passthrough 3 args)
    def on_select_from_list(self, widget, event):
        self.open_selected_item(event)

    #keyboard event on entry field
    def on_pattern_entry(self, widget, event):
        oldtitle = self._gotofile_window.get_title().replace(i.too_many_hits, "")
        if event.keyval == gtk.keysyms.Return:
            self.open_selected_item(event)
            return
        pattern = self._glade_entry_name.get_text()
        pattern = pattern.replace(" ","*")
        #modify lines below as needed, these defaults work pretty well
        rawpath = self._rootdir.replace("file://", "")
        filefilter = " | grep -s -v \"/\.\""
        cmd = ""
        if self._show_hidden:
            filefilter = ""
        if len(pattern) > 0:
            cmd = "cd " + rawpath + "; find . -maxdepth 10 -depth -type f -iwholename \"*" + pattern + "*\" " + filefilter + " | grep -v \"~$\" | head -n " + repr(max_result + 1) + " | sort"
            self._gotofile_window.set_title(i.searching)
        else:
            self._gotofile_window.set_title(i.enter_pattern)

        self._liststore.clear()
        maxcount = 0
        hits = os.popen(cmd).readlines()
        for file in hits:
            file = file.rstrip().replace("./", "") #remove cwd prefix
            name = os.path.basename(file)

            self._liststore.append([self.highlight_pattern(name, pattern), self.highlight_pattern(file, pattern), file])
            if maxcount > max_result:
                break
            maxcount = maxcount + 1
        if maxcount > max_result:
            oldtitle = oldtitle + i.too_many_hits
        self._gotofile_window.set_title(oldtitle)

        selected = []
        self._hit_list.get_selection().selected_foreach(self.foreach, selected)

        if len(selected) == 0:
            iter = self._liststore.get_iter_first()
            if iter != None:
                self._hit_list.get_selection().select_iter(iter)


    def highlight_pattern(self, path, pattern):
        query_list = pattern.lower().split("*")
        last_postion = 0
        for word in query_list:
            location = path.lower().find(word, last_postion)
            if location > -1:
                last_postion = (location + len(word) + 3)
                a_path = list(path)
                a_path.insert(location, "<b>")
                a_path.insert(location + len(word) + 1, "</b>")
                path = "".join(a_path)
        return path


    def show_go_to_file_dialog_cb(self, *args):
        self._rootdir = self.get_root_path()
        print self._rootdir
        self._gotofile_window.show()
        self._glade_entry_name.select_region(0,-1)
        self._glade_entry_name.grab_focus()


    def on_window_key(self, widget, event):
        if event.keyval == gtk.keysyms.Escape:
            self._gotofile_window.hide()


    def foreach(self, model, path, iter, selected):
        selected.append(model.get_value(iter, 2))


    def open_selected_item(self, event):
        selected = []
        self._hit_list.get_selection().selected_foreach(self.foreach, selected)
        for selected_file in selected:
            self._open_file(selected_file)
        self._gotofile_window.hide()


    def _open_file(self, filename):
        uri = self._rootdir + "/" + filename
        self.window.open_uri(uri, self._encoding)
        #dm = self.window.DocumentManager
        #dm.load_document(uri, self._encoding)


    def get_root_path(self):
        pm = self.locate_plugin('ProjectManager')
        if pm:
            return str(pm.get_project_root())
        else:
            return self.get_current_file_path()

