# ddc-brightness-gtk
A (very) simple GTK application for controlling the brightness of a connected monitor over the DDC/CI (Display Data Channel Command Interface) interface written in python.

For the program to work, you MUST be using linux and have ddcutil installed, which can be done in apt via:

`sudo apt-get install ddcutil`

To run the program cd into the same directory as the program and run the command:

`sudo python3 ddc.py`

The program must be run in sudo mode or else the brightness of the monitor will not change.

To make the program easier to use, add this line into your /home/.bashrc file:
  
`alias ddc='sudo python3 PATH-TO-DDC.PY/ddc.py'`
 
Now, you can simply type the command `ddc` to run the program
