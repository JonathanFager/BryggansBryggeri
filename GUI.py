# IMPORTS
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.widgets import Button
import serial
# import csv
import Tkinter

# arduinoSerial = serial.Serial('/dev/ttyACM1',9600) #CHECK!
t,T1, T2 = [0],[50],[50] #Initialise time and temp lists.
TempLow = -10
TempHigh = 110
minWidth = 60
measureOn = True

def updateAxis():	
	if t[-1]<=minWidth:
		plt.axis([0,minWidth,-10,110])
	else:
		plt.axis([t[-1]-minWidth,t[-1]+1,-10,110])

def switchMeasureMode():
	global measureOn
	measureOn = not measureOn

# fig,ax = plt.subplots()
# axnext = plt.axes([0, minWidth, TempLow, TempHigh])
#plt.ion()
plt.plot(t, T1,'r*-', label='Temp1')
plt.plot(t,T2,'b', label='Temp2 (Tejp)')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (C)')
plt.legend()
updateAxis()

while measureOn:
	#if(arduinoSerial.inWaiting()>0):
		# READ DATA FROM ARDUINO TO LIST OF FLOATS
		# TODO: Check length of read line, if wrong throw error
		# dataRaw = arduinoSerial.readline()
		# print dataRaw
		# dataList = dataRaw.split(",")
		# dataNum = [float(i) for i in dataList]
		# # # STORE TIMESTAMP AND TEMPERATURES
		# t.append(t[-1] + dataNum[0]/1000)
		# T1.append(dataNum[1])
		# T2.append(dataNum[2])

		# TESTING DATA (UNI RAND)
		t.append(t[-1]+1)
		T1.append(T1[-1]+np.random.standard_normal())
		T2.append(T2[-1]+np.random.standard_normal())
		plt.plot(t, T1,'r-', label='Top')
		plt.plot(t,T2,'b', label='Bottom')
		plt.pause(1)
		updateAxis()

	# no write commands until the arduino is ready
	# get time from arduino or python?

plt.show(block='True')




# , label='Bottom'

# # WRITE TO FILE 
# for item in thelist:
#   thefile.write("%s\n" % item)'

# with open('test.csv', 'wb') as f:
#     writer = csv.writer(f)

# t = range(10)
# T = np.sin(t)
# tmpRows = zip(t,T)
# print tmpRows[1]
# for row in tmpRows:
#     writer.writerow(row)