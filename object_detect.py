import dlib
from skimage import io

tracker = dlib.correlation_tracker()

def start_object_track(name, rect):
    img = io.imread(name)
    ret = tracker.start_track(img, dlib.rectangle(rect.left, rect.top, rect.right, rect.bottom))
    return ret

def update_object_track(name):
    img = io.imread(name)
    tracker.update(img)
    ret = tracker.get_position()
    return ret


