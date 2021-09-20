import enumm
import requests
import threading
import time
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
velocity_thread = threading.Thread(target=velocity,name='velocity')
velocity_thread.start()

while(True):
    print(enumm.altitude)
    time.sleep(1)