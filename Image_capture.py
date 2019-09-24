import numpy as np
import cv2
import random
import time
def videocap(i):
    cap = cv2.VideoCapture(-1)
    ret, frame = cap.read()
    cv2.imwrite('images/{index}.jpg'.format(index=int(i)),frame)
# When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()



