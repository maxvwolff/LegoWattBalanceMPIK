import matplotlib.pyplot as plt

from mcculw import ul
from mcculw.enums import ULRange
from mcculw.ul import ULError

import sys
sys.path.insert(0, 'LucidIO')

from LucidControlAO4 import LucidControlAO4
from Values import ValueVOS4
import IoReturn

import numpy as np

import time, math

from hardware import Hardware




def calibrate():
    # Fotodiode intensity calibration
    print("Give calibration values in m: ")
    L = float(input("L: "))
    l = float(input("l: "))

    print("Next, specify as many calibration points as you want! Begin with the levelled position (d = 0.0m)!")
    print("----- Stop with input 'q' -----")

    d_list = []
    a_list = []
    intensity_list = []

    while True:
        d = input("Move balance to specified position. d = ")
        if d == "q":
            break
        d = float(d)
        d_list.append(d)
        a = l * d / L
        a_list.append(a)
        intensity_list.append(hw.readChannel(3))

    slope, yoffset = np.polyfit(a_list, intensity_list, 1)

    print("##### RESULTS #####")       
    print("d values: " + str(d_list))
    print("a values: " + str(a_list))
    print("intensity values: " + str(intensity_list))
    print("slope: " + str(slope))
    print("y-offset: " + str(yoffset))

    plt.scatter(a_list, intensity_list, s=8)

    axes = plt.gca()
    plt.title('Fotodiode intensity calibration')
    plt.xlabel('a [m]')
    plt.ylabel('Fotodiode voltage [V]')
    x_vals = np.array(axes.get_xlim())
    y_vals = yoffset + slope * x_vals
    plt.plot(x_vals, y_vals, color='#f29f04', ls='--')
        
    plt.show()


def getNeededCurrent(p_gain, i_gain, d_gain, setpoint, duration):
    # PID control to level the balance to a satisfiable uncertainty
    t_start = time.time()
    t = 0

    last_error = 0
    i_correction = 0

    current_list = []

    while t < duration:
        t = time.time() - t_start
        error = setpoint - (hw.readFotodiode() - foto_yoffset) / foto_slope
        p_correction = p_gain * error
        i_correction += i_gain * error * dt
        d_correction = d_gain * (error - last_error) / dt

        total_correction = p_correction + i_correction + d_correction

        if total_correction > 12.0:
            total_correction = 12.0
        elif total_correction < -12.0:
            total_correction = -12.0
        
        hw.setOutput(total_correction)
        current_list.append(hw.readShuntVoltage() / 198)

        #print("error: " + str(error) + "  output: " + str(total_correction))
        last_error = error
        
        while time.time() - t_start < t + dt:
            pass

    # Measure current through coil
    I_mean = 0
    current_list_len = len(current_list)
    
    for i in range(current_list_len - 101, current_list_len):
        I_mean += hw.readShuntVoltage() / 198 # 198 Ohms shunt resistor
        
    I = I_mean / 100

    print("PID control finished. I = " + str(I) + " A  Error = " + str(last_error))

    plt.plot(current_list)
    plt.show()
    
    return I


def getNeededCurrentFast(p_gain, i_gain, d_gain):
    # PID control to level the balance to a satisfiable uncertainty
    t_start = time.time()
    t = 0

    last_error = 0
    i_correction = 0

    current_list = []

    meas_step = 1
    I1, I2, I3, I4, I5 = 0, 0, 0, 0, 0

    while True:
        t = time.time() - t_start
        
        if t >= 20 * meas_step:
            if meas_step == 1:
                print("Put the Tare MASS on the left side")
            elif meas_step == 2:
                I1 = sum(current_list[-100:]) / 100
                print("Put the TEST MASS on the right side")
            elif meas_step == 3:
                I2 = sum(current_list[-100:]) / 100
                print("Remove the TEST MASS on the right side")
            elif meas_step == 4:
                I3 = sum(current_list[-100:]) / 100
                print("Put the TEST MASS on the left right side")
            elif meas_step == 5:
                I4 = sum(current_list[-100:]) / 100
                print("Remove the TEST MASS on the right side")
            elif meas_step == 6:
                I5 = sum(current_list[-100:]) / 100
                print("Remove the TARE MASS on the left side")
            else:
                break

            meas_step += 1
        
        error = setpoint - (hw.readFotodiode() - foto_yoffset) / foto_slope
        p_correction = p_gain * error
        i_correction += i_gain * error * dt
        d_correction = d_gain * (error - last_error) / dt

        total_correction = p_correction + i_correction + d_correction

        if total_correction > 12.0:
            total_correction = 12.0
        elif total_correction < -12.0:
            total_correction = -12.0
        
        hw.setOutput(total_correction)
        current_list.append(hw.readShuntVoltage() / 198)

        last_error = error
        
        while time.time() - t_start < t + dt:
            pass

    I_total = - (I1 + I3 + I5) / 3 + (I2 + I4) / 2 

    print("PID control finished. I = " + str(I_total) + " A  Error = " + str(last_error))
    print("Currents [A]: ", I1, I2, I3, I4, I5)

    plt.plot(current_list)
    plt.show()
    
    return I_total






# Parameters
# Velocity Mode
max_coil_pos = 0.001 # 5mm
T = 1.5 # Period of the sin. actuation voltage in s
runningTime = 20 # Velocity Mode measuring time in s
dt = 0.001
p_gain_vel = 900
i_gain_vel = 700
d_gain_vel = 10


hw = Hardware()
hw.switchRelay(False)

#calibrate()

##### Calibration
hw.setOutput(0)
input("Move the balance in a levelled position and press enter!")
setpoint = hw.readFotodiode() # level position



##### Velocity Mode
t = 0
t_start = time.time()
# Fotodiode calibration values
foto_slope = 3.2721
foto_yoffset = -0.0174

t_list = []
t_start = time.time()
t = 0

last_error = 0
i_correction = 0
mean_intensity = 0

setpoint_list = []
coil_pos_list = []
induction_voltages = []
velocities = []

dt = 0.04

while t < runningTime:
    t = time.time() - t_start

    raw_intensity = hw.readFotodiode()
    coil_pos = (raw_intensity - foto_yoffset) / foto_slope # coil-position in m
    setpoint = max_coil_pos * math.sin(2*math.pi / T * t)
    error = setpoint - coil_pos
    p_correction = p_gain_vel * error
    i_correction += i_gain_vel * error * dt
    d_correction = d_gain_vel * (error - last_error) / dt

    total_correction = p_correction + i_correction + d_correction

    if total_correction > 12.0:
        total_correction = 12.0
    elif total_correction < -12.0:
        total_correction = -12.0
    
    hw.setOutput(total_correction)

    #t_list.append(t)
    setpoint_list.append(setpoint)
    coil_pos_list.append(coil_pos)
    induction_voltages.append(hw.readInductionVoltage())
    velocities.append(max_coil_pos * math.cos(2*math.pi / T * t - 0.63) * 2 * math.pi / T)
    mean_intensity += raw_intensity
    
    while time.time() - t_start < t + dt:
        pass

    #print("dt: " + str(time.time() - t_start - t))

axes = plt.gca()
plt.title('Velocity Mode PID control')
plt.xlabel('Time [s]')
plt.ylabel('Coil position [mm]')
plt.plot(setpoint_list)
plt.plot(coil_pos_list)
#plt.plot(induction_voltages)
#plt.plot(velocities)

plt.show()

hw.setOutput(0)





mean_intensity /= len(velocities)


# Fit to linear function -> slope will be BL
BL, offset = np.polyfit(velocities, induction_voltages, 1)

print("VELOCITY MODE FINISHED:  BL = " + str(BL) + " Offset = " + str(offset))


plt.scatter(velocities, induction_voltages, s=8)
axes = plt.gca()
plt.title('Velocity Mode BL-factor determination')
plt.xlabel('Velocity [m/s]')
plt.ylabel('Induction voltage [V]')
x_vals = np.array(axes.get_xlim())
y_vals = offset + BL * x_vals
plt.plot(x_vals, y_vals, color='#f29f04', ls='--')

    
plt.show()



hw.switchRelay(True)


##### Force Mode
g = 9.8326
p_gain = 1600
i_gain = 15000
d_gain = 35

dt = 0.01 #s

I_total = getNeededCurrentFast(p_gain, i_gain, d_gain)

I_total *= -1

mass = BL * I_total / g

print("FORCE MODE FINISHED:  m = " + str(mass) + " kg   I = " + str(I_total) + " A")

hw.setOutput(0)
