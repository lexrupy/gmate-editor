# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

from utils import get_language_for_mime_type, to_unicode_or_bust
from files import get_last_modification

from gnomevfs import AccessDeniedError, NotFoundError, EOFError
from gnomevfs import get_local_path_from_uri, get_uri_scheme, get_file_info
from gnomevfs import FILE_INFO_DEFAULT, FILE_INFO_GET_MIME_TYPE, OPEN_READ, URI
from gnomevfs import FILE_INFO_FORCE_SLOW_MIME_TYPE, FILE_INFO_FOLLOW_LINKS
from gnomevfs.async import open

from exceptions import PermissionError, OpenFileError, NotFoundError
from exceptions import AccessDeniedError, FileInfoError, FileInfoError
from exceptions import ReadFileError, CloseFileError, GnomeVfsError

# from EncodedFilesMetadata import get_value

from os import access, W_OK, R_OK
import os.path
from GMATE import i18n as i
from GMATE import GMATE_BACKUP_FOLDER

from files import get_mime_type

class GnomeFileManager(object):

    def __init__(self):
        self.__document = None
        self.__mime_type = None
        self.__encoding = None
        self.__uri = None
        self.__filename = None

    def open_file(self, document, uri, encoding, readonly=False):
        try:
            self.__encoding = encoding
            self.__document = document
            self.__uri = uri
            self.__filename = get_local_path_from_uri(uri)
            self.__readonly = readonly
            self.__handle = None
            self.__temp_buffer = ""
            self.__writable_vfs_schemes = ["ssh", "sftp", "smb", "dav", "davs", "ftp"]
            self.__get_file_info()
            self.__verify_permissions()
            self.__get_mime_type()
            self.__load_uri()
            self.__create_backup()
            self.__set_document_configuration()
        except:
            raise
#        except PermissionError:
#            self._error(i.exception_no_permission)
#        except AccessDeniedError:
#            self._error(i.exception_load_remote)
#        except FileInfoError:
#            self._error(i.exception_file_information)
#        except NotFoundError:
#            self._error(i.exception_file_not_exist)
#        except:
#            self._error(i.unknown_exception)


    def __get_mime_type(self):
        self.__mime_type = get_mime_type(self.__uri)
        return


    def __get_file_info(self):
        try:
            if self.__uri.startswith("file:///"): return
            # TODO: self.__document.init_authentication_manager()
            FILE_INFO_ACCESS_RIGHTS = 1 << 4
            fileinfo = get_file_info(self.__uri, FILE_INFO_DEFAULT |
                                        FILE_INFO_GET_MIME_TYPE |
                                        FILE_INFO_FORCE_SLOW_MIME_TYPE |
                                        FILE_INFO_FOLLOW_LINKS |
                                        FILE_INFO_ACCESS_RIGHTS)
            if not fileinfo:
                raise FileInfoError
        except AccessDeniedError:
            raise AccessDeniedError
        except NotFoundError:
            raise NotFoundError
        except:
            raise FileInfoError
        return


    def __verify_permissions(self):
        if self.__uri.startswith("file:///"):
            local_path = get_local_path_from_uri(self.__uri)
            if access(local_path, R_OK):
                if not access(local_path, W_OK):
                    self.__readonly = True
            else:
                raise PermissionError
        else:
            scheme = get_uri_scheme(self.__uri)
            if not scheme in self.__writable_vfs_schemes:
                self.__readonly = True
        return


    def __load_uri(self):
        try:
            open(URI(self.__uri), self.__open_cb, OPEN_READ, 10)
        except:
            self._error(i.exception_file_open)
        return


    def __open_cb(self, handle, result):
        try:
            self.__handle = handle
            if self.__uri.startswith("file:///"):
                try:
                    local_path = get_local_path_from_uri(self.__uri)
                    size = os.path.getsize(local_path)
                    if not (size): size = 4096
                    handle.read(size, self.__read_cb)
                except:
                    raise ReadFileError
            else:
                try:
                    handle.read(4096, self.__read_cb)
                except:
                    raise ReadFileError
        except ReadFileError:
            self._error(i.exception_file_read)
        return


    def __read_cb(self, handle, buffer, result, bytes):
        try:
            if self.__uri.startswith("file:///"):
                if not (result in (None, EOFError)): raise GnomeVfsError
                self.__insert_string_to_buffer(buffer, handle)
                try:
                    handle.close(self.__close_cb)
                except:
                    raise CloseFileError
            else:
                if result is None:
                    try:
                        self.__temp_buffer += buffer
                        handle.read(4096, self.__read_cb)
                    except:
                        raise ReadFileError
                elif (result == EOFError):
                    try:
                        self.__insert_string_to_buffer(self.__temp_buffer, handle)
                        handle.close(self.__close_cb)
                    except:
                        raise ReadFileError
                else:
                    raise GnomeVfsError
        except CloseFileError:
            self._error(i.exception_file_close)
        except ReadFileError:
            self._error(i.exception_file_read)
        except GnomeVfsError:
            self._error("GnomeVfsError")
        return


    def __close_cb(self, *args):
        # TODO: Put editor in read only mode here if file is read only
        self._destroy()
        return


    def __insert_string_to_buffer(self, string, handle=None):
        try:
            unicode_string = to_unicode_or_bust(string, self.__encoding)
            utf8_string = unicode_string.encode("utf-8")
            buf = self.__document.Buffer
            buf.begin_not_undoable_action()
            buf.set_text(utf8_string)
            buf.end_not_undoable_action()
            buf.set_modified(False)
        except UnicodeDecodeError:
            self._error(i.exception_unicode_decode)
        except ValueError:
            self._error(i.exception_unicode_decode)
        except UnicodeEncodeError:
            self._error(i.exception_unicode_encode)
        return


    def __create_backup(self):
        # TODO: Implement and Make configurable
        pass
#        backup_file = GMATE_BACKUP_FOLDER + self.__filename
#        dirname = os.path.dirname(backup_file)
#        if not os.path.exists(dirname):
#            print dirname
#            os.makedirs(dirname)
#        shutil.copy(self.filename, backup_file)


    def save_file(self, document, filename=None, encoding='utf-8'):
        # TODO: Implement File Save operation
        buf = document.Buffer
        string = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
        handler = open(document.filename, 'w')
        unicode_string = to_unicode_or_bust(string, encoding)
        handler.write(unicode_string)
        handler.flush()
        handler.close()
        last_mod = get_last_modification(document.filename)
        self.__document.last_modified_time = last_mod
        # 1. Check For Other Program Modifications by checking the last modified
        #    time whith last file modified time
        # 2. Check For Permissions to Save
        # 3. Encode File before writing to disk
        # 4. Write to a tmp file
        # 5. Copy tmp File over original file (For Crash Prevent)
        # 6. Delete old file
        return True

    def revert_backup(self, file_uri):
        # TODO: Revert backup created above
        pass

    def _error(self, error):
        # TODO: Show an Error dialog
        print error

    def __set_document_configuration(self):
        # TODO: Read the tab width, soft tabs and other confs from a vim-like line at
        #       beginning of file (First 5 lines) ex:
        #       ------------------------------------------------------------------------
        #       --gmate--: ts=4,st=True,rm=80
        #       ------------------------------------------------------------------------
        #       meaning: TabStops = 4
        #                SoftTabs = Enabled
        #                Rigth Margin = 80
        if self.__document:
            doc = self.__document
            lang = get_language_for_mime_type(self.__mime_type)
            buf = doc.Buffer
            doc.set_language(lang)
            doc.set_filename(self.__filename)
            doc.set_uri(self.__uri)
            buf.place_cursor(buf.get_start_iter())
            doc.last_modified_time = get_last_modification(self.__uri)

    def _destroy(self):
        del self
        self = None
        return

