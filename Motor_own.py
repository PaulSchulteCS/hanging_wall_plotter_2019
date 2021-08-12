import time
import RPi.GPIO as GPIO


'''
A = 7
B = 11
C = 13
D = 15



      1  2  3  4  5  6  7  8

Pin1  x  x                 x
Pin2     x  x  x
Pin3           x  x  x
Pin4                 x  x  x


'''
class Motor:
    A = 0
    B = 5
    C = 6
    D = 13

    def __init__(self,A,B,C,D):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(A, GPIO.OUT)
        GPIO.setup(B, GPIO.OUT)
        GPIO.setup(C, GPIO.OUT)
        GPIO.setup(D, GPIO.OUT)
        self.A = A
        self.B = B
        self.C = C
        self.D = D

    def __del__(self):
        self.GPIO_SETUP(0,0,0,0, 1, 512 * 8)



    def GPIO_SETUP(self, a,b,c,d,time1, degrees):   # degrees = Anzahl der Aufrufe von GPIO_SETUP in einem Aufruf von rt() oder lt()
        GPIO.output(self.A, a)
        GPIO.output(self.B, b)
        GPIO.output(self.C, c)
        GPIO.output(self.D, d)
        time.sleep(time1 / degrees)

    def rt(self, deg, time):

        '''
        siehe "http://robocraft.ru/files/datasheet/28BYJ-48.pdf"
        unter Stride Angle: 5.625° /64 => 0.087890625  (Umdrehung in ° bei einem Schritt)
        0.087890625 * 8 Schritte = 0.703125 für eine interne Umdrehung
        360 / 0.703125 = 512.0 Schritte für eine Umdrehung
        '''
        full_circle = 512.0
        degree = (full_circle/360)*deg    #CHANGE
        degree_save= (full_circle/360)*deg   #CHANGE
        self.GPIO_SETUP(0,0,0,0, time, degree_save * 8)

        while degree > 0.0:
            self.GPIO_SETUP(1,0,0,0, time, degree_save * 8)
            self.GPIO_SETUP(1,1,0,0, time, degree_save * 8)
            self.GPIO_SETUP(0,1,0,0, time, degree_save * 8)
            self.GPIO_SETUP(0,1,1,0, time, degree_save * 8)
            self.GPIO_SETUP(0,0,1,0, time, degree_save * 8)
            self.GPIO_SETUP(0,0,1,1, time, degree_save * 8)
            self.GPIO_SETUP(0,0,0,1, time, degree_save * 8)
            self.GPIO_SETUP(1,0,0,1, time, degree_save * 8)
            degree -= 1
        self.GPIO_SETUP(0,0,0,0, time, degree_save * 8)

    def lt(self, deg, time):

        full_circle = 512.0
        degree = (full_circle/360)*deg       #CHANGE
        degree_save= (full_circle/360)*deg    #CHANGE
        self.GPIO_SETUP(0,0,0,0, time, degree_save * 8)

        while degree > 0.0:
            self.GPIO_SETUP(1,0,0,1, time, degree_save * 8)
            self.GPIO_SETUP(0,0,0,1, time, degree_save * 8)
            self.GPIO_SETUP(0,0,1,1, time, degree_save * 8)
            self.GPIO_SETUP(0,0,1,0, time, degree_save * 8)
            self.GPIO_SETUP(0,1,1,0, time, degree_save * 8)
            self.GPIO_SETUP(0,1,0,0, time, degree_save * 8)
            self.GPIO_SETUP(1,1,0,0, time, degree_save * 8)
            self.GPIO_SETUP(1,0,0,0, time, degree_save * 8)
            degree -= 1
        self.GPIO_SETUP(0,0,0,0, time, degree_save * 8)

#MAIN #########################




