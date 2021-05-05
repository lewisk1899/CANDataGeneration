import csv
import cantools
import can
import os
import shutil
import math

from can import Message


class CSVtoMsg:

    def __init__(self, bag_name):
        self.db = cantools.database.load_file('dbc/toyota_rav4_2019.dbc')  # retrieve the dbc and set it to the database
        self.files = []
        # takes the bag file and removes the .bag to return the file where all the csvs are stored
        bag_name = bag_name.replace(".bag", "")
        # here we are appending all file names into our self.files attribute using the os library
        # name .bag change this to account for the output of wills code, a new directory should be created named after the bag file
        # bag_name.replace(".bag", "") # remove .bag
        # remove output folder and all files inside of it
        if(os.path.isfile(os.getcwd() + "/Outputs/")):
            try:
                shutil.rmtree(os.getcwd() + "/Outputs/")
            except OSError as e:
                print("Error: %s : %s" % (os.getcwd() + "/Outputs/", e.strerror))

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
        lka_msg = []
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
                elif message_type == "BRAKE":
                    msgs.append(self.data_to_dbc_brake(row))
                elif message_type == "LASER":
                    # left laser
                    msgs.append((self.data_to_dbc_left_laser_one(row, top_line), "TRACK_A_0"))
                    msgs.append((self.data_to_dbc_left_laser_two(row, top_line), "TRACK_A_1"))
                    msgs.append((self.data_to_dbc_left_laser_three(row, top_line), "TRACK_A_2"))
                    msgs.append((self.data_to_dbc_left_laser_four(row, top_line), "TRACK_A_3"))
                    msgs.append((self.data_to_dbc_left_laser_five(row, top_line), "TRACK_A_4"))
                    # front laser
                    msgs.append((self.data_to_dbc_front_laser_one(row, top_line), "TRACK_A_5"))
                    msgs.append((self.data_to_dbc_front_laser_two(row, top_line), "TRACK_A_6"))
                    msgs.append((self.data_to_dbc_front_laser_three(row, top_line), "TRACK_A_7"))
                    msgs.append((self.data_to_dbc_front_laser_four(row, top_line), "TRACK_A_8"))
                    msgs.append((self.data_to_dbc_front_laser_five(row, top_line), "TRACK_A_9"))
                    # right laser
                    msgs.append((self.data_to_dbc_right_laser_one(row, top_line), "TRACK_A_10"))
                    msgs.append((self.data_to_dbc_right_laser_two(row, top_line), "TRACK_A_11"))
                    msgs.append((self.data_to_dbc_right_laser_three(row, top_line), "TRACK_A_12"))
                    msgs.append((self.data_to_dbc_right_laser_four(row, top_line), "TRACK_A_13"))
                    msgs.append((self.data_to_dbc_right_laser_five(row, top_line), "TRACK_A_14"))
                    # lka needs lasers
                    msgs.append((self.data_to_dbc_laser_dst_check(row, top_line), "TOO_CLOSE_ALERT"))

            line_count += 1

        if message_type == "SPEED":
            self.write_file(msgs, "SPEED")  # write to txt file
        elif message_type == "KINEMATICS":
            self.write_file(msgs, "KINEMATICS")
        elif message_type == "LASER":
            self.write_file_laser(msgs)

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

    def write_file_laser(self, msgs):
        file_name = os.getcwd() + "/Outputs/" + "LASER".lower() + "CANData.txt"
        if (os.path.exists(os.getcwd() + "/Outputs/")):  # iff output directory exists, add another output file
            out_file = open(file_name, "w")
        else:  # see if directory exists, if not add directory
            os.mkdir(os.getcwd() + "/Outputs/")
            out_file = open(file_name, "w")

        for msg in msgs:
            out_file.write(msg[1] + ": " + str(msg[0]) + "\n")

    # return the message type we will be using to format our data
    # case is the file name, which should contain what message we are processing
    def chooseMsg(self, file_name):
        if "vel" in file_name:
            return "SPEED"
        elif "steer" in file_name:
            return "KINEMATICS"
        elif "laser" in file_name:
            return "LASER"
        else:
            return None

    def data_to_dbc_laser_dst_check(self, csv_line, info_line):
        indexes = (info_line.index("ranges_179"), info_line.index("ranges_178"), info_line.index("ranges_177"), info_line.index("ranges_176"), info_line.index("ranges_175"),
                  info_line.index("ranges_88"), info_line.index("ranges_89"), info_line.index("ranges_90"), info_line.index("ranges_91"), info_line.index("ranges_92"),
                  info_line.index("ranges_0"), info_line.index("ranges_1"), info_line.index("ranges_2"), info_line.index("ranges_3"), info_line.index("ranges_4")) # all laser positions in csv

        left_index = (info_line.index("ranges_179"), info_line.index("ranges_178"), info_line.index("ranges_177"), info_line.index("ranges_176"), info_line.index("ranges_175"))
        right_index = (info_line.index("ranges_88"), info_line.index("ranges_89"), info_line.index("ranges_90"), info_line.index("ranges_91"), info_line.index("ranges_92"))
        mid_index = (info_line.index("ranges_88"), info_line.index("ranges_89"), info_line.index("ranges_90"), info_line.index("ranges_91"), info_line.index("ranges_92"))

        # bin_left = 4 # 100
        # bin_mid = 2 # 010
        # bin_right = 1 # 001
        # bin_all = 7 # 111
        # bin_left_right = 5 # 101
        # bin_left_mid = 6 # 110
        # bin_right_mid = 3 # 011

        too_close_indexes = []
        dst = 0

        for index in indexes:
            if(csv_line[index] != "inf" and int(math.floor(float(csv_line[index]))) < 2): # value is less than two, which is close enough to set off our alert to create a msg
                # mark down the index and move on, msgs will be created later
                too_close_indexes.append(index)
        # figure out what combination of lasers it is
        binary_direction_indicator = 0
        left_accounted = 0
        right_accounted = 0
        mid_accounted = 0
        # showing directionality of which lasers are triggered through binary
        for index in too_close_indexes:
            if(index in left_index and left_accounted == 0):
                binary_direction_indicator += 100
                left_accounted = 1
            elif(index in mid_index and mid_accounted == 0):
                binary_direction_indicator += 10
                mid_accounted = 1
            elif(index in right_index and right_accounted == 0):
                binary_direction_indicator += 1
                right_accounted = 1

        bin_CAN = int(str(binary_direction_indicator), 2)

        # create the message
        msg_type = self.db.get_message_by_name("LASER_DST_CHECK")  # get message by name
        data = msg_type.encode({'LOCATION': bin_CAN})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # message type is speed, so we must convert with speed
    def data_to_dbc_speed(self, csv_line):
        avg_speed = math.sqrt(float(csv_line[1]) ** 2 + float(csv_line[3]) ** 2)  # calc average speed
        if(avg_speed > 250):
            avg_speed = 250
        msg_type = self.db.get_message_by_name("SPEED")  # get message by name
        data = msg_type.encode({'ENCODER': 0, 'CHECKSUM': 0, 'SPEED': abs(avg_speed)})
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    def data_to_dbc_steer(self, csv_line):
        torque = float(csv_line[6])  # calculate torque based on csv data
        msg_type = self.db.get_message_by_name("KINEMATICS")  # get message by name
        data = msg_type.encode(
            {'ACCEL_Y': 0, 'YAW_RATE': 0, 'STEERING_TORQUE': abs(torque)})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # BO_ 384 TRACK_A_0: 8 XXX
    #     SG_ COUNTER: 7 | 8 @ 0 + (1, 0)[0 | 255] "" XXX
    #     SG_ LAT_DIST: 31 | 11 @ 0 - (0.04, 0)[-50 | 50] "m" XXX
    #     SG_ LONG_DIST: 15 | 13 @ 0 + (0.04, 0)[0 | 300] "m" XXX
    #     SG_ NEW_TRACK: 36 | 1 @ 0 + (1, 0)[0 | 1] "" XXX
    #     SG_ REL_SPEED: 47 | 12 @ 0 - (0.025, 0)[-100 | 100] "m/s" XXX
    #     SG_ VALID: 48 | 1 @ 0 + (1, 0)[0 | 1] "" XXX
    #     SG_ CHECKSUM: 63 | 8 @ 0 + (1, 0)[0 | 255] "" XXX

    # laser number 179, ranges_179 (perpendicular to the car)
    def data_to_dbc_left_laser_one(self, csv_line, info_line):
        index = info_line.index("ranges_179")  # find the index of desired signal

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_0")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0}) # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 178, ranges_178
    def data_to_dbc_left_laser_two(self, csv_line, info_line):
        index = info_line.index("ranges_178")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_1")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 177, ranges_177
    def data_to_dbc_left_laser_three(self, csv_line, info_line):
        index = info_line.index("ranges_177")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_2")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 176, ranges_176
    def data_to_dbc_left_laser_four(self, csv_line, info_line):
        index = info_line.index("ranges_176")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_3")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 175, ranges_175
    def data_to_dbc_left_laser_five(self, csv_line, info_line):
        index = info_line.index("ranges_175")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_4")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 88, ranges_88
    def data_to_dbc_front_laser_one(self, csv_line, info_line):
        index = info_line.index("ranges_88")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_5")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 89, ranges_89
    def data_to_dbc_front_laser_two(self, csv_line, info_line):
        index = info_line.index("ranges_89")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_6")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 90, ranges_90 (parallel to the car)
    def data_to_dbc_front_laser_three(self, csv_line, info_line):
        index = info_line.index("ranges_90")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_7")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 91, ranges_91
    def data_to_dbc_front_laser_four(self, csv_line, info_line):
        index = info_line.index("ranges_91")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float
        msg_type = self.db.get_message_by_name("TRACK_A_8")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 92, ranges_92
    def data_to_dbc_front_laser_five(self, csv_line, info_line):
        index = info_line.index("ranges_92")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_9")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 0, ranges_0 (perpendicular to the car)
    def data_to_dbc_right_laser_one(self, csv_line, info_line):
        index = info_line.index("ranges_0")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_10")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 1, ranges_1
    def data_to_dbc_right_laser_two(self, csv_line, info_line):
        index = info_line.index("ranges_1")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_11")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 2, ranges_2
    def data_to_dbc_right_laser_three(self, csv_line, info_line):
        index = info_line.index("ranges_2")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_12")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 3, ranges_3
    def data_to_dbc_right_laser_four(self, csv_line, info_line):
        index = info_line.index("ranges_3")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_13")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    # laser number 4, ranges_4
    def data_to_dbc_right_laser_five(self, csv_line, info_line):
        index = info_line.index("ranges_4")

        long_distance = csv_line[index]  # value of desired signal
        if long_distance == "inf":  # no object? set to 300m
            distance = 300.0
        else:
            distance = float(long_distance)  # convert to float

        msg_type = self.db.get_message_by_name("TRACK_A_14")  # get message by name
        data = msg_type.encode({'COUNTER': 0, 'LAT_DIST': 30,
                                'LONG_DIST': distance, 'NEW_TRACK': 0,
                                'REL_SPEED': 0, 'VALID': 0, 'CHECKSUM': 0})  # encode message with data
        msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        return msg

    def data_to_dbc_brake(self, csv_line):
        # distance = float(csv_line[6])
        msg_type = self.db.get_message_by_name("BRAKE")  # get message by name
        # data = msg_type.encode() # encode message with data
        # msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        # return msg

    def data_to_dbc_wheel_speeds(self, csv_line):
        # distance = float(csv_line[6])
        msg_type = self.db.get_message_by_name("WHEEL_SPEEDS")  # get message by name
        # data = msg_type.encode() # encode message with data
        # msg: Message = can.Message(timestamp=float(csv_line[0]), arbitration_id=msg_type.frame_id, data=data)
        # return msg

    def run(self):
        # print(db.messages)  # show the messages for debugging
        self.parse_files()  # parse the files that we searched for earlier
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
