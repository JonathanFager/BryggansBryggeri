gfrom datetime import date
import operator

def getMean(investors):
	nbrOfDays = []
	dayItem = operator.itemgetter(*[1])
	invItem = operator.itemgetter(*[2])

	dates = map(dayItem,investors)
	dates[:] = [date.today() - x for x in dates]
	for x in dates:
		nbrOfDays.append(x.days)

	invest = map(invItem,investors)

	inv = map(invItem, investors)

	return [sum(nbrOfDays)/float(len(nbrOfDays)), sum(inv)/float(len(inv))]

def getDistance(investor,avg):
	datediff = date.today() - investor[1]
	investValue = pow(pow(datediff.days,2)/float(avg[0]) + pow(investor[2],2),0.5)/float(avg[1])
	investor.append(investValue)

def getRanking(investors):
	investors.sort(key=operator.itemgetter(3),reverse=True)


Invest = [["Daniel", date(2016, 10, 1), 500 ],["Svennis", date(2016, 9, 21), 600
],["Kasto", date(2016, 10, 9), 500], ["Johan", date(2016, 9, 23), 501],["Rolf", date(2016, 9, 22), 500
]]

avg = getMean(Invest)

for i in range(0,len(Invest)):
	getDistance(Invest[i], avg)

getRanking(Invest)

print "Nuvarande turordning:"
for i in Invest:
	
	print i[0]