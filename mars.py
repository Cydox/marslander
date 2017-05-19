import math
import matplotlib.pyplot as plt

def rho(h):
	i = 0
	while atm[i][0] <= h:
		i += 1
	gradient = (atm[i][1] - atm[i - 1][1]) / (atm[i][0] - atm[i - 1][0])
	
	return atm[i - 1][1] + gradient * (h - atm[i - 1][0])

f = open("atm.txt", "r")
lines = f.readlines()
f.close()

atm = []

for line in lines:
	if ord(line[0]) >= 48 and ord(line[0]) <= 57:
		row = [float(line.split(" ")[0]) * 1000, float(line.split(" ")[2])]
		atm.append(row)

hlist = []
xlist = []
vlist = []
tlist = []
fflist = []
glist = []

g = 3.711

h_t = 1750
fuel = 68

h = 20000.0
vX = 262.0 * math.cos(20.0 * math.pi / 180.0)
vY = -262.0 * math.sin(20.0 * math.pi / 180.0)
x = 0.0
vYRef = -2.0
fuelFlow = 0.0
v_e = 4400.0
m = 699.0 + fuel


deltat = 0.01
t = 0

while h > 0:
	t = t + deltat
	
	if fuel > 0.0 and h > 0.3 and h < h_t:
		fuelFlow = (m * g) / (4400.0) + 0.05 * (vYRef - vY)
		if fuelFlow > 5:
			fuelFlow = 5
	else:
		fuelFlow = 0
	
	m -= fuelFlow * deltat
	fuel -= fuelFlow * deltat
	vTotal = math.sqrt((vX * vX) + (vY * vY))
	thrust = v_e * fuelFlow
	drag = 4.92 * 0.5 * vTotal * vTotal * rho(h)
	
	F_x = (vX / vTotal) * (-thrust - drag)
	F_y = (vY / vTotal) * (-thrust - drag) - m * g

	a_x = F_x / m
	a_y = F_y / m

	vX += a_x * deltat
	vY += a_y * deltat

	x += vX * deltat
	h += vY * deltat
	
	hlist.append(h)
	xlist.append(x)
	vlist.append(vTotal)
	tlist.append(t)
	fflist.append(fuelFlow)
	glist.append(math.degrees(math.atan2(vX, vY)) - 90)


	#print h
	#print vY
	#print fuelFlow

print vY
plt.subplot(231)
plt.title("Trajectory")
plt.plot(xlist, hlist)
plt.subplot(232)
plt.title("Speed")
plt.plot(vlist, hlist)
plt.subplot(233)
plt.title("Mdot vs time")
plt.plot(tlist, fflist)
plt.subplot(234)
plt.title("Alt vs time")
plt.plot(tlist, hlist)
plt.subplot(235)
plt.title("Speed vs time")
plt.plot(tlist, vlist)
plt.subplot(236)
plt.title("Gamma vs time")
plt.plot(tlist, glist)

plt.show()

