# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 21:00:52 2017

@author: Ashley
"""

# getCSVTable
import parseCSV

#import csv
import matplotlib.pyplot as plt
import numpy as np
# File Dialog
import tkinter as tk
from tkinter import filedialog


#%%

def openFileDialog():
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    return filename


#%% Analysis Tools

def diff(value,time,maxRate=-1):
    diffValue = np.diff(value)
    diffTime = np.diff(time)
    diffRate = diffValue/diffTime
    # Cap rate outputs at maxRate to avoid outliers (low efficiency loop)
    for i, iRate in enumerate(diffRate):
        if maxRate != -1 and abs(iRate) > maxRate:
            diffRate[i] = 0
    return diffRate


#%% Visualization Routines

def plotJewelArm(dataTable):
    time = dataTable['time']
    jewelArm = dataTable['JEWEL_ARM']
    plt.clf()
    plt.title("Jewel Arm over time")
    plt.plot(time,jewelArm, '-', label='jewelArm')
    plt.xlabel('Time (s)')
    plt.ylabel('Jewel Arm Servo [0,1]')
    plt.legend()
    plt.show()

def plotXYPosition(dataTable):
    time = dataTable['time']
    x = dataTable['x_in']
    y = dataTable['y_in']
    theta = dataTable['theta_rad']
    plt.clf()
    plt.title("Mecanum Navigation Position")
    plt.plot(x,y, 'r--.', label='position')
    plt.xlabel('X inches')
    plt.ylabel('Y inches')
    plt.legend()
    plt.show()

def plotMotorTickRateVsPower(dataTable):
    time = dataTable['time']
    motorTicks = dataTable['DRIVE_FRONT_LEFT_ticks']
    motorTickRate = diff(motorTicks,time)
    motorPower = dataTable['DRIVE_FRONT_LEFT_power']
    plt.clf()
    plt.title("Motor Ticks vs Power")
    plt.plot(motorPower[0:-1], motorTickRate, 'b.', label='position')
    plt.xlabel('Power')
    plt.ylabel('Tick Rate')
    plt.legend()
    plt.show()
    
def plotMotorData(dataTable, motorName):
    time = dataTable['time']
    motorPower = dataTable[motorName + '_power']
    motorTicks = dataTable[motorName + '_ticks']
    
    fig, ax1 = plt.subplots()    
    plt.title(motorName + " MOTOR")
    ax1.plot(time, motorPower, 'r.', label='power')
    ax1.set_xlabel('time (s)')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('Motor Power', color='r')
    ax1.tick_params('y', colors='r')
    
    # Create twin axis
    ax2 = ax1.twinx()
    ax2.plot(time, motorTicks, 'b.', label='ticks')

    ax2.set_ylabel('Encoder Ticks', color='b')
    ax2.tick_params('y', colors='b')
    
    fig.tight_layout()
#    plt.legend()
    plt.show()
    

#%% Main routine, run if module is executed directly, rather than imported.

def main():
    dataTable = parseCSV.getDictionary('telemetry1_defectiveBackLeftEncoder.csv')
    plt.close("all")
    
    plt.figure()
    plotJewelArm(dataTable)
    plt.figure()
    plotXYPosition(dataTable)
#    plt.figure()
#    plotMotorTickRateVsPower(dataTable)
    
    # Display data for all motors
    driveMotors = ['DRIVE_FRONT_LEFT','DRIVE_FRONT_RIGHT',
                   'DRIVE_BACK_LEFT','DRIVE_BACK_RIGHT']
    for i,motor in enumerate(driveMotors):
        plotMotorData(dataTable,motor)


if __name__ == '__main__':
    main()

