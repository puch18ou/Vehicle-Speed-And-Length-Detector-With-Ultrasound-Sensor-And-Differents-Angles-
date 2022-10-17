from asyncio.windows_events import NULL
from contextlib import nullcontext
from doctest import ELLIPSIS_MARKER
from gettext import find
from operator import truediv
from pyexpat.errors import XML_ERROR_INVALID_TOKEN
import re
from this import d
from turtle import title
from xml.sax.handler import property_interning_dict
import matplotlib.pyplot as plt
from matplotlib import gridspec
import json
from more_itertools import locate
from math import cos, dist, nan, pi, sin, tan, radians, pow
import numpy as np
from scipy import signal 


global simulationStepFactor
global angles
global targetSpeed
correctionParameter = 1.65

def jsonKeys2int(x):
    if isinstance(x, dict):
            return {int(k):v for k,v in x.items()}
    return x

def AbsError(x_val, x):
    sum =0
    for xi in x_val:
        sum = sum + abs(xi - x)
    
    return sum / len(x_val)

def median(dataset):
    data = sorted(dataset)
    index = len(data) // 2
    
    # If the dataset is odd  
    if len(dataset) % 2 != 0:
        return data[index]
    
    # If the dataset is even
    return (data[index - 1] + data[index]) / 2


def find_max(iterable, peakindex, t):
    maxarray = []
    dt = []
    index = 1
    for i in range (5):
        maximum = 0
        for i in peakindex[0]:
            value = iterable[i]
            if value > maximum and not(value in maxarray):
                maximum = value
                index = i
        maxarray.append(maximum)
        dt.append(t[index])
    return dt


def AddSubPlot(title,  position, datax, datay, color, name, axisyname):    
    ax0 = plt.subplot(position)
    ax0.set_title(title)
    ax0.plot(datax, datay, color, label=name)
    plt.xlabel('Simulation step')
    plt.ylabel(axisyname)
    plt.grid()
    plt.legend()
    
def GetSpecificDataToShow(dataToEvaluate):
    listdata = list(dataToEvaluate.values())
    firstdata = listdata[0] - 0.035
    indexitems = list(locate(dataToEvaluate.values(), lambda x: x < firstdata))
    newlistData = dataToEvaluate.copy()
    for key in dataToEvaluate:
        if (key < (indexitems[0] - indexitems[0]*0.05)):
            newlistData.pop(key)
        elif (key > (indexitems[len(indexitems) -1] + indexitems[len(indexitems) -1]*0.05)):
            newlistData.pop(key)
    return newlistData

def GetSpecificDataToSolve(dataToEvaluate):
    listdata = list(dataToEvaluate.values())
    firstdata = listdata[0] - 0.035
    indexitems2 = list(locate(dataToEvaluate.values(), lambda x: x < firstdata))
    newlistData = dataToEvaluate.copy()
    for key in dataToEvaluate:
        if (key <= (indexitems2[0] + 1)):
            newlistData.pop(key)
        elif (key > (indexitems2[len(indexitems2) -1] - 1)):
            newlistData.pop(key)            
            
    return newlistData

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def SetSmoothFilter(t, values, smoothparameter):
    if (smoothparameter == 1): return t, values
    values = smooth(values, smoothparameter)
    valuesToDelete = int((smoothparameter-1)/2)
    values = values[valuesToDelete:-valuesToDelete]
    t = t[valuesToDelete:-valuesToDelete]

    return t, values

def NewFilter(values, index):
    # for i in range(0, index):
    #     sum = 0
    #     ind = 0
    #     for j in range(0, index + i + 1):
    #         if (-j + index != i):
    #             sum = sum + values[i - j + index]
    #             ind = ind + 1
    #     values[i] = sum/ind

    for i in range(index, len(values)-index):
        sum = 0
        ind = 0
        for j in range(-index, index):
            if (j != i):
                sum = sum + values[i-j]
                ind = ind + 1
        values[i] = sum/ind
    return values

def GenerateDataFromOldData(newlistData):
    t = list(newlistData.keys())
    values = list(newlistData.values())

    newData_t = []
    newData_value = []
    newData_t.append(t[0])
    newData_value.append(values[0])

    iteraciones = 4

    for i in range(0, len(values)-1):
        for j in range(0, iteraciones):
            newData_t.append(t[i] + (j+1)/4)
            newData_value.append(values[i] + (values[i+1] - values[i]) * (j+1)/4)

    return newData_t, newData_value


def closest(valuearray,value):
    diff = value
    valueout = 0
    for val in valuearray:
        diff_i = abs(val - value)
        if (diff_i <= diff):
            diff = diff_i
            valueout = val

    return valueout



def EvaluateSpeedAndLengthData(device, module, data, angle):   
    global targetSpeed
    angle =  angles[device - 1][module -1] * -1
    dataToEvaluate = jsonKeys2int(data[str(device)][str(module)])
    
    newlistData = GetSpecificDataToShow(dataToEvaluate)
    newlistData2 = GetSpecificDataToSolve(dataToEvaluate)

    t = list(newlistData2.keys())
    values = list(newlistData2.values())



    values = NewFilter(values, 5)
    values = NewFilter(values, 5)
    
    valuesToDelete = 10
    values = values[valuesToDelete:-valuesToDelete]
    t = t[valuesToDelete:-valuesToDelete]    


    fig_original = plt.figure(figsize=(10,10))
    gs2 = gridspec.GridSpec(1, 1) 
    AddSubPlot('Data 1 '+ str(180 - angle) + 'º', gs2[0], list(newlistData.keys()), list(newlistData.values()), 'b-', 'data', "Distance")



    fig = plt.figure(figsize=(10,10))
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')

    gs = gridspec.GridSpec(3, 1) 
    
    AddSubPlot('Data ' + str(180 - angle) + 'º', gs[0], t, values, 'b-', 'data', "Distance")

    data_1stdev = np.gradient(values)
    AddSubPlot('1st derivative' + str(180 - angle) + 'º', gs[1], t, data_1stdev, 'b-', 'data', "slope")
    
    data_2nddev = np.gradient(data_1stdev)
    AddSubPlot('2nd derivative' + str(180 - angle) + 'º', gs[2], t, data_2nddev, 'b-', 'data', "Impulse")


    indstart = [] 
    indend = []
    
    parameterlow = max(abs(max(data_2nddev)), abs(min(data_2nddev))) *0.7

    parameterlow = median(data_2nddev) * 10

    peaksindex = signal.find_peaks(data_2nddev)

    maxpiks = find_max(data_2nddev, peaksindex, t)

    parameterlow = data_2nddev[t.index(maxpiks[len(maxpiks) - 1])] *1.1

    indstart.append(t[0])    
    maxval = True
    for i in range(1, len(data_2nddev)):
        if (data_2nddev[i] >= parameterlow and maxval == False):
            maxval = True
            indend.append(t[i])
        elif (data_2nddev[i] < parameterlow and maxval == True):
            maxval = False
            indstart.append(t[i])

    indend.append(t[i])

    speed = 0
    stdspeed = 0

    if len(indstart) > len(indend):
        indstart.pop(0)
    elif len(indstart) < len(indend):
        indend.pop(len(indend) - 1)


    # Velocidades
    print("")
    if (len(indend)>0 and len(indstart)>0):
        speedarray = []
        distarray = []
        std1 = []
        abs1 = []
        for k in range(0, len(indend)):
            spd = []
            for i in range(indstart[k], indend[k]):
                value1 = dataToEvaluate[i]
                value2 = dataToEvaluate[i+1]
                spd.append(((value2 - value1) * cos(angle * pi / 180) / (1)) * 1000)

            if (len(spd) == 0):
                spd2 = 0
            else:
                avg = sum(spd) / len(spd)
                spd2 = [x for x in spd if x < avg + avg *0.3 and x > avg - avg *0.3]
                
            if (len(spd2) == 0):
                spd3 = 0
            else:
                spd3 = sum(spd2) / len(spd2)

            print("Velocidad (m/s) = " + str(spd3))
            print("Velocidad (km/h) = " + str(spd3 * 3.6))

            std2 = np.std(spd2)

            abs2 = 0
            if (len(spd2)>0):
                abs2 = AbsError(spd2, targetSpeed)

            speedarray.append(spd3)
            std1.append(std2)
            abs1.append(abs2)

        speed = closest(speedarray, targetSpeed)
        stdspeed = std1[(speedarray.index(speed))]
        absspeed = abs1[(speedarray.index(speed))]
    else:
        print("Error")

    
    # Longitudes
    print("")
    diffTime = []
    dt = []
    repeat = True
    for i in range(1, len(data_1stdev)):
        if (round(data_1stdev[i],3) == 0):
            if (repeat == True):
                dt.append(t[i])
            else:
                repeat = False
                diffTime.append(dt)
                dt = []
    if (repeat == True):
        diffTime.append(dt)


    lengthTime = 0
    for i in range(0, len(diffTime)):
        if (len(diffTime[i])> lengthTime):
            lengthTime = len(diffTime[i])

    length = lengthTime * speed * correctionParameter / 1000

    
    return speed, stdspeed, absspeed, length, str(180 - angle)

def GetFile(angles):
    file = ""
    folder = ""
    for i in range(0, len(angles)):
        if (angles[i] != 0):
            if (len(folder) > 0): 
                folder = folder + "_"
                file = file + "_"
            folder = folder + str(i + 1) + "-" + str(len(angles[i]))
            file = file + str(i + 1) + "["
            for j in range(0, len(angles[i])):
                if (j > 0): file = file + ","
                file = file + str(-1* angles[i][j])            
            file = file + "]"

    return 'Data/' + folder + '/' + file + '.json'



def EvaluateLength(device, module, data, angles, speed):   
    angle =  angles[device - 1][module -1] * -1
    dataToEvaluate = jsonKeys2int(data[str(device)][str(module)])
    
    newlistData = GetSpecificDataToShow(dataToEvaluate)
    newlistData2 = GetSpecificDataToSolve(dataToEvaluate)

    t = list(newlistData2.keys())
    values = list(newlistData2.values())



    values = NewFilter(values, 5)
    values = NewFilter(values, 5)
    
    valuesToDelete = 10
    values = values[valuesToDelete:-valuesToDelete]
    t = t[valuesToDelete:-valuesToDelete]    


    fig_original = plt.figure(figsize=(10,10))
    gs2 = gridspec.GridSpec(1, 1) 
    AddSubPlot('Data 1 '+ str(180 - angle) + 'º', gs2[0], list(newlistData.keys()), list(newlistData.values()), 'b-', 'data', "Distance")



    fig = plt.figure(figsize=(10,10))
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')

    gs = gridspec.GridSpec(3, 1) 
    
    AddSubPlot('Data ' + str(180 - angle) + 'º', gs[0], t, values, 'b-', 'data', "Distance")

    data_1stdev = np.gradient(values)
    AddSubPlot('1st derivative' + str(180 - angle) + 'º', gs[1], t, data_1stdev, 'b-', 'data', "Slope")
    
    data_2nddev = np.gradient(data_1stdev)
    AddSubPlot('2nd derivative' + str(180 - angle) + 'º', gs[2], t, data_2nddev, 'b-', 'data', "Impulse")


    indstart = [] 
    indend = []
    
    parameterlow = max(abs(max(data_2nddev)), abs(min(data_2nddev))) *0.7

    parameterlow = median(data_2nddev) * 10

    peaksindex = signal.find_peaks(data_2nddev)

    maxpiks = find_max(data_2nddev, peaksindex, t)

    parameterlow = data_2nddev[t.index(maxpiks[len(maxpiks) - 1])] * 1.1

    indstart.append(t[0])    
    maxval = True
    for i in range(1, len(data_2nddev)):
        if (data_2nddev[i] >= parameterlow and maxval == False):
            maxval = True
            indend.append(t[i])
        elif (data_2nddev[i] < parameterlow and maxval == True):
            maxval = False
            indstart.append(t[i])

    indend.append(t[i])

    # speed = 0

    # Velocidades
    # print("")
    # if (len(indend)>0 and len(indstart)>0):
    #     speedarray = []
    #     distarray = []
    #     for k in range(0, len(indend)):
    #         spd = []
    #         for i in range(indstart[k], indend[k]):
    #             value1 = dataToEvaluate[i]
    #             value2 = dataToEvaluate[i+1]
    #             spd.append(((value2 - value1) * cos(angle * pi / 180) / (1)) * 1000)
            
    #         avg = sum(spd) / len(spd)
    #         spd2 = [x for x in spd if x < avg + avg *0.3 and x > avg - avg *0.3]
    #         if (len(spd2) == 0):
    #             spd3 = 0
    #         else:
    #             spd3 = sum(spd2) / len(spd2)

    #         print("Velocidad (m/s) = " + str(spd3))
    #         print("Velocidad (km/h) = " + str(spd3 * 3.6))

    #         speedarray.append(spd3)

    #     speed = max(speedarray)
    # else:
    #     print("Error")

    
    # Longitudes
    print("")
    diffTime = []
    dt = []
    repeat = True
    for i in range(1, len(data_1stdev)):
        if (round(data_1stdev[i],3) == 0):
            if (repeat == True):
                dt.append(t[i])
            else:
                repeat = False
                diffTime.append(dt)
                dt = []
    if (repeat == True):
        diffTime.append(dt)


    lengthTime = 0
    for i in range(0, len(diffTime)):
        if (len(diffTime[i])> lengthTime):
            lengthTime = len(diffTime[i])

    length = lengthTime * speed * correctionParameter / 1000

    return length, str(180 - angle)


def SaveData(angles, speeds, stdspeeds, absspeeds, lengths):
    global targetSpeed
    global targetLength

    datamsg = {}
    print("")
    print("")
    print("--------------------- Velocidades ---------------------------")
    datamsg["Speed"] = {}
    datamsg["Speed"]["Speed"] = {}
    datamsg["Speed"]["STD"] = {}
    datamsg["Speed"]["Absolute Error"] = {}
    datamsg["Speed"]["Relative Error"] = {}
    for i in range(0, len(speeds)):
        datamsg["Speed"]["Speed"][str(angles[i])] = str(speeds[i])+ " m/s"
        print("Velocidad con el ángulo " + str(angles[i]) + " = " + str(speeds[i]) + " m/s;  " + str(speeds[i] * 3.6) + "km/h")
        datamsg["Speed"]["STD"][str(angles[i])] = str(stdspeeds[i])+ " m/s"
        print("STD con el ángulo " + str(angles[i]) + " = " + str(stdspeeds[i]) + " m/s")
        datamsg["Speed"]["Absolute Error"][str(angles[i])] = str(absspeeds[i])+ " %"
        print("Absolute Error con el ángulo " + str(angles[i]) + " = " + str(absspeeds[i]) + " %")
        datamsg["Speed"]["Relative Error"][str(angles[i])] = str(absspeeds[i]/targetSpeed*100) + " %"
        print("Relative Error con el ángulo " + str(angles[i]) + " = " + str(absspeeds[i]/targetSpeed*100) + " %")
        print("------------------------------------------------")



    print("")
    print("----------------------- Longitudes -------------------------")
    datamsg["Length"] = {}
    datamsg["Length"]["Length"] = {}
    datamsg["Length"]["Absolute Error"] = {}
    datamsg["Length"]["Relative Error"] = {}
    for i in range(0, len(lengths)):
        datamsg["Length"]["Length"][str(angles[i])] = str(lengths[i])+ " m"
        print("Longitud con el ángulo " + str(angles[i]) + " = " + str(lengths[i]) + " m")
        datamsg["Length"]["Absolute Error"][str(angles[i])] = str(abs(lengths[i] - targetLength)) + " %"
        print("Absolute Error con el ángulo " + str(angles[i]) + " = " + str(abs(lengths[i] - targetLength)) + " %")
        datamsg["Length"]["Relative Error"][str(angles[i])] = str(abs(lengths[i] - targetLength)*100/targetLength)+ " %"
        print("Relative Error con el ángulo " + str(angles[i]) + " = " + str(abs(lengths[i] - targetLength)*100/targetLength)+ " %")
        print("------------------------------------------------")


    with open("Data/Data_speed" + str(targetSpeed) + ".json", 'w') as f:
        json.dump(datamsg, f)


def Main():
    global simulationStepFactor
    global angles
    global targetSpeed
    global targetLength

    file = GetFile(angles)
    print(file)
    with open(file, 'r') as f:
        data = json.load(f)

    
    with open('Data/Manifest.json', 'r') as f:
        dataManifest = json.load(f)


    simulationStepFactor = float(dataManifest["Simulation step"][0:len(dataManifest["Simulation step"])-3])

    speed1, stdspeed1, absspeed1, length1, angle1 = EvaluateSpeedAndLengthData(1, 1, data, angles)
    plt.tight_layout(h_pad = 1)
    speed2, stdspeed2, absspeed2, length2, angle2 = EvaluateSpeedAndLengthData(1, 5, data, angles)
    plt.tight_layout(h_pad = 1)
    speed3, stdspeed3, absspeed3, length3, angle3 = EvaluateSpeedAndLengthData(1, 2, data, angles)
    plt.tight_layout(h_pad = 1)
    speed4, stdspeed4, absspeed4, length4, angle4 = EvaluateSpeedAndLengthData(1, 4, data, angles)
    plt.tight_layout(h_pad = 1)



    length90, angle90 = EvaluateLength(1, 3, data, angles, speed2)
    plt.tight_layout(h_pad = 1)

    angles = [angle2, angle4, angle3, angle1, angle90]
    speeds = [speed2, speed4, speed3, speed1]
    stdspeeds = [stdspeed2, stdspeed4, stdspeed3, stdspeed1]
    absspeeds = [absspeed2, absspeed4, absspeed3, absspeed1]
    lengths = [length2, length4, length3, length1, length90]

    
    SaveData(angles, speeds, stdspeeds, absspeeds, lengths)


     
    plt.show()    


    x = 0