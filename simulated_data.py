from random import uniform
def generate_imu_data_low():
    return (uniform(0, 1), uniform(0, 1), uniform(9, 9.8))

def generate_imu_data_high():
    return (uniform(5.3, 10), uniform(5.3, 10), uniform(5.3, 10))

def generate_altitude_data_low():
    return uniform(0, 300)

def generate_altitude_data_high():
    return uniform(400, 5000)