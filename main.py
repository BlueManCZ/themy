#!/usr/bin/env python3

import gi
import subprocess

from time import sleep

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class GUIApp:
    def __init__(self, glade_file):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.builder.connect_signals(self)
        self.add_dialog = self.builder.get_object("add_dialog")

    def launch(self):
        window = self.builder.get_object("main_window")
        window.show_all()
        Gtk.main()

    # Main window

    def on_destroy(self, *args):
        Gtk.main_quit()
        quit()

    def add_application(self, *args):
        self.add_dialog.show()

    # Add dialog

    def select_application(self, *args):
        print("Hello")

    def on_add_dialog_destroy(self, *args):
        print("Heey")
        self.add_dialog.destroy()

    def on_add_dialog_delete_event(self, *args):
        self.add_dialog.hide()
        return True


dark = ["atom", "discord", "jetbrains-pycharm", "lmms", "spotify"]

last_window_id = ""

while True:
    # output = subprocess.run(["wmctrl", "-l"], capture_output=True)
    # windows_count = len(output.stdout.split(b'\n'))
    # print(windows_count)

    myapp = GUIApp("ui.glade")
    myapp.launch()

    sleep(0.5)

    output = subprocess.run(["xprop", "-root", "_NET_ACTIVE_WINDOW"], capture_output=True)
    active_window_id = output.stdout.split(b"# ")[1]
    # print(active_window_id)

    if active_window_id == last_window_id:
        continue

    last_window_id = active_window_id

    output2 = subprocess.run(["xprop", "-id", active_window_id, "WM_CLASS"], capture_output=True)
    print(output2.stdout)
    wm_classes = output2.stdout.split(b'"')[1:4]
    print(wm_classes)

    for wm_class in wm_classes:
        if wm_class.decode() in dark:
            print("Match")
            subprocess.run(["xprop", "-id", active_window_id, "-f", "_GTK_THEME_VARIANT", "8u", "-set", "_GTK_THEME_VARIANT", "dark"])
            break
