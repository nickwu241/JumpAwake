from __future__ import division
import cv2
import time
import sys
import datetime
import grequests

import numpy as np
import imutils
from skimage.measure import compare_ssim

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

def checkAction(background_f, frame, y0, x0, height, width, version=0):
    verbose = False
    #Convert frames to grayscale
    background_f_gray = cv2.cvtColor(background_f, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Compute Strutural Similarity Index (SSIM) btwn the two frames
    (score,frame_diff) = compare_ssim(background_f_gray, frame_gray, full= True)
    frame_diff = (frame_diff * 255).astype("uint8") #convert float it uint8
    if verbose == True:
        print("SSIM: {}".format(score))
        if score < .5:
            print("Score under 0.5!")

    c_max = None
    #To locate the differences
    if True:
        #Threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(frame_diff, 200, 255,
            cv2.THRESH_BINARY_INV )[1]
            #| cv2.THRESH_OTSU
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if len(cnts) > 0:
            c_max = max(cnts, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(c_max)
            if w > width/2:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if verbose == True:
                cv2.imshow("Diff"+str(version), frame_diff)
                cv2.imshow("Thresh"+str(version), thresh)
        else:
            for c in cnts:
                # compute the bounding box of the contour and then draw the
                # bounding box on both input images to represent where the two
                # images differ
                if verbose == True:
                    (x, y, w, h) = cv2.boundingRect(c)
                    #cv2.rectangle(background_f, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.imshow("Diff"+str(version), frame_diff)
                    cv2.imshow("Thresh"+str(version), thresh)
    confidence = score
    return confidence

def main(endpoint, name):
    faceCascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    hasFrame, frame = cap.read()
    current_time = datetime.datetime.now()
    finish = current_time + datetime.timedelta(seconds=3)

    frame_count = 0
    tt_opencvHaar = 0
    vid_writer = cv2.VideoWriter('output-haar-{}.avi'.format(str(0).split(".")[0]),cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame.shape[1],frame.shape[0]))
    avg2 = np.float32(frame)
    background_frame = None

    #Start up calibration
    while current_time < finish:
        current_time = datetime.datetime.now()
        hasFrame, frame = cap.read()
        if not hasFrame:
            break
        frame_count += 1

        t = time.time()
        background_frame = cv2.GaussianBlur(frame, (5,5), 0)
        cv2.accumulateWeighted(background_frame,avg2,0.01)

        bboxes = detectFaces(faceCascade, frame)
        #shift bounding box up 50% of height to clear user head
        #bboxes = [bboxes[:][0], bboxes[:][1]-bboxes[:][3]/2, bboxes[:][2], bboxes[:][3]]
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

    state = 0
    trip_threshold = 0.5
    jump_timeout_time = 1
    jump_debounce_time = .5
    jump_start_time = time.time()
    jump_stop_time = time.time()
    n_actions = 0
    found = False
    count_pulse = False
    while True:
        hasFrame, frame = cap.read()
        if not hasFrame:
            break
        frame_count += 1
        #0 - looking for action
        #1 - jump in action



        t = time.time()
        outOpencvHaar, _ = drawBoundingBoxes(faceCascade, frame, bboxes)

        for index, faces in enumerate(bboxes, start=0):
            x0, y0, height, width = bboxes[0]
            y0 = y0 - int(height/2)
            frame_cropped_check = frame[max(0, y0-height):y0, x0:x0+width]
            bkg_frame_check = background_frame[max(0, y0-height):y0, x0:x0+width]

            diff = checkAction(bkg_frame_check, frame_cropped_check, y0, x0, height, width, 0)

            # if diff < trip_threshold and not found:
            #     print("in air")
            #     found = True
            #     time.sleep(0.1)
            # elif diff > trip_threshold and found:
            #     print("jump detected")
            #     found = False

            if diff < trip_threshold: #reset state
                if found == False: #Rising edge
                    jump_start_time = time.time()
                found = True
            else:
                if found == True: #Falling edge
                    jump_stop_time = time.time()
                    if jump_stop_time > jump_start_time and count_pulse == False:
                        print("Pulse Time: "+str(round(jump_stop_time-jump_start_time, 2)))
                        pulse_duration = round(jump_stop_time-jump_start_time, 2)

                        if pulse_duration < jump_debounce_time:
                            count_pulse = True
                found = False

            if count_pulse == True:
                count_pulse = False
                n_actions += 1
                print("Jumping jack "+str(n_actions))
                grequests.post("http://{0}/{1}/jump".format(endpoint, name))



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

