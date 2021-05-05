# CANDataGeneration
ECE 473 Lewis Koplon, Fernando Gutierrez, Will Mund

This software will take your .bag rosbag file (from rosbag record) and output some of that data as CAN messages to multiple text files. 
These messages are generated from the toyota_rav4_2019.dbc.

In this final implementation, the generated messages are for velocity data, steering data, laser data, and a custom signal we implemented to track if an object is too close the vehicle via the lasers.

Installation guide:

1) Install dependencies:

        pip3 install bagpy
        pip3 install cantools
        pip3 install can


2) Clone repository into home directory and select correct branch:

        git clone https://github.com/lewisk1899/CANDataGeneration
        cd CANDataGeneration
        git checkout origin/main


3) Move desired .bag file into the CAN directory (which is inside the CANDataGeneration folder) with python files


4) Run the software:

        python3 CANrun.py -i <bag_file_name>

Note) For help you can run:

        python3 CANrun.py -h




Your outputs are in a directory called "outputs" as multiple .txt files sorted by message type.

These outputs are organized by timestamp, with each field of the CAN message labeled as well.

Additionally, if you use the test.bag file, know that it was generated from a car sitting perfectly still, meaning the velocity will not be populated.
