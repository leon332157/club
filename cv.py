import numpy as np
from PIL import ImageGrab
import cv2

while True:
    printscreen_pil = ImageGrab.grab()
    printscreen_numpy = np.array(printscreen_pil.getdata(), dtype='uint8')
    cv2.imshow('window', printscreen_numpy)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
