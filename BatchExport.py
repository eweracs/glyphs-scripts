# MenuTitle: Batch Export
# -*- coding: utf-8 -*-

__doc__ = """
Exports font in specified formats, nicely sorted into folders
"""

import os
import vanilla


class ExportWindow:

    def __init__(self):
        self.font = Font
        self.export_path = None
        self.otf_status = 0
        self.otf_autohint_status = False
        self.ttf_status = 0
        self.ttf_autohint_status = False
        self.variable_status = 0
        self.web_source_status = "OTF"
        self.web_autohint_status = False
        self.woff_status = 0
        self.woff2_status = 0
        self.eot_status = 0

        # UI elements indent init
        x = 10
        y = 10

        self.w = vanilla.FloatingWindow((0, 0), "Batch Export")

        self.w.desktop_title = vanilla.TextBox((x, y, 200, 20), "Desktop")
        y += 24

        self.w.otf_checkbox = vanilla.CheckBox((x, y, 200, 22), "OTF",
                                               callback=self.otf_select)
        x += 16
        y += 26
        self.w.otf_autohint = vanilla.CheckBox((x, y, 200, 18), "Autohint",
                                               sizeStyle="small", callback=self.otf_autohint_select)
        x -= 16
        y += 26

        self.w.ttf_checkbox = vanilla.CheckBox((x, y, 200, 22), "TTF",
                                               callback=self.ttf_select)
        x += 16
        y += 26
        self.w.ttf_autohint = vanilla.CheckBox((x, y, 200, 18), "Autohint",
                                               sizeStyle="small", callback=self.ttf_autohint_select)
        x -= 16
        y += 26

        self.w.variable_checkbox = vanilla.CheckBox((x, y, 200, 22), "Variable",
                                                    callback=self.variable_select)
        y = 10

        x += 150
        self.w.web_title = vanilla.TextBox((x, y, 200, 20), "Web")
        y += 24

        self.w.web_source = vanilla.PopUpButton((x, y, 100, 22), ["OTF", "TTF"], callback=self.web_source_select)
        y += 26
        x += 16
        self.w.web_autohint = vanilla.CheckBox((x, y, 200, 18), "Autohint",
                                               sizeStyle="small", callback=self.web_autohint_select)
        x -= 16
        y += 26

        self.w.woff_checkbox = vanilla.CheckBox((x, y, 200, 20), "WOFF", callback=self.woff_select)
        y += 26
        self.w.woff2_checkbox = vanilla.CheckBox((x, y, 200, 20), "WOFF2", callback=self.woff2_select)
        y += 26
        self.w.eot_checkbox = vanilla.CheckBox((x, y, 200, 20), "EOT", callback=self.eot_select)
        y += 30

        self.w.export_button = vanilla.Button((10, y, -10, 20), "Export", callback=self.export_selection)
        y = 200

        self.w.resize(320, y)
        self.w.center()
        self.w.open()
        self.w.makeKey()

    def otf_select(self, sender):
        self.otf_status = sender.get()

    def otf_autohint_select(self, sender):
        if sender.get() == 1:
            self.otf_autohint_status = True

    def ttf_select(self, sender):
        self.ttf_status = sender.get()

    def ttf_autohint_select(self, sender):
        if sender.get() == 1:
            self.ttf_autohint_status = True

    def variable_select(self, sender):
        self.variable_status = sender.get()

    def web_source_select(self, sender):
        if sender.get() == 1:
            self.web_source_status = "TTF"

    def web_autohint_select(self, sender):
        if sender.get() == 1:
            self.web_autohint_status = True

    def woff_select(self, sender):
        self.woff_status = sender.get()

    def woff2_select(self, sender):
        self.woff2_status = sender.get()

    def eot_select(self, sender):
        self.eot_status = sender.get()

    def generate_fonts(self, fontformat, path, autohint_status, **kwargs):
        for instance in self.font.instances:
            if instance.active:
                instance.generate(fontformat, path, autohint_status, **kwargs)

    def export_selection(self, sender):
        self.export_path = GetFolder()  # open parent directory to write files to

        if self.otf_status == 1:
            if not os.path.exists(self.export_path + "/Desktop/OTF"):  # create OTF file directory if not present yet
                os.makedirs(self.export_path + "/Desktop/OTF")
            self.generate_fonts("OTF", self.export_path + "/Desktop/OTF", self.otf_autohint_status)

        if self.ttf_status == 1:
            if not os.path.exists(self.export_path + "/Desktop/TTF"):  # create TTF file directory if not present yet
                os.makedirs(self.export_path + "/Desktop/TTF")
            self.generate_fonts("TTF", self.export_path + "/Desktop/TTF", self.ttf_autohint_status)

        if self.variable_status == 1:
            if not os.path.exists(self.export_path + "/Desktop/Variable"):  # create Variable file directory if not present yet
                os.makedirs(self.export_path + "/Desktop/Variable")
            self.font.export(VARIABLE, FontPath=self.export_path + "/Desktop/Variable")

        if self.woff_status == 1:
            if not os.path.exists(self.export_path + "/Web/WOFF"):  # create WOFF file directory if not present yet
                os.makedirs(self.export_path + "/Web/WOFF")
            self.generate_fonts(self.web_source_status, self.export_path + "/Web/WOFF", self.web_autohint_status, Containers=[WOFF])

        if self.woff2_status == 1:
            if not os.path.exists(self.export_path + "/Web/WOFF2"):  # create WOFF2 file directory if not present yet
                os.makedirs(self.export_path + "/Web/WOFF2")
            self.generate_fonts(self.web_source_status, self.export_path + "/Web/WOFF2", self.web_autohint_status, Containers=[WOFF2])

        if self.eot_status == 1:
            if not os.path.exists(self.export_path + "/Web/EOT"):  # create EOT file directory if not present yet
                os.makedirs(self.export_path + "/Web/EOT")
            self.generate_fonts(self.web_source_status, self.export_path + "/Web/EOT", self.web_autohint_status, Containers=[EOT])

        self.w.close()


ExportWindow()
