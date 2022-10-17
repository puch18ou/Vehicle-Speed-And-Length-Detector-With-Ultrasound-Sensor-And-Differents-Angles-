import Simulation as simulation
import ShowGraphics as showGraphics
import sys

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def CalculateDevicesAndModules():
    correct = False

    # Set number of devices
    devices = 1
    while (correct == False):
        inp = str(input("Number of devices (1, 2 or 3): "))
        if (inp == "1" or inp == "2" or inp == "3"):
            devices = int(inp)
            correct = True
        else:
            print("Data is not correct")

    devicesEnable = [True,False,False]
    for i in range(0, devices):
        devicesEnable[i] = True

    # Set number of modules per device   
    modules = []
    for i in range(0, devices):
        correct = False
        while (correct == False):
            inp = str(input("Number of modules (1 to 5) for device " + str(i+1) + ": " ))
            if (inp == "1" or inp == "2" or inp == "3" or inp == "4" or inp == "5"):
                modules.append(int(inp))
                correct = True
            else:
                print("Data is not correct")


    
    # Set angles of each modules per device       
    angles = []
    correct = False
    for i in range(0, devices):
        anglesdevice = []
        for j in range(0, modules[i]):
            correct = False
            while (correct == False):
                inp = input("Set angle (30º to 150º) module " + str(j+1) + " for device " + str(i+1) +  ": " )
                if (RepresentsInt(inp) and int(inp) >= 30 and int(inp) <= 150 and not(int(inp) in anglesdevice)):
                    anglesdevice.append(-1 * int(inp))
                    correct = True
                else:
                    print("Data is not correct")
        angles.append(anglesdevice)




    angulo_start = []
    for i in range(0, len(devicesEnable)):
        if not(devicesEnable[i]):
            angles.append(0)

    return angles

speed = 10

class Main:
    simulation.doAllSimulations = False
    simulation.simulationindex = 0
    simulation.speed = speed # m/s
    simulation.sensorFrequency = 1000 # Hz
    simulation.showSimulation = False
    simulation.angulo_start = [[-30,-45,-90,-135,-150],0,0] #CalculateDevicesAndModules()
    simulation.Main()
    showGraphics.angles = simulation.angulo_start
    showGraphics.targetSpeed = speed
    showGraphics.targetLength = 3.7
    showGraphics.Main()

    x = 0