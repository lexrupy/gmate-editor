# -*- coding: utf-8 -*-
# GMate - Plugin Based Programmer's Text Editor
# Copyright © 2008-2009 Alexandre da Silva
#
# This file is part of Gmate.
#
# See LICENTE.TXT for licence information

import sys
import os
from GMATE import GMATE_PLUGIN_HOME_FOLDER, GMATE_PLUGIN_CORE_FOLDER
from GMATE.gmate_plugin import GMatePlugin


class PluginInfo:
    """
        Describes the plugin information
    """
    module = None
    name = None
    description = None
    authors = None
    website = None


__plugin_instances = {}


def get_plugin_instance_by_class_name(classname):
    if __plugin_instances.has_key(classname):
        return __plugin_instances[classname]
    return None


def trigger_method(method_name, *args):
    for p in __plugin_instances.iterkeys():
        instance = __plugin_instances[p]
        if hasattr(instance, method_name):
            method = getattr(instance, method_name)
            method(*args)
    return None


def list_plugins(plugin_list):
    """
        Return a list of loadable plugins given the list of .gmplugin files
    """
    result = []
    for plugin in plugin_list:
        p = PluginInfo()
        f = open(plugin)
        for l in f.readlines():
            if l.startswith('Module='):
                p.module = l[7:].replace('\n','')
            if l.startswith('Name='):
                p.name = l[5:].replace('\n','')
            if l.startswith('Description='):
                p.description = l[12:].replace('\n','')
            if l.startswith('Authors='):
                p.authors = l[8:].replace('\n','')
            if l.startswith('Website='):
                p.website = l[8:].replace('\n','')
        result.append(p)
    return result


def load_plugins():
    """
        Look up at plugin folders and try to load the found plugins
    """
    plugin_list = map(lambda f: os.path.join(GMATE_PLUGIN_CORE_FOLDER, f),
        filter(lambda f: f.endswith('.gmplugin'), os.listdir(GMATE_PLUGIN_CORE_FOLDER))
    ) + map(lambda f: os.path.join(GMATE_PLUGIN_HOME_FOLDER, f),
        filter(lambda f: f.endswith('.gmplugin'), os.listdir(GMATE_PLUGIN_HOME_FOLDER))
    )
    plugins = list_plugins(plugin_list)
    for p in plugins:
        try:
            # TODO: Check if plugin is enabled before import
            __import__(p.module, None, None, [''])
            #print "imported", p.module
        except:
            #raise
            print '**Warning: Plugin "%s" cannot be loaded' % p.name


def init_plugin_system():
    """
        Initialize the plugin system.
    """
    if not GMATE_PLUGIN_CORE_FOLDER in sys.path:
        sys.path.insert(0, GMATE_PLUGIN_CORE_FOLDER)
    load_plugins()


def initialize_plugins(window, uimanager):
    """
        Look up at all Plugins found and setup them, by calling *setup* method./
    """
    for plugin in GMatePlugin.__subclasses__():
        # Store only classname to prevent double instanciating
        classname = plugin.__name__
        if not classname in __plugin_instances:
            p = __plugin_instances[classname] = plugin(window, uimanager)
            setattr(p, 'locate_plugin', get_plugin_instance_by_class_name)
            p.setup()
            #print "Loaded Plugin %s" % str(plugin)

