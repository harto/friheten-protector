import cv2

def capture(frame, rects):
    raw = frame.raw
    for (x, y, w, h) in rects:
        cv2.rectangle(raw,
                      (x, y),
                      (x + w, y + h),
                      color=(0, 0, 255),
                      thickness=2)
    # write out
