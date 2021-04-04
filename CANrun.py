import sys
from os import path
import getopt
import CSVGenerator
from CSVGenerator import CSVGenerator

class CANrun:

    def __init__(self, bag_file):
        self.input_bag_file = bag_file  # bag file
        self.generator = CSVGenerator(self.input_bag_file)
        self.generator.run()

# def main():
#     CANrun("2021-03-05-14-21-09.bag")

def main(argv):
    input_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile="])
    except getopt.GetoptError:
        print("CANrun.py -i <bag_file>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: CANrun.py -i <bag_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            if arg.endswith(".bag") and path.exists(arg):
                input_file = arg
            elif path.exists(arg):
                print("usage: CANrun.py -i <bag_file>")
                print("Please provide the program a bag file from ROS")
                sys.exit(1)  #
            else:
                print("File does not exist")
                sys.exit(1)
    print('Bag file is "' + input_file + '"')
    CANrun(input_file)
    print("CANData has been outputted in a text file to the Outputs folder in the working directory")


main(sys.argv[1:])

# main()