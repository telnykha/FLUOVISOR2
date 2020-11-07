import math

def calc_loss(x, y, x1, y1):
    return math.sqrt((x1 - x) * (x1 - x) + (y1 - y) * (y1 - y))