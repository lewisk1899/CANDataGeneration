## IS this title

You can use the [editor on GitHub](https://github.com/lewisk1899/CANDataGeneration/edit/gh-pages/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

ECE 473 Lewis Koplon, Fernando Gutierrez, Will Mund

This software will take your .bag rosbag file (from rosbag record) and output some of that data as CAN messages to multiple text files. 
These messages are generated from the toyota_rav4_2019.dbc.

In this current implementation, the generated messages are for velocity, steering, and laser data only.
Data from the lasers will be used in the next implementation for LKA messages.

Installation guide:

1) Install dependencies:

        pip3 install bagpy
        pip3 install cantools
        pip3 install can


2) Clone repository into home directory and select correct branch:

        git clone https://github.com/lewisk1899/CANDataGeneration
        cd CANDataGeneration
        git checkout origin/beta_branch


3) Move desired .bag file into the CANDataGeneration directory with python files


4) Run the software:

        python3 CANrun.py -i <bag_file_name>

Note) For help you can run:

        python3 CANrun.py -h




Your outputs are in a directory called "outputs" as multiple .txt files sorted by message type.

These outputs are organized by timestamp, with each field of the CAN message labeled as well.

Additionally, if you use the test.bag file, know that it was generated from a car sitting perfectly still, meaning the velocity will not be populated.

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/lewisk1899/CANDataGeneration/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
