# MenuTitle: Export Profiles
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

        self.selected_formats = {}

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

        self.w.export_button = vanilla.Button((10, y, -10, 20), "Export...", callback=self.export_selection)
        y = 200

        self.w.resize(320, y)
        self.w.center()
        self.w.open()
        self.w.makeKey()

    def otf_select(self, sender):
        if sender.get() == 1:
            self.selected_formats["OTF"] = [OTF, False, PLAIN]
        else:
            del self.selected_formats["OTF"]

    def otf_autohint_select(self, sender):
        if sender.get() == 1:
            self.selected_formats["OTF"][1] = True
        else:
            self.selected_formats["OTF"][1] = False

    def ttf_select(self, sender):
        if sender.get() == 1:
            self.selected_formats["TTF"] = [TTF, False, PLAIN]
        else:
            del self.selected_formats["TTF"]

    def ttf_autohint_select(self, sender):
        if sender.get() == 1:
            self.selected_formats["TTF"][1] = True
        else:
            self.selected_formats["TTF"][1] = False

    def variable_select(self, sender):
        if sender.get() == 1:
            self.selected_formats["Variable"] = [VARIABLE, False, PLAIN]
        else:
            del self.selected_formats[VARIABLE]

    def web_source_select(self, sender):
        if sender.get() == 1:
            self.web_source_status = TTF
        else:
            self.web_source_status = OTF

    def web_autohint_select(self, sender):
        if sender.get() == 1:
            self.web_autohint_status = True
        else:
            self.web_autohint_status = False

    def woff_select(self, sender):
        if sender.get() == 1:
            self.selected_formats["WOFF"] = [self.web_source_status, self.web_autohint_status, WOFF]
        else:
            del self.selected_formats["WOFF"]

    def woff2_select(self, sender):
        if sender.get() == 1:
            self.selected_formats["WOFF2"] = [self.web_source_status, self.web_autohint_status, WOFF2]
        else:
            del self.selected_formats["WOFF2"]

    def eot_select(self, sender):
        if sender.get() == 1:
            self.selected_formats["EOT"] = [self.web_source_status, self.web_autohint_status, EOT]
        else:
            del self.selected_formats["EOT"]

    def export_selection(self, sender):
        self.export_path = GetFolder()  # open parent directory to write files to
        for format in self.selected_formats:
            if format == "TTF" or format == "OTF" or format == "Variable":
                if not os.path.exists(self.export_path + "/Desktop/" + format):
                    os.makedirs(self.export_path + "/Desktop/" + format)
                self.font.export(self.selected_formats[format][0], FontPath=self.export_path + "/Desktop/" + format,
                                 AutoHint=self.selected_formats[format][1],
                                 Containers=[self.selected_formats[format][2]])
            else:
                if not os.path.exists(self.export_path + "/Web/" + format):
                    os.makedirs(self.export_path + "/Web/" + format)
                self.font.export(self.selected_formats[format][0], FontPath=self.export_path + "/Web/" + format,
                                 AutoHint=self.selected_formats[format][1],
                                 Containers=[self.selected_formats[format][2]])

        self.w.close()


ExportWindow()
