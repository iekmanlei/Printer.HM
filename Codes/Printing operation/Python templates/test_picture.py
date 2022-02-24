'''
Program template for printing operations with picture as the geometry input.

Inputs of the printing parameters are defined in lines 155 - 166.
'''


# Import modules
import os
import sys
import serial 
import time
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

# Import my modules
import transform_rot as transform
import gcodemod_inkscape as gcodemod

# Import dispensing arduino
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

# Function
def my_range(start, end, step):
    while start >= end:
        yield start
        start = start-step
        
def return_():
    a = swift.get_position(wait=True, timeout=None, callback=None)
    swift.set_position(x=a[0], y=a[1], z=10, speed=3000, wait=True)
    swift.set_position(x=150, y=0, z=10, wait=True)
    swift.set_position(x=105, wait=True)
    swift.set_position(z=20, wait=True)
    swift.set_position(x=115, wait=True)
    swift.set_position(x=105, wait=True)
    sys.exit()
     
def extrusion(printhead):
    if printhead == 3:
        o =  ArduinoSerial.write(b'3')
    if printhead == 2:
        o =  ArduinoSerial.write(b'2')
    if printhead == 1:
        o =  ArduinoSerial.write(b'1')
    return o

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
     
def calibration(Z0, a_gcode, b_gcode, r_stage):
    x_cal = [0]
    y_cal = [0]
    xyarm_cal = transform.coordinateTransfer(x_cal, y_cal, a_gcode, b_gcode, r_stage).T  
    z_check = False
    while z_check == False: 
        swift.flush_cmd(wait_stop=True)
        swift.set_position(xyarm_cal[0, 0], xyarm_cal[0, 1], 10, speed=3000, timeout=20)
        time.sleep(1)
        swift.set_position(xyarm_cal[0, 0], xyarm_cal[0, 1], Z0, wait=True)
        swift.flush_cmd(wait_stop=True)
        
        isPosition = input('Is the z-position correct? Please type any key to continue [Y/n/R (Return)]: ')
    
        if isPosition == 'R':
            return_()
        
        elif isPosition == 'n':
            shift_z = input('Enter the z shifting value: ')
            Z0 = float(Z0) + float(shift_z)
        
        else:
            z_check = True
            pass
        
        print('Calibrated z = ' + str(Z0)) 
        
        # Perform xy calibration 
        print('\nPerforming xy calibration')
        xy_check = False
        while xy_check == False: 
            print('Is the xy (central) position correct?')
            isPosition = input('Is the xy-position correct? Please type any key to continue [Y/n/R]: ')
            if isPosition == 'R':
                return_()
            elif isPosition == 'n':
                shift_a = input('Enter the x shifting value: ')
                shift_b = input('Enter the y shifting value: ')
                a_gcode = float(a_gcode) + float(shift_a)
                b_gcode = float(b_gcode) + float(shift_b)
                xy_check = False
                xyarm_cal = transform.coordinateTransfer(x_cal, y_cal, a_gcode, b_gcode, r_stage).T  
                swift.flush_cmd(wait_stop=True)
                swift.set_position(xyarm_cal[0, 0], xyarm_cal[0, 1], 10, speed=3000, timeout=20)
                time.sleep(1)
                swift.set_position(xyarm_cal[0, 0], xyarm_cal[0, 1], Z0, wait=True)
                swift.flush_cmd(wait_stop=True)
            
            else: 
                xy_check = True
                pass      
    print('x, y = ' + str(a_gcode) + ',' + str(b_gcode)) 
    return a_gcode, b_gcode

# User-defined parameters
spp =  10 # Printing speed
spnp = 2000  # Speed at non-printing paths
Z0 = 67.5 # Starting z position
delaytime = 30000 # Delaytime in μs between steps of the stepper motor
printhead = 3 # Assigned number of the printhead in use, 1 - 4 (4 printheads)
stage = 1 # Petri dish '1': 35 mm, '2': 55 mm, '3': 90 mm, '4': 35 mm heating stage
          # Rectangular container '5': 33 mm, '6': 40 mm
          # '7': Standard glass slide
offset = [0, 0, Z0] # Setting as [0,0,Z0] means printing at the central point (a_gcode,b_gcde) of the stage at Z0
convert_to_arduino(delaytime)
inkscape_file = r"C:\Users\49250\Documents\uArm-Python-SDK-2.0\code\Butterfly2_0001.txt"

bigCoor = gcodemod.read(inkscape_file, offset) # Import gcode
x_gcode = bigCoor[:, 0] # Import x coord from gcode file
y_gcode = bigCoor[:, 1] # Import y coord from gcode file
z_gcode = bigCoor[:, 2] # Import z coord from gcode file
e_gcode = bigCoor[:, 3]  # Import extrusion information from gcode file 


ab = [[282.5,146.5], [282,72.5], [285,-1], [280,-74]] #Approx. positions of printheads 1,2,3,4
stage_mega_r = [33, 44.5, 60, 36, 33, 38.2, 29.8]
a_gcode = ab[printhead - 1][0] # x coord of the printhead from uArm base, mm 
b_gcode = ab[printhead - 1][1] # y coord of the printhead from uArm base, mm
r_stage = stage_mega_r[stage - 1]

a_gcode, b_coord = calibration(Z0, a_gcode, b_gcode, r_stage) # Calibration
# Transfrom printing coordinates to uArm coordinates, same ref point.
xyarm_gcode = transform.coordinateTransfer(x_gcode, y_gcode, a_gcode, b_gcode, r_stage).T
zarm_gcode = np.copy(z_gcode)  # z position, do no transform z coordinates

print('Picture coordinates: ')
for i in range(xyarm_gcode.shape[0]):
    print(np.append(xyarm_gcode[i], zarm_gcode[i]))
print('')

# Print to std out for checking coordinates!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

# Start here-------
print('\nMove to the first position')
swift.flush_cmd(wait_stop=True)
swift.set_position(xyarm_gcode[0, 0], xyarm_gcode[0, 1], 10, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(xyarm_gcode[0, 0], xyarm_gcode[0, 1], zarm_gcode[0], wait=True)


# Print to std out for checking Z0!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    return_()
    
print('\nStart printing')
swift.set_buzzer(frequency=3000, duration=0.1)

extrusion(printhead)
time.sleep(1)

for n, etem in enumerate(e_gcode):
        # pause for every n layer
    if etem == 1: # printing
         extrusion(printhead) # Turn on printhead
         swift.set_position(xyarm_gcode[n, 0], xyarm_gcode[n, 1], zarm_gcode[n],
                speed=spp, wait=True)
    elif etem == 0: # stop printing
        ArduinoSerial.write(b'5') # Turn off printheads
        #swift.set_position(z=63,speed=spnp, wait=True)
        swift.set_position(xyarm_gcode[n, 0], xyarm_gcode[n, 1], zarm_gcode[n],
                speed=spnp, wait=True)
    swift.flush_cmd()
    print(xyarm_gcode[n, 0],xyarm_gcode[n, 1],zarm_gcode[n])

    
ArduinoSerial.write(b'5') # Turn off all printheads at the end
swift.set_buzzer(frequency=3000, duration=0.1)
print('\nPrinting finished')  

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
print('Printing done!')