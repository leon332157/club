import SimpleHTTPServer
import urllib
import StringIO
import posixpath, sys, string
import time

from VideoCapture import *

cam = Device(devnum=0)
# ~ cam.setResolution(640, 480) # VGA
# ~ cam.setResolution(768, 576) # PAL
# ~ cam.setResolution(384, 288) # PAL / 4
# ~ cam.setResolution(192, 144) # PAL / 16
# ~ cam.setResolution(80, 60) # Minimum


sys.stderr = sys.stdout


class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def sendImage(self):
        try:
            image = cam.getImage(timestamp=3, boldfont=1)
            stros = StringIO.StringIO()
            image.save(stros, "jpeg")
            jpgStr = stros.getvalue()
            sys.stderr.write("len: %d\n" % len(jpgStr))
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()
            self.wfile.write(jpgStr)
        except:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("Problem sending image: %s\n" % self.path)

    def pushImages(self):
        self.separator = "abcdef"
        self.maxFrames = 0
        try:
            self.send_response(200)
            self.send_header("Content-type",
                             "multipart/x-mixed-replace;boundary=%s" % self.separator)
            self.end_headers()
            self.wfile.write("--%s\r\n" % self.separator)
            frameNo = 0
            while 1:
                time.sleep(0.04)
                frameNo = frameNo + 1
                if self.maxFrames > 0 and frameNo > 1000:
                    break
                image = cam.getImage(timestamp=3, boldfont=1)
                stros = StringIO.StringIO()
                image.save(stros, "jpeg")
                jpgStr = stros.getvalue()
                sys.stderr.write("len: %d\n" % len(jpgStr))
                self.wfile.write("Content-type: image/jpeg\r\n")
                # self.wfile.write("Content-length: %d\r\n" % len(jpgStr))
                self.wfile.write("\r\n")
                self.wfile.write(jpgStr)
                self.wfile.write("\r\n--%s\r\n" % self.separator)
        except:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("Problem sending image: %s\n" % self.path)

    def do_GET(self):
        """Serve a GET request."""
        if self.path[:len("/quit")] == "/quit":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("exiting....")
            global cam
            del cam
            sys.exit(0)
        if self.path[:len("/cam")] == "/cam":
            self.sendImage()
            return
        if self.path[:len("/push")] == "/push":
            self.pushImages()
            return
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        return


if len(sys.argv) == 1:
    sys.argv = (sys.argv[0], "8000")

SimpleHTTPServer.test(MyHandler)
