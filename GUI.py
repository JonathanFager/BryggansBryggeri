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
import csv
import time

HEADLINE= ("Verdana", 30)
LARGE_FONT = ("Verdana", 20)
style.use("ggplot")

# LOOP for continuous running
def animate(i):
	global t, T1, T2
	
	
	if measureOn:
		# #Brownian motion for testing
		#alpha = 0.1
		# t.append(t[-1]+1)
		# T1.append(T1[-1]+np.random.standard_normal()-alpha*(T1[-1]-getRefTemp()))
		# refTempList.append(getRefTemp())
		# updateGraph()
		if(arduinoSerial.inWaiting()>0):
		# # READ DATA FROM ARDUINO TO LIST OF FLOATS
		# # TODO: Check length of read line, if wrong throw error
			dataRaw = arduinoSerial.readline().decode().strip('\r\n')
			print(dataRaw)
			dataList = dataRaw.split(",")
			dataNum = [float(i) for i in dataList]
			# # STORE TIMESTAMP AND TEMPERATURES
			t.append(t[-1]+1)
			# t.append(dataNum[0]/1000)
			T1.append(dataNum[1])
			T2.append(dataNum[2])
			refTempList.append(getRefTemp())
			updateGraph()
		
def getRefTemp():
	return refTemp[brewStep]

# Manually setting reference temperature
def setRefTemp(newSetpoint):
	global refTemp
	refTemp = newSetpoint

def getReceptStr(i):
	ReceptStr = ['','','','','','','']
	# ReceptStr[0]= "Recept: English bitter"
	# ReceptStr[1]="1. Värm vatten till " + str(refTemp[0]) +"\u00b0C"
	# ReceptStr[2]="2. Mäska i " + str(timers[0]) + "min"
	# ReceptStr[3]="3. Värm till " + str(refTemp[1]) +"\u00b0C" 
	# ReceptStr[4]="4. Vila i " + str(timers[1]) + " min"
	# ReceptStr[5]="5. Mäska ur med 2l. vatten. Värm till " + str(refTemp[2]) +"\u00b0C"
	# ReceptStr[6]="6. Koka i  " + str(timers[2]) +" min"

	# Christmas Edition
	ReceptStr[0] = "GLÖGG"
	ReceptStr[1] = "Heat with caution to 77\u00b0C"
	ReceptStr[2] = "Ethanol boils at 78\u00b0C"
	ReceptStr[3] = "Stop heating when a light smoke rises"
	return ReceptStr[i]
	


def getTimer():
	timer = timers[brewStep]
	timeStr=['','','']
	for i in range(len(timers)):
		Seconds = 60-(t[-1]-timeInStep[i-1])%60
		if Seconds == 60:
			Seconds = "00"
		totMinPassed = np.floor(t[-1]/60+timeInStep[i])
		Minutes = int(timers[i] - totMinPassed)-1
		timeStr[i] = str(Minutes)+":"+str(Seconds)
	return timeStr

def updateGraph():
	minWidth = 120
	a.clear()
	a.set_ylim(0,110)
	if t[-1]<minWidth:
		a.set_xlim(0,t[-1]+10)
		a.text(0,110,"T1: " + str(np.round_(T1[-1])),fontsize=16)
		a.text(0,115,"T2: " + str(np.round_(T2[-1])),fontsize=16)
		a.text(0,120,"Timer: " + getTimer()[brewStep],fontsize=16)
	else:
		a.set_xlim(t[-1]-minWidth,t[-1]+10)
		a.text(t[-1]-minWidth,110,"T1: " + str(np.round_(T1[-1])),fontsize=16)
		a.text(t[-1]-minWidth,115,"T2: " + str(np.round_(T2[-1])),fontsize=16)
		a.text(t[-1]-minWidth,120,"Timer: " + getTimer()[brewStep],fontsize=16)
	a.plot(t,T1,'r')
	a.plot(t,T2,'b')
	a.plot(t,refTempList,'k')
	a.set_axis_bgcolor('white')

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
	global brewStep, timeInStep
	if brewStep == len(refTemp)-1:
		timeInStep = [0,0,0]
		brewStep = 0
		print('Brewsteps finished')
	else: 
		timeInStep[brewStep] = t[-1]
		brewStep += 1

def writeToFile():
	writeTempList = [t, T1]
	writeTempList = list(map(list, zip(*writeTempList))) #Transpose list for readability
	date = (time.strftime("%y%m%d"))
	with open("./Brewdata/ESB"+date+".csv", "w") as f:
		writer = csv.writer(f)
		writer.writerows(writeTempList)


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
        frame.grid(row=0, column=1, sticky="nswe")
        frame.configure(bg='white')
        self.show_frame(StartPage)

        frame = Recipes(container, self)
        self.frames[Recipes] = frame
        frame.grid(row=0, column=0, sticky="nswe")
        self.show_frame(Recipes)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Bryggning", font=LARGE_FONT)
        label.pack(side="top")

        resetButton = ttk.Button(self, text="Reset",command=resetGraph)
        resetButton.pack(side="top", anchor="w", fill="x")

        toggleMeasureButton = ttk.Button(self, text="Pause/Unpuase", command=switchMeasureMode)
        toggleMeasureButton.pack(side="top", anchor="w",fill="x")

        nextButton = ttk.Button(self, text="Next",command=next)
        nextButton.pack(side="top", anchor="w",fill="x")

        nextButton = ttk.Button(self, text="Save",command=writeToFile)
        nextButton.pack(side="top", anchor="w",fill="x")

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        # canvas.get_tk_widget().gre
        canvas.get_tk_widget().pack(side=tk.LEFT,fill=tk.BOTH, expand=True)

        # toolbar = NavigationToolbar2TkAgg(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class Recipes(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		# for i in range(6):
		# 	if i==0:
		# 		alignment = 'center'
		# 		label = tk.Label(self, text=getReceptStr(i), font=HEADLINE,anchor=alignment)
		# 		label.pack(pady=10,padx=10)
		# 	else:
		# 		alignment = 'w'
		# 		label = tk.Label(self, text=getReceptStr(i), font=LARGE_FONT,anchor=alignment)
		# 		label.pack(pady=10,padx=10)
		# # Christmas Edition
		for i in range(6):
			if i==0:
				alignment = 'center'
				label = tk.Label(self, text=getReceptStr(i), font=HEADLINE,anchor=alignment)
				label.pack(pady=10,padx=10)
			else:
				alignment = 'w'
				label = tk.Label(self, text=getReceptStr(i), font=LARGE_FONT,anchor=alignment)
				label.pack(pady=10,padx=10)
			
			
		myButton = tk.Button(self,borderwidth=0)
		photoimage = tk.PhotoImage(file="Graphics/christmas1.png")
		photoimage.zoom(1)
		myButton.image = photoimage
		myButton.configure(image=photoimage)
		myButton.pack(pady=100,padx=100)
		# christmasCanvas = tk.Canvas(self)
		# christmas_image = tk.PhotoImage(file ="Graphics/christmas.png")
		# #Resizing
		# christmas_image = christmas_image.subsample(1, 1) #See below for more: 
		# #Shrinks the image by a factor of 2 effectively
		# christmasCanvas.create_image(0, 0, image = christmas_image, anchor = "nw")
		# self.christmas_image = christmas_image 
		# christmasCanvas.pack()


# # Configure arduino port communication. Make sure port adress is correct
#arduinoSerial = serial.Serial('/dev/ttyACM0',9600) #CHECK!

f = Figure()
a = f.add_subplot(111)
t = [0]
T1 = [15]
T2 = [50]
refTemp = [75,80,100]
timers = [60,10,60]
timeInStep = [0,0,0]
brewStep = 0
refTempList = [getRefTemp()]
measureOn = False
beige = '#CABBA0'
green = '#008200'
red = '#FF0000'
# print(dir(a))
# TODO Database recipes, getLiters.
app = BryggansApp()
app.geometry("1280x780")
app.tk_setPalette(background='white', foreground=red,
               activeBackground='white', activeForeground=red)
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()

# "Recept: Epo IPA \n 1. Värm vatten till " + str(refTemp[0]) +"\u00b0C \n 2. Mäska i " + str(timers[0]) + "min \n 3. Värm till " + str(refTemp[1]) +"\u00b0C\n 4. Mäska i " + str(timers[1]) + " min \n 5. Värm till " + str(refTemp[2]) +"\u00b0C \n 6. Koka i  " + str(timers[2]) +" min"
  