'''
Program template for dispensing operations.

Inputs of the printing parameters are defined in lines 88 - 92.
'''

# Import modules
import os
import sys
import serial 
import time
import numpy as np
import transform_rot as transform
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

# Import Arduino
ArduinoSerial = serial.Serial('COM3',2400) #COM3 is the port of syringe pump
time.sleep(2)

# Import uArm
swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
swift.waiting_ready(timeout=3)
device_info = swift.get_device_info()
print(device_info)
firmware_version = device_info['firmware_version']
if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
    swift.set_speed_factor(0.0005)
swift.set_mode(0)

# My function
def my_range(start, end, step):
    while start >= end:
        yield start
        start = start-step
  
def convert_to_arduino(number):
    while number > 30000 or number <= 0:
        number = int(input('input the delaytime you want to set, maximum 30000, the larger the delaytime is the slower the pump will be, dont set it too small!'))
    else:
        length = len(str(number))
    
    if length == 1: #send first charater to the Arduino, let it know how many numbers it needs to wait before convert numbers in buffer into delaytime)
        ArduinoSerial.write(b'1')
    if length == 2:
        ArduinoSerial.write(b'2')
    if length == 3:
        ArduinoSerial.write(b'3')
    if length == 4:
        ArduinoSerial.write(b'4')
    if length == 5:
        ArduinoSerial.write(b'5')
    
    for i in str(number):#send numbers in the delaytime individually
        print(i)
        if int(i) == 0:
            ArduinoSerial.write(b'0')
        if int(i) == 1:
            ArduinoSerial.write(b'1')
        if int(i) == 2:
            ArduinoSerial.write(b'2')
        if int(i) == 3:
            ArduinoSerial.write(b'3')
        if int(i) == 4:
            ArduinoSerial.wrie(b'4')
        if int(i) == 5:
            ArduinoSerial.write(b'5')
        if int(i) == 6:
            ArduinoSerial.write(b'6')
        if int(i) == 7:
            ArduinoSerial.write(b'7')
        if int(i) == 8:
            ArduinoSerial.write(b'8')
        if int(i) == 9:
            ArduinoSerial.write(b'9')  
    print('Delaytime sent to Arduino!')

def return_():
    a = swift.get_position(wait=True, timeout=None, callback=None)
    swift.set_position(x=a[0], y=a[1], z=10, speed=3000, wait=True)
    swift.set_position(x=150, y=0, z=10, wait=True)
    swift.set_position(x=105, wait=True)
    swift.set_position(z=20, wait=True)
    swift.set_position(x=115, wait=True)
    swift.set_position(x=105, wait=True)
    sys.exit()
    
# User-defined inputs    
# Setting size of the droplet area   
x_rect = [20,-20]
y_rect = [20,-20]
number = 10 # Number of points between the above defined coordinates

# Define the number of droplets in the area 
x_i = []
y_i = []
for x in np.linspace(x_rect[0], x_rect[1], number):
    for y in np.linspace(y_rect[0], y_rect[1], number):
        x_i.append(x)
        y_i.append(y)
        
# Define printing parameters        
spp = 6000 # Dispensing speed of the stage
Z0 = 67.5 # Starting z position
delaytime = 30000 # Delaytime in μs between steps of the stepper motor, 
                  # controlling the extrusion rate
printhead = 3 # Assigned number of the printhead in use, 1 - 4 (4 printheads)
stage = 1 # Assigned number of the stage
          # Petri dish '1': 35 mm, '2': 55 mm, '3': 90 mm, '4': 35 mm heating stage
          # Rectangular container '5': 33 mm, '6': 40 mm
          # '7': Standard glass slide
offset = [0, 0, Z0] # Setting as [0,0,Z0] means printing at the central point (a_gcode,b_gcde) of the stage at Z0

# Operation    
convert_to_arduino(delaytime) # Send delaytime to Arduino
ab = [[282.5,146.5], [282,72.5], [285,-1], [280,-74]] #Approx. positions of printheads 1,2,3,4
stage_mega_r = [33, 44.5, 60, 36, 33, 38.2, 29.8]
a_coord = ab[printhead-1][0] # x coord of the printhead from uArm base, mm 
b_coord= ab[printhead-1][1] # y coord of the printhead from uArm base, mm
r_stage = stage_mega_r[stage-1]

xyarm_coord = transform.coordinateTransfer(x_i, y_i, a_coord, b_coord, r_stage).T     
print('Circle coordinates: ')
for i in range(xyarm_coord.shape[0]):
    print(xyarm_coord[i])
print('')

# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

# Printing parameters
z = 65.5 # Starting z position
spp = 200 # printing speed

# Start here-------
print('\nMove to the first  position')
swift.flush_cmd(wait_stop=True)
swift.set_position(xyarm_coord[0, 0], xyarm_coord[0, 1], 10, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(xyarm_coord[0, 0], xyarm_coord[0, 1], z, wait=True)


# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    return_()

    
print('\nStart dispensing')
swift.set_buzzer(frequency=3000, duration=0.1)
#time.sleep(2)
for n, (x, y) in enumerate(xyarm_coord):
    if n > 0 :
        swift.set_position(x, y, z-20, speed=spp, wait=True)
        swift.set_position(x, y, z, speed=spp, wait=True)
    
    ArduinoSerial.write(b'3')
    time.sleep(1)
    ArduinoSerial.write(b'5')
    swift.set_position(x, y, z-20, speed=spp, wait=True)
    swift.flush_cmd(wait_stop=True)  
    
ArduinoSerial.write(b'5') # Turn off printheads       
swift.set_buzzer(frequency=3000, duration=0.1)
print('\nDispensing finished')  

print('\nLowering nozzle to z = 10')
swift.set_position(z=10, speed=3000, wait=True)
print('......')

# Always return to the initial position!!! 
print('\nReturn to starting position.(around X95 Y0 Z20)')
swift.set_position(x=200, y=0, z=10, wait=True)
swift.flush_cmd()
swift.set_position(x=150, y=0, z=10, wait=True)
swift.flush_cmd()
swift.set_position(x=130, y=0, z=10, wait=True)
swift.set_position(z=20, wait=True)
swift.set_position(x=115, wait=True)
swift.set_position(x=105, wait=True)
swift.flush_cmd()
swift.flush_cmd()
swift.set_buzzer(frequency=1000, duration=0.1)
time.sleep(2)

ArduinoSerial.close()
print('Dispensing done!')