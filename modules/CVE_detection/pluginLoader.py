# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab

import os
import imp

class pluginLoader:
    def __init__(self, fileFormat, docType, fileName, extractionFolder, args, json_result):
        self.args = args
        pathToPluginFiles = './modules/CVE_detection' + fileFormat + docType
        self.pluginFiles = []
        self.loadedPlugins = []
        try:
            self.pluginFiles = os.listdir(pathToPluginFiles)
        except:
            self.pluginFiles = []

        for plugin in self.pluginFiles:
            if plugin.endswith('.py'):
                imported = imp.load_source(plugin.split('.')[0], pathToPluginFiles + '/' + plugin)
                self.loadedPlugins += [imported.getNewInstance(fileName, docType, extractionFolder, args, json_result)]

    def runDetectors(self):
        for plugin in self.loadedPlugins:
            if not self.args.json:
                try:
                    plugin.report()
                except:
                    pass
            plugin.check()
