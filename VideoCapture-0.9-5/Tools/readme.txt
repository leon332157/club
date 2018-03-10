webcam-uploader.py
------------------
Uploades a picture obtained by video-capturing to the web periodically.

The destination of the picture and the interval between successive uploads is
specified in the webcam-uploader.ini file.  Further details are given there.


webcam-saver.py
---------------
Monitors a picture on the web for (and saves it in case of) any changes.

The location of the picture to observe and the interval between probing is
specified in the webcam-saver.ini file.  Further details are given there.


webcam-watcher.py
-----------------
Periodically retrieves a picture from the web and displays it in a window.

Several URLs can be specified in the webcam-watcher.ini file.  By
right-clicking at the picture another URL can be selected.


  -------------------------------------------------------
                     |   requirements   |    runs on
                     |  DX8  PIL  PyQt  |  Win32  Linux
  -------------------------------------------------------
    webcam-uploader  |   x    x    -    |    x      -
    webcam-saver     |   -    *    -    |    x      x
    webcam-watcher   |   -    x    x    |    x      x
  -------------------------------------------------------

                              * ... if available, used for checking the image
