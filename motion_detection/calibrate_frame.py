from __future__ import division
import cv2
import time
import sys
import datetime

def downscale_frame(frame, scaled_height=300):
    new_frame = frame.copy()
    height, width, _ = new_frame.shape

    scaled_width = int((width / height) * scaled_height)
    return cv2.resize(new_frame, (scaled_width, scaled_height))


def drawBoundingBoxes(faceCascade, frame, bboxes):
    frameHeight, _, _ = frame.shape

    for x, y, w, h in bboxes:
        cv2.rectangle(frame, (x, y), (x + w, y - h), (0, 255, 0),
                      int(round(frameHeight / 150)), 4)
    return frame, bboxes

def detectFaces(faceCascade, frame, inHeight=300, inWidth=0):
    frameOpenCVHaar = frame.copy()
    frameHeight, frameWidth, _ = frameOpenCVHaar.shape

    scaled_frame = downscale_frame(frame)
    scaledHeight, scaledWidth, _ = scaled_frame.shape

    frameGray = cv2.cvtColor(scaled_frame, cv2.COLOR_BGR2GRAY)

    boundingBoxes = faceCascade.detectMultiScale(frameGray)
    ratio_x = frameWidth / scaledWidth
    ratio_y = frameHeight / scaledHeight

    return [( int(x * ratio_y), int(y * ratio_x), int(w * ratio_x) , int(h * ratio_y) ) for (x, y, w, h) in boundingBoxes]

if __name__ == "__main__" :
    source = 0
    if len(sys.argv) > 1:
        source = sys.argv[1]

    faceCascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(source)
    hasFrame, frame = cap.read()
    current_time = datetime.datetime.now()
    finish = current_time + datetime.timedelta(seconds=3)

    frame_count = 0
    tt_opencvHaar = 0
    vid_writer = cv2.VideoWriter('output-haar-{}.avi'.format(str(source).split(".")[0]),cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame.shape[1],frame.shape[0]))

    while current_time < finish:
        current_time = datetime.datetime.now()
        hasFrame, frame = cap.read()
        if not hasFrame:
            break
        frame_count += 1

        t = time.time()
        bboxes = detectFaces(faceCascade, frame)
        frame, _ = drawBoundingBoxes(faceCascade, frame, bboxes)
        tt_opencvHaar += time.time() - t
        fpsOpencvHaar = frame_count / tt_opencvHaar

        label = "OpenCV Haar ; FPS : {:.2f}".format(fpsOpencvHaar)
        cv2.putText(frame, label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3, cv2.LINE_AA)

        cv2.imshow("Face Detection Comparison", frame)

        vid_writer.write(frame)
        if frame_count == 1:
            tt_opencvHaar = 0
        k = cv2.waitKey(10)
        if k == 27:
            break


    while True:
        hasFrame, frame = cap.read()
        if not hasFrame:
            break
        frame_count += 1

        t = time.time()
        outOpencvHaar, _ = drawBoundingBoxes(faceCascade, frame, bboxes)
        tt_opencvHaar += time.time() - t
        fpsOpencvHaar = frame_count / tt_opencvHaar

        label = "OpenCV Haar ; FPS : {:.2f}".format(fpsOpencvHaar)
        cv2.putText(outOpencvHaar, label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3, cv2.LINE_AA)

        cv2.imshow("Face Detection Comparison", outOpencvHaar)

        vid_writer.write(outOpencvHaar)
        if frame_count == 1:
            tt_opencvHaar = 0

        k = cv2.waitKey(10)
        if k == 27:
            break
    cv2.destroyAllWindows()
    vid_writer.release()

