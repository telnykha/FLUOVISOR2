import os
import math
import cv2
import numpy as np
from view_database import read_rect, draw_circle


def view_track(path):
    tracker = None
    width = 0
    for f in os.listdir(path):
        f = os.path.join(path, f)
        baseName, ext = os.path.splitext(f)
        cx = 0
        cy = 0
        h = 0
        if ext == '.jpg':
            rect = read_rect(f)
            image = cv2.imread(f)
            if width == 0:
                width = int((rect[0][2] - rect[0][0])/2)
            if tracker is None:
                cx = 0.5 * (rect[0][0] + rect[0][2])
                cy = 0.5 * (rect[0][1] + rect[0][3])
                bbox = (int(cx-100), int(cy-100), 200,200)
                #bbox = cv2.selectROI(frame, False)
                tracker = cv2.TrackerMIL_create()
                tracker.init(image, bbox)
            else:
                ok, bbox = tracker.update(image)
                if ok:
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    cv2.rectangle(image, p1, p2, (255, 0, 0), 2, 1)
                    p1 = (p1[0] + 100, p1[1] + 100)
                    cv2.circle(image, p1, width, (255,255,255))
                else:
                    cv2.putText(image, "Tracking failure detected", (100, 80),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            # tracker.draw(image)
            # if not rect is None:
            if rect is not None:
                draw_circle(rect, image)
            cv2.imshow("track", image)
            key = cv2.waitKey(0)
            if key == 27:
                break


if __name__ == '__main__':
    path = "G:\\database\\fluovisor\\track00029\\"
    view_track(path)
