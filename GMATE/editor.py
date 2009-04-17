# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import gtk
import gtksourceview2 as sw
import os

import GMATE

from GMATE.configuration import get_settings
from GMATE.document_manager import DocumentManager
from GMATE.status_bar import StatusBar
from GMATE.side_panel import SidePanel
from GMATE import i18n as i
from GMATE import plugin_system as plugin
from GMATE import get_style_scheme_manager, get_language_manager

#from GMATE import plugin_system as plugin

settings = get_settings()


class GmateEditor(gtk.Window):

    def __init__(self):
        super(GmateEditor, self).__init__(gtk.WINDOW_TOPLEVEL)
        # Connect Window Events ------------------------------------------------
        self.connect('delete-event', self.__delete_event_cb)
        self.set_property('border-width', 0)

        # GtkSourveView Objects ------------------------------------------------
        self.style_manager = get_style_scheme_manager()
        self.language_manager = get_language_manager()

        # Document Information -------------------------------------------------
        self.__active_document = None

        # Main Window Widgets --------------------------------------------------
        # Setup UIManager
        self.__uimanager = gtk.UIManager()
        self.__accelgroup = self.__uimanager.get_accel_group()
        self.add_accel_group(self.__accelgroup)
        # Setup Clipboard
        display = gtk.gdk.display_manager_get().get_default_display()
        self.__clipboard = gtk.Clipboard(display, "CLIPBOARD")
        self.__clip_primary = gtk.Clipboard(display, 'PRIMARY')
         # Setup Action Group
        self.__actiongroup = ag = gtk.ActionGroup('GMateUiManager')
        ag.add_actions(self.__actions())
        self.__uimanager.insert_action_group(ag, 0)
        self.__uimanager.add_ui_from_string(self.__ui_str())
        # Setup the Notebook (Tabbed Document)
        self.__notebook = gtk.Notebook()
        self.__notebook.set_property('tab-border', 2)
        self.__notebook.set_property('tab-hborder', 0)
        self.__notebook.set_property('tab-vborder', 0)
        self.__notebook.set_property('show-border', False)
        self.__notebook.set_property('can-focus', False)
        # TODO: Configuration for tab position
        self.__notebook.set_tab_pos(settings.tab_position())
        self.__notebook.set_scrollable(True)
        self.__notebook.set_show_tabs(True)

        # Setup Event Handling -------------------------------------------------
        self.__nb_change_page_id = self.__notebook.connect('switch-page', self.__nb_change_page_cb)
        self.__uimanager.connect('connect-proxy', self.__uimanager_connect_proxy_cb)
        self.__uimanager.connect('disconnect-proxy', self.__uimanager_disconnect_proxy_cb)

        # Setup the Status Bar -------------------------------------------------
        self.__status_box = StatusBar()
        self.__main_screen = gtk.VBox(False, GMATE.DEFAULT_BORDER_WIDTH)

        self.__side_panel = SidePanel()

        # TODO: Store and retrieve the last used size
        self.__side_panel.set_size_request(220, -1)
        self.__center_screen = gtk.HBox(False, GMATE.DEFAULT_BORDER_WIDTH)
        self.__left_hpaned = gtk.HPaned()
        self.__left_hpaned.pack1(self.__side_panel, False, True)
        self.__left_hpaned.pack2(self.__notebook, True, True)
        self.__center_screen.pack_start(self.__left_hpaned, True, True)
        menubar = self.__uimanager.get_widget('/MenuBar')
        self.__main_screen.pack_start(menubar, False, False)
        self.__main_screen.pack_start(self.__center_screen, True, True)
        self.__main_screen.pack_start(self.__status_box, False, False)
        self.DocumentManager = DocumentManager(self, self.__notebook, self.__status_box)
        self.add(self.__main_screen)
        self.set_border_width(GMATE.DEFAULT_BORDER_WIDTH)

        x, y, w, h = settings.get_last_window_bounds()
        #print x, y, w, h
        self.set_default_size(w, h)
        self.move(x, y)

        # Initialize Plugin System
        plugin.init_plugin_system()
        plugin.initialize_plugins(self, self.__uimanager)
        self.__main_screen.show_all()
        self.show()


    def __actions(self):
        return [
        ('File', None, i.menu_file),
            ('New',          gtk.STOCK_NEW,             i.menu_new,           None,                i.menu_new_desc,           self.new_document),
            ('Open',         gtk.STOCK_OPEN,            i.menu_open,          None,                i.menu_open_desc,          self.open_document),
            ('Save',         gtk.STOCK_SAVE,            i.menu_save,          None,                i.menu_save_desc,          self.__save_current),
            ('SaveAs',       gtk.STOCK_SAVE_AS,         i.menu_save_as,       None,                i.menu_save_as_desc,       self.__quit_cb),
            ('SaveAll',      gtk.STOCK_SAVE,            i.menu_save_all,      '<shift><control>s', i.menu_save_all_desc,      self.__quit_cb),
            ('Revert',       gtk.STOCK_REVERT_TO_SAVED, i.menu_revert,        None,                i.menu_revert_desc,        self.__quit_cb),
            ('CloseCurrent', gtk.STOCK_CLOSE,           i.menu_close_current, None,                i.menu_close_current_desc, self.__close_current),
            ('CloseAll',     gtk.STOCK_CLOSE,           i.menu_close_all,     '<shift><control>w', i.menu_close_all_desc,     self.__close_all_cb),
            ('Quit',         gtk.STOCK_QUIT,            i.menu_quit,          None,                i.menu_quit_desc,          self.__quit_cb),
        ('Edit', None, i.menu_edit),
            ('Undo',        gtk.STOCK_UNDO,        i.menu_undo,        None,         i.menu_undo_desc,        None),
            ('Redo',        gtk.STOCK_REDO,        i.menu_redo,        None,         i.menu_redo_desc,        None),
            ('Cut',         gtk.STOCK_CUT,         i.menu_cut,         None,         i.menu_cut_desc,         self.__cut_clipboard_cb),
            ('Copy',        gtk.STOCK_COPY,        i.menu_copy,        None,         i.menu_copy_desc,        self.__copy_clipboard_cb),
            ('Paste',       gtk.STOCK_PASTE,       i.menu_paste,       None,         i.menu_paste_desc,       self.__paste_clipboard_cb),
            ('Delete',      gtk.STOCK_DELETE,      i.menu_delete,      None,         i.menu_delete_desc,      self.__delete_selection_cb),
            ('SelectAll',   gtk.STOCK_SELECT_ALL,  i.menu_selectall,   '<control>a', i.menu_selectall_desc,   self.__select_all_cb),
            ('Preferences', gtk.STOCK_PREFERENCES, i.menu_preferences, None,         i.menu_preferences_desc, None),
        ('Search', None, i.menu_search),
            ('Find',       gtk.STOCK_FIND,             i.menu_find,      None,        i.menu_find_desc,      None),
            ('FindNext',   gtk.STOCK_GO_FORWARD,       i.menu_findnext,  'F3',        i.menu_findnext_desc,  None),
            ('FindPrior',  gtk.STOCK_GO_BACK,          i.menu_findprior, '<shift>F3', i.menu_findprior_desc, None),
            ('FindInc',    gtk.STOCK_FIND,             i.menu_findinc,   None,        i.menu_findinc_desc,   self.__quit_cb),
            ('Replace',    gtk.STOCK_FIND_AND_REPLACE, i.menu_replace,   None,        i.menu_replace_desc,   self.__quit_cb),
            ('GoToLine',   gtk.STOCK_JUMP_TO,          i.menu_gotoline,  None,        i.menu_gotoline_desc,  self.__quit_cb),
        ('About', None, i.menu_about),
            ('AboutGMate', gtk.STOCK_ABOUT, i.menu_about_gmate, None, i.menu_about_gmate_desc, self.__quit_cb)
        ]


    def __ui_str(self):
        return '''<ui>
        <menubar name="MenuBar">
          <menu action="File">
            <menuitem action="New"/>
            <menuitem action="Open"/>
            <separator/>
            <menuitem action="Save"/>
            <menuitem action="SaveAs"/>
            <menuitem action="SaveAll"/>
            <menuitem action="Revert"/>
            <separator/>
            <menuitem action="CloseCurrent"/>
            <menuitem action="CloseAll"/>
            <separator/>
            <menuitem action="Quit"/>
          </menu>
          <menu action="Edit">
            <menuitem action="Undo"/>
            <menuitem action="Redo"/>
            <separator/>
            <menuitem action="Cut"/>
            <menuitem action="Copy"/>
            <menuitem action="Paste"/>
            <menuitem action="Delete"/>
            <separator/>
            <menuitem action="SelectAll"/>
            <separator/>
            <menuitem action="Preferences"/>
          </menu>
          <menu action="Search">
            <menuitem action="Find"/>
            <menuitem action="FindNext"/>
            <menuitem action="FindPrior"/>
            <menuitem action="FindInc"/>
            <separator/>
            <menuitem action="Replace"/>
            <separator/>
            <menuitem action="GoToLine"/>
          </menu>
          <menu action="About">
            <menuitem action="AboutGMate"/>
          </menu>
        </menubar>
        </ui>'''

    # Public Methods ===========================================================

    def open_uri(self, file_uri, encoding='utf-8'):
        """
            Open the File URI in editor
        """
        doc = self.DocumentManager.load_document(file_uri, encoding)
        self.set_active_document(doc)
        return doc


    def new_document(self, widget=None):
        """
            Create a New document buffer and set the focus on it
        """
        new_doc = self.DocumentManager.new_document('python')
        self.set_active_document(new_doc)
        return new_doc


    def open_document(self, widget=None):
        # TODO: Create a separated Open Document Manager
        dialog = gtk.FileChooserDialog("Open File..", None,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL,
            gtk.RESPONSE_CANCEL,
            gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("Text Files")
        filter.add_mime_type("text/*")
        dialog.add_filter(filter)
        response = dialog.run()
        # TODO: Manage File Encoding....
        if response == gtk.RESPONSE_OK:
             fname = dialog.get_uri()
             self.open_uri(fname)
        dialog.destroy()


    def set_active_document(self, doc):
        self.__status_box.set_document(doc)
        self.__active_document = doc
        self.__notebook.handler_block(self.__nb_change_page_id)
        page = self.__notebook.page_num(self.__active_document)
        self.__notebook.set_current_page(page)
        self.__notebook.handler_unblock(self.__nb_change_page_id)
        self.__active_document.View.grab_focus()
        fname = doc.get_filename()
        if fname:
            title = "%s (%s)" % (os.path.basename(fname), os.path.dirname(fname))
        else:
            title = doc.get_tab_title()
        self.set_title('%s - GMate' % title)


    def get_active_document(self):
        """
            Return the current Active Document
        """
        return self.__active_document


    def get_status_box(self):
        return self.__status_box


    def get_side_panel(self):
        return self.__side_panel


    # Private methods ==========================================================
    def __save_current(self, widget=None):
        self.__active_document.save()


    def __close_current(self, widget=None):
        self.__active_document.close()


    def __cut_clipboard_cb(self, *args):
        owner = self.__clip_primary.get_owner()
        selection_text = None
        if isinstance(owner, sw.Buffer):
            buf, view = self.__active_document.get_buffer_view()
            buf.cut_clipboard(self.__clipboard, view.get_editable())
        elif isinstance(owner, gtk.Editable):
            owner.cut_clipboard(self.__clipboard)
        else:
            selection_text = self.__clip_primary.wait_for_text()
        if selection_text:
            self.__clipboard.set_text(selection_text, -1)
        return


    def __copy_clipboard_cb(self, *args):
        selection_text = None
        if self.__clip_primary.get_owner():
            selection_text = self.__clip_primary.wait_for_text()
        if selection_text:
            self.__clipboard.set_text(selection_text, -1)
        return


    def __paste_clipboard_cb(self, *args):
        w = self.get_focus()
        if isinstance(w, sw.View):
            buf, view = self.__active_document.get_buffer_view()
            buf.paste_clipboard(self.__clipboard, None, view.get_editable())
        elif isinstance(w, gtk.Editable):
            w.paste_clipboard(self.__clipboard, None, w.get_editable())
        return


    def __select_all_cb(self, *args):
        w = self.get_focus()
        if isinstance(w, sw.View):
            buf = self.__active_document.buffer
            start, end = buf.get_bounds()
            buf.select_range(start, end)
        elif isinstance(w, gtk.Editable):
            start, end = w.get_selection_bounds()
            w.select_region(start, end)
        return


    def __close_all_cb(self, *args):
        while self.__active_document:
            self.__active_document.close()


    def __delete_selection_cb(self, *args):
        buf = self.__active_document.buffer
        buf.delete_selection(True, True)


    def __nb_change_page_cb(self, notebook, page, page_num):
        plugin.trigger_method('desactivate_document', self.__active_document)
        doc = notebook.get_nth_page(page_num)
        self.set_active_document(doc)
        plugin.trigger_method('activate_document', doc)


    # Statusbar...... from Python FAQ
    def __menu_item_select_cb(self, menuitem, tooltip):
        self.__status_box.status_text.push(-1, tooltip)


    def __menu_item_deselect_cb(self, menuitem, tooltip=None):
        self.__status_box.status_text.pop(-1)


    def __uimanager_connect_proxy_cb(self, uimgr, action, widget):
        tooltip = action.get_property('tooltip')
        if isinstance(widget, gtk.MenuItem) and tooltip:
            cid = widget.connect('select', self.__menu_item_select_cb, tooltip)
            cid2 = widget.connect('deselect', self.__menu_item_deselect_cb)
            widget.set_data('app::connect-ids', (cid, cid2))


    def __uimanager_disconnect_proxy_cb(self, uimgr, action, widget):
        cids = widget.get_data('app::connect-ids') or ()
        for cid in cids:
            widget.disconnect(cid)


    def __delete_event_cb(self, widget, event):
        x, y, w, h = self.get_allocation()
        x, y = self.get_position()
        # For Some reason (I think window decoratinos) here pygtk add +3 and +25
        # pixels for x and y
        settings.set_last_window_bounds([x-3, y-25, w, h])
        # TODO: To prevent window from close, return True and not call __quit_cb
        self.__quit_cb(widget)
        return False


    def __quit_cb(self, widget):
        """
            Exit the editor Window
        """
        can_close = True
        if can_close:
            gtk.main_quit()
            return False
        return True

