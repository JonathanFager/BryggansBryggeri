import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import tkinter as tk
from tkinter import ttk
# IMPORTS
import serial
# import csv





LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

# LOOP for continuous running
def animate(i):
	global t, T1, T2
	alpha = 0.1
	#Brownian motion for testing
	if measureOn:
		t.append(t[-1]+1)
		T1.append(T1[-1]+np.random.standard_normal()-alpha*(T1[-1]-getRefTemp()))
		refTempList.append(getRefTemp())
		a.clear()
		a.set_ylim(0,110)
		a.set_xlim(0,t[-1]+10)
		a.plot(t,T1,'r')
		a.plot(t,refTempList,'k')
		
		#if(arduinoSerial.inWaiting()>0):
		# # READ DATA FROM ARDUINO TO LIST OF FLOATS
		# # TODO: Check length of read line, if wrong throw error
		# dataRaw = arduinoSerial.readline()
		# print dataRaw
		# dataList = dataRaw.split(",")
		# dataNum = [float(i) for i in dataList]
		# # # STORE TIMESTAMP AND TEMPERATURES
		# t.append(t[-1] + dataNum[0]/1000)
		# T1.append(dataNum[1])
		# T2.append(dataNum[2])
		# refTempList.append(getRefTemp())
		# a.clear()
		# a.set_ylim(0,110)
		# a.set_xlim(0,t[-1]+10)
		# a.plot(t,T1,'r')
		# a.plot(t,refTempList,'k')

def getRefTemp():
	return refTemp[brewStep]

def getTimer():
	timer = timers[brewStep]
	timeStr=['','','']
	for i in range(len(timers)):
		if i==brewStep:
			Minutes = timers[i]-t[-1]%60
			Seconds = 60-t[-1]
		else:
			Minutes = timers[i]
			Seconds = 60

		timeStr[i] = str(Minutes)+":"+str(Seconds)
	return timeStr

# Manually setting reference temperature
def setRefTemp(newSetpoint):
	global refTemp
	refTemp = newSetpoint

def resetGraph():
	global t, T1, T2, refTempList, brewStep
	t = [0]
	T1 = [T1[-1]]
	T2 = [T2[-1]]
	brewStep = 0
	refTempList = [getRefTemp()]
	a.clear()

def switchMeasureMode():
	global measureOn
	measureOn = not measureOn

def next():
	global brewStep
	if brewStep == len(refTemp)-1:
		brewStep = 0
		print('Brewsteps finished')
	else: 
		brewStep += 1

class BryggansApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Bryggans Bryggeri")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # for F in (StartPage, Recipes):

        #     frame = F(container, self)

        #     self.frames[F] = frame

        #     frame.grid(row=0, column=0, sticky="nsew")
        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=1, sticky="nsw")
        self.show_frame(StartPage)

        frame = Recipes(container, self)
        self.frames[Recipes] = frame
        frame.grid(row=0, column=0, sticky="nsw")
        self.show_frame(Recipes)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Bryggning", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        resetButton = ttk.Button(self, text="Reset",command=resetGraph)
        resetButton.pack()

        toggleMeasureButton = ttk.Button(self, text="Pause/Unpuase", command=switchMeasureMode)
        toggleMeasureButton.pack()

        nextButton = ttk.Button(self, text="Next",command=next)
        nextButton.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        # canvas.get_tk_widget().gre
        canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class Recipes(tk.Frame):

    def __init__(self, parent, controller):
        ReceptStr = "Recept: Epo IPA \n 1. Värm vatten till " + str(refTemp[0]) +"\u00b0C \n 2. Mäska i " + str(timers[0]) + "min. Återstående tid " + getTimer()[0] + "\n 3. Värm till " + str(refTemp[1]) +"\u00b0C\n 4. Mäska i " + str(timers[1]) + "min. Återstående tid " + getTimer()[1] + "\n 5. Värm till " + str(refTemp[2]) +"\u00b0C \n 6. Koka i  " + str(timers[2]) + " min. Återstående tid " + getTimer()[2]
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=ReceptStr, font=LARGE_FONT)
        label.pack(pady=10,padx=10)

# arduinoSerial = serial.Serial('/dev/ttyACM1',9600) #CHECK!

f = Figure()
a = f.add_subplot(111)
t = [0]
T1 = [50]
T2 = [50]
refTemp = [66,75,100]
timers = [60,10,60]
brewStep = 0
refTempList = [getRefTemp()]
measureOn = False
# print(dir(a))
# TODO Database recipes, getLiters.
app = BryggansApp()
app.geometry("1280x780")
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
  