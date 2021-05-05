# CANDataGeneration
ECE 473 Lewis Koplon, Fernando Gutierrez, Will Mund

This software will take your .bag rosbag file (from rosbag record) and output some of that data as CAN messages to multiple text files. 
These messages are generated from the toyota_rav4_2019.dbc. Which contains one additional custom message we created called, LASER_DST_CHECK, which contains the data for which laser group if any has an object within 1 meter of its origin.

In this final implementation, the generated messages are for velocity data, steering data, laser data, and the custom signal we implemented.

Installation guide:

1) Install dependencies:

        pip3 install bagpy
        pip3 install cantools
        pip3 install can


2) Clone repository into home directory:

        git clone https://github.com/lewisk1899/CANDataGeneration
        


3) Move desired .bag file into the CAN directory (which is inside the CANDataGeneration folder) with the python files that are already there


4) Run the software:
    
        cd CANDataGeneration/CAN
        python3 CANrun.py -i <bag_file_name>

Note) For help you can run:

        python3 CANrun.py -h




Your outputs are in a directory called "outputs" as multiple .txt files sorted by message type. Steering data is contained in the kinematics file, velocity in the speed file, and laser data in the laser file.

These outputs are organized by timestamp, with each field of the CAN message labeled as well.

Additionally, if you use the test1.bag or test3.bag files, know that it was generated from a car sitting perfectly still, meaning the velocity will not be populated with meaningful values. test3.bag was created in a simulation where the vehicle was surrounded by three close cars, thus triggering our custom warning signal that an object is too close. 
