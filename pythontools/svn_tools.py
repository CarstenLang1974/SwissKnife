"""
This script is adapted from http://stackoverflow.com/a/10286163/2464295 but without the
multi threading factor of it.
Usage: `externals.py https://svn-server/repository`
Do note that the script is excluding src and hidden directories that starts with dot. Just modify the file
as it's not parameterized.
If you want this script to run faster, SSH to the SVN server and use file protocol.
Usage: `externals.py file:///svn/repository`
"""

import os
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
import sys
from xml.dom import minidom

EXT_PATH = "path"
EXT_REVISION = "revision"
EXT_NAME = "name"

def processLine(line):
    external = None
    content = line.split()
    if len(content)==2:
        external = dict()
        external[EXT_NAME] = content[1]
        t = content[0].partition('@')
        if len(t)==3:
            external[EXT_PATH] = t[0]
            if len(t[2])==0:
                external[EXT_REVISION] = "HEAD"
            else:
                external[EXT_REVISION] = t[2]
        else:
            external[EXT_PATH]=content[0]
            external[EXT_REVISION] = "HEAD"
        #print(">>>" + str(content))
        #print(">>> external: {} --- {}".format(content[0], content[1]))
    return external

def getAbsoluteSVNPath(url):
    #print("SVN relative path:" + url)
    absPath = url
    if (url.startswith(r"^/..")):
        absPath = url.replace(r"^/..",r"https://gullstrand.zeiss.org/svn",1)
    elif (url.startswith(r"^/")):
        absPath = url.replace(r"^/",r"https://gullstrand.zeiss.org/svn/czm/",1)
    #print("SVN absolute path:" + absPath)
    return absPath

def getExterns(url, base_dir):
    result = None
    print(">> external of {} (base dir: '{}')".format(url, base_dir))

    cmd = 'svn propget svn:externals "%s"' % url
    pipe = os.popen(cmd, 'r')
    data = pipe.read()
    pipe.close()

    if (data):
        print("#", url)
        #print(data.strip())
        result = list()
        for line in data.splitlines():
            external = processLine(line)
            if external:
                result.append(external)

    return result

def getLastCommitInfo(url):
    cmd = 'svn log -l 1 --xml "%s"' % url
    print('>>>' + cmd)
    pipe = os.popen(cmd, 'r')
    data = pipe.read()
    pipe.close()

    # parse xml output of svn command
    mydoc = minidom.parseString(data)

    revisionElements = mydoc.getElementsByTagName('logentry')
    revision = revisionElements[0].attributes['revision'].value
    #print('revision:' + revision)

    authorElements = mydoc.getElementsByTagName('author')
    author = authorElements[0].firstChild.data
    #print('author:' + author)

    dateElements = mydoc.getElementsByTagName('date')
    date = dateElements[0].firstChild.data
    #print('date:' + date)

    msgElements = mydoc.getElementsByTagName('msg')
    if msgElements[0].firstChild is not None:
        msg = msgElements[0].firstChild.data
    else:
        msg = ""
    #print('msg:' + msg)
    return revision,author,date,msg

def processDir(url, base_dir, recursive=False):
    url = getAbsoluteSVNPath(url)
    result = getExterns(url, base_dir )

    if (recursive):
        cmd = 'svn list "%s"' % url
        pipe = os.popen(cmd, 'r')
        listing = pipe.read().splitlines()
        pipe.close()

        dir_list = []
        for node in listing:
            if node.endswith('/') and not node.endswith('src/') and not node.startswith('.'):
                dir_list.append(node)

        for node in dir_list:
            print("> url:'{}', node:'{}', base_dir:'{}'".format(url, node, base_dir))
            processDir(url+node, base_dir+node )

    return result

def analyzePath(url, base_dir = ''):
    result = processDir(url, base_dir, recursive=False )
    print(result)
    return result
