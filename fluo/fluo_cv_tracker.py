import cv2
from fluo_track_core import fluo_tracker


class fluo_cv_track(fluo_tracker):
    def __init__(self, x, y, radius=100, tname="BOOSTING"):
        super().__init__(x, y, radius)
        self.tracker = None
        self.tracker_name = tname

    def fluo_predict(self, image, blank=None):
        if self.tracker is None:
            """
                make template 
            """
            if self.tracker_name == "BOOSTING":
                self.tracker = cv2.TrackerBoosting_create()
            elif self.tracker_name == "MIL":
                self.tracker = cv2.TrackerMIL_create()
            elif self.tracker_name == "KCF":
                self.tracker = cv2.TrackerKCF_create()
            elif self.tracker_name == "TLD":
                self.tracker = cv2.TrackerTLD_create()
            elif self.tracker_name == "MEDIANFLOW":
                self.tracker = cv2.TrackerMedianFlow_create()
            elif self.tracker_name == "MOSSE":
                self.tracker = cv2.TrackerMOSSE_create()
            elif self.tracker_name == "CSRT":
                self.tracker = cv2.TrackerCSRT_create()
            else:
                raise Exception("cannot create tracker: " + self.tracker_name)

            bbox = (int(self.x - self.radius), int(self.y - self.radius), int(2 * self.radius), int(2 * self.radius))
            self.tracker.init(image, bbox)

        else:
            ok, bbox = self.tracker.update(image)
            if ok:
                self.x = bbox[0] + self.radius
                self.y = bbox[1] + self.radius
            else:
                return 0, 0, False

        return self.x, self.y, True
