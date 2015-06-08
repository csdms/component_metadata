"""
Auxiliary functions for xml_to_yaml_converter.py

isAllWhiteSpace checks to see if there is really text
covertXml2Yaml creates a dirty dictionary of the yaml file
create_yaml_file modifies the dirty dictionary to fit the format of TopoFlow parameter files

perignon@colorado.edu
June 8, 2015
"""

import yaml
import sys, string, re
from xml.dom import minidom
from xml.dom import Node
import numpy as np

NonWhiteSpacePattern = re.compile('\S')
def isAllWhiteSpace(text):
    if NonWhiteSpacePattern.search(text):
        return 0
    return 1

def convertXml2Yaml(obj, objL):
    objDict = {}
    
    attrs = obj.attributes
    if attrs.length > 0:
        attrDict = {}
        for idx in range(attrs.length):
            attr = attrs.item(idx)
            attrDict[attr.name] = attr.value
        objL.append(attrDict)
        
    text = []
    for child in obj.childNodes:
        if child.nodeType == Node.TEXT_NODE and not isAllWhiteSpace(child.nodeValue):
            text.append(child.nodeValue)
    if text:
        textStr = "".join(text)
        objDict[obj.nodeName] = textStr
        
    children = []
    for child in obj.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            obj, ls = convertXml2Yaml(child, objL)
            if obj:
                children.append(obj)
    if children:
        objL.append(children)
        
    return objDict, objL


def create_yaml_file(inFileName):

    doc = minidom.parse(inFileName)
    root = doc.childNodes[0]
    [objD, objL] = convertXml2Yaml(root,[])
    
    [objD, objL] = convertXml2Yaml(root,[])

    # remove the structures that are too broad and leave only the ones that relate specifically to parameters
    
    flags = np.diff([len(item) for item in objL] + [1]) # the zeros are the bad entries
    objList = [objL[i] for i,j in enumerate(flags) if j != 0]

    # turn all lists in the list to individual dictionaries, clean the formatting
    
    allEntries = {}
    flag = 0 # no in-progress parameter

    for obj in objList:

        if type(obj) is dict and len(obj) == 1:

            if flag == 1: # reached a new parameter
                allEntries[key] = param
                flag = 0

            if flag == 0:

                param = {}
                key = str(obj.values()[0])
                key = string.rsplit(key,'/',1)[-1]
                flag = 1 # parameter in progress

        if type(obj) is list:

            vals = dict([(str(item.keys()[0]),str(item.values()[0])) for item in obj])

            if vals.has_key('max'):
                param['range'] = vals
            else:
                try:
                    vals['name'] = vals.pop('label')[:-1]
                except:
                    pass
                try:
                    vals['description'] = vals.pop('help_brief')
                except:
                    pass

                param.update(vals)

    allEntries[key] = param
    
    return allEntries