from bagpy import bagreader
import bagpy
import CSVtoMsg
from CSVtoMsg import CSVtoMsg


class CSVGenerator:

    def __init__(self, bag_file):
        self.bag_file_name = bag_file
        self.b = bagreader(bag_file)
        self.csv_vel = []
        self.csv_odom = []
        self.csv_steering = []
        self.csv_front_laser_pointers = []

    # testing purposes
    def read_data(self):
        self.csv_vel = self.b.vel_data()
        self.csv_odom = self.b.odometry_data()
        self.csv_steering = self.b.wrench_data()
        self.csv_front_laser_pointers = self.b.laser_data()

    def run(self):
        self.read_data()  # read data for testing i think
        to_message = CSVtoMsg(self.bag_file_name)  # convert the csvs to msgs
        to_message.run()
