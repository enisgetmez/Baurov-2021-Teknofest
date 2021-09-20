import control
import enumm
import time
import sensor_to_target
import ai_cam
import threading
def ai_calistir():
    print("ai baslatiliyor")
    while(True):
        if(enumm.durum ==1):
            ai_cam.detection()
ai_thread = threading.Thread(target=ai_calistir,name='ai_calistir')
ai_thread.start()
def duvar_tespit():
    tic = time.time()
    toc = 0
    distance = 0
    tic2 = time.time()
    temp_vy = 0
    while(toc < 10):
        altitude = enumm.altitude
        if(altitude > 0.75):
            z_pwm = 850
        elif(altitude < 0.55):
            z_pwm = 150
        elif(int(altitude) == -1):
            z_pwm = 500
        else:
            z_pwm = 500
        control.hareket(0, -500, z_pwm, 0)
        toc = time.time()-tic
        vx, vy, vz, altitude, valid = enumm.vx, enumm.vy, enumm.vz, enumm.altitude, enumm.valid
        if(valid):
            temp_vy = vy
        else:
            vy = temp_vy
        toc2 = time.time()-tic2
        tic2 = time.time()
        #altitude = control.get_vfr_data()
        roll, pitch, yaw = enumm.imu_roll, enumm.imu_pitch, enumm.imu_yaw
        if yaw > 180:
            yaw = yaw-360
        elif(int(yaw) == 0):
            yaw = 1
            #print("Yaw :",yaw,"Depth :",altitude,"Valid :",valid)

        time_step = toc2
        distance = vy*time_step+distance
        print(distance)
        if(distance < 0.5):
            enumm.duvar_konum = 1
            enumm.tarama_durum = True
        else:
            enumm.duvar_konum = 2
            enumm.tarama_durum = True
    sensor_to_target.time_forward(15,0)
    if(enumm.duvar_konum ==1):
        sensor_to_target.yaw_donme(-90)
        sensor_to_target.time_forward(10,-90)
    elif(enumm.duvar_konum ==2):
        sensor_to_target.yaw_donme(90)
        sensor_to_target.time_forward(18,90)

def hedef_git():
    while(True):
        vx, vy, vz, altitude, valid = enumm.vx, enumm.vy, enumm.vz, enumm.altitude, enumm.valid
        if(altitude > 0.75):
                z_pwm = 850
        elif(altitude < 0.65):
                z_pwm = 150
        elif(int(altitude) == -1):
                z_pwm = 500
        else:
                z_pwm = 500
        if(enumm.daire_tespit ==True):
            print("hedefe gidiliyor")
            control.hareket(300,0,z_pwm,0)
        else:
            for i in range(1000):
                print("alcaliyorum",i)
                control.hareket(300,0,700,0)
            break


def tarama():
    global ai_thread
    print("tarama basladi")
    enumm.durum = 1
    x_yon = 0
    y_yon = 0
    r_yon = 0
    duvar_konum = enumm.duvar_konum
    if(duvar_konum == 1):
        x_yon = -1
    else:
        x_yon = 1
    altitude = enumm.altitude
    x_orta = 640/2
    y_orta = 360/2
    tolerance = 20
    ortalama_count = 0
    durum = 1
    print("yaw donme basladi")
    sensor_to_target.yaw_donme(0)
    print("yaw donme bitti")
    while(True):
        roll, pitch, yaw = enumm.imu_roll, enumm.imu_pitch, enumm.imu_yaw
        vx, vy, vz, altitude, valid = enumm.vx, enumm.vy, enumm.vz, enumm.altitude, enumm.valid
        if(altitude > 0.95):
                z_pwm = 850
        elif(altitude < 0.85):
                z_pwm = 100
        elif(int(altitude) == -1):
                z_pwm = 100
        else:
                z_pwm = 500
        if(enumm.tarama_durum == True):
            if(enumm.zaman < 2000):
                control.hareket(0, 0, z_pwm, -300)
                enumm.zaman +=1
                print(enumm.zaman)
            else:
                print("tarama durum false")
                sensor_to_target.yaw_donme(0)
                sensor_to_target.time_forward(8,0)
        else:
            yaw = enumm.imu_yaw
            print("kapi detect ", durum)
            if(durum == 1):
                print("width,height: ",enumm.daire_w,enumm.daire_h)
                if(enumm.daire_x>x_orta):
                    print("sag gidiyor")
                    control.hareket(50,0,z_pwm,200)
                elif(enumm.daire_x<x_orta):
                    print("sol gidiyor")
                    control.hareket(50,0,z_pwm,-200)
                if(abs(enumm.daire_x-x_orta)<tolerance):
                    ortalama_count +=1
                    print("ortalama_count: ",ortalama_count)
                else:
                    ortalama_count = 0
                if(ortalama_count >= 15):
                    enumm.last_yaw = enumm.imu_yaw
                    print("tarama bitti")
                    hedef_git()
                    #for i in range(15):
                    #    control.hareket(0,0,0,0)
                    break
                