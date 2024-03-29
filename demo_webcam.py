import argparse
import cv2

from yolo import YOLO

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--device', default=0, help='Device to use')
ap.add_argument('-c', '--confidence', default=0.5, help='Confidence for yolo')
args = ap.parse_args()

classes = ["good", "bad", "none"]


print("loading yolov4-tiny...")
yolo = YOLO("models/mask-yolov4-tiny.cfg", "models/mask-yolov4-tiny.weights", classes)

yolo.size = int(416)
yolo.confidence = float(args.confidence)

colors = [(0, 255, 0), (0, 165, 255), (0, 0, 255)]

print("starting webcam...")
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    width, height, inference_time, results = yolo.inference(frame)
    for detection in results:
        id, name, confidence, x, y, w, h = detection
        cx = x + (w / 2)
        cy = y + (h / 2)

        # draw a bounding box rectangle and label on the image
        color = colors[id]
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        text = "%s (%s)" % (name, round(confidence, 2))
        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 2)

    cv2.imshow("preview", frame)

    rval, frame = vc.read()

    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break
cv2.destroyWindow("preview")
vc.release()
