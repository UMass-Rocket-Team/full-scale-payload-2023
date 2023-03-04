import rocket_time
from pandas import read_csv
import singleton
class DataSimulator(metaclass=singleton.Singleton):
    def __init__(self):
        #open a csv file located in the downloads folder with the data to read from
        #read the data from the csv file
        with open(r'simulation_files/sim_data.csv', "r") as f:
            self.data = read_csv(f)
        #create a new rocket timer
        self.timer = rocket_time.RocketTimer()
    def get_data_at_time(self):
        #Return the data from self.data at the time closes to the current time
        cur_time = self.timer.time_since_init_ms()
        self.data = self.data[self.data["Time"] >= cur_time]
        if self.data.empty:
            raise StopIteration
        return self.data.iloc[0]

    def accel(self):
        #Return the acceleration data from self.data at the time closes to the current time using the get_data_at_time function
        data = self.get_data_at_time()
        return data["Accel_X"], data["Accel_Y"], data["Accel_Z"]
        
    def altitude(self):
        #Return the altitude data from self.data at the time closes to the current time using the get_data_at_time function
        return self.get_data_at_time()["Altitude"]



# simulator = DataSimulator()
# controller = rocket_controller.RocketController()

# def print_accel():
#     print("Accel: " + str(simulator.accel()))
# def print_altitude():
#     print("Altitude: " + str(simulator.altitude()))
# controller.do_every([print_accel, print_altitude], [10, 10])

#PREVIOUS CODE TO GENERATE RANDOM DATA
#from random import uniform

# def generate_imu_data_low():
#     return (uniform(0, 1), uniform(0, 1), uniform(9, 9.8))

# def generate_imu_data_high():
#     return (uniform(5.3, 10), uniform(5.3, 10), uniform(5.3, 10))

# def generate_altitude_data_low():
#     return uniform(0, 300)

# def generate_altitude_data_high():
#     return uniform(400, 5000)