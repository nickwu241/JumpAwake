from __future__ import division
import cv2
import time
import subprocess
import sys
import datetime
import requests

import numpy as np
import imutils
from skimage.measure import compare_ssim
from imutils.video import VideoStream

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

def drawBoxes(frame, faceFrames,b=0,g=0,r=255):
    #print(str(faceFrames.shape))
    #print(str(len(faceFrames)/4))
    if True:
        #for faces in range(0, len(faceFrames)/4):
        if len(faceFrames)<4:
            pass
        else:
            #[startX, startY, endX, endY] = faceFrames
            [x0, y0, width, height] = faceFrames

            #text = "{:.2f}%".format(confidence * 100)
            # y = startY - 10
            # if startY - 10 > 10:
            #     pass
            # else:
            #     startY + 10
           # cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
            cv2.rectangle(frame, (x0, y0), (x0+width, y0+height), (b, g, r), 2)

            #cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    #cv2.imshow("Frame", frame)
    return frame

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

def detectFaces2(frame, net, confidence_threshold=0.5):
    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))
    # pass the blob through the network and obtain the detections and predictions

    net.setInput(blob)
    detections = net.forward()
    faceFrames = [[] for _ in range(detections.shape[2])]
    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence < confidence_threshold:
            continue

        # compute the (x, y)-coordinates of the bounding box for the
        # object
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        #faceFrames[i] = [startX, startY, endX, endY]
        faceFrames[i]  = [startX, startY, endX-startX, endY-startY]
        #[x0, y0, width, height]

    return faceFrames

def checkAction(background_f, frame, y0, x0, height, width, version=0):
    verbose = False
    debug = True
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
    bbox_triggered = []
    #To locate the differences
    if False:
        #Threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(frame_diff, 0, 255,
            cv2.THRESH_BINARY_INV )[1]
            #| cv2.THRESH_OTSU
        if debug == True:
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            if len(cnts) > 0:
                c_max = max(cnts, key=cv2.contourArea)
                (x, y, w, h) = cv2.boundingRect(c_max)
                bbox_triggered = [x, y, w, h]

                if verbose == True:
                    if w > width/2:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
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
    else:
        bbox_triggered = [0,0,0,0]
    confidence = score

    return confidence, bbox_triggered

def main(endpoint, name, duration):
    source = 0
    debug = True
    haar = False
    if haar == True:
        faceCascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')

    #DNN METHOD load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")

    #cap = cv2.VideoCapture(source)
    # initialize the video stream and allow the cammera sensor to warmup
    cap = VideoStream(usePiCamera=-1 > 0).start()
    time.sleep(2)

    frame = cap.read()
    frame = imutils.resize(frame, width=400)
    current_time = datetime.datetime.now()
    finish = current_time + datetime.timedelta(seconds=1)

    if haar==True:
        hasFrame = True
        frame_count = 0
        tt_opencvHaar = 0
        vid_writer = cv2.VideoWriter('output-haar-{}.avi'.format(str(source).split(".")[0]),cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame.shape[1],frame.shape[0]))

    avg2 = np.float32(frame)
    background_frame = None

    #Start up calibration
    while current_time < finish:
        current_time = datetime.datetime.now()
        hasFrame =True
        frame = cap.read()
        frame = imutils.resize(frame, width=400)
        #frame = cv2.flip( frame, 1 )

        #background_frame = cv2.GaussianBlur(frame, (5,5), 0)
        background_frame = frame
        cv2.accumulateWeighted(background_frame,avg2,0.01)

        if haar == True:
            bboxes = detectFaces(faceCascade, frame)
            frame, _ = drawBoundingBoxes(faceCascade, frame, bboxes)
            if not hasFrame:
                break
            frame_count += 1

            t = time.time()
            tt_opencvHaar += time.time() - t
            fpsOpencvHaar = frame_count / tt_opencvHaar

            label = "OpenCV Haar ; FPS : {:.2f}".format(fpsOpencvHaar)
            cv2.putText(frame, label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3, cv2.LINE_AA)

            vid_writer.write(frame)
            if frame_count == 1:
                tt_opencvHaar = 0

        else:
            bboxes = detectFaces2(frame, net)
            if debug == True:
                for faces in bboxes:
                    drawBoxes(frame, faces, 255,0,255)

        if debug == True:
            cv2.imshow("Face Detection Comparison", frame)

        k = cv2.waitKey(10)
        if k == 27:
            break


    trip_threshold = 0.5
    jump_timeout_time = 1
    jump_debounce_time = .1
    jump_start_time = time.time()
    jump_stop_time = time.time()
    n_actions = 0
    found = False
    count_pulse = False

    start_time = time.time()
    # subprocess.Popen(['afplay', 'smw_coin.wav'])

    while (time.time() - start_time) < duration:
        hasFrame = True
        frame = cap.read()
        frame = imutils.resize(frame, width=400)
        #frame = cv2.flip( frame, 1 )

        if haar == True:
            if not hasFrame:
                break
            frame_count += 1

            t = time.time()
            outOpencvHaar, _ = drawBoundingBoxes(faceCascade, frame, bboxes)
        else:
            #bboxes = detectFaces2(frame)
            if debug == True:
                for faces in bboxes:
                    frame_draw = drawBoxes(frame, faces,0,255,0)
                    cv2.imshow("Face Detection Comparison", frame_draw)

        for index, faces in enumerate(bboxes, start=0):
            try:
                x0, y0, width, height = bboxes[0]
            except ValueError:
                continue
            if y0 > int(height/2):
                y0 = y0 - int(height/2)
            frame_cropped_check = frame[max(0, y0-width):y0, x0:x0+width]
            bkg_frame_check = background_frame[max(0, y0-width):y0, x0:x0+width]

            diff, bbox_triggered = checkAction(bkg_frame_check, frame_cropped_check, y0, x0, width, width, 0)
            #print(str(bboxes[0])) #[x, y, w, h]
            if len(bbox_triggered)>1 and bbox_triggered[2] > width/2:
                if debug == True:
                    frame_draw = drawBoxes(frame_draw, [x0,max(0, y0-height),bbox_triggered[2],bbox_triggered[3]], 0,0,255)
                    cv2.imshow("Face Detection Comparison", frame_draw)

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

                        if pulse_duration < jump_timeout_time and pulse_duration > jump_debounce_time:
                            count_pulse = True
                found = False

            if count_pulse == True:
                count_pulse = False
                n_actions += 1
                print("Jumping jack "+str(n_actions))
                if endpoint ==  "local":
                    pass
                else:
                    subprocess.Popen(['curl', '-X', 'POST', "http://{0}/{1}/jump".format(endpoint, name)])
                    # subprocess.Popen(['afplay', 'smw_jump.wav'])


        if haar == True:
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
    time.sleep(0.5)

    if haar == True:
        vid_writer.release()


#temp hardcode
if __name__ == '__main__':
    main("local", "name", 20)
