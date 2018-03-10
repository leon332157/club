# webcam-uploader.py
# by Markus Gritsch (gritsch@iue.tuwien.ac.at)

"""Uploades a picture obtained by video-capturing to the net periodically.

The destination of the picture and the interval between successive uploads is
specified in the webcam-uploader.ini file.  Further details are given there.
"""

import ConfigParser, StringIO, time, os, sys, string

if os.name == 'posix':
    testWithoutVideoCapture = 1
else:  # 'nt'
    testWithoutVideoCapture = 0


def upload(firsttime, uploadstarttime):
    global uploadedimages, totaluploadtime
    fp = None
    ftp = None
    try:
        # get an image from the webcam
        if testWithoutVideoCapture:
            im = Image.open('offline2.jpg')
        else:
            im = cam.getImage(timestamp=3, boldfont=1)

        # save it to a string buffer
        fp = StringIO.StringIO()
        im.save(fp, format, quality=quality)
        fp.flush()
        fp.seek(0)

        # establish an FTP connection and upload it
        if verbose:
            print
            time.asctime(time.localtime(uploadstarttime))[11:19], 'uploading started ...',
            sys.stdout.flush()  # necessary when using scp
        ftp = ftplib.FTP(host, user, passwd)
        ftp.storbinary('STOR ' + filename, fp, 8192)
        if firsttime:
            ftp.sendcmd('SITE CHMOD 644 ' + filename)
        if verbose:
            endtime = time.time()
            delta = endtime - uploadstarttime
            print
            'done at', time.asctime(time.localtime(endtime))[11:19],
            print
            '(took %.2f seconds)' % delta
            uploadedimages += 1
            totaluploadtime += delta
    except IOError:
        type, value = sys.exc_info()[:2]
        print
        'webcam-uploader.py: ' + str(type) + ':', value
    if ftp:
        ftp.close()
    if fp:
        fp.close()


parser = ConfigParser.ConfigParser()
parser.read('webcam-uploader.ini')
method = parser.get('uploader', 'method')
host = parser.get('uploader', 'host')
user = parser.get('uploader', 'user')
passwd = parser.get('uploader', 'passwd')
filename = parser.get('uploader', 'filename')
devnum = int(parser.get('uploader', 'devnum'))
interval = int(parser.get('uploader', 'interval'))
quality = int(parser.get('uploader', 'quality'))
verbose = int(parser.get('uploader', 'verbose'))

if not passwd:
    import getpass

    passwd = getpass.getpass()

if method == 'ftp':
    import ftplib
elif method == 'scp':
    import scpdropin as ftplib

    if os.name == 'posix':
        f, g = os.popen4('ssh-add -p', 'w')
        f.write(passwd + '\n')
        f.close()
        g.close()
    else:  # 'nt'
        pass  # on Win32, we can pipe the password into scp2.exe
else:
    raise Exception, 'invalid transfer method specified in .ini file'

print
'''
To terminate uploading, press Ctrl+C to exit gracefully.
Do not terminate this program by closing the window.
'''

root, ext = os.path.splitext(filename)
head, tail = os.path.split(root)

fd = open('template.html', 'rt')
temp = fd.read()
fd.close()

temp = string.replace(temp, '-{INTERVAL}-', str(interval))
temp = string.replace(temp, '-{HTMLURL}-', tail + '.html')
temp = string.replace(temp, '-{JSINTERVAL}-', str(interval * 1000 + 1000))
temp = string.replace(temp, '-{IMGSRC}-', tail + ext)
temp = string.replace(temp, '-{IMGNAME}-', tail)

print
'uploading HTML-file ' + root + '.html ...',
sys.stdout.flush()  # necessary when using scp
fp = StringIO.StringIO(temp)
ftp = ftplib.FTP(host, user, passwd)
ftp.storlines('STOR ' + root + '.html', fp)
ftp.sendcmd('SITE CHMOD 644 ' + root + '.html')
ftp.close()
fp.close()
print
'done'

# determine the desired image format
ext = ext.lower()
if ext == '.jpg' or ext == '.jpeg':
    format = 'JPEG'
elif ext == '.gif':
    format = 'GIF'
elif ext == '.bmp':
    format = 'BMP'
else:
    raise ValueError, 'unsupportet image format'

if testWithoutVideoCapture:
    from PIL import Image
else:
    import VideoCapture

    cam = VideoCapture.Device(devnum=devnum)

if verbose:
    uploadedimages = 0
    totaluploadtime = 0
firsttime = 1
sessionstarttime = int(time.time())
while 1:
    try:
        recenttime = now = int(time.time())
        upload(firsttime=firsttime, uploadstarttime=now)
        firsttime = 0
        while now == recenttime or (now - sessionstarttime) % interval:
            now = int(time.time())
            time.sleep(0.2)
    except KeyboardInterrupt:
        if verbose:
            print
            print
            uploadedimages, 'images uploaded with an',
            print
            'average upload time of %.2f seconds.' % (totaluploadtime / uploadedimages)
        print
        print
        'uploading offline-image ...',
        sys.stdout.flush()  # necessary when using scp
        fp = open('offline.jpg', 'rb')
        ftp = ftplib.FTP(host, user, passwd)
        ftp.storbinary('STOR ' + filename, fp, 8192)
        ftp.close()
        fp.close()
        print
        'done'
        print
        'Program terminated - now it is save to close the window.'
        sys.exit()
