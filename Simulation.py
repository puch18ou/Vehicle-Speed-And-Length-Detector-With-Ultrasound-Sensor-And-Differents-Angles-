from cmath import sqrt
from math import cos, dist, fabs, nan, pi, sin, tan, radians, pow
from operator import truediv
import time
import threading
import pygame
import sys
import time
import itertools
import json
import datetime
import os, psutil
import random

global doAllSimulations
global angulo_start
global showSimulation

doAllSimulations = True

times = 0
posiciony_detection = 388

multiplyFactor = 37
simulationTime = 37
pixelperm = 0.031 # pixeles per m
global sensorFrequency
aceleration = 0
global speed #2.65
speed = 2.65

contador_vehiculos = 0

global simulationStep
simulationStep = 1
global simulationindex
simulationindex = 1


signals = []
signals_type = {'signals_vehicles':0, 'signals_pedestrian':1}

# speeds = {'car':0.225, 'bus':1.8, 'truck':1.8, 'bike':2.5, 'p_young':1.5, 'p_older':1.2}  # average speeds of vehicles and pedestrians

# Coordinates of vehicles' start
xVeh = {'down':[400,400], 'right':[0,0]}
anchoCarril = 130
largoCarril = 1600
xVeh2 = {'car':[300,1600], 'bus':[300,1600], 'truck':[300,1600], 'bike':[300,1600]}
yVeh = {'down':[0,0], 'right':[posiciony_detection + anchoCarril/2 - 25,posiciony_detection + anchoCarril/2 - 25]} 

file = ""

vehicles = {'down': {0:[], 1:[], 2:[], 'crossed':0}, 'right': {0:[], 1:[], 2:[], 'crossed':0}}
pedestrians = {'right': {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 'crossed':0}, 
'left': {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 'crossed':0}}
vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'bike'}
pedestrianTypes = {0:'p_young', 1:'p_older'}
directionNumbers = {0:'down', 1:'right'}
directionNumbersPedestrian = {0:'right', 1:'left'}

signalTimerCoods = [(810,210),(530,550)]
signalCoods = [(810,230),(530,570)]
signalCounts = [(1000,100),(200,600)]
signalCountsLC = [(1000,140),(200,640)]
signalCountsLCMax = [(1000,120),(200,620)]


detectors = {0:[], 1:[], 22:[], 3:[], 4:[], 5:[]}

devices = (1,2,3)
global indexDevices
indexDevices = 0
noOfDevices = devices[len(devices) - 1]
modules = (1,3,5)
global indexModule
indexModule = [0,0,0]
noOfModules = modules[len(modules) - 1]


angules = [-150,-135,-120,-90,-60,-45,-30]
# Dispositivo y módulo

# Dispositivo
alturaDispositivo = posiciony_detection + anchoCarril
listLightDetectors = [(828, alturaDispositivo), (528,alturaDispositivo), (1128, alturaDispositivo)]
detectorPpal = [(800,alturaDispositivo - 6), (500,alturaDispositivo - 6), (1100,alturaDispositivo - 6)]

# Modulo
signalDetection = []
angulo_start = []

# Contador
countsalida = {0:0,1:0} 
countLongitudCola = {0:0,1:0}
countMaxLCT = {0:0,1:0}

deteccionpir = {0:False,1:False}

estado = 0
tipoControl = 1
seHaDetectadoVehiculo = False
seHaDetectadoPeaton = False



pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""
        
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehX, vehicleClass, direction_number, direction, angulo_start):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speed
        self.direction_number = direction_number
        self.direction = direction
        self.x = xVeh[direction][lane]
        self.y = yVeh[direction][lane]
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        path = file + "images/" + direction + "/" + vehicleClass + ".png"
        self.image = pygame.image.load(path)
        self.type = 0 #'vehicle'
        self.find = True
        self.lightDetector = []
        self.signalDetection = []
        self.HazCaptura = False
        self.angulo_start = angulo_start
        # self.Points = [(72,0),(75,0),(76,4),(88,4),(93,4),
        # (93,2),(104,2),(114,5),(121,14),(124,23),(124,34),(121,42),(114,51),(104,54),(93,54),
        # (88,53),(76,53),(75,56),(72,56),(72,53),(27,54),(5,49),(3,39),(3,17),(5,7),(27,2),(72,4),(72,0)]
        # self.Points = [(72,0),(104,2),(114,5),(121,14),(124,23),(124,34),(121,42),(114,51),(104,54),(27,54),(5,49),(3,39),(3,17),(5,7),(27,2),(72,0)]
        self.Points = [(72,0),(104,2),(114,5),(124,14),(124,42),(114,51),(104,54),(27,54),(5,49),(3,39),(3,17),(5,7),(27,2),(72,0)]
        # self.Points = [(0,0),(150,0),(150,60),(0,60),(0,0)]
        
        simulation.add(self)


        for i in range(1,devices[len(devices) - 1] + 1):
            lightdetector = []
            signaldetector = []
            for j in range(1,modules[len(modules) - 1] + 1):
                lightdetector.append(0)
                signaldetector.append((0,0))
            self.lightDetector.append(lightdetector)
            self.signalDetection.append(signaldetector)


    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        countsalida[1] += 1
        if(self.direction=='down'):
            self.lightDetector[0] = 0
            
            # Deteccion_de_vehiculos(self, 0) 
            # Deteccion_de_vehiculos(self, 1)               

            self.y += self.speed

        elif(self.direction=='right'):

            for i in range(1,devices[indexDevices] + 1):
                for j in range(1,modules[indexModule[i - 1]] + 1):
                    self.lightDetector[i-1][j-1] = 0
                    Deteccion_de_vehiculos(self, i - 1, j - 1) 

            self.x += self.speed
            if (aceleration != 0):
                self.speed = self.speed + aceleration

    def delete(self):
        simulation.remove(self)


def Deteccion_de_vehiculos(self, noOfDevice, noOfModule):

    angulo_inic = self.angulo_start[noOfDevice][noOfModule]
    angulo = angulo_inic * pi / 180

    self.lightDetector[noOfDevice][noOfModule] = anchoCarril / abs(sin(angulo))
    self.signalDetection[noOfDevice][noOfModule] = (0,0)

    if (self.find == True):
        for i in range(1, len(self.Points)):
            iscorrect = DetectLineSection(self, self.x + self.Points[i-1][0], self.x + self.Points[i][0], self.y +self.Points[i-1][1], self.y + self.Points[i][1], angulo, noOfDevice, noOfModule)
            if (iscorrect): 
                self.find = True
         
def DetectLineSection(self, x1, x2, y1, y2, angulo, noOfDevice, noOfModule):
    if (x1 == x2 and pi == abs(angulo)):
        return False
    elif (x1 != x2 and pi != abs(angulo)):
        param1 = (y2 - y1)/(x2 - x1)
        eqx = (listLightDetectors[noOfDevice][1] - listLightDetectors[noOfDevice][0]*tan(angulo) + param1*x1 - y1) / (param1 - (tan(angulo)))
        eqy = (y2 - y1) * ((eqx - x1)/(x2 - x1)) + y1
    elif (x1 == x2 or pi == abs(angulo)):
        param1 = (x2 - x1)/(y2 - y1)
        eqy = (listLightDetectors[noOfDevice][0] - listLightDetectors[noOfDevice][1]*((cos(angulo)/sin(angulo))) + param1*y1 - x1) / (param1 - (cos(angulo)/sin(angulo)))
        eqx = (x2 - x1) * ((eqy - y1)/(y2 - y1)) + x1        

    lightDetector = abs((sqrt(pow(listLightDetectors[noOfDevice][0] - eqx, 2) + pow(listLightDetectors[noOfDevice][1] - eqy,2))).real)
    if (self.signalDetection[noOfDevice][noOfModule] == (0,0) or (self.lightDetector[noOfDevice][noOfModule] > lightDetector)):
        correct = CheckIfPointsAreInLine(x1, x2, y1, y2,eqx,eqy)
        if (correct == True):
            self.lightDetector[noOfDevice][noOfModule] = lightDetector
            self.signalDetection[noOfDevice][noOfModule] = (eqx - 20,eqy- 20)
            return True
        else:
            return False
    else:
        return False

def CheckIfPointsAreInLine(x1, x2, y1, y2, solutionX, solutionY):
    if ((x1 <= x2 and x1 <= solutionX and x2 >= solutionX 
    or x1 >= x2 and x1 >= solutionX and x2 <= solutionX)
    and (y1 <= y2 and y1 <= solutionY and y2 >= solutionY 
    or y1 >= y2 and y1 >= solutionY and y2 <= solutionY)):
        return True
    else: 
        return False



# Initialization of signals with default values
def initialize():
    #inicializar contadores
    for i in range(0,1):  
        countsalida[i] = 0
        countLongitudCola[i] = 0
        countMaxLCT[i] = 0


# Generating vehicles in the simulation
def generateNewVehicle(contador_vehiculos, angulo_start):
    vehicle_type = contador_vehiculos 
    lane_number =  1 
    x1 = xVeh2[vehicleTypes[vehicle_type]][0]
    x2 = xVeh2[vehicleTypes[vehicle_type]][1]
    pos_vehX = (x1+x2)/2
    
    direction_number = 1
    Vehicle(lane_number,pos_vehX, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number], angulo_start)


def GetAllAngle(angules):
    perm = []
    for i in range(0,len(devices)):        
        permin = []
        if (i>0):
            permin.append([0])
        for j in range(0,len(modules)):
            j_mod = modules[j]
            permin.append([p for p in itertools.combinations(angules, r=j_mod)])
        perm.append(permin)

    lengthSimulations = []
    lengthSimulations2 = 0
    allAngles = []
    for i1 in range(0,len(perm[0])):
        for i2 in range(0,len(perm[1])):
            for i3 in range(0,len(perm[2])): 
                if (perm[1][i2][0] == 0 and perm[2][i3][0] != 0): 
                    break
                listin = list(itertools.product(perm[0][i1], perm[1][i2], perm[2][i3]))
                lengthSimulations.append(len(listin))
                lengthSimulations2 = lengthSimulations2 + len(listin)
                allAngles.append(listin)

    return lengthSimulations, allAngles


def GetNewAngle(allAngles, lengthSimulations, simulation):
    simulationlength = 0
    for i in range(0,len(lengthSimulations)):
        if (simulation < simulationlength + lengthSimulations[i]):
            angulo_start = allAngles[i][simulation - simulationlength]
            break
        else:            
            simulationlength = simulationlength + lengthSimulations[i]

    return angulo_start


def blitRotate(surf, image, pos, originPos, angle):
    """
    The blitRotate function draws a rotated image to the screen.
    The function takes 5 arguments:
        1) The surface on which the image will be drawn (pygame.Surface)
        2) The image that will be drawn (pygame.Surface)
        3) The position of the center of where the rotation will occur (tuple, ints).  This is in x,y coordinates from top left corner of screen/surface.  Note that this is not a tuple with two ints in it; it's just an int with another int inside it!  So you can do blitRotate(screen
    
    :param surf: Draw the image on
    :param image: Draw the image on the screen
    :param pos: Indicate the position of the mouse cursor and originpos is used to indicate
    :param originPos: Specify the pivot point of the rotation
    :param angle: Rotate the image around its center
    :return: The origin of the rotated image
    :doc-author: Trelent
    """
    # calcaulate the axis aligned bounding box of the rotated image
    w, h         = image.get_size()
    sin_a, cos_a = sin(radians(angle)), cos(radians(angle)) 
    min_x, min_y = min([0, sin_a*h, cos_a*w, sin_a*h + cos_a*w]), max([0, sin_a*w, -cos_a*h, sin_a*w - cos_a*h])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_x - pivot_move[0], pos[1] - originPos[1] - min_y + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)



def ResetData(indexDevices, indexModule, simulationindex):
    """
    The ResetData function is used to reset the data dictionary.
    It is called when a new simulation is started and it creates an empty dictionary with the following structure:
    {Simulation index : 1, Distance unit : &quot;mm&quot;, Simulation Start : &quot;dd/mm/yyyy hh:mm:ss&quot;, Elapsed Time : 0, Error Found : None}
    The first key (Simulation index) represents the number of simulations that have been run. The second key (Distance unit) 
    is used to indicate if distances are in meters or millimeters. The third key (Simulation Start) indicates when a simulation was started. 
    
    :param indexDevices: Select the device to be used in the simulation
    :param indexModule: Define the number of modules in each device
    :param simulationindex: Keep track of the simulation number
    :return: A dictionary with the following structure:
    :doc-author: Trelent
    """
    data = {}
    data["Simulation index"] = simulationindex
    data["Distance unit"] = "mm" 
    data["Simulation Start"] = datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S")
    data["Elapsed Time"] = "0"
    data["Error Found"] = "None"
    for i in range(0,devices[indexDevices]):  
        data[i + 1] = {}
        for j in range(0,modules[indexModule[i]]):  
            data[i+1][j+1] = dict.fromkeys(range(1, simulationStep))    
    return data


def GenerateManifest():
    """
    The GenerateManifest function generates a manifest file that contains information about the simulation.
    It takes no arguments and returns nothing.
    
    :return: A dictionary containing the following data:
    :doc-author: Trelent
    """
    
    l1, l2, l3 = psutil.getloadavg()

    data = {}
    data["Simulation step"] = str(simulationTime) + " ms"
    data["Simulation Start"] = str(datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S"))
    if not("Simulation End" in data.keys()):
        data["Simulation End"] = ""
    data["Simulation Parameters"] = {}
    data["Simulation Parameters"]["RAM Usage"] = str(round(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2,2)) + " MB"
    data["Simulation Parameters"]["CPU Usage"] = str((l3/os.cpu_count()) * 100)

    with open(file + "Data/Manifest.json", 'w') as f:
        json.dump(data, f)

    return data


def Main():    
    global doAllSimulations
    global simulationindex
    global angulo_start
    global speed
    global sensorFrequency
    global showSimulation
    
    simulationStep = 1

    stepsPerMilisecond = sensorFrequency

    speed = speed / (pixelperm * stepsPerMilisecond)

    thread1 = threading.Thread(name="initialization",target=initialize, args=())    # initialization
    thread1.daemon = True
    thread1.start()
  
    manifestData = GenerateManifest()

    show = showSimulation

    global indexDevices
    global indexModule

    # Colours 
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize 
    screenWidth = 1800
    screenHeight = 1000
    screenSize = (screenWidth, screenHeight)

    # Setting background image i.e. image of intersection
    if(show):
        screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)    
        background = pygame.image.load(file + 'images/intersection.png')
        pygame.display.flip()
        pygame.display.set_caption(file + "SIMULATION")

        # Loading signal images and font
        signaldetect = []
        detection = []
        LightTraffic = []
        for i in range(0,devices[len(devices)-1]):  
            detectionOnOff = []
            LightTraffic_per_device = []
            signaldetect.append(pygame.image.load(file + 'images/lights/SignalDetect.png'))
            detection.append(pygame.image.load(file + 'images/lights/DetectorPpal.png'))
            for j in range(0,modules[len(modules)-1]):  
                detection_per_device_On = pygame.image.load(file + 'images/lights/Detector.png')
                detection_per_device_Off = pygame.image.load(file + 'images/lights/DetectorOff.png')
                LightTraffic_per_device = [detection_per_device_On, detection_per_device_Off]
                detectionOnOff.append(LightTraffic_per_device)        
            LightTraffic.append(detectionOnOff)
    
    originpose = (100,100)    
    pivot = (0, 50)

    simulationMsgError = {}
    with open(file + "Data/Error.json", 'w') as f:
        json.dump(simulationMsgError, f)


    signalDetection2 = []
    signalDetection = []
    for i in range(1,devices[len(devices) - 1] + 1):
        signaldetector = []
        for j in range(1,modules[len(modules) - 1] + 1):
            signaldetector.append((0,0))
        signalDetection2.append(signaldetector)
        signalDetection.append(signaldetector)

    font = pygame.font.Font(None, 30)
        
    lenOfSimulations = 0
    lenOfSimulations, allAngles = GetAllAngle(angules)


    allsimulations = 0
    for i in  lenOfSimulations:
        allsimulations = allsimulations + i

    if (doAllSimulations):
        angulo_start = []
        angulo_start = GetNewAngle(allAngles, lenOfSimulations, simulationindex)
    print(angulo_start)
    indexDevices = 0
    indexModule = [0,0,0]

    for ind in range(0,len(angulo_start)):
        if (angulo_start[ind] != 0):
            indexDevices = indexDevices + 1
            if (len(angulo_start[ind])>=1):
                indexModule[ind] = len(angulo_start[ind])
                for ind2 in range(0,len(modules)):
                    if (modules[ind2] == indexModule[ind]):
                        indexModule[ind] = ind2
                
    indexDevices = devices[indexDevices - 1] - 1



    generateNewVehicle(contador_vehiculos, angulo_start)    
    tipoVehiculo = -1
    if(show):
        time.sleep(4.5)
    startTime = time.time()

    data = ResetData(indexDevices, indexModule, simulationindex)

    simulationError = ""
    simulationMsgError = {}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

                            
        if(show):
            screen.blit(background,(0,0))
            for i in range(0, devices[indexDevices]):
                screen.blit(detection[i],detectorPpal[i])
                screen.blit(signaldetect[i],signalDetection[i][0])        

        signalTexts = ["",""]
        countSalTexts = ["",""]
        countLCTexts = ["",""]
        countMaxLCTexts = ["",""]

        verdeant = [0,0]

        capturar = False  
        
        # Inicializamos los detectores a la distancia máxima
        for i in range(0,devices[indexDevices]):  
            detectors[i] = []
            for j in range(0,modules[indexModule[i]]):  
                angulo_inic = angulo_start[i][j]
                angulo = angulo_inic * pi / 180
                dist_maxima = abs(anchoCarril / sin(angulo))
                detectors[i].append(dist_maxima)



        # display the vehicles
        try:
            for movimiento in simulation:
                if(show):
                    screen.blit(movimiento.image, [movimiento.x, movimiento.y])
                movimiento.move()
                if (movimiento.type == 0):
                    for i in range(0,devices[indexDevices]):   
                        for j in range(0,modules[indexModule[i]]):  
                            if movimiento.lightDetector[i][j] >= 1:
                                detectors[i][j] = movimiento.lightDetector[i][j]
                                signalDetection2[i][j] = movimiento.signalDetection[i][j]

                if (movimiento.HazCaptura):
                    capturar = True                   

                tipoVehiculo = movimiento.vehicleClass
        except:
            simulationError = "Simulation Error"
            print(simulationError)

        
        try:
            if (simulationError == ""):
                for i in range(0,devices[indexDevices]):   
                    for j in range(0,modules[indexModule[i]]):  
                        angulo_inic = angulo_start[i][j]
                        angulo = angulo_inic * pi / 180
                        dist_maxima = abs(anchoCarril / sin(angulo))
                        if (tipoVehiculo != ""):        
                            randomError = random.uniform(-0.003, 0.003)
                            data[i+1][j+1][simulationStep] = detectors[i][j] / (1/ pixelperm) + randomError #multiplyFactor  
                            if detectors[i][j] < dist_maxima:
                                if(show):
                                    blitRotate(screen, LightTraffic[i][j][0], listLightDetectors[i], pivot, -1*angulo_inic)
                                signalDetection[i][j] = signalDetection2[i][j]
                            else:
                                signalDetection[i][j] = (0,0)                        
                                if(show):
                                    blitRotate(screen, LightTraffic[i][j][1], listLightDetectors[i], pivot, -1*angulo_inic)
                            if(show):
                                screen.blit(signaldetect[i],signalDetection[i][j])        
        except:
            simulationError = "Data Error"
            print(simulationError)
            
        
        if (tipoVehiculo != ""):         
            simulationStep = simulationStep + 1


        if(show):
            if capturar:
                rect = pygame.Rect(465, 120, 415, 470)
                sub = screen.subsurface(rect)
                pygame.image.save(sub, "car_" + str(angulo_inic) + ".png")


        if (simulationStep > largoCarril / speed or simulationError != ""):
            filename = "" 
            directoryname = ""
            try:
                if (simulationError == ""):
                    filename = "" 
                    directoryname = ""
                    for indexdev in range(0,devices[indexDevices]):
                        directoryname = directoryname + str(indexdev + 1) + "-"
                        filename = filename + str(indexdev + 1) + "["
                        indexmodules = 0
                        for indexmod in range(0,modules[indexModule[indexdev]]):
                            angle = angulo_start[indexdev][indexmod] * -1
                            filename = filename + str(angle) + ","           
                            indexmodules = indexmodules + 1                     
                        directoryname = directoryname + str(indexmodules) + "_"
                        filename = filename[0:len(filename)-1] + "]_"

                    filename = filename[0:len(filename)-1]
                    directoryname = directoryname[0:len(directoryname)-1]
            except:
                simulationError = "File Error"
                print(simulationError)

            endTime = time.time()
            elapsedTime = (endTime - startTime)
            print("Simulacion: " + str(simulationindex) + "/" + str(allsimulations) + "; angulos: " + filename + ", elapsedTime: " + str(elapsedTime))

            data["Elapsed Time"] = str(round(elapsedTime,2)) + " ms"
            if (simulationError != ""):
                data["Error Found"] = "Yes: " + simulationError        
                if (simulationError == "File Error"):
                    simulationMsgError[simulationindex] = simulationError
                else:
                    simulationMsgError[simulationindex] = simulationError + " - " + filename
                    
                with open(file + "Data/Error.json", 'w') as f:
                    json.dump(simulationMsgError, f)
            else: 
                data["Error Found"] = "None"
            if (directoryname == ""): directoryname = "Error"
            folder = file + "Data/" + directoryname
            if not os.path.exists(folder):
                os.makedirs(folder)

            with open(folder + "/" + filename + '.json', 'w') as f:
                json.dump(data, f)

                
            startTime = time.time()
            simulationError = ""


            simulationindex = simulationindex + 1
            if (simulationindex >= allsimulations):
                l1, l2, l3 = psutil.getloadavg()
                manifestData["Simulation End"] = str(datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S"))
                manifestData["Simulation Parameters"]["RAM Usage"] = str(round(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2,2)) + " MB"
                manifestData["Simulation Parameters"]["CPU Usage"] = str((l3/os.cpu_count()) * 100) + "%"    
                with open(file + "Data/Manifest.json", 'w') as f:
                    json.dump(manifestData, f)                 
                break 
            elif doAllSimulations == False:
                with open(file + "Data/Manifest.json", 'w') as f:
                    json.dump(manifestData, f) 
                break
            
            

            angulo_start = GetNewAngle(allAngles, lenOfSimulations, simulationindex)

            for movimiento in simulation:
                movimiento.delete()
                movimiento = None  
            generateNewVehicle(contador_vehiculos,angulo_start)

            indexDevices = 0
            indexModule = [0,0,0]

            for ind in range(0,len(angulo_start)):
                if (angulo_start[ind] != 0):
                    indexDevices = indexDevices + 1
                    if (len(angulo_start[ind])>=1):
                        indexModule[ind] = len(angulo_start[ind])
                        for ind2 in range(0,len(modules)):
                            if (modules[ind2] == indexModule[ind]):
                                indexModule[ind] = ind2

            indexDevices = devices[indexDevices - 1] - 1
            simulationStep = 1
            data = ResetData(indexDevices, indexModule, simulationindex)

                
                
        if(show):
            # countSalTexts[0] = font.render('contador posicion = '+ str(simulationStep), True, white, black)
            # screen.blit(countSalTexts[0],signalCounts[0])
            pygame.display.update()

