from machine import Pin, PWM
from time import sleep

m1 = [PWM(Pin(2)), PWM(Pin(3))] # Motor m1, pins IN1 and IN2 are connected to pins 2 and 3

#Add more motors as needed. Can reuse the functions below for all motors.


# minspeed is zero, maxspeed is 65025
def spin_forward(motor, speed):
    motor[0].freq(1000)
    motor[1].freq(1000)
    motor[0].duty_u16(speed)
    motor[1].duty_u16(0)
    sleep(0.0001)
    
def spin_backward(motor, speed):
    motor[0].freq(1000)
    motor[1].freq(1000)
    motor[0].duty_u16(0)
    motor[1].duty_u16(speed)
    sleep(0.0001)
    
def brake(motor):
    motor[0].freq(1000)
    motor[1].freq(1000)
    motor[0].duty_u16(0)
    motor[1].duty_u16(0)
    sleep(0.0001)
    
spin_forward(m1, 65025)
sleep(1)
spin_backward(m1, 65025)
sleep(1)
brake(m1)
