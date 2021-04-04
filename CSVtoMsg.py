import csv
import cantools
import can
import os
import math

from can import Message


class CSVtoMsg:

    def __init__(self, bag_name):
        self.db = cantools.database.load_file('dbc/toyota_rav4_2019.dbc')  # retrieve the dbc and set it to the database
        self.files = []
        # takes the bag file and removes the .bag to return the file where all the csvs are stored
        bag_name = bag_name.replace(".bag","")
        # here we are appending all file names into our self.files attribute using the os library
        # name .bag change this to account for the output of wills code, a new directory should be created named after the bag file
        # bag_name.replace(".bag", "") # remove .bag
        print(os.getcwd() + "/" + bag_name)
        for file_name in os.listdir(os.getcwd() + "/" + bag_name):  # get directory
            if file_name.endswith(".csv"):  # if the file we are looking at append to self.files
                x = os.getcwd() + "/" + bag_name + "/" + file_name  # specify the path
                new_file_name = x.replace("catvehicle-", '')  # remove the unnecessary catvehicle
                os.rename(x, new_file_name)  # rename the old file with new file
                self.files.append(new_file_name)  # must specify where in the directory even more to use in code

    def get_num_files(self):
        return len(self.files)

    def parse_files(self):
        for file in self.files:
            case = file
            with open(file) as csv_file:
                message_type = self.chooseMsg(file)  # type of message we are sending
                self.read_file(csv_file, message_type)

    def read_file(self, csv_file, message_type):
        msgs = []
        csv_reader = csv.reader(csv_file, delimiter=',')  # specify the delimiter and its respective csv
        line_count = 0  # line count to keep track of where we are
        for row in csv_reader:  # go through row by row
            if line_count == 0:  # if top line, save it and print it
                top_line = row  # storing the top line
                # print(" ".join(top_line))
            else:
                if message_type == "SPEED":
                    msgs.append(self.data_to_dbc_speed(row))  # convert row to CANmessage
                elif message_type == "KINEMATICS":
                    msgs.append(self.data_to_dbc_steer(row))  # convert row to CANmessage
            line_count += 1
        if message_type == "SPEED":
            self.write_file(msgs, "SPEED")  # write to txt file
        elif message_type == "KINEMATICS":
            self.write_file(msgs, "KINEMATICS")

        # pull topic line from csv
        # parse everything after that
        # line by line we will create a new message using the DBC format in CANtools
        # add message to either a text file or a list that will later print or pass to another function

    def write_file(self, msgs, message_type):
        file_name = os.getcwd() + "/Outputs/" + message_type.lower() + "CANData.txt"
        if (os.path.exists(os.getcwd() + "/Outputs/")):  # iff output directory exists, add another output file
            out_file = open(file_name, "w")
        else:  # see if directory exists, if not add directory
            os.mkdir(os.getcwd() + "/Outputs/")
            out_file = open(file_name, "w")

        for msg in msgs:
            out_file.write(str(msg) + "\n")

    # return the message type we will be using to format our data
    # case is the file name, which should contain what message we are processing
    def chooseMsg(self, file_name):
        if "vel" in file_name:
            return "SPEED"
        elif "steer" in file_name:
            return "KINEMATICS"
        else:
            return None

    # message type is speed, so we must convert with speed
    def data_to_dbc_speed(self, csv_line):
        avg_speed = math.sqrt(float(csv_line[1]) ** 2 + float(csv_line[3]) ** 2) # calc average speed
        msg_type = self.db.get_message_by_name("SPEED") # get message by name
        data = msg_type.encode({'ENCODER': 0, 'CHECKSUM': 0, 'SPEED': avg_speed})
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    def data_to_dbc_steer(self, csv_line):
        torque = float(csv_line[6])  # calculate torque based on csv data
        msg_type = self.db.get_message_by_name("KINEMATICS") # get message by name
        data = msg_type.encode({'ACCEL_Y': 0, 'YAW_RATE': 0, 'STEERING_TORQUE': abs(torque)}) # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    def run(self):
        #db = cantools.database.load_file('dbc/toyota_rav4_2019.dbc')  # retrieve the dbc and set it to the database
        # print(db.messages)  # show the messages for debugging
        self.parse_files()  # parse the files that we searched for earlier
        #speed_message = db.get_message_by_name('KINEMATICS')  # define speed message
        #print(speed_message)
        #print(speed_message.signals)

    # def line_to_dbc_form(self, csv_line):
    # here we will convert the line to a can tools dbc file
    # follow documentation on how to convert a raw can message to a dbc message

# def main():
#     bag_name = "CSVs"
#     test = CSVtoMsg(bag_name)
#     test.run()
#     print(test.get_num_files())
#
#
# main()
