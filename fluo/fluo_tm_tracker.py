"""
    Template matching  fluo tracker.
    should track center of mass area of interest on the images taken
    FLOUVISOR device

    author: Alex A.Telnykh
    date: october 2020
"""
import cv2
from fluo.fluo_track_core import fluo_tracker

class fluo_tm_track(fluo_tracker):
    def __init__(self, x, y, radius=100):
        super().__init__(x, y, radius)
        self.Tmpl = None

    def fluo_predict(self, image, blank=None):
        if self.Tmpl is None:
            """
                make template 
            """
            self.Tmpl = image[int(self.y - self.radius):int(self.y+self.radius), int(self.x - self.radius):int(self.x + self.radius)]

        result = cv2.matchTemplate(image, self.Tmpl, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        #print(max_val, min_val, min_loc)
        if min_val > 0.3:
             return 0, 0, False
        _x = min_loc[0] + self.radius
        _y = min_loc[1] + self.radius
        self.x = _x
        self.y = _y
        self.Tmpl = image[int(self.y - self.radius):int(self.y + self.radius),
                    int(self.x - self.radius):int(self.x + self.radius)]
        return self.x, self.y, True