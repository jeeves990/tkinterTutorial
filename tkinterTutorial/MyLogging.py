import os
import sys
import time as TM

"""This provides a lineno() function to make it easy to grab the line number that we're on.

Danny Yoo (dyoo@hkn.eecs.berkeley.edu)
"""
from os import path
from os.path import basename
import inspect
from tkinter import messagebox as MSGBOX

class LoggingHelpers():
    def __init__(self, *args, **kwargs):
        pass

def getlinenumber(scriptname = None):
    """Returns the current line number in our program."""
    if scriptname:
        basename = scriptname
    else:
        basename = getscriptname()
    return basename +':'  +str(inspect.currentframe().f_back.f_lineno)


def getscriptname():
    ''' returns the scriptname '''
    frm = inspect.currentframe()
    frmsplit = str(frm).split("'")
    #print(frmsplit)
    try:
        for s in frmsplit:
            if path.exists(s):
                return os.path.basename(s)
    except:
        pass
    else:
        print('no filename found in inspect.currentframe()')
        return None

            
class MyLog():
    def __init__(self, deleteifempty = False, *args, **kwargs):
        if 'logfilename' in kwargs:
            self.logfilename = kwargs['logfilename']
            logdirname = ''
            if 'dirname' in kwargs:
                logdirname = kwargs['dirname']
            if not logdirname:
                self.logfilename = self.getExLogFilename(self.logfilename)
            else:
                self.logfilename = self.getExLogFilename(self.logfilename, dirname = logdirname)
        else:
            self.logfilename = self.bldLogFileName()

        if 'append2file' in kwargs:
            self.modeString = 'w+'
        else:
            self.modeString = 'w'
        
        if 'filename' in kwargs:
            self.filename = kwargs['filename']
        else:
            self.filename = self.logfilename
        
        self.deleteIfEmpty = deleteifempty

        ##print('the logfilename is: ', logfilename)
        #print(self.logfilename)
        ''' do not append to the log file '''
        with open(self.logfilename, self.modeString):
            return
        # if execution gets past here, self.logfilename did not open.
        MSGBOX.showerror()
        sys.exit(121212)


    def __del__(self):
        print('this is the destructor')
        if self.deleteIfEmpty and os.path.getsize(self.logfilename) == 0:
            os.remove(self.logfilename)
            print("log file [{0}] has been removed.".format(self.logfilename))
       
        

    def bldLogFileName(self):
        self.basename = os.path.basename(__file__)
        dirname = os.path.dirname(__file__).replace('/', '\\')
        return os.path.join(dirname, self.basename.rsplit('.')[0]) + self.getLocalTime() + '.log'


    def getExLogFilename(self, logname, **kwargs):
        self.basename = logname
        if 'dirname' in kwargs:
            dirname = kwargs['dirname']
        else:
            dirname = os.path.dirname(__file__).replace('/', '\\')
        return os.path.join(dirname, self.basename.rsplit('.')[0]) + self.getLocalTime() + '.log'


    def addlogentry(self, logmsg, **kwargs):  ##scriptname, fcnname, lineno
        msgString = '{}: '.format(self.getLocalTime())
        if 'scriptname' in kwargs:
            msgString += '[{}]: '.format(basename(kwargs['scriptname']))
        if 'fcnname' in kwargs:
            msgString +=  '[{}]: '.format(kwargs['fcnname'])
        if 'lineno' in kwargs:
            msgString += 'line: [{}]: '.format(kwargs['lineno'])
        msgString += '{0}>>{1}<<\n'.format(msgString, logmsg)
        with open(self.logfilename, 'a') as file:
            file.write(msgString)

    def getLocalTime(self):
        ltm = TM.localtime()
        #localtime = "%s%s%s%s%s%s" % (ltm[0], ltm[1], ltm[2], ltm[3], ltm[4], ltm[5])
        localtime = "%4d%2.2d%2.2d-%2.2d%2.2d%2.2d" % (int(ltm[0]), int(ltm[1]), int(ltm[2]),
                                                       int(ltm[3]), int(ltm[4]), int(ltm[5]))
        '''
        time.struct_time(tm_year=2020, tm_mon=3, tm_mday=15, 
            tm_hour=19, tm_min=50, tm_sec=53, 
            tm_wday=6, tm_yday=75, tm_isdst=1)
        '''
        return localtime


if __name__ == '__main__':
    MYL = MyLog(filename = 'hello big boy', deleteifempty = True)
    MYL.addlogentry(sys.argv[0] +getscriptname())
    MYL.addlogentry("well, hello there. My it's been a long, long time", getlinenumber(getscriptname()))


