import numpy as np
import cv2
#import client
from PIL import ImageGrab
import math
import imutils
from numpy.lib.function_base import angle
#url = mobese.secili()
confidenceThreshold = 0.9
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

px_to_mt = 15/180

foto = cv2.imread("test.png")
foto = cv2.flip(foto, 0)
def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def calculate(foto):
    global az
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
    boxes2 = []
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
                x2 = int(centerX + (width/2))
                y2 = int(centerY + (height/2))
                #print("x",x)
                #print("y",y)
                #print("r",width)
                #print("centerx",centerX)
                #print("centery",centerY)
                #hubele = abs(width-x)/2
                #hebele = abs(height-y)/2
                #print("s ",hubele)
                boxes.append([x, y, int(width), int(height)])
                boxes2.append([x2, y2, int(width), int(height)])

                cv2.rectangle(frame, (x,y), (x + width, y + height), (0,255,0), 2)
                confidences.append(float(confidence))
                classIDs.append(classID)


    detectionNMS = cv2.dnn.NMSBoxes(boxes, confidences, confidenceThreshold, NMSThreshold)
    cv2.rectangle(frame,(318,147),(318+5,147+5),(0,0,255), 2)
    if(len(detectionNMS)>0):
        for i in detectionNMS.flatten():
            (x, y) = (boxes[i][0],boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            #color = [int(c) for c in COLORS[classIDs[i]]]
            #cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 2)
        if(len(detectionNMS)>0):
            print("hedef bulundu")
           # cv2.imshow('sonuc', frame)
            #cv2.waitKey(0)
            return True, boxes,boxes2
        else:
            return False, 0,0
rotate = 0

def u_olustur(boxes):
    length = len(boxes)
    px_tolerans = 15
    overlap = 0
    if(length>=3):
        for i in range(length):
            for j in range(length):
                x_fark = abs(boxes[i][0]-boxes[j][0])
                y_fark = abs(boxes[i][1]-boxes[j][1])
                if(x_fark+y_fark<px_tolerans):
                    overlap = 1
                    enis = i
        if(overlap ==0):
            del boxes[1]
        elif(overlap ==1):
            del boxes[enis]
    return boxes



def merkez_bul(boxes,boxes2):
    length = len(boxes)
    try:
        px_tolerans = 10
        x_average = (int(boxes[0][0])+int(boxes[1][0])+int(boxes[2][0]))/3
        y_average = (int(boxes[0][1])+int(boxes[1][1])+int(boxes[2][1]))/3
        x_std = np.std([int(boxes[0][0]),int(boxes[1][0]),int(boxes[2][0])])
        y_std = np.std([int(boxes[0][1]),int(boxes[1][1]),int(boxes[2][1])])

        x_average2 = (int(boxes2[0][0])+int(boxes2[1][0])+int(boxes2[2][0]))/3
        y_average2 = (int(boxes2[0][1])+int(boxes2[1][1])+int(boxes2[2][1]))/3
        x_std2 = np.std([int(boxes2[0][0]),int(boxes2[1][0]),int(boxes2[2][0])])
        y_std2 = np.std([int(boxes2[0][1]),int(boxes2[1][1]),int(boxes2[2][1])])


        if(x_std<px_tolerans):
            width_list = [boxes[0][2],boxes[1][2],boxes[2][2]]
            width_min = min(width_list)
            width_min_index = width_list.index(width_min)


            height_min = min(boxes[0][3],boxes[1][3],boxes[2][3])

            y_sifir = (boxes[0][1]+boxes[1][1]+boxes[2][1]-boxes[width_min_index][1])/2+height_min/2
            x_sifir = x_average+width_min/2
            print(0)
        elif(y_std< px_tolerans):
            height_list = [boxes[0][3],boxes[1][3],boxes[2][3]]
            height_min = min(height_list)
            height_min_index = height_list.index(height_min)
            width_min = min(boxes[0][2],boxes[1][2],boxes[2][2])
            x_sifir = (boxes[0][0]+boxes[1][0]+boxes[2][0]-boxes[height_min_index][0])/2+width_min/2
            y_sifir = y_average+height_min/2
            print(1)
        elif(x_std2< px_tolerans):
            width_list = [boxes2[0][2],boxes2[1][2],boxes2[2][2]]
            width_min = min(width_list)
            width_min_index = width_list.index(width_min)
            height_min = min(boxes2[0][3],boxes2[1][3],boxes2[2][3])
            y_sifir = (boxes2[0][1]+boxes2[1][1]+boxes2[2][1]-boxes2[width_min_index][1])/2-height_min/2
            x_sifir = x_average2-width_min/2
            print(2)
        elif(y_std2< px_tolerans):
            height_list = [boxes2[0][3],boxes2[1][3],boxes2[2][3]]
            height_min = min(height_list)
            height_min_index = height_list.index(height_min)
            width_min = min(boxes2[0][2],boxes2[1][2],boxes2[2][2])
            x_sifir = (boxes2[0][0]+boxes2[1][0]+boxes2[2][0]-boxes2[height_min_index][0])/2-width_min/2
            y_sifir = y_average2-height_min/2
            print(3)
        print(x_sifir,y_sifir)
    except Exception as e:
        print(e)

def ai_baslat():
    rotate2 = 0
    for i in range(0,360):
        rotate2 +=1
        try:
            data_2,boxes_2,boxes_2_2 = calculate(rotate_image(foto,i))
        except Exception as e:
            print(e,"Denenen Rotasyon :",i)
            data_2 = False

        if(data_2 == True):
            print("Robotun dönmesi gereken derece: ",rotate2,"Konum Dataları: ",str(boxes_2[0][0]+boxes_2[0][2]/2),",",str(boxes_2[0][1]+boxes_2[0][3]/2))
            distance_1 = math.sqrt(((boxes_2[0][0]+boxes_2[0][2]/2)-320)**2+((boxes_2[0][1]+boxes_2[0][3]/2)-240)**2)*px_to_mt
            angle_final = np.arctan2((240-(boxes_2[0][1]+boxes_2[0][3]/2)),((boxes_2[0][0]+boxes_2[0][2]/2)-320))
            angle_final = angle_final*180/np.pi
            print("distance: ",distance_1)
            print("angle_final: ", angle_final)
            total_angle = rotate2-angle_final
            if(total_angle<180):
                total_angle = total_angle
            elif(total_angle>180):
                total_angle = 360-total_angle
            return angle_final,rotate2,distance_1
            #hedef_konum_x = 320+(boxes_2[0][0]+boxes_2[0][2]/2-320)*np.cos(int(rotate_fark))
            #hedef_konum_y = 240+(boxes_2[0][1]+boxes_2[0][3]/2-240)*np.cos(int(rotate_fark))
            #print(hedef_konum_y,hedef_konum_x)
            break
    #video_capture.release()
    #cv2.destroyAllWindows()
#ai_baslat()