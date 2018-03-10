# webcam-server.py
# by Don Garrett (dgarrett@acm.org)

__version__ = "0.1"

__all__ = ["VideoCaptureRequestHandler"]

import VideoCapture

import BaseHTTPServer
import StringIO
import shutil
import ConfigParser


class VideoCaptureRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """Runs a web server that serves images captured from the local camera.

    All requests are served with a freshly snapped image. This is not suitable
    for heavy traffic. No files are served other than a captured image.

    A version derived from SimpleHTTPServer could serve a wrapper page/site as
    well.

    It should be possible to cache the image to improve performance.
   """

    server_version = "VideoCapture/" + __version__

    # SharedCamera is a class variable that must be initialized externally
    #   before the class is used. Not the best design, but where else
    #   to hang it?
    SharedCamera = None
    Quality = 75

    def do_GET(self):
        """Serve a GET request."""

        self.do_HEAD()

        # Snap a current image
        image = self.SharedCamera.getImage()

        # save it to a string buffer, and write that out the network
        #  connection
        fp = StringIO.StringIO()
        image.save(fp, "jpeg", quality=self.Quality)
        fp.flush()
        fp.seek(0)

        shutil.copyfileobj(fp, self.wfile)
        fp.close()

        # XXX This would be simpler, if it didn't freak out for reasons
        #   that look like a C library assuming fp points to a file
        #   on disk.
        #
        # image.save(self.wfile, "jpeg")
        #

    def do_HEAD(self):
        """Serve a HEAD request."""

        self.send_response(200)
        self.send_header("Content-type", 'image/jpeg')
        self.end_headers()


def main():
    parser = ConfigParser.ConfigParser()
    parser.read('webcam-server.ini')

    # Start the image capture stuff
    devnum = int(parser.get('httpd', 'devnum'))
    quality = int(parser.get('httpd', 'quality'))

    cam = VideoCapture.Device(devnum=devnum)
    VideoCaptureRequestHandler.SharedCamera = cam
    VideoCaptureRequestHandler.Quality = quality

    # Start the web server
    address = parser.get('httpd', 'address')
    port = int(parser.get('httpd', 'port'))

    server_address = (address, port)

    httpd = BaseHTTPServer.HTTPServer(server_address,
                                      VideoCaptureRequestHandler)

    sa = httpd.socket.getsockname()
    print
    "Serving HTTP on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()


if __name__ == '__main__':
    main()
