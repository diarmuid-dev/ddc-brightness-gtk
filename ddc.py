import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
import gi.pygtkcompat
import sys
import os
import subprocess


class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Scale Example", application=app)
        self.set_default_size(400, 100)
        self.set_border_width(5)

        # two adjustments (initial value, min value, max value,
        # step increment - press cursor keys to see!,
        # page increment - click around the handle to see!,
        # page size - not used here)
        self.ad1 = Gtk.Adjustment(0, 0, 100, 5, 10, 0)

        # Initialise an horizontal scale
        self.h_scale = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.ad1)
        self.h_scale.set_digits(0)
        self.h_scale.set_hexpand(True)
        self.h_scale.set_valign(Gtk.Align.START)

        # Connect the button-release-event with the callback function changeBrightness 
        self.h_scale.connect("button-release-event", self.changeBrightness)

        # Add a text entry later for manual brightness entry via keyboard
        self.textEntry = Gtk.Entry()

        # An instructions label
        self.label = Gtk.Label()
        self.label.set_text("Drag the slider to select your screen brightness")

        # a grid to attach the widgets
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_column_homogeneous(True)
        grid.attach(self.h_scale, 0, 0, 2, 1)
        grid.attach(self.label, 0, 1, 2, 1)


        self.add(grid)

    def setBrightness(self, brightness):
        self.h_scale.set_value(brightness)

    def changeBrightness(self, wdg, event):
        if (sys.platform == "linux"):
            #os.system(f"ddcutil --bus=1 setvcp 10 {str(int(self.h_scale.get_value()))}")
            subprocess.Popen(["ddcutil", "--bus=1", "setvcp", "10", f"{str(int(self.h_scale.get_value()))}"], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT)

class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        # Get the initial brightness of the monitor
        init_val = subprocess.Popen(["ddcutil", "--bus=1", "getvcp", "10"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
        val = init_val.communicate()
        init_bright = str(val[0]).split("=")[1].split(",")[0].strip()

        if (init_bright.endswith('errno')):
            print("This script requires root privileges, run in sudo")
            exit(0)


        win = MyWindow(self)
        win.setBrightness(int(init_bright))
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
