import os
from shutil import copyfile
track_count: int = 0
out_dir: str = ''
def file_count(path):
    count = 0
    for f in os.listdir(path):
        baseName, ext = os.path.splitext(f)
        if ext == '.jpg':
            count = count + 1
    return count
def merge(dirName, dst):
    global track_count
    global out_dir
    for f in os.listdir(dirName):
        f = os.path.join(dirName, f)
        baseName, ext = os.path.splitext(f)
        dir, fileName = os.path.split(f)
        if ext == '.tiff' or ext == '.xml':
            a=1
            #copy file
            #print(fileName)
            copyfile(f, os.path.join(out_dir, fileName))
        elif os.path.isdir(f):
            if f.find('track') != -1 and (int(len(os.listdir(f))) - 1) / 5 > 40:
                print(f, (int(len(os.listdir(f))) - 1)/5)
                track_count += 1
                if not os.path.isdir(os.path.join(dst, 'track' + "{:05d}".format(track_count))):
                    #print(os.path.join(dst, 'track' + "{:05d}".format(track_count)))
                    os.mkdir(os.path.join(dst, 'track' + "{:05d}".format(track_count)))
                out_dir = os.path.join(dst, 'track' + "{:05d}".format(track_count))
            merge(os.path.join(dirName, f), dst)
    return None
if __name__ == '__main__':
    path = "H:\\database\\fluovisor\\test\\"
    dst = "H:\\database\\fluovisor\\longtracks\\"
    merge(path, dst)