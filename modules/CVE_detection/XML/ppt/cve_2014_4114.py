# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab

import os
import fnmatch
import string

def getNewInstance(fileName, docType, extractionFolder):
    return CVE_2014_4114_detector(fileName, docType, extractionFolder)


class CVE_2014_4114_detector:

    def __init__(self, fileName, docType, extractionFolder):
        self.extractionFolder = extractionFolder
        self.fileName = fileName
        self.docType = docType

    def check(self):
        check_path = os.path.join(self.extractionFolder, 'ppt', 'embeddings')
        results = []
        if os.path.exists(check_path):
            for fn in os.listdir(check_path):
                cfn = os.path.join(check_path, fn)
                with open(cfn, "rb") as f:
                    result = ""
                    for c in f.read():
                        if c in string.printable:
                            result += c
                            continue
                        else:
                            if len(result)>=4:
                                results.append(result)
                            result = ""
        for item in results:
            if item.endswith('.inf') or item.endswith('.INF'):
                print ">> possible CVE-2014-4114 exploit attempt found: %s" % (item)
