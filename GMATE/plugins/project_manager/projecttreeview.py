# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

"""A widget used to display the file/folder structure of projects."""

import re

import gtk
import gnomevfs

from GMATE import files
from pathdescriptor import PathDescriptor
from icons import Icons
from settings import Settings
from i18n import msg0002, msg0003, err0010, err0011

class ProjectTreeView(gtk.TreeView):
    """A widget for displaying the files within a repositoy."""

    def __init__(self):
        """Constructor.
        Creates the initial view of the project repository."""
        super(ProjectTreeView, self).__init__()
        self.__current_repository = None
        self.__activate_file = None
        self.__refresh = None
        self.__settings = Settings()
        self.__initialize_treeview()
        self.__initialize_icons()
        self.__initialize_columns()

    def set_activate_file(self, afile=None):
        """Sets the method to use when activating a file."""
        if afile is not None and not callable(afile):
            raise ValueError, err0010
        self.__activate_file = afile

    def set_refresh(self, refresh=None):
        """Sets the method to use when refreshing."""
        if refresh is not None and not callable(refresh):
            raise ValueError, err0011
        self.__refresh = refresh

    def get_repository(self):
        """Gets the URI associated with the currently opened repository."""
        return self.__current_repository

    def refresh(self):
        """Refreshes the current view."""
        current_repo = self.get_repository()
        # Check to be sure we have a current repository
        if current_repo is not None:
            # Collection to hold all expanded rows
            open_paths = []
            # Append all the expanded paths to the collection
            self.map_expanded_rows(self.__map_expanded_rows, open_paths)
            self.__refresh()
            # Expand all previously expanded paths
            path_iter = self.get_model().get_iter_root()
            self.__expand_previously_open_rows(path_iter, open_paths)
            del open_paths[0:]

            self.queue_draw()

    def set_repository(self, uri):
        """Sets the repository to be viewed.

        @param uri: The URI to set the repository to.
        @type uri: a gnomevfs.URI

        """
        self.__current_repository = uri

        self.get_model().clear()

        # Create the root directory within the list
        parent_dir = self.__append_descriptor(uri, True, None)

        # Be sure there is a loading item within the current directory
        self.__append_loading_cell(parent_dir)

        # Expand the current directory to show the rest of the files
        iterpath = self.get_model().get_path(parent_dir)
        self.expand_row(iterpath, False)

        self.queue_draw()

    def __expand_previously_open_rows(self, path_iter, open_paths):
        """Expands any previously opened paths after a refresh."""
        while path_iter is not None:
            desc = self.get_model().get_value(path_iter, 0)

            # Be sure we have a PathDescriptor
            if isinstance(desc, PathDescriptor):
                # If the path was previously opened open it
                if desc.get_uri() in open_paths:
                    path = self.get_model().get_path(path_iter)
                    self.expand_row(path, False)

                    # Remove it from the list
                    open_paths.remove(desc.get_uri())

                # If the iterator has children, check to see if any should
                # be open
                if self.get_model().iter_has_child(path_iter):
                    child = self.get_model().iter_nth_child(path_iter, 0)
                    self.__expand_previously_open_rows(child, open_paths)

            # Move to the next row
            path_iter = self.get_model().iter_next(path_iter)

    def __map_expanded_rows(self, widget, path, data):
        """Store previously opened paths."""
        # Append URI values to track what is open
        path_iter = self.get_model().get_iter(path)

        if path_iter is not None:
            desc = self.get_model().get_value(path_iter, 0)

            if isinstance(desc, PathDescriptor):
                data.append(desc.get_uri())

    def __initialize_treeview(self):
        """Create the view and set its properties."""
        treestore = gtk.TreeStore(object, gtk.gdk.Pixbuf, gtk.gdk.Pixbuf)

        self.set_property(u'model', treestore)
        self.set_property(u'enable-search', False)
        self.set_property(u'headers-visible', False)

        self.connect(u'test-expand-row', self.__on_expand_row)
        self.connect(u'row-activated', self.__on_row_activated)
        self.connect(u'row-collapsed', self.__on_collapse_row)

    def __initialize_columns(self):
        """Creates the columns for the view."""
        # Create the necessary widgets for the view
        image_renderer = gtk.CellRendererPixbuf()
        name_renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn()

        # Pach the icon renderer and the text label renderer into the view
        column.pack_start(image_renderer, False)
        column.pack_start(name_renderer, True)

        # Set the icons for the icon renderer
        column.set_attributes(image_renderer, pixbuf=1, pixbuf_expander_open=2,
                              pixbuf_expander_closed=1)

        # Set the texit labels method for retrieving the file's name
        column.set_cell_data_func(name_renderer, self.__retrieve_filename)

        self.append_column(column)

    def __initialize_icons(self):
        """Retrieves the icons needed to display within the file view."""
        self.__icons = Icons(self)

    def __populate_directory(self, uri, parent=None):
        """Populates the directory list alphabetically by directory then by
        file.

        @param uri: the URI of the directory.
        @type uri: a gnomevfs.URI

        @param parent: the parent iterator to append the child to.
        @type parent: a gtk.TreeIter
        """
        # Retrieve directories alphabetically
        directory = gnomevfs.DirectoryHandle(uri)
        file_filter = self.__settings.get_file_filter()
        show_file = None

        if len(file_filter) > 0:
            comp = re.compile(file_filter)

            def __show_file(file_name):
                if comp.search(file_name) is not None:
                    return True

                return False

            show_file = __show_file

        for file_info in sorted(directory, cmp=self.__compare_files):
            # Process folders
            if files.is_visible_dir(file_info):
                file_uri = uri.append_file_name(file_info.name)

                cur_dir = self.__append_descriptor(file_uri, True, parent)
                self.__append_loading_cell(cur_dir)

            # Process Files
            elif files.is_visible_file(file_info):
                if show_file is not None and not show_file(file_info.name):
                    continue

                file_uri = uri.append_file_name(file_info.name)

                self.__append_descriptor(file_uri, False, parent)

    def __compare_files(self, file_a, file_b):
        """Compares to files and determines which is first based on file type
        and file name."""
        type_a = file_a.type
        type_b = file_b.type

        # Make folders the most important in the list
        if type_a == gnomevfs.FILE_TYPE_DIRECTORY: type_a = 0
        else: type_a = 1

        if type_b == gnomevfs.FILE_TYPE_DIRECTORY: type_b = 0
        else: type_b = 1

        type_comp = cmp(type_a, type_b)

        # If the files are the same type then compare names
        if type_comp == 0:
            return cmp(file_a.name, file_b.name)

        return type_comp

    def __empty_directory(self, iterator):
        """Removes all the items within a directory on the tree."""
        model = self.get_model()

        # Remove each of the child nodes within the iterator
        while model.iter_has_child(iterator):
            child = model.iter_nth_child(iterator, 0)
            model.remove(child)

    def __append_descriptor(self, uri, is_dir, parent):
        """Creates a tree node with a path descriptor."""
        open_icon = None
        default_icon = None

        # Retrieve a default and open icon if the URI is a folder, otherwise
        # just a default icon
        if is_dir:
            open_icon = self.__icons.folder_open
            default_icon = self.__icons.folder
        else:
            default_icon = self.__icons.retrieve_file_icon(str(uri))

        # Create a descriptor and append a new node that represents that
        # descriptor into the tree
        desc = PathDescriptor(uri, is_dir)
        parent_dir = self.get_model().append(parent, [desc, default_icon,
                                                      open_icon])

        # Attach the corresponding tree iterator to the descriptor
        desc.set_iter(parent_dir)

        return parent_dir

    def __append_empty_cell(self, iterator):
        """Creates an 'empty' cell within the tree."""
        self.get_model().append(iterator, [msg0003, None, None])

    def __append_loading_cell(self, iterator):
        """Creates a 'loading' cell within the tree."""
        self.get_model().append(iterator, [msg0002, None, None])

    def __retrieve_filename(self, column, cell, model, iterator):
        """Retrieves the filename of the PathDescriptor."""
        desc = model.get_value(iterator, 0)

        # Retrieve the filename of the PathDescriptor or string.
        if isinstance(desc, PathDescriptor):
            cell.set_property(u'text', desc.get_name())
        else:
            cell.set_property(u'text', desc)

    def __on_expand_row(self, widget, iterator, path, data=None):
        """Empties a directory then loads in the files."""
        if iterator is not None:
            desc = self.get_model().get_value(iterator, 0)

            if not isinstance(desc, PathDescriptor):
                return

            # If the object is a directory clear its contents within the tree
            # and rescan it
            if desc.is_dir():
                self.freeze_child_notify()

                # Empty the directory
                self.__empty_directory(iterator)

                self.__populate_directory(desc.get_uri(), iterator)

                # Append an "Empty" cell if the directory is empty
                if not self.get_model().iter_has_child(iterator):
                    self.__append_empty_cell(iterator)

                self.thaw_child_notify()
                self.queue_draw()

    def __on_collapse_row(self, widget, iterator, path, data=None):
        """Empties a directory to conserve memory."""
        if iterator is not None:
            desc = self.get_model().get_value(iterator, 0)

            if not isinstance(desc, PathDescriptor):
                return

            # If the object is a directory clear its contents within the tree
            # and rescan it
            if desc.is_dir():
                self.freeze_child_notify()

                # Empty the directory
                self.__empty_directory(iterator)

                # Append a loading node to be used later when expanding
                self.__append_loading_cell(iterator)

                self.thaw_child_notify()
                self.queue_draw()

    def __on_row_activated(self, widget, path, view_column, data=None):
        """Enters a directory or loads a file."""
        iterator = self.get_model().get_iter(path)

        if iterator is not None:
            desc = self.get_model().get_value(iterator, 0)

            # Be sure we hane a PathDescriptor before we try to activate the
            # node.
            if not isinstance(desc, PathDescriptor):
                return

            # Expand or collapse a directory
            if desc.is_dir():
                if self.row_expanded(path):
                    self.collapse_row(path)
                else:
                    self.expand_row(path, False)

            # Activate the file
            else:
                if self.__activate_file is not None:
                    self.__activate_file(desc)

            self.queue_draw()

