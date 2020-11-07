import os
from shutil import copyfile

track_count: int = 0
file_count: int = 0
out_dir: str = ''

def process_directory(dirName, dst):
    global track_count
    global file_count
    global out_dir
    for f in os.listdir(dirName):
        f = os.path.join(dirName, f)
        baseName, ext = os.path.splitext(f)
        dir, fileName = os.path.split(f)
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
                print("Copy [", fileName, "]")
                copyfile(f, os.path.join(out_dir, "{:05d}_0".format(file_count) + '.tiff'))
                copyfile(f[0:f.find('_0.')] + '_400.tiff', os.path.join(out_dir, "{:05d}_400".format(file_count) + '.tiff'))
                copyfile(f[0:f.find('_0.')] + '_660.tiff', os.path.join(out_dir, "{:05d}_660".format(file_count) + '.tiff'))
                copyfile(f[0:f.find('_0.')] + '_740.tiff', os.path.join(out_dir, "{:05d}_740".format(file_count) + '.tiff'))
                file_count = file_count + 1
        elif os.path.isdir(f):
            print("\nDescending into directory", f)
            if f.find('Full') != -1:
                track_count = track_count + 1
                file_count = 0
                if not os.path.isdir(os.path.join(dst, 'track' + "{:05d}".format(track_count))):
                    os.mkdir(os.path.join(dst, 'track' + "{:05d}".format(track_count) ))
                out_dir = os.path.join(dst, 'track' + "{:05d}".format(track_count))
            process_directory(os.path.join(dirName, f), dst)


def ConvertDatabase(path, dst):
    if not os.path.isdir(dst):
        print("make dir", dst)
        os.mkdir(dst)
    process_directory(path, dst)


if __name__ == '__main__':
    # convert database
    path = "H:\\database\\fluovisor\\source\\For fluovisor\\"
    dst = "H:\\database\\fluovisor\\test\\set2\\"
    ConvertDatabase(path, dst)
