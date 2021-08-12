import RPi.GPIO as gpio
import time

class Servo:
    def __init__(self, servopin):
        gpio.setmode(gpio.BCM)
        gpio.setup(servopin, gpio.OUT)
        self.p = gpio.PWM(servopin, 50)
        self.p.start(2.5)
    
    def up(self):
        self.p.ChangeDutyCycle(2.5)
    
    def down(self):
        self.p.ChangeDutyCycle(7.5)
        
        
    
    '''
        p.ChangeDutyCycle(7.5) # nach links
        time.sleep(1)
        p.ChangeDutyCycle(12.5) # nach rechts
        time.sleep(1)
        p.ChangeDutyCycle(2.5) # nach vorne
        time.sleep(1)'''
    
