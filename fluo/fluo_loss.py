import os
import time
import cv2
import argparse
from utils.view_database import read_rect
from utils.draw_gt import draw_ground_truth
from fluo.fluo_urils import calc_loss
from fluo.fluo_create_tracker import create_tracker
from utils.convert_database import bytescaling

the_tracker = "null"
area_radius = 100
db = "tiff"


def get_loss_tiff(dir_name, tracker_name):
    loss_min = 1000
    loss_max = 0
    loss_average = 0
    items_count = 0
    tracker = None
    blank_image = draw_ground_truth(dir_name)
    t = 0
    num_skip = 0
    for f in os.listdir(dir_name):
        f = os.path.join(dir_name, f)
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
                rects = read_rect(f[0:f.find('_0.')] + '.xml')
                if not rects is None:
                    items_count += 1
                    x = (rects[0][0] + rects[0][2]) / 2
                    y = (rects[0][1] + rects[0][3]) / 2
                    if tracker is None:
                        print("try to create tracker: " + the_tracker)
                        tracker = create_tracker(tracker_name, x, y, area_radius)
                        if tracker is None:
                            raise Exception("cannot create tracker: " + tracker_name)
                        print("done")
                    img = cv2.imread(f[0:f.find('_0.')] + '_660.tiff', -1)
                    image0 = bytescaling(img)
                    image = cv2.merge((image0, image0, image0))
                    t_start = time.time()
                    _x, _y, res = tracker.fluo_predict(image, blank_image)
                    if res:
                        t_end = time.time()
                        loss = calc_loss(x, y, _x, _y)
                        # print(loss)
                        if loss_max < loss:
                            loss_max = loss
                        if loss_min > loss:
                            loss_min = loss
                        loss_average += loss
                        t += (t_end - t_start)

                    else:
                        num_skip += 1
    if items_count != 0:
        loss_average /= items_count
        t /= items_count
        return items_count, loss_min, loss_max, loss_average, blank_image, t, num_skip
    else:
        return 0, 0, 0, 0, None, 0, 0


def get_loss_jpeg(dir_name, tracker_name):
    loss_min = 1000
    loss_max = 0
    loss_average = 0
    items_count = 0
    tracker = None
    blank_image = draw_ground_truth(dir_name)
    t = 0
    num_skip = 0
    for f in os.listdir(dir_name):
        f = os.path.join(dir_name, f)
        baseName, ext = os.path.splitext(f)
        if ext == '.jpg':
            rects = read_rect(f)
            if not rects is None:
                items_count += 1
                x = (rects[0][0] + rects[0][2]) / 2
                y = (rects[0][1] + rects[0][3]) / 2
                if tracker is None:
                    print("try to create tracker: " + the_tracker)
                    tracker = create_tracker(tracker_name, x, y, area_radius)
                    if tracker is None:
                        raise Exception("cannot create tracker: " + tracker_name)
                    print("done")

                image = cv2.imread(f)
                t_start = time.time()
                _x, _y, res = tracker.fluo_predict(image, blank_image)
                if res:
                    t_end = time.time()
                    loss = calc_loss(x, y, _x, _y)
                    # print(loss)
                    if loss_max < loss:
                        loss_max = loss
                    if loss_min > loss:
                        loss_min = loss
                    loss_average += loss
                    t += (t_end - t_start)

                else:
                    num_skip += 1
    if items_count != 0:
        loss_average /= items_count
        t /= items_count
        return items_count, loss_min, loss_max, loss_average, blank_image, t, num_skip
    else:
        return 0, 0, 0, 0, None, 0, 0


def process_database(dir_name):
    file_name = os.path.join(dir_name, the_tracker + ".txt")
    average = 0
    count = 0
    max_average = 0
    max_value = 0
    taverage = 0
    skipped = 0
    total = 0
    with open(file_name, "w") as file_out:
        for f in os.listdir(dir_name):
            f = os.path.join(dir_name, f)
            baseName, ext = os.path.splitext(f)
            if os.path.isdir(f):
                try:
                    if db == "jpeg":
                        ic, lmin, lmax, lavg, img, t, sk = get_loss_jpeg(f, the_tracker)
                    else:
                        ic, lmin, lmax, lavg, img, t, sk = get_loss_tiff(f, the_tracker)
                    if lmax > max_value:
                        max_value = lmax
                except Exception as e:
                    print(e)
                    continue

                print(f, "{:8.3f}".format(ic), "{:8.3f}".format(lmin), "{:8.3f}".format(lmax), "{:8.3f}".format(lavg),
                      "{0:5.0f}".format(1000 * t), "{0:8.0f}".format(sk))
                print(f, "{:8.3f}".format(ic), "{:8.3f}".format(lmin), "{:8.3f}".format(lmax), "{:8.3f}".format(lavg),
                      "{0:5.0f}".format(1000 * t), "{0:8.0f}".format(sk),
                      file=file_out)
                average += lavg
                count += 1
                max_average += lmax
                taverage += t
                skipped += sk
                total += ic
                if not img is None:
                    pos = f.find('track')
                    if pos > 0:
                        s = f[pos:len(f):1] + ".jpg"
                        file_name = dir_name + "\\" + s
                        cv2.imwrite(file_name, img)

        print("==================================================")
        print("tracker = " + the_tracker)
        print("radius = {:8.3}".format(area_radius))
        print("total = {:8.3f} items".format(total))
        print("skipped = {:8.3f} %".format(100 * skipped / total))
        print("time = {:8.3f} ms".format(1000 * taverage / count))
        print("max average error = {:8.3f} pix".format(max_average / count))
        print("max value error = {:8.3f} pix".format(max_value))
        print("average error = {:8.3f} pix".format(average / count))
        print("==================================================")
        print("tracker = " + the_tracker, file=file_out)
        print("radius = {:8.3}".format(area_radius), file=file_out)
        print("total = {:8.3f} items".format(total), file=file_out)
        print("skipped = {:8.3f} %".format(100 * skipped / total), file=file_out)
        print("time = {:8.3f} ms".format(1000 * taverage / count), file=file_out)
        print("max average error = {:8.3f} pix".format(max_average / count), file=file_out)
        print("max value error = {:8.3f} pix".format(max_value), file=file_out)
        print("average error = {:8.3f} pix".format(average / count), file=file_out)

    file_out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="FLUO LOSS RESEARCH")
    parser.add_argument("-tracker", "--tracker", help="specify name of tracker", default="null", type=str)
    parser.add_argument("-radius", "--radius", help="specify radius of tracker", default=100, type=float)
    args = parser.parse_args()
    the_tracker = args.tracker
    area_radius = args.radius

    path = 'H:\\database\\fluovisor\\test\\set2\\'
    # H:\database\fluovisor\tracks\set2
    process_database(path)
