# python3 ReadGCode.py <file>
import VPlotter
import sys

#Motor1
pin1= 0
pin2= 5
pin3= 6
pin4= 13

#Motor2
pin5= 12
pin6= 16
pin7= 20
pin8= 21

#servo
pinservo= 24

max_geschwindigkeit=25/6.175      # 25mm   &   6.175 s    pro Umdrehung 

#Origin
DISTANCEX= 422.5 # 42.25 cm
DISTANCEY= 430 # 43.0 cm


def start(file):
    
    a= open("GCode/" + file)
    global lines
    lines = a.readlines()
    a.close()
    
    plotter=  VPlotter.VPlotter(DISTANCEX, DISTANCEY, pin1, pin2, pin3, pin4, pin5, pin6, pin7, pin8, max_geschwindigkeit, pinservo)
    plotter.GoOrigin()
    
    for i in range(len(lines)):
        line= lines[i]
        if line.startswith("G00") or line.startswith("G01"):
            #print("Line" + str(i + 1) + ": " + lines[i])
            params= line.split(" ")
            if params[1].startswith("X"):
                plotter.GoPoint(float(params[1][1:]), float(params[2][1:]))
            elif params[1].startswith("Z"):
                plotter.TogglePen(float(params[1][1:]))
            
        elif line.startswith("G02"):
            params= line.split(" ")
            plotter.arc(2, float(params[1][1:]), float(params[2][1:]), float(params[4][1:]), float(params[5][1:]))
        
        elif line.startswith("G03"):
            params= line.split(" ")
            plotter.arc(3, float(params[1][1:]), float(params[2][1:]), float(params[4][1:]), float(params[5][1:]))
        
        

start(sys.argv[1])
    

        


    
    
    
    
'''    
for line in lines:
        #if line.startswith("G00"):
        print("Line " + str(lines.index(line)) + ": " + line)
'''