from fluo.fluo_null_traclker import fluo_null_track
from fluo.fluo_lk_tracker import fluo_lk_track
from fluo.fluo_shift_tracker import fluo_sift_track
from fluo.fluo_tm_tracker import fluo_tm_track
from fluo.fluo_cv_tracker import fluo_cv_track

def create_tracker(name, x, y, radius = 100):
    if name == 'NULL':
        return fluo_null_track(x, y)
    elif name == 'LK':
        return fluo_lk_track(x, y, radius)
    elif name == 'SIFT':
        return fluo_sift_track(x, y, int(radius))
    elif name == 'TM':
        return fluo_tm_track(x, y , radius)
    elif name == "BOOSTING":
        return fluo_cv_track(x,y, radius, "BOOSTING")
    elif name == "MIL":
        return fluo_cv_track(x, y, radius, "MIL")
    elif name == "KCF":
        return fluo_cv_track(x, y, radius, "KCF")
    elif name == "TLD":
        return fluo_cv_track(x, y, radius, "TLD")
    elif name == "MEDIANFLOW":
        return fluo_cv_track(x, y, radius, "MEDIANFLOW")
    elif name == "MOSSE":
        return fluo_cv_track(x, y, radius, "MOSSE")
    elif name == "CSRT":
        return fluo_cv_track(x, y, radius, "CSRT")
    else:
        return None