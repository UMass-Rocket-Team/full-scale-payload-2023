from machine import Pin, PWM #import necessary packages
from time import sleep

IN1 = Pin(3, Pin.OUT) #define pins for controlling motor direction
IN2 = Pin(2, Pin.OUT)

speed = PWM(Pin(4)) # define pin for controlling motor speed using PWM
speed.freq(1000) # PWM frequency


# info specific to motor being used
# max speed: 60000
# min speed: 30000



def map_speed(speed_percentage): # Takes values 0-100 as input and returns PWM values for use with the motor control
    return 30000 + 300 * speed_percentage

def spin_forward_orientation(speed): # Speed controlled motor spinning forward
        s = int(map_speed(speed))
        speed = PWM(Pin(4))
        speed.freq(1000)
        speed.duty_u16(s)
        IN1.low()  #spin forward
        IN2.high()
        if speed == 0:
            brake()

def spin_backward_orientation(speed): # Speed controlled motor spinning backward
        s = int(map_speed(speed))
        speed = PWM(Pin(4))
        speed.freq(1000)
        speed.duty_u16(s)
        IN1.high()  #spin backward
        IN2.low()
        if speed == 0:
            brake()

def brake_orientation(): # Turn off the motor entirely
        print("brake pressed")
        IN1.low()  #stop
        IN2.low()



for i in range(0,100): #Sample loop demonstrating motor speed being controlled
    sleep(0.05)
    print(i)
    spin_forward_orientation(i)

sleep(1) # wait for a second
brake_orientation() # turn off the motor

