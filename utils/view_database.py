import cv2
import os
import xml.etree.ElementTree as ET
from fluo.fluo_create_tracker import create_tracker
from utils.convert_database import bytescaling
from fluo.fluo_urils import calc_loss

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

        if ext == '.tiff':
            if f.find('_superposition') != -1:
                continue
            if f.find('_400.') != -1:
                continue
            if f.find('_660.') != -1:
                continue
            if f.find('_740.') != -1:
                continue
            else:
                rect = read_rect(f[0:f.find('_0.')] + '.xml')
                # if rect is None:
                #    continue
                img = cv2.imread(f[0:f.find('_0.')] + '_660.tiff', -1)
                image0 = bytescaling(img)
                image = cv2.merge((image0, image0, image0))
                if tracker is None:
                    x = (rect[0][0] + rect[0][2]) / 2
                    y = (rect[0][1] + rect[0][3]) / 2
                    tracker = create_tracker("CSRT", x, y, 125)
                    r = (rect[0][2] - rect[0][0]) / 2
                loss = -1
                if rect is not None:
                    _x = (rect[0][0] + rect[0][2]) / 2
                    _y = (rect[0][1] + rect[0][3]) / 2
                    loss = calc_loss(x, y, _x, _y)
                x, y, res = tracker.fluo_predict(image)
                print(loss)
                if res:
                    cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 255))
                if not rect is None:
                    draw_circle(rect, image)
                cv2.putText(image, "frame " + str(count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
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
    path = "H:\\database\\fluovisor\\test\\set2\\track00018\\"
    view_database(path)
