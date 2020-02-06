## @package gmapcatcher.fileUtils
# A common location for all the File I/O Utilities

import os
import re
import codecs
from time import time

#Count for the markers
count = 0

##To delete all markers / check the marker deletion, do:
## cd .GMapCatcher
## gedit markers

## Return all the locations from a given file (filePath)
def read_file(strInfo, filePath, maxLine=0):
    fileData = {}
    if os.path.exists(filePath):
        p = re.compile(strInfo + '="([^"]+)".*lat="([^"]+)".*lng="([^"]+)".*')
        q = re.compile('.*zoom="([^"]+)".*')
        file = open(filePath, "r")
        for line in file:
            try:
                # the file should be in UTF-8, so decoding is needed
                line = line.decode("UTF-8")
                if (line[0] != '#'):
                    m = p.search(line)
                    if m:
                        zoom = 10
                        z = q.search(line)
                        if z:
                            zoom = int(z.group(1))
                        if m.group(1) in fileData:
                            name = '%s %i' % (m.group(1), len(fileData))
                        else:
                            name = m.group(1)
                        fileData[name] = (float(m.group(2)),
                                                float(m.group(3)),
                                                zoom)
                if (maxLine > 0):
                    if (len(fileData) > maxLine):
                        break
            except:
                pass
        file.close()
        return fileData
    else:
        write_file(strInfo, filePath, fileData)
        return None


## Writes all the locations (fileData) to given file (filePath)
def write_file(strInfo, filePath, fileData):
    try:
        file = open(filePath, "w")
    except Exception:
        print 'Error! Can NOT write file:'
        print '  ' + filePath
        return

    file.write(codecs.BOM_UTF8+"# This is the " + strInfo + "s file used by GMapCatcher.\n" +
        "#\n" +
        "# This file contains a list of Locations/Position.\n" +
        "# Each entry should be kept on an individual line,\n" +
        "# and MUST have a unique name.\n" +
        "# The latitude, longitud and zoom should be TAB separated.\n" +
        "#\n" +
        "# Additionally, comments (such as these) may be inserted on\n" +
        "# lines sarting with a '#' symbol.\n" +
        "#\n" + "# For example:\n" + "#\n" +
        ('#   ' + strInfo + '="%s"\tlat="%f"\tlng="%f"\tzoom="%i"\n' %
         ("Paris, France", 48.856667, 2.350987, 5)) + "#\n")
    count = 0     
    for l in sorted(fileData.keys()):
        # The method 'write' takes an unicode string here and acording to python manual
        # it translates it automatically to string buffer acording to system defaults.
        # Probably all systems translate unicode to UTF-8
        file.write(strInfo + '="%s"\tlat="%f"\tlng="%f"\tzoom="%i"\n' %
                  (l.encode('UTF-8'), fileData[l][0], fileData[l][1], fileData[l][2]))
        file.write("%i" % (count))                    
    file.close()


## Deletes a given file
def del_file(filename):
    try:
        os.remove(filename)
    except:
        pass

# Deletes the earliest marker from the marker file
def deleteMarkers(filePath):
    infile = open(filePath,'r').readlines()
    with open(filePath,'w') as outfile:
	counter = 0
	first_marker= 0 # index of first marker line in markers in .GMapCatcher
        for index,line in enumerate(infile):
	    if line[0] != 'M' and line[0] != '#':
	        first_marker = counter 
		print("first marker is : " + str(first_marker))
		break 
            counter = counter + 1 
	counter = 0
	for index, line in enumerate(infile):
            if counter != first_marker:
                outfile.write(line)
	    counter = counter + 1
    
## Append the location (strData) to given file (filePath)
def append_file(strInfo, filePath, strData, strName, extraTag=False, landmark = False):
    ##count = 0
    global count
    try:
        file = open(filePath, "a")
        ##text = file.readlines()
    except Exception:
        print 'Error! Can NOT write file:'
        print '  ' + filePath
        return
    if landmark == False: 
        file.write("%i " % (count))
    else:
        file.write("M ")
    if extraTag:
    	count = count + 1
        file.write(strInfo + '="%s"\tlat="%s"\tlng="%s"\tzoom="%i"\t%s\n' %
                  (strName, strData[0], strData[1], strData[2] + 2, extraTag))
    else:
    	count = count + 1
        file.write(strInfo + '="%s"\tlat="%s"\tlng="%s"\tzoom="%i"\n' %
                  (strName, strData[0], strData[1], strData[2] + 2))
        #Makes sure there's only 5 markers on the screen
        if (count > 5):
            deleteMarkers(filePath)
    file.close()


## Writes a new gtkrc file with the given theme
def write_gtkrc(strTheme):
    filePath = './etc/gtk-2.0/gtkrc'
    try:
        file = open(filePath, "w")
    except Exception:
        print 'Error! Can NOT write file:'
        print '  ' + filePath
        return

    file.write('# You can change the GMapCatcher theme here!\n' +
               '#\n' +
               '#gtk-theme-name = "Industrial"\n' +
               '#gtk-theme-name = "XFCE-4.2"\n' +
               '\n' +
               'gtk-theme-name = "' + strTheme + '"')
    file.close()


## Returns the current theme from the gtkrc file
def read_gtkrc():
    filePath = './etc/gtk-2.0/gtkrc'
    if os.path.exists(filePath):
        file = open(filePath, "r")
        for line in file:
            line = line.strip()
            if line.startswith('gtk-theme-name'):
                return line[17:].strip('"')


## Returns all the available themes
def get_themes():
    themesPath = './share/themes/'
    myThemes = []
    if os.path.isdir(themesPath):
        for l in os.listdir(themesPath):
            if os.path.isdir(themesPath + l) and (l[0] != '.'):
                myThemes += [l]
    return myThemes


## Returns all the available tracks
def get_tracks():
    tracksPath = './tracks'
    myTracks = []
    if os.path.isdir(tracksPath):
        for l in os.listdir(tracksPath):
            #if os.path.isdir(tracksPath + l):
            myTracks += [tracksPath + '/' + l]
    return myTracks


## Checks if a directory exist if not it will be created
def check_dir(strPath, strSubPath=None):
    if (strSubPath is not None):
        strPath = os.path.join(strPath, strSubPath)
    if not os.path.isdir(strPath):
        try:
            os.makedirs(strPath)
        except Exception:
            print 'Error! Can not create directory:'
            print '  ' + strPath
    return strPath




## Check if the file is older than given time
#  (24h * 3600s/h) = 86400s
def is_old(filename, intDays):
    if os.path.isfile(filename):
        if (int(time() - os.path.getmtime(filename)) > (86400 * intDays)):
            return True
    return False


## Remove file if is older than given time
def delete_old(filename, intDays):
    if is_old(filename, intDays):
        try:
            os.remove(filename)
            return True
        except:
            pass
    return False
