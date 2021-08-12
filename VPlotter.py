import math
from threading import Thread
import Motor_own
import time
import Servo

class VPlotter:
    
    x= 0 #actual position
    y= 0 #actual position
    distanceX= 0
    distanceY= 0
    max_geschwindigkeit= 0
    
    
    def __init__(self, distanceBetweenMotors, distanceYtoOrigin, pin1, pin2, pin3, pin4, pin5, pin6, pin7, pin8, geschw, servo):
        self.distanceX= distanceBetweenMotors
        self.distanceY= distanceYtoOrigin
        self.motor1 = Motor_own.Motor(pin1, pin2, pin3, pin4)
        self.motor2 = Motor_own.Motor(pin5, pin6, pin7, pin8)
        self.xa= self.distanceX / 2
        self.xb= self.distanceX / 2
        self.max_geschwindigkeit= geschw
        self.x= 0
        self.y= 0
    
        self.servo= Servo.Servo(servo)
        
        
    def GoOrigin(self):
        pass
    
    def TogglePen(self, richtung):
        if richtung < 0:
            print("Stift unten")   # später Stift herunterfahren
            self.servo.down()
            
        else:
            print("Stift oben") # später Stift hochfahren
            self.servo.up()
    
    def GoPoint(self, x, y):
        
        a1= math.sqrt((self.xa + self.x) ** 2 + (self.distanceY - self.y) ** 2)
        b1= math.sqrt((self.xb - self.x) ** 2 + (self.distanceY - self.y) ** 2)
        
        self.x= x
        self.y= y
        print("X: " + str(self.x), "Y: " + str(self.y))
        
        a2= math.sqrt((self.xa + x) ** 2 + (self.distanceY - y) ** 2)
        b2= math.sqrt((self.xb - x) ** 2 + (self.distanceY - y) ** 2)
        
        print("A ",a2-a1)
        print("B ", b2-b1)
        
        if abs(a2 - a1) >= abs(b2 - b1):
            t1 = Thread(target = self.MotorBewegen, args=(1, a2 - a1, (a2 - a1) / self.max_geschwindigkeit,))
            t2 = Thread(target = self.MotorBewegen, args=(2, b2 - b1, (a2 - a1) / self.max_geschwindigkeit,))
            t1.start()
            t2.start()
            
            t1.join() # look, if thread is finished
            t2.join() # look, if thread is finished
            
            #time.sleep(abs((a2 - a1) / self.max_geschwindigkeit) + 3)  #3 ERSETZEN undzwar gucken, ob thread vorbei
                
            
        else:
            t1 = Thread(target = self.MotorBewegen, args=(1, a2 - a1, (b2 - b1) / self.max_geschwindigkeit,))
            t2 = Thread(target = self.MotorBewegen, args=(2, b2 - b1, (b2 - b1) / self.max_geschwindigkeit,))
            t1.start()
            t2.start()
            
            t1.join() # look, if thread is finished
            t2.join() # look, if thread is finished
                
            #time.sleep(abs((b2 - b1) / self.max_geschwindigkeit) + 3)  #3 ERSETZEN undzwar gucken, ob thread vorbei 
            
        
                
    def MotorBewegen(self, motor, length, time):
        if length == 0:
            return
        if motor == 1:
            if length >= 0:
                self.motor1.lt(length/(25/360), abs(time))   #25mm pro 360° also: 25/360 mm pro grad
            else:
                self.motor1.rt(-length/(25/360), abs(time))

        elif motor == 2:
            if length >= 0:
                self.motor2.rt(length/(25/360), abs(time))
            else:
                self.motor2.lt(-length/(25/360), abs(time))
                
                
                
                
                
                
                
     

    def Quadrant(self, x, y, mx, my):
        if x >= mx:
            if y >= my:
                return 1  # erster Quadrant
            elif y < my:
                return 4  # vierter Quadrant
        elif x < mx:
            if y >= my:
                return 2  # zweiter Quadrant
            elif y < my:
                return 3  # dritter Quadrant
    
     

    def arc(self, direction, dir_x, dir_y, i, j):
            mx= self.x + i
            my= self.y + j
            radius= math.sqrt(i ** 2 + j ** 2)
            print("Radius:", radius)
        
            #for x in range(self.x, dir_x, 0.1):
        
            if direction == 2:
                print("G02")
                print("X AND Y", self.x, self.y)
                 
                 
                quadrant_start= self.Quadrant(self.x, self.y, mx, my)
                quadrant_pos= quadrant_start # aktuelle position
                quadrant_end= self.Quadrant(dir_x, dir_y, mx, my)
                
                while quadrant_pos != quadrant_end :            #geht bis zum Anfang des letzen Quadrantens
                    if quadrant_pos == 1 :
                
                        arc_x= self.x + 1
                        while arc_x < mx + radius:
                            arc_y= math.sqrt(radius**2 - (arc_x- mx)**2) + my
                            self.GoPoint(arc_x, arc_y)
                            arc_x+= 1
                            
                        arc_x= mx + radius - 0.1
                        arc_y= math.sqrt(radius**2 - (arc_x- mx)**2) + my
                        self.GoPoint(arc_x, arc_y)            #GEHE AUCH WIRKLICH BIS ZUM ENDE DES ERSTEN QUADRANTEN
                        quadrant_pos= 4
                        
                    elif quadrant_pos == 2 :
                
                        arc_x= self.x + 1
                        while arc_x < mx:
                            arc_y= math.sqrt(radius**2 - (arc_x- mx)**2) + my
                            self.GoPoint(arc_x, arc_y)
                            arc_x+= 1
                            
                        arc_x= mx
                        arc_y= math.sqrt(radius**2 - (arc_x- mx)**2) + my
                        self.GoPoint(arc_x, arc_y)            #GEHE AUCH WIRKLICH BIS ZUM ENDE DES ZWEITEN QUADRANTEN
                        quadrant_pos= 1
                    
                        
                    elif quadrant_pos == 3:
                        arc_x= self.x - 1
                        while arc_x > mx - radius:
                            arc_y= -math.sqrt(radius**2 - (arc_x- mx)**2) + my
                            self.GoPoint(arc_x, arc_y)
                            arc_x-= 1
                            
                        arc_x= mx - radius + 0.1
                        arc_y= math.sqrt(radius**2 - (arc_x- mx)**2) + my
                        self.GoPoint(arc_x, arc_y)            #GEHE AUCH WIRKLICH BIS ZUM ENDE DES DRITTEN QUADRANTEN
                        quadrant_pos= 2
                        
                    elif quadrant_pos == 4:
                        arc_x= self.x - 1
                        while arc_x > mx:
                            arc_y= -math.sqrt(radius**2 - (arc_x- mx)**2) + my
                            self.GoPoint(arc_x, arc_y)
                            arc_x-= 1
                            
                        arc_x= mx
                        arc_y= -math.sqrt(radius**2 - (arc_x- mx)**2) + my
                        self.GoPoint(arc_x, arc_y)            #GEHE AUCH WIRKLICH BIS ZUM ENDE DES VIERTEN QUADRANTEN
                        quadrant_pos= 3
                        
                        
                
                
                if quadrant_pos == 1 or quadrant_pos == 2:
                    arc_x= self.x + 1
                    while arc_x < dir_x:
                        arc_y= math.sqrt(radius**2 - (arc_x- mx)**2) + my
                        self.GoPoint(arc_x, arc_y)
                        arc_x+= 1
                    self.GoPoint(dir_x, dir_y)            #GEHE AUCH WIRKLICH BIS ZUM PUNKT
                        
                elif quadrant_pos == 3 or quadrant_pos == 4:
                    arc_x= self.x - 1
                    while arc_x > dir_x:
                        arc_y= -math.sqrt(radius**2 - (arc_x- mx)**2) + my
                        self.GoPoint(arc_x, arc_y)
                        arc_x-= 1
                    self.GoPoint(dir_x, dir_y)            #GEHE AUCH WIRKLICH BIS ZUM PUNKT
                
                
                
                
                
            elif direction == 3:
                print("G03")
                print("X AND Y", self.x, self.y)
                 
                 
                quadrant_start= self.Quadrant(self.x, self.y, mx, my)
                quadrant_pos= quadrant_start # aktuelle position
                quadrant_end= self.Quadrant(dir_x, dir_y, mx, my)
                
                while quadrant_pos != quadrant_end :            #geht bis zum Anfang des letzen Quadrantens
                    if quadrant_pos == 1 :
                
                        arc_x= self.x - 1
                        while arc_x > mx:
                            arc_y= math.sqrt(radius**2 - (arc_x- mx)**2) + my
                            self.GoPoint(arc_x, arc_y)
                            arc_x-= 1
                            
                        arc_x= mx
                        arc_y= math.sqrt(radius**2 - (arc_x- mx)**2) + my
                        self.GoPoint(arc_x, arc_y)            #GEHE AUCH WIRKLICH BIS ZUM ENDE DES ERSTEN QUADRANTEN
                        quadrant_pos= 2
                        
                    elif quadrant_pos == 2 :
                
                        arc_x= self.x - 1
                        while arc_x > mx - radius:
                            arc_y= math.sqrt(radius**2 - (arc_x- mx)**2) + my
                            self.GoPoint(arc_x, arc_y)
                            arc_x-= 1
                            
                        arc_x= mx - radius + 0.1
                        arc_y= math.sqrt(radius**2 - (arc_x- mx)**2) + my
                        self.GoPoint(arc_x, arc_y)            #GEHE AUCH WIRKLICH BIS ZUM ENDE DES ZWEITEN QUADRANTEN
                        quadrant_pos= 3
                    
                        
                    elif quadrant_pos == 3:
                        arc_x= self.x + 1
                        while arc_x < mx:
                            arc_y= -math.sqrt(radius**2 - (arc_x- mx)**2) + my
                            self.GoPoint(arc_x, arc_y)
                            arc_x+= 1
                            
                        arc_x= mx
                        arc_y= -math.sqrt(radius**2 - (arc_x- mx)**2) + my
                        self.GoPoint(arc_x, arc_y)            #GEHE AUCH WIRKLICH BIS ZUM ENDE DES DRITTEN QUADRANTEN
                        quadrant_pos= 4
                        
                    elif quadrant_pos == 4:
                        arc_x= self.x + 1
                        while arc_x < mx + radius:
                            arc_y= -math.sqrt(radius**2 - (arc_x- mx)**2) + my
                            self.GoPoint(arc_x, arc_y)
                            arc_x+= 1
                            
                        arc_x= mx + radius - 0.1
                        arc_y= math.sqrt(radius**2 - (arc_x- mx)**2) + my
                        self.GoPoint(arc_x, arc_y)            #GEHE AUCH WIRKLICH BIS ZUM ENDE DES VIERTEN QUADRANTEN
                        quadrant_pos= 1
                        
                        
                
                
                if quadrant_pos == 1 or quadrant_pos == 2:
                    arc_x= self.x - 1
                    while arc_x  > dir_x:
                        arc_y= math.sqrt(radius**2 - (arc_x- mx)**2) + my
                        self.GoPoint(arc_x, arc_y)
                        arc_x-= 1
                    self.GoPoint(dir_x, dir_y)            #GEHE AUCH WIRKLICH BIS ZUM PUNKT
                        
                elif quadrant_pos == 3 or quadrant_pos == 4:
                    arc_x= self.x + 1
                    while arc_x < dir_x:
                        arc_y= -math.sqrt(radius**2 - (arc_x- mx)**2) + my
                        self.GoPoint(arc_x, arc_y)
                        arc_x+= 1
                    self.GoPoint(dir_x, dir_y)            #GEHE AUCH WIRKLICH BIS ZUM PUNKT
