"""
Оценка уровня выгорания.
Входные данные: база данных xxx_0.tiff xxx_400.tiff xxx_660.tiff xxx_740.tiff xxx.xml
xxx меняется от 0 до числа кадров в эксперименте
выходные данные: текстовый файл формата
trackID frameID Burout_400 Burnout_660 Burnout_400t Burnout_660t
где Burout_400 Burnout_660 - значения выгорания по разметке
Burnout_400t Burnout_660t - значения выгорания по трекеру
"""
import os
import cv2
import numpy as np
from utils.view_database import read_rect
from fluo.fluo_create_tracker import create_tracker
from utils.convert_database import bytescaling
from fluo.fluo_urils import calc_loss

TRACKER = "MOSSE"

def process_dir(path , file_out = None):
    count = 0
    trackID = path[path.find('track'):]
    trackID = trackID[trackID.find('0'):]
    tracker = None
    for f in os.listdir(path):
        baseName, ext = os.path.splitext(f)
        f = os.path.join(path, f)
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
                # read data
                img0 = cv2.imread(f, -1)
                img400 = cv2.imread(f[0:f.find('_0.')] + '_400.tiff', -1)
                img660 = cv2.imread(f[0:f.find('_0.')] + '_660.tiff', -1)
                img740 = cv2.imread(f[0:f.find('_0.')] + '_740.tiff', -1)
                # img400 = img400 - img0
                # img660 = img660 - img0
                # img740 = img740 - img0
                rect = read_rect(f[0:f.find('_0.')] + '.xml')
                sum400 = -1
                sum660 = -1
                _sum400 = -1
                _sum660 = -1
                x = -1
                y = -1
                _x = -1
                _y = -1
                if rect is None:
                    print("нет разметки")
                else:
                    x = (rect[0][0] + rect[0][2]) / 2
                    y = (rect[0][1] + rect[0][3]) / 2

                    res = False
                    if tracker == None:
                        tracker = create_tracker(TRACKER, x, y, 125)

                    img = bytescaling(img740)
                    image = cv2.merge((img, img, img))
                    _x, _y, res = tracker.fluo_predict(image)

                    r = 10
                    s = 4 * r * r

                    sum400 = np.sum(img400[int(y - r):int(y + r), int(x - r):int(x + r)]) / s
                    sum660 = np.sum(img660[int(y - r):int(y + r), int(x - r):int(x + r)]) / s
                    if res:
                        _sum400 = np.sum(img400[int(_y - r):int(_y + r), int(_x - r):int(_x + r)]) / s
                        _sum660 = np.sum(img660[int(_y - r):int(_y + r), int(_x - r):int(_x + r)]) / s
                loss = calc_loss(x,y,_x,_y)
                print(trackID, "{:05d}".format(count), "{:8.3f}".format(sum400), "{:8.3f}".format(sum660),
                      "{:8.3f}".format(_sum400), "{:8.3f}".format(_sum660), "{:8.3f}".format(loss))
                print(trackID, "{:05d}".format(count), "{:8.3f}".format(sum400), "{:8.3f}".format(sum660),
                      "{:8.3f}".format(_sum400), "{:8.3f}".format(_sum660), "{:8.3f}".format(loss), file= file_out)

                count += 1

    print(path, count)


def burnout(path):
    file_name = os.path.join(path, TRACKER+"burnout.txt")
    fileout = open(file_name, "w")
    print(path, file=fileout)
    for f in os.listdir(path):
        f1 = os.path.join(path, f)
        if os.path.isdir(f1):
            if f.find('track') != -1:
                process_dir(f1, fileout)
    fileout.close()
    return None


if __name__ == '__main__':
    path = "H:\\database\\fluovisor\\test\\set2\\"
    burnout(path)
