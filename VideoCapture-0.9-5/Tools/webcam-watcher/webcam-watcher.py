# webcam-watcher.py
# by Markus Gritsch (gritsch@iue.tuwien.ac.at)

"""Periodically retrieves a picture from the web and displays it in a window.

Several URLs can be specified in the webcam-watcher.ini file.  The current
picture can be changed by right-clicking at it.
"""

verbose = 1
timeout = 60  # for the retrieve-thread

import sys, urllib, os, threading, string, stat
from qt import *
from PIL import Image

if sys.platform == 'win32':
    from PIL import JpegImagePlugin, BmpImagePlugin  # for py2exe

from cam_form import Cam

TRUE = 1
FALSE = 0


class RetrieveThread(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent
        self.goon = 1
        self.setDaemon(1)
        self.start()

    def run(self):
        # beware of the stunning logic!
        if verbose: print
        '>> thread started'
        try:
            tmpfile = urllib.urlretrieve(self.parent.camurl)[0]
            self.parent.watchdogtimer.stop()
        except IOError:
            self.onexception()
            return
        if os.stat(tmpfile)[stat.ST_SIZE] == 0:
            self.parent.campix = 'invalid'
            if verbose: print
            '>> campix had size 0'
            os.remove(tmpfile)
            self.goon = 0
            return
        f = open(tmpfile, 'rb')
        try:
            im = Image.open(f)  # raises an exception, if file is not at least an image (but the image may be corrupt)
            try:
                im.load()
            except IOError:
                self.parent.campix = 'invalid'
                if verbose: print
                '>> campix was invalid'
                f.close()
                os.remove(tmpfile)
                self.goon = 0
                return
            if sys.platform == 'win32':  # because Qt on Win32 has no jpeg support
                outfile = os.path.splitext(tmpfile)[0] + '.bmp'
                im.save(outfile)
                f.close()
                os.remove(tmpfile)
                tmpfile = outfile
            if self.goon:
                campix = QPixmap(tmpfile)
                self.parent.campix = campix
                if verbose: print
                '>> campix updated'
        except IOError:
            self.onexception()
        f.close()
        os.remove(tmpfile)
        if self.goon:
            self.goon = 0
            if verbose: print
            '>> thread terminated normally'

    def onexception(self):
        self.parent.watchdogtimer.stop()
        if self.goon:
            self.goon = 0
            self.parent.errorflag = 1
            if verbose:
                type, value = sys.exc_info()[:2]
                print
                str(type) + ':', value


class MyPopupMenu(QPopupMenu):
    def __init__(self, parent):
        QPopupMenu.__init__(self, parent)
        self.parent = parent

        self.data, self.defaultindex = self.getdata('webcam-watcher.ini')

        self.iddict = {}
        for dataset in self.data:
            id = self.insertItem(dataset[0], self.seturl)
            # self.setItemParameter(id, id)
            self.iddict[id] = dataset

        self.previousid = -1

    def seturl(self, id):
        if hasattr(self.parent, 'retrievethread'):
            self.parent.retrievethread.goon = 0
        self.parent.showretrieve()
        self.parent.name = self.iddict[id][0]
        self.parent.setCaption(self.parent.name)  # Shannon
        self.parent.reloadtimer.changeInterval(self.iddict[id][1] * 1000 / 2)
        self.parent.camurl = self.iddict[id][2]
        self.parent.setgetone()
        self.setItemChecked(self.previousid, FALSE)
        self.setItemChecked(id, TRUE)
        self.previousid = id

    def selectdefault(self):
        self.seturl(self.idAt(self.defaultindex))

    def getdata(self, filename):
        f = open(filename, 'rt')
        lines = f.readlines()
        f.close()

        data = []
        defaultindex = 0
        i = 0
        for line in lines:
            # strip comments
            # in case no comment is found, index == -1
            # so at least \n is stripped, which is fine
            index = string.find(line, '#')
            line = line[:index]
            # ignore lines which contain nothing but whitespace
            if string.strip(line) == '':
                continue
            # look for a <default> entry
            line = string.strip(line)
            if line[-len('<default>'):] == '<default>':
                defaultindex = i
                line = line[:-len('<default>')]
            # separate alias and number
            index = string.find(line, ':')
            name = string.strip(line[:index])
            rest = string.split(line[index + 1:])
            # some error checking
            if index == -1:
                continue
            try:
                interval = int(rest[0])
            except ValueError:
                continue
            if interval == 0 or string.lower(rest[1][:7]) != 'http://':
                continue
            # add entry
            data.append((name, interval, rest[1]))
            i = i + 1
        return data, defaultindex


class MyEventFilter(QObject):
    def __init__(self, parent):
        QObject.__init__(self, parent)
        self.parent = parent

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == QEvent.RightButton:
                self.parent.myPopupMenu.popup(event.globalPos())
                return TRUE
        return FALSE


class TopLevelWindow(Cam):
    def __init__(self):
        Cam.__init__(self)

        self.setIcon(QPixmap('cam.png'))

        self.PixmapLabel1.setBackgroundMode(QWidget.NoBackground)  # flickerfree
        self.retrieve = QPixmap('retrieving.png')
        self.error = QPixmap('error.png')

        self.name = ''
        self.errorflag = 0
        self.getone = 0
        self.campix = None

        self.reloadtimer = QTimer(self, 'reloadTeima')
        self.connect(self.reloadtimer, SIGNAL('timeout()'), self.setgetone)
        self.reloadtimer.start(10000, FALSE)

        self.polltimer = QTimer(self, 'pollTeima')
        self.connect(self.polltimer, SIGNAL('timeout()'), self.polltheflags)
        self.polltimer.start(100, FALSE)

        self.watchdogtimer = QTimer(self, 'watchdogTeima')
        self.connect(self.watchdogtimer, SIGNAL('timeout()'), self.cleargoon)

        self.myPopupMenu = MyPopupMenu(self)
        self.myPopupMenu.selectdefault()

        self.myeventfilter = MyEventFilter(self)
        self.PixmapLabel1.installEventFilter(self.myeventfilter)

    # ~ def mousePressEvent(self, mouseEvent):
    # ~ if mouseEvent.button() == QEvent.RightButton:
    # ~ self.myPopupMenu.popup(mouseEvent.globalPos())

    def showretrieve(self):
        self.PixmapLabel1.setPixmap(self.retrieve)
        self.setFixedSize(self.retrieve.size())
        self.campix = None  # not totally beautyful, but better than nothing

    def showerror(self):
        self.PixmapLabel1.setPixmap(self.error)
        self.setFixedSize(self.error.size())
        self.campix = None  # not totally beautyful, but better than nothing

    def setgetone(self):
        if verbose: print
        '>> getone = 1'
        self.getone = 1

    def cleargoon(self):
        if verbose: print
        '>> watchdog-timer expired'
        self.retrievethread.goon = 0

    def polltheflags(self):
        if self.errorflag:
            self.errorflag = 0
            self.showerror()
        if self.campix == 'invalid':
            self.setgetone()
        elif self.campix:
            self.PixmapLabel1.setPixmap(self.campix)
            self.setFixedSize(self.campix.size())
            self.campix = None
        if self.getone and (not hasattr(self, 'retrievethread') or self.retrievethread.goon == 0):
            self.getone = 0
            if verbose: print
            '>> getone = 0'
            self.retrievethread = RetrieveThread(self)
            self.watchdogtimer.start(timeout * 1000, TRUE)  # singleshot
        if self.retrievethread.goon == 1 and self.campix == 'invalid' and str(
                self.caption()) != self.name + ' (polling)':
            self.setCaption(self.name + ' (polling)')
        elif self.retrievethread.goon == 1 and self.campix != 'invalid' and str(
                self.caption()) != self.name + ' (retrieving)':
            self.setCaption(self.name + ' (retrieving)')
        elif self.retrievethread.goon == 0 and str(self.caption()) != self.name:
            self.setCaption(self.name)


a = QApplication(sys.argv)
QObject.connect(a, SIGNAL('lastWindowClosed()'), a, SLOT('quit()'))
w = TopLevelWindow()
a.setMainWidget(w)
w.show()
a.exec_loop()
