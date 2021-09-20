import numpy as np
import cv2
import datetime
import enumm
import imutils
import time


def detection():
    print(2)
    confidenceThreshold = 0.8
    NMSThreshold = 0.3
    modelConfiguration = 'yolov3_custom_train.cfg'
    modelWeights = 'daire_son.weights'
    labels = ['daire']

    np.random.seed(10)
    COLORS = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")
    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    outputLayer = net.getLayerNames()
    outputLayer = [outputLayer[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    video_capture = cv2.VideoCapture(0)
    (W, H) = (None, None)
    while True:
        tic = time.time()
        if(True):
            ret, frame = video_capture.read()
            enumm.frame_available = ret
            print("frame available :",enumm.frame_available)
            frame = imutils.resize(frame,640,360)
            if W is None or H is None:
                (H,W) = frame.shape[:2]

            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (288, 288), swapRB = True, crop = False)
            net.setInput(blob)
            layersOutputs = net.forward(outputLayer)

            boxes = []
            confidences = []
            classIDs = []
            centerX = 0
            for output in layersOutputs:
                for detection in output:
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]
                    if confidence > confidenceThreshold:
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY,  width, height) = box.astype('int')
                        x = int(centerX - (width/2))
                        y = int(centerY - (height/2))
                        enumm.daire_x = centerX
                        enumm.daire_y = centerY
                        enumm.daire_w = width
                        enumm.daire_h = height
                        enumm.daire_tespit = True
                        enumm.tarama_durum = False
                        #enumm.kapi_detect = 1
                        print("Merkez X:",centerX,"Merkez Y:",centerY)
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
            if(centerX>0):
                enumm.daire_tespit = True
            else:
                enumm.daire_tespit = False
                

            detectionNMS = cv2.dnn.NMSBoxes(boxes, confidences, confidenceThreshold, NMSThreshold)
            #if(len(detectionNMS) > 0):
                #for i in detectionNMS.flatten():


                    #color = [int(c) for c in COLORS[classIDs[i]]]
                    #cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    #text = '{}: {:.4f}'.format(labels[classIDs[i]], confidences[i])
                    #cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)



            #cv2.imshow('sonuc', frame)
            #if(cv2.waitKey(1) & 0xFF == ord('q')):
            #    break
        else:
            video_capture.release()
            cv2.destroyAllWindows()
            break
        toc = tic - time.time()
        print("time:",toc)


detection()
