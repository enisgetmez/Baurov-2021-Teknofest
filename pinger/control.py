from pymavlink import mavutil
import time
import threading
import random

master = mavutil.mavlink_connection('/dev/ttyACM0',baud=115200)
master.wait_heartbeat()
def hareket(x=0,y=0,z=500,r=0):
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        0)
    buttons = 1 << 6
    master.mav.manual_control_send(
        master.target_system,
        x,
        y,
        z,
        r, #yaw
        buttons)
