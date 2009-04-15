# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

from GMATE.gmate_plugin import GMatePlugin
import re

# TODO: put all in configuration
# RUBY
re_indent_next = re.compile(r'[^#]*\s+do(\s*|(\s+\|.+\|\s*))|\s*(if\s+.*|elsif.*|else.*|do(\s*|\s+.*)|case\s+.*|when\s+.*|while\s+.*|for\s+.*|until\s+.*|loop\s+.*|def\s+.*|class\s+.*|module\s+.*|begin.*|unless\s+.*|rescue.*|ensure.*)+')
re_unindent_curr = re.compile(r'^\s*(else.*|end\s*|elsif.*|rescue.*|when.*|ensure.*)$')
#re_unindent_next = re.compile(r'^\s*(end\s*|else.*|rescue.*|elsif.*|when.*|ensure.*)$')
unindent_keystrokes = 'edfn'

class SmartIndent(GMatePlugin):

    def setup(self):
        self.__text_view_keypress_id = None
#        self.__line_indented = False
#        self.__line_unindented = False

    def activate_document(self, document=None):
        if document:
            self.__text_view = document.View
            self.__text_view.connect ('key-press-event', self.__key_press_cb)
            # TODO: Connect by some way the line indented event or if not exists
            # create a variable 'current_line with a number' and compare with
            # current to test by a needed unindentation

    def desactivate_document(self, document=None):
        if self.__text_view_keypress_id:
            self.__textview.disconnect(self.__text_view_keypress_id)
            self.__text_view_keypress_id = None

    def close_document(self, document=None):
        self.desactivate_document(document)

    def __get_current_line(self, view, buf):
        cursor_iter = buf.get_iter_at_mark(buf.get_insert())
        line_start_iter = cursor_iter.copy()
        view.backward_display_line_start(line_start_iter)
        return buf.get_text(line_start_iter, cursor_iter)

    def __key_press_cb(self, view, event):
        buf = view.get_buffer()
        if buf.get_has_selection(): return
        # Get tabs/indent configuration
        if view.get_insert_spaces_instead_of_tabs():
          indent_width = ' ' * view.get_tab_width()
        else:
          indent_width = '\t'
        # O Press enter test if need to indent next line
        if event.keyval == 65293:
            # Check next line indentation for current line
            line = self.__get_current_line(view, buf)
            if re_indent_next.match(line):
                old_indent = line[:len(line) - len(line.lstrip())]
                indent = '\n'+ old_indent + indent_width
                buf.insert_interactive_at_cursor(indent, True)
                # Indented marked as true
                #self.__line_indented = True
                return True
            elif re_unindent_next.match(line):
              # Necessary?
              pass
        elif event.keyval == 65288:
            #if self.__line_unindented:
                # Indent
            #if self.__line_indented:
                # Unindent
            # TODO: Need to do something when press backspace to
            # undo last indent/unindent
            pass
        elif event.keyval in [ord(k) for k in unindent_keystrokes]:
            line = self.__get_current_line(view, buf)
            line_eval = line+chr(event.keyval)
            if re_unindent_curr.match(line_eval):
                cursor_iter = buf.get_iter_at_mark(buf.get_insert())
                line_start_iter = cursor_iter.copy()
                view.backward_display_line_start(line_start_iter)
                iter_end_del = buf.get_iter_at_offset(line_start_iter.get_offset() + len(indent_width))
                text = buf.get_text(line_start_iter, iter_end_del)
                if text.strip() == '':
                    buf.delete_interactive(line_start_iter, iter_end_del, True)
                    self.__line_unindented = True
                    return False
        return False

    def teardown(self):
        del self
        self = None
        return

