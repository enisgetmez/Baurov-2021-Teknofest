import sonar
import sensor_to_target
import enumm
import time
import requests
import json
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
        return roll,pitch,yaw

def baslat():
    time.sleep(20)
    sensor_to_target.yuzeyden_ayril()
    print("target_yaw_yuzeyden_ayril tamam")
    sensor_to_target.yaw_donme(0)
    print("yaw sifirlama tamam")
    sensor_to_target.time_forward(10,0)
    print("starting forward tamam")
    sensor_to_target.yuzeye_in()
    print("yuzeye in tamam")
    imu_data()
    print("yaw_data : ",enumm.imu_yaw)
    sonar.tarama_360()
    print("sonar tamam")
    import ai
    import ai2
    try:
        angle_final,rotate2,distance_1 = ai.ai_baslat()

    except:
        pass
    del ai
    del ai2
    print("ai tamam")
    target_yaw = sensor_to_target.target_yaw(angle_final,rotate2)
    enumm.durum =1
    print("target yaw:",target_yaw)
    print("target_yaw tamam")
    sensor_to_target.yuzeyden_ayril()
    print("target_yaw_yuzeyden_ayril tamam")
    sensor_to_target.yaw_donme(target_yaw)
    print("yaw sifirlama tamam")
    sensor_to_target.forward([0,0],[(0.1+abs(float(distance_1)-3.5)),.0],target_yaw)
    print("ilk gidis tamam")
    sensor_to_target.yuzeye_in()
    print("yuzeye inis tamam")
    import kapi_kamera
    kapi_kamera.kapi_ortalama(0)
    print("kapidan gecildi")
    sensor_to_target.bitis()
    print("bitti")
baslat()