import requests
import time

from requests.api import head
import control
import enumm
import threading

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
imu_thread = threading.Thread(target=imu_data,name='imu_data')
velocity_thread = threading.Thread(target=velocity,name='velocity')

imu_thread.start()
velocity_thread.start()

def zamanlayici_calistir(saniye):
	enumm.zaman_kontrolcusu=0
	time.sleep(int(saniye))
	enumm.zaman_kontrolcusu=1


def zaman_git(saniye,target):
	zamanlayici_calistir(saniye)
	while(enumm.zaman_kontrolcusu ==0):
		roll,pitch,yaw = enumm.imu_roll,enumm.imu_pitch,enumm.imu_yaw
		vx,vy,vz,altitude,valid = enumm.vx,enumm.vy,enumm.vz,enumm.altitude,enumm.valid
		delta_yaw = yaw-target
		if(altitude>0.75):
			z_pwm = 850
		elif(altitude<0.55):
			z_pwm = 150
		else :
			z_pwm = 500
		if yaw>180:
			yaw = yaw-360
		elif(int(yaw) ==0):
			yaw = 1
		control.hareket(500,0,int(z_pwm),int(300*(-delta_yaw/abs(delta_yaw))))

def yaw_donme(target):
	yaw_sifir_count = 0
	while(True):
		yaw = enumm.imu_yaw
		delta_yaw = yaw-target
		if delta_yaw>180:
			delta_yaw = delta_yaw-360
		control.hareket(0,0,500,int(300*(-delta_yaw/(0.01+abs(delta_yaw)))))
		if delta_yaw>180:
			delta_yaw = delta_yaw-360
		print(delta_yaw)
		time.sleep(0.1)
		if(delta_yaw<5 and delta_yaw>-5):
			yaw_sifir_count=yaw_sifir_count+1
		else:
			yaw_sifir_count=0
		if(yaw_sifir_count==3):
			break

def yuzeyden_ayril():
	enumm.target_yaw = enumm.imu_yaw
	for i in range(40):
		control.hareket(0,0,0,0)
		time.sleep(0.1)
def yuzeye_in():
	enumm.target_yaw = enumm.imu_yaw
	for i in range(35):
		control.hareket(0,0,1000,0)
		time.sleep(0.1)


def yaw_sifirlama(target_yaw):
	roll,pitch,yaw = enumm.imu_roll,enumm.imu_pitch,enumm.imu_yaw
	vx,vy,vz,altitude,valid = enumm.vx,enumm.vy,enumm.vz,enumm.altitude,enumm.valid
	#altitude = control.get_vfr_data()
	yaw_sifir_count = 0
	if yaw>180:
		yaw = yaw-360
	while(True):
		vx,vy,vz,altitude,valid = enumm.vx,enumm.vy,enumm.vz,enumm.altitude,enumm.valid
		#altitude = control.get_vfr_data()
		if(altitude>0.75):
			z_pwm = 750
		elif(altitude<0.55):
			z_pwm = 250
		else :
			z_pwm = 500		
		control.hareket(0,0,500,int(300*(-(yaw-target_yaw)/abs(yaw-target_yaw))))
		roll,pitch,yaw = enumm.imu_roll,enumm.imu_pitch,enumm.imu_yaw
		if yaw>180:
			yaw = yaw-360
		print(yaw,altitude,valid)
		time.sleep(0.1)
		if(yaw<5 and yaw>-5):
			yaw_sifir_count=yaw_sifir_count+1
		else:
			yaw_sifir_count=0
		if(yaw_sifir_count==3):
			break

	print("yaw sifirlandi")
def time_forward(zaman,yaw_direction):
	vx,vy,vz,altitude,valid = enumm.vx,enumm.vy,enumm.vz,enumm.altitude,enumm.valid
	#altitude = control.get_vfr_data()
	roll,pitch,yaw = enumm.imu_roll,enumm.imu_pitch,enumm.imu_yaw
	if yaw>180:
		yaw = yaw-360
	elif(int(yaw) ==0):
		yaw = 1
	
	tic = time.time()
	toc = 0
	while(toc < zaman):	
	
		if(altitude>0.75):
			z_pwm = 850
		elif(altitude<0.55):
			z_pwm = 150
		else :
			z_pwm = 500

		delta_yaw = yaw-yaw_direction
		if delta_yaw>180:
			delta_yaw = delta_yaw-360

		control.hareket(400,0,500,int(300*(-delta_yaw/(abs(delta_yaw)+0.01))))

		roll,pitch,yaw = enumm.imu_roll,enumm.imu_pitch,enumm.imu_yaw
		if yaw>180:
			yaw = yaw-360
		elif(int(yaw) ==0):
			yaw = 1


		toc =time.time()-tic


def forward(start,end,yaw_direction):
	vx,vy,vz,altitude,valid = enumm.vx,enumm.vy,enumm.vz,enumm.altitude,enumm.valid
	#altitude = control.get_vfr_data()
	roll,pitch,yaw = enumm.imu_roll,enumm.imu_pitch,enumm.imu_yaw
	if yaw>180:
		yaw = yaw-360
	elif(int(yaw) ==0):
		yaw = 1
	time_step = 1/50
	location = start
	tolerance = 0.1
	max_distance = 25
	temp_vx = 0
	tic = time.time()
	while(abs(int(location[0]*10)-int(end[0]*10))):
		
		x_distance = end[0]-location[0]
		x_pwm = 1000*(1-(max_distance-x_distance)/max_distance)
		
		if(altitude>0.75):
			z_pwm = 850
		elif(altitude<0.55):
			z_pwm = 150
		else :
			z_pwm = 500
		
		
	
		delta_yaw = yaw-yaw_direction
		if delta_yaw>180:
			delta_yaw = delta_yaw-360

		control.hareket(500,0,500,int(300*(-delta_yaw/abs(delta_yaw))))

		#control.hareket(500,0,int(z_pwm),0) # ileri

		#control.hareket(500,0,int(z_pwm),0)
		
		
		#if(valid):

		vx,vy,vz,altitude,valid = enumm.vx,enumm.vy,enumm.vz,enumm.altitude,enumm.valid
		if(valid):
			temp_vx = vx
		else:
			vx = temp_vx
		toc = time.time()-tic
		tic = time.time()
		#altitude = control.get_vfr_data()
		roll,pitch,yaw = enumm.imu_roll,enumm.imu_pitch,enumm.imu_yaw
		if yaw>180:
			yaw = yaw-360
		elif(int(yaw) ==0):
			yaw = 1
		#print("Yaw :",yaw,"Depth :",altitude,"Valid :",valid)
		
		time_step = toc
		location[0] = vx*time_step+location[0]
		print("x distance traveled :", location[0], "Velocity : ", vx,"valid:",enumm.valid)
	
	for i in range(5):
		control.hareket(0,0,500,0)
		time.sleep(0.1)
		#time.sleep(time_step)

def lateral(start,end):
	vx,vy,vz,altitude,valid = enumm.vx,enumm.vy,enumm.vz,enumm.altitude,enumm.valid
	#altitude = control.get_vfr_data()
	roll,pitch,yaw = enumm.imu_roll,enumm.imu_pitch,enumm.imu_yaw
	if yaw>180:
		yaw = yaw-360
	elif(yaw ==0):
		yaw = 1
	time_step = 1/50
	location = start
	tolerance = 0.1
	max_distance = 25
	tic = time.time()
	while(abs(int(location[1]*10)-int(end[1]*10))):
		
		y_distance = end[1]-location[1]
		y_pwm = 1000*(1-(max_distance-y_distance)/max_distance)
		
		if(altitude>0.75):
			z_pwm = 750
		elif(altitude<0.55):
			z_pwm = 250
		else :
			z_pwm = 500
		
		
		control.hareket(0,-500,int(z_pwm),int(250*(-yaw/abs(yaw)))) # ileri
		#control.hareket(500,0,int(z_pwm),0)
		
		
		#if(valid):

		vx,vy,vz,altitude,valid = enumm.vx,enumm.vy,enumm.vz,enumm.altitude,enumm.valid
		toc = time.time()-tic
		tic = time.time()
		#altitude = control.get_vfr_data()
		roll,pitch,yaw = enumm.imu_roll,enumm.imu_pitch,enumm.imu_yaw
		if yaw>180:
			yaw = yaw-360
		#print("Yaw :",yaw,"Depth :",altitude,"Valid :",valid)
		
		time_step = toc
		location[1] = vy*time_step+location[1]
		print("y distance traveled :", location[1], "Velocity : ", vy)
	control.hareket(0,0,500,0)

def target_yaw(angle_final,rotate2):
	if (angle_final <0):
	    angle_final = 360 + angle_final

	heading_final = angle_final-rotate2-180
	target_yaw = enumm.imu_yaw-heading_final
	print("imu yaw: ",enumm.imu_yaw,"heading_final: ", heading_final)

	if (target_yaw > 180):
	    target_yaw = target_yaw-360
	elif (target_yaw < -180):
	    target_yaw = target_yaw+360
	return target_yaw

def bitis():
	control.hareket(0,0,500,0)
	time.sleep(30)

#start = [0.1,0.2]
#end = [3,1.0]
#yaw_donme(20)
#yaw_sifirlama()
#euler_distance(start,end)
#forward(start,end)
#lateral(start,end)
#while(True):
#	print(enumm.imu_yaw)