import sensor_to_target
import enumm
import time
import requests
import json
import baslangic
import threading
def sensors():
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
        response2 = requests.get("http://192.168.194.95/api/v1/velocity")
        data2 = response2.json()
        vx = data2["vx"]
        vy = data2["vy"]
        vz = data2["vz"]
        altitude = data2["altitude"]
        valid = data2["velocity_valid"]

        enumm.vx = vx
        enumm.vy = vy
        enumm.vz = vz
        enumm.altitude = altitude
        enumm.valid = valid
sensors_thread = threading.Thread(target=sensors,name='sensors')

def baslat():
    time.sleep(25)
    sensor_to_target.yaw_donme(0)
    print("yaw sifirlama tamam")
    #sensor_to_target.yuzeyden_ayril()
    print("target_yaw_yuzeyden_ayril tamam")
    baslangic.duvar_tespit()
    sensor_to_target.yuzeyden_ayril()
    baslangic.tarama()
    # sensor_to_target.time_forward(10,0)
    # print("starting forward tamam")
    # sensor_to_target.yuzeye_in()
    # print("yuzeye in tamam")
    # print("yaw_data : ",enumm.imu_yaw)
    # print("sonar tamam")
    # print("ai tamam")
    # target_yaw = sensor_to_target.target_yaw(angle_final,rotate2)
    # enumm.durum =1
    # print("target yaw:",target_yaw)
    # print("target_yaw tamam")
    # sensor_to_target.yuzeyden_ayril()
    # print("target_yaw_yuzeyden_ayril tamam")
    # sensor_to_target.yaw_donme(target_yaw)
    # print("yaw sifirlama tamam")
    # sensor_to_target.forward([0,0],[(0.1+abs(float(distance_1)-3.5)),.0],target_yaw)
    # print("ilk gidis tamam")
    # sensor_to_target.yuzeye_in()
    # print("yuzeye inis tamam")
    # import kapi_kamera
    # kapi_kamera.kapi_ortalama(0)
    # print("kapidan gecildi")
    # sensor_to_target.bitis()
    print("bitti")
baslat()