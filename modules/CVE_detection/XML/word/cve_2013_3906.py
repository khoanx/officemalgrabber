# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab

import os
import fnmatch
import re

def getNewInstance(fileName, docType, extractionFolder, args, json_result):
    return CVE_2013_3906_detector(fileName, docType, extractionFolder, args, json_result)


class CVE_2013_3906_detector:
    pathToActiveX = ''
    fileName = ''
    docType = ''
    MSTabStripClassID = '1EFB6596-857C-11D1-B16A-00C0F0283628'

    def __init__(self, fileName, docType, extractionFolder, args, json_result):
        self.pathToActiveX = extractionFolder + docType + '/activeX'
        self.fileName = fileName
        self.docType = docType
        self.args = args
        self.json_result = json_result
        self.urlRE = re.compile('((https?|ftp):((\/\/)|(\\\\))+[\d\w:@\/()~_?\+\-=\\\.&]*)')

    def check(self):
        activeXContainers = []

        fileNames = []

        for dirname, dirnames, filenames in os.walk(self.pathToActiveX):
            for filename in filenames:
                fileNames.append(os.path.join(dirname, filename))

        filtered = fnmatch.filter(fileNames, '*activeX*.xml')
        tabStripCounter = 0

        for activeXcontrol in filtered:
            currentControl = open(activeXcontrol, 'r')
            controlText = currentControl.read()

            #the Class-ID: 1EFB6596-857C-11D1-B16A-00C0F0283628 identifies an activeX-control as TabStrip
            if self.MSTabStripClassID in controlText:
                tabStripCounter = tabStripCounter + 1
                activeXBinFileName = activeXcontrol[:-3]
                activeXBinFileName += 'bin'
                activeXContainers.append(activeXBinFileName)

            currentControl.close()

        fileSizesAndOccurences = []
        for activeXFile in activeXContainers:
            statinfo = os.stat(activeXFile)
            if len(fileSizesAndOccurences) == 0:
                fileSizesAndOccurences.append((statinfo.st_size, 0))
            found = False
            for item in range(0, len(fileSizesAndOccurences)):
                if fileSizesAndOccurences[item][0] == statinfo.st_size:
                    fileSizesAndOccurences[item] = (statinfo.st_size, fileSizesAndOccurences[item][1]+1)
                    found = True
            if not found:
                fileSizesAndOccurences.append((statinfo.st_size, 1))
            fp = open(activeXFile, 'r')
            content = fp.read()
            fp.close()
            match = self.urlRE.search(content)
            if match:
                self.json_result['detections'].append({'type': 'URL', 'location': match.group()})

        sameSize = 0
        for items in fileSizesAndOccurences:
            sameSize = max(sameSize, items[1])

        #the thresholds of 300 and 200 were randomly chosen and should be set to a more sophisticated value
        if tabStripCounter > 300 and sameSize > 200:
            if self.args.json:
                self.json_result['signatures'].append({'match': 'cve-2013-3906'})
            else:
                print '>> found an exploit for CVE-2013-3906!'
