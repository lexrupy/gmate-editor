# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

from GMATE.gmate_plugin import GMatePlugin
import re

# TODO: put all in configuration (Or Not)
START_KEYVALS = [34,  39,   96,   40,   91,   123,  60]
END_KEYVALS   = [34,  39,   96,   41,   93,   125,  62]
TWIN_START    = ['"', "'",  '`',  '(',  '[',  '{',  '<']
TWIN_END      = ['"', "'",  '`',  ')',  ']',  '}',  '>']

class PairComplete(GMatePlugin):

    def setup(self):
        self.__text_view_keypress_id = None

    def activate_document(self, document=None):
        if document:
            self.__text_view = document.View
            self.__text_view.connect ('key-press-event', self.__key_press_cb)

    def desactivate_document(self, document=None):
        if self.__text_view_keypress_id:
            self.__textview.disconnect(self.__text_view_keypress_id)
            self.__text_view_keypress_id = None

    def close_document(self, document=None):
        self.desactivate_document(document)

    def __key_press_cb(self, view, event):
        print event.keyval
        buf = view.get_buffer()
        cursor_mark = buf.get_insert()
        cursor_iter = buf.get_iter_at_mark(cursor_mark)
        if (event.keyval in START_KEYVALS or
            event.keyval in END_KEYVALS or
                event.keyval in (65288, 65293)):
          back_iter = cursor_iter.copy()
          back_char = back_iter.backward_char()
          back_char = buf.get_text(back_iter, cursor_iter)
          forward_iter = cursor_iter.copy()
          forward_char = forward_iter.forward_char()
          forward_char = buf.get_text(cursor_iter, forward_iter)
          if event.keyval in START_KEYVALS:
            index = START_KEYVALS.index(event.keyval)
            start_str = TWIN_START[index]
            end_str = TWIN_END[index]
          else:
            start_str, end_str = None, None
          # Here is the meat of the logic
          if buf.get_has_selection() and event.keyval not in (65288, 65535):
            # pad the selected text with twins
            start_iter, end_iter = buf.get_selection_bounds()
            selected_text = start_iter.get_text(end_iter)
            buf.delete(start_iter, end_iter)
            buf.insert_at_cursor(start_str + selected_text + end_str)
            return True
          elif end_str != forward_char and end_str != None:
            # insert the twin that matches your typed twin
            buf.insert(cursor_iter, end_str)
            if cursor_iter.backward_char():
              buf.place_cursor (cursor_iter)
          elif event.keyval == 65288 and back_char in TWIN_START and forward_char in TWIN_END:
            # delete twins when backspacing starting char next to ending char
            if TWIN_START.index(back_char) == TWIN_END.index(forward_char):
                cursor_iter = buf.get_iter_at_mark(buf.get_insert())
                forward_iter = cursor_iter.copy()
                if forward_iter.forward_char():
                  buf.delete(back_iter, forward_iter)
                  return True
          elif event.keyval in END_KEYVALS:
            # stop people from closing an already closed pair
            index = END_KEYVALS.index(event.keyval)
            if TWIN_END[index] == forward_char :
              cursor_iter = buf.get_iter_at_mark(buf.get_insert())
              forward_iter = cursor_iter.copy()
              if forward_iter.forward_char():
                buf.place_cursor(forward_iter)
                return True
          elif event.keyval == 65293 and forward_char == '}':
            # add proper indentation when hitting before a closing bracket
            cursor_iter = buf.get_iter_at_mark(buf.get_insert ())
            line_start_iter = cursor_iter.copy()
            view.backward_display_line_start(line_start_iter)
            line = buf.get_text(line_start_iter, cursor_iter)
            preceding_white_space_pattern = re.compile(r'^(\s*)')
            groups = preceding_white_space_pattern.search(line).groups()
            preceding_white_space = groups[0]
            plen = len(preceding_white_space)
            buf.insert_at_cursor('\n')
            buf.insert_at_cursor(preceding_white_space)
            buf.insert_at_cursor('\n')
            cursor_mark = buf.get_insert()
            cursor_iter = buf.get_iter_at_mark(cursor_mark)
            buf.insert_at_cursor(preceding_white_space)
            cursor_mark = buf.get_insert()
            cursor_iter = buf.get_iter_at_mark(cursor_mark)
            for i in range(plen + 1):
              if cursor_iter.backward_char():
                buf.place_cursor(cursor_iter)
            if view.get_insert_spaces_instead_of_tabs():
              buf.insert_at_cursor(' ' * view.get_tab_width())
            else:
              buf.insert_at_cursor('\t')
            return True


    def teardown(self):
        """
        Handles callback when the "destroy" signal is emitted.
        """
        del self
        self = None
        return

