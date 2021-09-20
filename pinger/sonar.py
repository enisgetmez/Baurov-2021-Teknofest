from brping import Ping360
import numpy as np
import threading
import control
import enumm
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
myPing = Ping360()
myPing.connect_serial("/dev/ttyUSB0", 921600)

abcd = 0
def yuzeye_in():
	global abcd
	enumm.target_yaw = enumm.imu_yaw
	while(True):
		if(abcd==1):
			control.hareket(0,0,1000,0)
			if(enumm.durum ==1):
				abcd=0
				break
    
yuzeye_in_thread = threading.Thread(target=yuzeye_in,name='yuzeye_in')
if myPing.initialize() is False:
    print("Failed to initialize Ping!")
    exit(1)

arr_zeros = np.zeros((400,1199))
def aci_ayarla(aci):
    binary_list = []
    decimal_list = []
    myPing.transmitAngle(aci)
    data = myPing.get_device_data          #get_auto_device_data

    data = str(data).split("- _data(hex):")[1]
    liste = data.split("- _data(string):")[0]
    liste = liste.replace("[","").replace("]","").replace("'","").replace(" ","")
    liste = liste.split(",")

    del liste[-1]

    for i in range(len(liste)):
	    binary = str(bin(int(liste[i], 16))) 
	    binary_list.append(binary)

    if aci == 1:
		    for i in range(len(liste)):
			    temp=int(bytearray(binary_list[i], "utf8"),2)
			    arr_zeros[aci,i] = temp
    else:
        for i in range(len(liste)):
            temp=int(bytearray(binary_list[i], "utf8"),2) 
            arr_zeros[aci,i] = temp


def polardata(arr):
	theta, r = np.mgrid[0:2*np.pi:400j, 0:1:1199j]
	fig = plt.figure()
	ax = fig.add_subplot(111,polar = 'True')
	ax.pcolormesh(theta, r, arr,shading='auto') #X,Y & data2D must all be same dimensions
    
	#plt.imsave('test.png',fig)
	plt.savefig("test.png")
	#plt.show()
	
yuzeye_in_thread.start()

def tarama_360():
    global abcd
    abcd=1
    myPing.initialize()
    myPing.set_transmit_duration(80)
    myPing.set_sample_period(666)
    myPing.set_transmit_frequency(700)
    myPing.set_number_of_samples(1200)
    myPing.initialize()
    for j in range(0,400):
        aci_ayarla(j)
    #print(arr_zeros)
    polardata(arr_zeros)
    print("goruntu olusturuldu")
    abcd = 0

#print(str(myPing.readDeviceInformation()))

#tarama_360()
