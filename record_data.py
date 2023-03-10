import time
import csv
import busio
import adafruit_bno055
import adafruit_mpl3115a2

# Initialize IMU and altitude sensor
i2c = busio.I2C(SCL, SDA)
imu = adafruit_bno055.BNO055_I2C(i2c, 0x28)
alt = adafruit_mpl3115a2.MPL3115A2(i2c, address=0x60)

# Open CSV files for writing
imu_file = open('imu_data.csv', 'w', newline='')
imu_writer = csv.writer(imu_file)
alt_file = open('alt_data.csv', 'w', newline='')
alt_writer = csv.writer(alt_file)

# Write header rows to CSV files
imu_writer.writerow(['Time', 'Accelerometer X', 'Accelerometer Y', 'Accelerometer Z', 'Gyroscope X', 'Gyroscope Y', 'Gyroscope Z', 'Euler X', 'Euler Y', 'Euler Z', 'Quaternion W', 'Quaternion X', 'Quaternion Y', 'Quaternion Z'])
alt_writer.writerow(['Time', 'Altitude'])

# Read and log data from sensors
while True:
    # Get timestamp
    timestamp = time.monotonic()

    # Read IMU data
    accel_x, accel_y, accel_z = imu.acceleration
    gyro_x, gyro_y, gyro_z = imu.gyro
    euler_x, euler_y, euler_z = imu.euler
    quat_w, quat_x, quat_y, quat_z = imu.quaternion

    # Write IMU data to CSV
    imu_writer.writerow([timestamp, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, euler_x, euler_y, euler_z, quat_w, quat_x, quat_y, quat_z])

    # Read altitude data
    altitude = alt.altitude

    # Write altitude data to CSV
    alt_writer.writerow([timestamp, altitude])

    # Wait for next sample
    time.sleep(0.1)
