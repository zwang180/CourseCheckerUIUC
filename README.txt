Mac OS 10.8 and above is required for this script to run
Open a Terminal(ctrl + space then type terminal and press enter)
This tutorial is designed for a Mac OS without any pre-setup environment, all from scratch
if any of the following command is not working, and "sudo" at the beginning and try again,
enter your password if they prompt for it
EX. sudo pip install ......

Note, cd /path/to/folder will navigate you to the specific folder, any time if you do not
know the exact path of the folder/file, simply drag it into your terminal window and you will
get the path.

1. Install Xcode
This step is recommended. Note, this will be a PERTTY BIG download.
In your terminal type:
xcode-select --install
then press enter, follow the prompt and wait for the process to complete

2. Install Homebrew
Continue in your terminal window, type:
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
press enter, and wait for the process to complete

3. Install Python & Pip
Since this script is written in python 2.7, all you need is just type the following command in your terminal,
press enter and wait, as always:
brew install python

4. Update Pip
with following command:
pip install --upgrade pip

5. Install Virtualenv and set up one(recommended)
Install:
pip install virtualenv
Set up: navigate to your desired folder and run(replace name-you-choose any name you want)
virtualenv name-you-choose
after the process complete, activate the environment by:
source name-you-choose/bin/activate
exit the environment any time by:
deavtivate

6. Install Required Packages:
1). Pip part
navigate to the directory of this file, and there should be a requirements.txt in the same folder, run command:
pip install -r requirements.txt
2). Homebrew part
brew install terminal-notifier

7. Run the script by(in the same directory)
python name_of_scirpt.py
You could also make use of the applescript by modifying the path to your directory in the applescript

For further information, go to https://github.com/zwang180/AutoCourseStatusCheckUIUC
Further function including auto register will be developed but not recommend since it could result in serious consequences.
