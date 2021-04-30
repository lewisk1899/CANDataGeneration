## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/lewisk1899/CANDataGeneration/edit/gh-pages/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

# Header 1
## Header 2
### Header 3

ECE 473 Lewis Koplon, Fernando Gutierrez, Will Mund

This software will take your .bag rosbag file (from rosbag record) and output some of that data as CAN messages to multiple text files. 
These messages are generated from the toyota_rav4_2019.dbc.

In this current implementation, the generated messages are for velocity, steering, and laser data only.
Data from the lasers will be used in the next implementation for LKA messages.

## Installation guide:

### 1) Install dependencies:

        pip3 install bagpy
        pip3 install cantools
        pip3 install can


### 2) Clone repository into home directory and select correct branch:

        git clone https://github.com/lewisk1899/CANDataGeneration
        cd CANDataGeneration
        git checkout origin/beta_branch


### 3) Move desired .bag file into the CANDataGeneration directory with python files


### 4) Run the software:

        python3 CANrun.py -i <bag_file_name>

### Note) For help you can run:

        python3 CANrun.py -h

