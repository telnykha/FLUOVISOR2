import os
from shutil import copyfile

def put_xml(src, dst):
    for f in os.listdir(src):
        f = os.path.join(src, f)
        baseName, ext = os.path.splitext(f)
        dir, fileName = os.path.split(f)
        if ext == '.xml':
           copyfile(f, os.path.join(dst,fileName))
        elif os.path.isdir(f):
            print("\nDescending into directory", f)
            s = f[f.find('track0'):f.find('track0') + (len(f) -f.find('track0'))]
            outDir = os.path.join(dst, s)
            put_xml(f, outDir)
if __name__ == '__main__':
    dst_name = "H:\\database\\fluovisor\\tracks\\set2_660\\"
    src_name = "H:\\database\\fluovisor\\tracks\\set2\\"
    put_xml(src_name, dst_name)