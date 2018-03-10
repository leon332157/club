# webcam-saver.py
# by Markus Gritsch (gritsch@iue.tuwien.ac.at)

"""Monitors a picture on the net for (and saves it in case of) any changes.

The location of the picture to observe and the interval between probing is
specified in the webcam-saver.ini file.  Further details are given there.
"""

verbose = 1

import urllib, time, string, os, stat

try:
    from PIL import Image

    havePIL = 1
except ImportError:
    havePIL = 0

f = open('webcam-saver.ini')
camurl = string.strip(f.readline())
interval = int(f.readline())
f.close()


def diff(file1, file2):
    """diff(file1, file2) -> integer

    Returns 1 if file1 differs from file2.  1 is also returned if one file or
    both files are not found.  Use this function only for small files, because
    no optimisation is done so the whole files are read into the memory.
    """
    try:
        f1 = open(file1, 'rb')
    except IOError:
        return 1
    try:
        f2 = open(file2, 'rb')
    except IOError:
        f1.close()
        return 1
    im1 = f1.read()
    im2 = f2.read()
    f1.close()
    f2.close()
    if im1 != im2:
        return 1
    if verbose: print
    'same as old one ...',
    return 0


if havePIL:
    def valid(file):
        f = open(file, 'rb')
        im = Image.open(f)
        try:
            im.load()  # actually try to load it
            f.close()
            return 1
        except IOError:
            f.close()
            if verbose: print
            'image is invalid ...',
            return 0
else:
    print
    'WARNING: PIL not present.  Can not check if downloaded images are corrupt.'


    def valid(file):
        return 1


def notzero(file):
    if os.stat(file)[stat.ST_SIZE]:
        return 1
    else:
        if verbose: print
        'size is zero ...',
        return 0


print
'Everytime this program is started it begins counting from 0.'
i = 0
oldlocalfile = ''
while 1:
    recenttime = time.time()
    head, tail = os.path.split(camurl)
    root, ext = os.path.splitext(tail)
    localfile = root + '_' + string.zfill(i, 5) + ext
    try:
        if verbose: print
        time.asctime(time.localtime(time.time()))[11:19], 'retrieving image ...',
        urllib.urlretrieve(camurl, localfile)
        if notzero(localfile) and valid(localfile) and diff(oldlocalfile, localfile):
            oldlocalfile = localfile
            i = i + 1
            if verbose: print
            'got a new one!  Saved as', localfile
        else:
            os.remove(localfile)
            if verbose: print
            'image deleted'
    except:
        import sys

        type, value = sys.exc_info()[:2]
        print
        'webcam-saver.py: ' + str(type) + ':', value
    while time.time() - recenttime < interval:
        time.sleep(1)
