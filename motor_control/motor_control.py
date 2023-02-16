from machine import Pin, PWM
from time import sleep

IN1 = Pin(3, Pin.OUT)
IN2 = Pin(2, Pin.OUT)

speed = PWM(Pin(4))
speed.freq(1000)

# max speed: 60000
# min speed: 30000



def map_speed(speed_percentage):
    return 30000 + 300 * speed_percentage

def spin_forward(speed):
        s = int(map_speed(speed))
        speed = PWM(Pin(4))
        speed.freq(1000)
        speed.duty_u16(s)
        IN1.low()  #spin forward
        IN2.high()
        if speed == 0:
            brake()

def spin_backward(speed):
        s = int(map_speed(speed))
        speed = PWM(Pin(4))
        speed.freq(1000)
        speed.duty_u16(s)
        IN1.high()  #spin backward
        IN2.low()
        if speed == 0:
            brake()

def brake():
        print("brake pressed")
        IN1.low()  #stop
        IN2.low()



for i in range(0,100):
    sleep(0.05)
    print(i)
    spin_forward(i)

sleep(1)
brake()

