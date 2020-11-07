import cv2
import os
import xml.etree.ElementTree as ET
from fluo_create_tracker import create_tracker

def file_count(path):
    count = 0
    for f in os.listdir(path):
        baseName, ext = os.path.splitext(f)
        if ext == '.jpg':
            count = count + 1
    return count


def read_rect(path):
    rects = []
    thisFile = path
    base = os.path.splitext(path)[0] + '.xml'
    if not os.path.exists(base):
        return None
    if not os.path.isfile(base):
        return None
    # parse an xml file by name
    tree = ET.parse(base)
    root = tree.getroot()
    # print(root.attrib)
    for elem in root:
        left = int(elem.get('left'))
        right = int(elem.get('right'))
        top = int(elem.get('top'))
        bottom = int(elem.get('bottom'))
        rects.append([left, top, right, bottom])
    return rects


def draw_circle(rects, image):
    for i in range(len(rects)):
        x = (rects[i][0] + rects[i][2]) / 2
        y = (rects[i][1] + rects[i][3]) / 2
        r = (rects[i][2] - rects[i][0]) / 2
        cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0))
    return None


def view_database(path):
    print(file_count(path))
    r = None
    tracker = None
    count = 0
    for f in os.listdir(path):
        f = os.path.join(path, f)
        baseName, ext = os.path.splitext(f)
        if ext == '.jpg':
            rect = read_rect(f)
            #if rect is None:
            #    continue
            image = cv2.imread(f)
            if tracker is None:
                x = (rect[0][0] + rect[0][2]) / 2
                y = (rect[0][1] + rect[0][3]) / 2
                tracker = create_tracker("MEDIANFLOW", x, y, 100)
                r = (rect[0][2] - rect[0][0]) / 2

            #_x = (rect[0][0] + rect[0][2]) / 2
            #_y = (rect[0][1] + rect[0][3]) / 2

            x, y, res = tracker.fluo_predict(image)

            #loss = calc_loss(x, y, _x, _y)
            # print(loss)
            if res:
                cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 255))
            if not rect is None:
                draw_circle(rect, image)
            dir = os.path.join(path, 'debug')
            if not os.path.isdir(dir):
                os.mkdir(os.path.join(path, 'debug'))
            fileName = os.path.join(path, 'debug\\' + str(count) + '.jpg')
            cv2.imwrite(fileName, image)
            count += 1
            cv2.imshow("track", image)
            key = cv2.waitKey(0)
            if key == 27:
               break


if __name__ == '__main__':
    path = "H:\\database\\fluovisor\\tracks\\set1_660\\track00027\\"
    view_database(path)
