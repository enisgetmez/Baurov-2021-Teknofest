import requests
import time

from requests.api import head
import control
import enumm
import threading
import ai_cam
def imu_data():
    while(True):
        response = requests.get('http://192.168.194.95/api/v1/imu')
        data = response.json()
#       print(data)
        pitch = data["pitch"]
        roll = data["roll"]
        yaw = data["yaw"]
        enumm.imu_pitch = pitch
        enumm.imu_roll = roll
        enumm.imu_yaw = yaw
        #return roll,pitch,yaw
def velocity():
    while(True):
        response = requests.get("http://192.168.194.95/api/v1/velocity")
        data = response.json()
        vx = data["vx"]
        vy = data["vy"]
        vz = data["vz"]
        altitude = data["altitude"]
        valid = data["velocity_valid"]

        enumm.vx = vx
        enumm.vy = vy
        enumm.vz = vz
        enumm.altitude = altitude
        enumm.valid = valid
        #return vx,vy,vz, altitude,valid

def ai_calistir():
    print(1)
    ai_cam.detection()

imu_thread = threading.Thread(target=imu_data,name='imu_data')
velocity_thread = threading.Thread(target=velocity,name='velocity')
ai_thread = threading.Thread(target=ai_calistir,name='ai_calistir')
velocity_thread.start()
imu_thread.start()
ai_thread.start()
def kapi_ortalama(yaw_direction):
    x_orta = 640/2
    y_orta = 360/2
    tolerance = 20
    ortalama_count = 0
    durum = 1
    while(True):
        x,y,w,h,durum = enumm.kapi_x,enumm.kapi_y,enumm.kapi_w,enumm.kapi_h,enumm.kapi_detect
        yaw = enumm.imu_yaw
        print("kapi detect ", durum)
        if(durum == 1):
            print("width,height: ",w,h)
            delta_yaw = yaw-yaw_direction
            if delta_yaw>180:
                delta_yaw = delta_yaw-360
            print("delta_yaw",delta_yaw)
            if(x>x_orta):
                print("sag gidiyor")
                control.hareket(0,-600,500,int(400*(-delta_yaw/(abs(delta_yaw)+0.1))))
            elif(x<x_orta):
                print("sol gidiyor")
                control.hareket(0,600,500,int(400*(-delta_yaw/(abs(delta_yaw)+0.1))))
            if(abs(x-x_orta)<tolerance):
                ortalama_count +=1
                print("ortalama_count: ",ortalama_count)
            else:
                ortalama_count = 0
            if(ortalama_count >= 25):
                print("orta gidiyor")
                enumm.kapi_kontrol = 1
                enumm.last_yaw = enumm.imu_yaw
                #for i in range(15):
                #    control.hareket(0,0,0,0)
                break
            print(x,y)
        else:
            control.hareket(0,0,500,400)
            print("kapi araniyor")
            print("kamera durum: ",enumm.frame_available)
    for i in range(2500):
        delta_yaw = enumm.imu_yaw-enumm.last_yaw
        valid_altitude = enumm.valid
        if delta_yaw>180:
            delta_yaw = delta_yaw-360
        altitude = enumm.altitude
        print("altitude :",altitude," delta_yaw :",delta_yaw)
        print("delta_yaw",delta_yaw)
        if(valid_altitude):
            if(altitude>0.70):
                z_pwm = 850
            elif(altitude<0.60):
                z_pwm = 150
            else :
                z_pwm = 500
        else:
            z_pwm = 250
        control.hareket(400,0,z_pwm,int(250*(-delta_yaw/(abs(delta_yaw)+0.1))))
kapi_ortalama(0)