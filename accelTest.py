from mpu6050 import mpu6050
import time

mpu = mpu6050(0x68)

staringTime = time.time_ns()
angle = 0

while True:

    accel = mpu.get_accel_data()
    #endTime = time.time_ns()
    
    #angle += ((endTime - staringTime) * 0.000000001) * gyro_data['z']

    #staringTime = endTime

    #if angle > 360:
     # angle = 0
    #if angle < 0:
    #  angle = 360 - angle

    print("accel X : "+str(accel['x']))
    print("accel Y : "+str(accel['y']))
    print("accel Z : "+str(accel['z']))
    print()
    #print(angle)
    #print()
    print("-------------------------------")

    time.sleep(0.01)