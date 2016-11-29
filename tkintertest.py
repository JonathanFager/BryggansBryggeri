import numpy as np
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

HEADLINE= ("Verdana", 30)
LARGE_FONT = ("Verdana", 20)
style.use("ggplot")

# Data to read from. Styled 'Brewdata/RecipeName+Date.csv'
BatchFilePath = 'Brewdata/ESB161126.csv'
# Generate array from csv
data = np.genfromtxt(BatchFilePath, dtype=float, delimiter=',', names=True,skip_header=4)
t = data['t']
T1 = data['T1']
# T2 = data['T2']

plt.plot(t,T1)
plt.show()