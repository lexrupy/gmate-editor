# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import gtk
import gnomevfs

from GMATE import files
from GMATE import i18n as i

def error(message):
    """Displays on error dialog with a single stock OK button."""
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL,
                               gtk.MESSAGE_ERROR,
                               gtk.BUTTONS_OK,
                               message)
    response = dialog.run()
    dialog.destroy()

def choice_ok_cancel(message, cancelDefault=False):
    """Displays an ok/cancel message dialog."""
    default = gtk.RESPONSE_OK
    if cancelDefault:
        default = gtk.RESPONSE_CANCEL
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL,
                               gtk.MESSAGE_QUESTION,
                               gtk.BUTTONS_OK_CANCEL,
                               message)
    dialog.set_default_response(default)
    response = dialog.run()
    dialog.destroy()
    return response

def choice_yes_no(message, noDefault=False):
    """Displays an yes/no message dialog."""
    default = gtk.RESPONSE_YES
    if noDefault:
        default = gtk.RESPONSE_NO
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL,
                               gtk.MESSAGE_QUESTION,
                               gtk.BUTTONS_YES_NO,
                               message)
    dialog.set_default_response(default)
    response = dialog.run()
    dialog.destroy()
    return response

def retrieve_new_file_name(uri=None):
    """Get the name of a file to create."""
    dialog = gtk.FileChooserDialog(action=gtk.FILE_CHOOSER_ACTION_SAVE)
    dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                       gtk.STOCK_ADD, gtk.RESPONSE_OK)
    # Default to the users home directory
    if uri is None:
        uri = files.get_user_home_uri()
    dialog.set_current_folder_uri(str(uri))
    # Get the response and the URI
    response = dialog.run()
    file_uri = dialog.get_uri()
    dialog.destroy()
    if response == gtk.RESPONSE_OK:
        if file_uri is not None:
            write = True
            # Check to be sure if the user wants to overwrite a file
            if gnomevfs.exists(file_uri):
                response = choice_yes_no(i.file_already_exists, True)
                if response == gtk.RESPONSE_NO:
                    write = False
            if write:
                # Return the new filename
                return file_uri
        else:
            raise IOError, i.no_file_specified
    return None

def retrieve_new_file_name(uri=None):
    """Get the name of a file to create."""
    dialog = gtk.FileChooserDialog(action=gtk.FILE_CHOOSER_ACTION_SAVE)
    dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                       gtk.STOCK_SAVE, gtk.RESPONSE_OK)
    # Default to the users home directory
    if uri is None:
        uri = files.get_user_home_uri()
    dialog.set_current_folder_uri(str(uri))
    # Get the response and the URI
    response = dialog.run()
    file_uri = dialog.get_uri()
    dialog.destroy()
    if response == gtk.RESPONSE_OK:
        if file_uri is not None:
            write = True
            # Check to be sure if the user wants to overwrite a file
            if gnomevfs.exists(file_uri):
                response = choice_yes_no(i.file_already_exists, True)
                if response == gtk.RESPONSE_NO:
                    write = False
            if write:
                # Return the new filename
                return file_uri
        else:
            raise IOError, i.no_file_specified
    return None

