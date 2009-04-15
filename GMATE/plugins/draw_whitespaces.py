# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

"""
This module documents a class that draws white spaces in GMate.
This is a port of Gedit's whitespace plugin. All credit goes to
Copyright (C) 2006 - Paolo Borelli
Copyright (C) 2007 - Steve Frécinaux
"""

from GMATE.gmate_plugin import GMatePlugin

class WhiteSpaceDrawer(GMatePlugin):
    """
    This class draws white spaces in the buffer.
    """
    def setup(self):
        self.__text_view_event_after_id = None


    def activate_document(self, document=None):
        if document:
            self.__textview = document.View
            # TODO: Read color from configuration
            self.__color_cb("orange")
            self.__show = True
            self.__text_view_event_after_id =  self.__textview.connect(
                'event-after', self.__event_after_cb)


    def desactivate_document(self, document=None):
        if self.__text_view_event_after_id:
            self.__textview.disconnect(self.__text_view_event_after_id)
            self.__text_view_event_after_id = None


    def close_document(self, document=None):
        self.desactivate_document(document)


    def __draw_whitespaces(self, event, start, end):
        cr = event.window.cairo_create()
        cr.set_source_color(self.__color)
        cr.set_line_width(0.8)
        while start.compare(end) <= 0:
            c = start.get_char()
            if c == '\t':
                self.__draw_tab(cr, start)
            elif c == '\040':
                self.__draw_space(cr, start)
            elif c == '\302\240':
                self.__draw_nbsp(cr, start)
            if not start.forward_char(): break
        cr.stroke()
        return False

    def __draw_tab(self, cr, iterator):
        rect = self.__textview.get_iter_location(iterator)
        from gtk import TEXT_WINDOW_TEXT
        x, y = self.__textview.buffer_to_window_coords(TEXT_WINDOW_TEXT,
                                                rect.x,
                                                rect.y + rect.height * 2 / 3)
        cr.save()
        cr.move_to(x + 4, y)
        cr.rel_line_to(rect.width - 8, 0)
        cr.rel_line_to(-3,-3)
        cr.rel_move_to(+3,+3)
        cr.rel_line_to(-3,+3)
        cr.restore()
        return False

    def __draw_space(self, cr, iterator):
        rect = self.__textview.get_iter_location(iterator)
        from gtk import TEXT_WINDOW_TEXT
        x, y = self.__textview.buffer_to_window_coords(TEXT_WINDOW_TEXT,
                                                rect.x + rect.width / 2,
                                                rect.y + rect.height * 2 / 3)
        cr.save()
        cr.move_to(x, y)
        from math import pi
        cr.arc(x, y, 0.8, 0, 2 * pi)
        cr.restore()
        return False

    def __draw_nbsp(self, cr, iterator):
        rect = self.__textview.get_iter_location(iterator)
        from gtk import TEXT_WINDOW_TEXT
        x, y = self.__textview.buffer_to_window_coords(TEXT_WINDOW_TEXT, rect.x, rect.y + rect.height / 2)
        cr.save()
        cr.move_to(x + 2, y - 2)
        cr.rel_line_to(+7,0)
        cr.rel_line_to(-3.5,+6.06)
        cr.rel_line_to(-3.5,-6.06)
        cr.restore()
        return False

    def __event_after_cb(self, textview, event):
        if self.__show is False: return False
        from gtk.gdk import EXPOSE
        from gtk import TEXT_WINDOW_TEXT
        if event.type != EXPOSE or \
            event.window != textview.get_window(TEXT_WINDOW_TEXT):
            return False
        y = textview.window_to_buffer_coords(TEXT_WINDOW_TEXT, event.area.x, event.area.y)[1]
        start = textview.get_line_at_y(y)[0]
        end = textview.get_line_at_y(y + event.area.height)[0]
        end.forward_to_line_end()
        self.__draw_whitespaces(event, start, end)
        return False

    def __color_cb(self, color):
        from gtk.gdk import color_parse
        self.__color = color_parse(color)
        return False

    def teardown(self):
        del self
        self = None
        return

