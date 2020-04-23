"""-------------------Solar System-------------------------------
This program shows the movement of the planets around the sun.
You only have to input the maximum time of movement of the planets.
All the information of the planets is given in .txt files.
"""
# Libraries
# ---------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Class
# ------------------------------------------------------------------
class Cuerpoceleste:
    """This class represents a planet"""
    def __init__(self, Rad, vel_angp):
        """Initialization Function"""
        self.nameplanet = ""
        self.Radius = Rad
        self.wplanet = vel_angp
        self.satelites = []

    def coordx(self, time):
        """Calculate the position in x of the planet"""
        return self.Radius*np.cos(self.wplanet*time)

    def coordy(self, time):
        """Calculate the position in y of the planet"""
        return self.Radius*np.sin(self.wplanet*time)

    def dibp(self, sub):
        """Draw the planet"""
        dibpla, = sub.plot([], [], 'o', ms=7, label=self.nameplanet)
        return dibpla

    def position(self, time):
        """Give the positioin in x and y of the planet"""
        xplanet = self.coordx(time)
        yplanet = self.coordy(time)
        return xplanet, yplanet


class Satelite(Cuerpoceleste):
    """This class represents a satelite of a planet"""
    def __init__(self, Rad, vel_angp, rad, vel_angs):
        """Inicialization Function"""
        Cuerpoceleste.__init__(self, Rad, vel_angp)
        self.namesat = ""
        self.radius = rad
        self.wsat = vel_angs

    def dibs(self, sub):
        """Draw the satelite"""
        dibsat, = sub.plot([], [], 'o', ms=3, label=self.namesat)
        return dibsat

    def position(self, time):
        """Give the position in x and y of the satelite"""
        xsatelite = self.coordx(time) + self.radius*np.cos(self.wsat*time)
        ysatelite = self.coordy(time) + self.radius*np.sin(self.wsat*time)
        return xsatelite, ysatelite
# ------------------------------o------------------------------------


# Functions
# ----------------------------------------------------------------------
def cargar_data():
    """Given a list with all the information of planets and satelites"""
    l_univers = []
    fpla = open("Universe.txt", 'r')
    for linea in fpla:
        linea1 = linea.split(";")
        pla = Cuerpoceleste(float(linea1[1]), float(linea1[2]))
        pla.nameplanet = linea1[0]
        l_sat = []
        gsat = open(pla.nameplanet+".txt", 'r')
        for line in gsat:
            line1 = line.split(";")
            satel = Satelite(pla.Radius, pla.wplanet, float(line1[1]), float(line1[2]))
            satel.namesat = line1[0]
            l_sat.append(satel)
        pla.satelites = l_sat
        gsat.close()
        l_univers.append(pla)
    fpla.close()
    return l_univers


def init():
    """Inicialization of the elements of the plot"""
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)
    i = 0
    j = 0
    for i in range(len(lislineaspla)):
        lislineaspla[i].set_data(lispospla[i][0], lispospla[i][1])
        for j in range(len(lislineassat)):
            lislineassat[j].set_data(lispossat[j][0], lispossat[j][1])
    return lislineaspla, lislineassat
# --------------------------------o------------------------------------

# -----------------------PRINCIPAL PROGRAM-----------------------------
# Constants
# ------------------------------------
T_MAX = float(input("Maximum Time:"))
DT = 0.02
# ------------------------------------

# Variables
# --------------------------
lista_total = cargar_data()
lislineaspla = []
lislineassat = []
lispossat = []
lispospla = []
# --------------------------

# Plotting
# -------------------------------------------------------
fig, ax = plt.subplots()
for cuerpo in lista_total:
    lislineaspla.append(cuerpo.dibp(ax))
    lispospla.append([[], []])
    for sate in cuerpo.satelites:
        lislineassat.append(sate.dibs(ax))
        lispossat.append([[], []])
DOT1 = plt.scatter(0, 0, s=175, c='yellow', label="Sun")
# -------------------------------------------------------


# Functions
# -------------------------------------------------------
def data_gen():
    """Generate the data used to animate the plot"""
    t_ini = 0.0
    coorpla = []
    coorsat = []
    for planeta in lista_total:
        coorpla.append([])
        for sat in planeta.satelites:
            coorsat.append([])
    while t_ini < T_MAX:
        t_ini = t_ini + DT
        i = 0
        for i in range(len(lista_total)):
            coorpla[i] = lista_total[i].position(t_ini)
            for sat in lista_total[i].satelites:
                coorsat.pop(0)
                coorsat.append(sat.position(t_ini))
        yield coorpla, coorsat


def run(data):
    """Update the data of the positions of planets and satellites
    data: is the information generated in data_gen"""
    coorpla = data[0]
    coorsat = data[1]
    i = 0
    j = 0
    for i in range(len(lislineaspla)):
        lispospla[i][0] = coorpla[i][0]
        lispospla[i][1] = coorpla[i][1]
        for j in range(len(lislineassat)):
            lispossat[j][0] = coorsat[j][0]
            lispossat[j][1] = coorsat[j][1]
    i = 0
    j = 0
    for i in range(len(lislineaspla)):
        lislineaspla[i].set_data(lispospla[i][0], lispospla[i][1])
        for j in range(len(lislineassat)):
            lislineassat[j].set_data(lispossat[j][0], lispossat[j][1])
    return lislineaspla, lislineassat
# ------------------------------------------------------------------------------

# Animation of the plot and show
ANI = animation.FuncAnimation(fig, run, data_gen, interval=25,
                              repeat=False, init_func=init)
plt.legend(bbox_to_anchor=(0., 1.03, 1., .10), prop={'size': 6.5},
           loc=10, ncol=5, title=r'Solar System')
plt.show()
# -------------------------------------------------------------------
# ------------------------------o------------------------------------
