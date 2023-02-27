import random

def generate_imu_data_low():
    return (random.randint(0, 1.5), random.randint(0, 1.5), random.randint(9, 9.8))

def generate_imu_data_high():
    return (random.randint(5.3, 10), random.randint(5.3, 10), random.randint(5.3, 10))

def generate_altitude_data_low():
    return random.randint(0, 300)

def generate_altitude_data_high():
    return random.randint(300, 5000)