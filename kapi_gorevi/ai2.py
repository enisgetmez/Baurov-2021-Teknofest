import numpy as np
import cv2
#import client
from PIL import ImageGrab
import imutils
#url = mobese.secili()
confidenceThreshold = 0.1
NMSThreshold = 0.3
modelConfiguration = 'yolov4-tiny.cfg'
modelWeights = 'kapi.weights'
labels = ['kapi']
np.random.seed(10)
COLORS = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
outputLayer = net.getLayerNames()
outputLayer = [outputLayer[i[0] - 1] for i in net.getUnconnectedOutLayers()]
#video_capture = cv2.VideoCapture(0)


#foto = cv2.imread("data18.png")
foto = 0
def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def calculate(foto):
    (W, H) = (None, None)
    #printscreen =  np.array(ImageGrab.grab(bbox=(0,0,1920,1080)))
    frame = foto
    #frame = cv2.cvtColor(printscreen,cv2.COLOR_BGR2RGB)
    #ret,frame = video_capture.read()
    if W is None or H is None:
        (H,W) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB = True, crop = False)
    net.setInput(blob)
    layersOutputs = net.forward(outputLayer)

    boxes = []
    confidences = []
    classIDs = []
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
                #print("x",x)
                #print("y",y)
                #print("r",width)
                #print("centerx",centerX)
                #print("centery",centerY)
                #hubele = abs(width-x)/2
                #hebele = abs(height-y)/2
                #print("s ",hubele)
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)


    detectionNMS = cv2.dnn.NMSBoxes(boxes, confidences, confidenceThreshold, NMSThreshold)
    if(len(detectionNMS)>0):
        for i in detectionNMS.flatten():
            (x, y) = (boxes[i][0],boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            #color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 2)
        if(len(detectionNMS)>0):
            cv2.imshow('sonuc', frame)
            cv2.waitKey(0)
            return True, boxes
        else:
            return False, 0
rotate = 0
"""
for i in range(0,360):
    rotate +=1
    try:
        data,boxes = calculate(rotate_image(foto,i))
    except:
        data = False

    if(data == True):
        print("Robotun dönmesi gereken derece: ",rotate,"Konum Dataları: ",str(boxes))
        break
"""
#video_capture.release()
cv2.destroyAllWindows()