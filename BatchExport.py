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
		self.parent_path = None
		self.export_path = None
		self.web_source_status = "OTF"

		self.selected_formats = {}
		self.prefs = Glyphs.defaults["com.eweracs.BatchExport.exportprefs"]  # import saved preferences

		# if preferences exist, copy values to new python dict (NSDictionary doesn't work through Py-ObjC bridge)
		if self.prefs:
			for key in self.prefs:
				self.selected_formats[key] = dict(self.prefs[key])
				self.selected_formats[key]["Containers"] = list(self.selected_formats[key]["Containers"])
		else:
			self.selected_formats = {"OTF": {"Export": False, "Type": "Desktop", "Output": "OTF",
			                                 "Autohint": False, "Containers": [PLAIN]},
			                         "TTF": {"Export": False, "Type": "Desktop", "Output": "TTF",
			                                 "Autohint": False, "Containers": [PLAIN]},
			                         "VAR": {"Export": False, "Type": "Desktop", "Output": VARIABLE,
			                                 "Autohint": False, "Containers": [PLAIN]},
			                         "Web": {"Export": False, "Type": "Web", "Output": "OTF",
			                                 "Autohint": False, "Containers": []}
			                         }

		# UI elements indent init
		x = 10
		y = 10

		self.w = vanilla.FloatingWindow((0, 0), "Batch Export")

		self.w.desktop_title = vanilla.TextBox((x, y, 200, 20), "Desktop")
		y += 24

		self.w.otf_checkbox = vanilla.CheckBox((x, y, 200, 22), "OTF",
		                                       callback=self.otf_select, value=int(self.selected_formats["OTF"]["Export"]))
		x += 16
		y += 26
		self.w.otf_autohint = vanilla.CheckBox((x, y, 200, 18), "Autohint",
		                                       sizeStyle="small", callback=self.otf_autohint_select,
		                                       value=int(self.selected_formats["OTF"]["Autohint"]))
		x -= 16
		y += 26

		self.w.ttf_checkbox = vanilla.CheckBox((x, y, 200, 22), "TTF",
		                                       callback=self.ttf_select, value=int(self.selected_formats["TTF"]["Export"]))
		x += 16
		y += 26
		self.w.ttf_autohint = vanilla.CheckBox((x, y, 200, 18), "Autohint",
		                                       sizeStyle="small", callback=self.ttf_autohint_select,
		                                       value=int(self.selected_formats["TTF"]["Autohint"]))
		x -= 16
		y += 26

		self.w.variable_checkbox = vanilla.CheckBox((x, y, 200, 22), "VAR",
		                                            callback=self.variable_select,
		                                            value=int(self.selected_formats["VAR"]["Export"]))
		y = 10

		x += 150
		self.w.web_title = vanilla.TextBox((x, y, 200, 20), "Web")
		y += 24

		self.w.web_source = vanilla.PopUpButton((x, y, 100, 22), ["OTF", "TTF"], callback=self.web_source_select)
		self.w.web_source.set(self.selected_formats["Web"]["Output"] != "OTF")
		y += 26
		x += 16
		self.w.web_autohint = vanilla.CheckBox((x, y, 200, 18), "Autohint",
		                                       sizeStyle="small", callback=self.web_autohint_select,
		                                       value=int(self.selected_formats["Web"]["Autohint"]))
		x -= 16
		y += 26

		self.w.woff_checkbox = vanilla.CheckBox((x, y, 200, 20), "WOFF", callback=self.woff_select,
		                                        value=WOFF in self.selected_formats["Web"]["Containers"])
		y += 26
		self.w.woff2_checkbox = vanilla.CheckBox((x, y, 200, 20), "WOFF2", callback=self.woff2_select,
		                                         value=WOFF2 in self.selected_formats["Web"]["Containers"])
		y += 26
		self.w.eot_checkbox = vanilla.CheckBox((x, y, 200, 20), "EOT", callback=self.eot_select,
		                                       value=EOT in self.selected_formats["Web"]["Containers"])
		y += 30

		self.w.export_button = vanilla.Button((10, y, -10, 20), "Export...", callback=self.export_selection)
		y = 200

		self.export_button_toggle()
		self.w.resize(320, y)
		self.w.center()
		self.w.open()
		self.w.makeKey()

	def export_button_toggle(self):
		self.w.export_button.enable(self.w.otf_checkbox.get() + self.w.ttf_checkbox.get() + self.w.variable_checkbox.get() +
		                            self.w.woff_checkbox.get() + self.w.woff2_checkbox.get() + self.w.eot_checkbox.get() > 0)

	def otf_select(self, sender):
		self.selected_formats["OTF"]["Export"] = sender.get() == 1
		self.export_button_toggle()

	def otf_autohint_select(self, sender):
		self.selected_formats["OTF"]["Autohint"] = sender.get() == 1

	def ttf_select(self, sender):
		self.selected_formats["TTF"]["Export"] = sender.get() == 1
		self.export_button_toggle()

	def ttf_autohint_select(self, sender):
		self.selected_formats["TTF"]["Autohint"] = sender.get() == 1

	def variable_select(self, sender):
		self.selected_formats["VAR"]["Export"] = sender.get() == 1
		self.export_button_toggle()

	def web_source_select(self, sender):
		if sender.get() == 1:
			self.selected_formats["Web"]["Output"] = "TTF"
		else:
			self.selected_formats["Web"]["Output"] = "OTF"

	def web_autohint_select(self, sender):
		self.selected_formats["Web"]["Autohint"] = sender.get() == 1

	def woff_select(self, sender):
		if sender.get() == 1:
			self.selected_formats["Web"]["Containers"].append(WOFF)
		else:
			self.selected_formats["Web"]["Containers"].remove(WOFF)
		self.selected_formats["Web"]["Export"] = len(self.selected_formats["Web"]["Containers"]) > 0
		self.export_button_toggle()

	def woff2_select(self, sender):
		if sender.get() == 1:
			self.selected_formats["Web"]["Containers"].append(WOFF2)
		else:
			self.selected_formats["Web"]["Containers"].remove(WOFF2)
		self.selected_formats["Web"]["Export"] = len(self.selected_formats["Web"]["Containers"]) > 0
		self.export_button_toggle()

	def eot_select(self, sender):
		if sender.get() == 1:
			self.selected_formats["Web"]["Containers"].append(EOT)
		else:
			self.selected_formats["Web"]["Containers"].remove(EOT)
		self.selected_formats["Web"]["Export"] = len(self.selected_formats["Web"]["Containers"]) > 0
		self.export_button_toggle()

	def export_selection(self, sender):
		self.parent_path = GetFolder()  # open parent directory to write files to
		for i in self.selected_formats:
			if self.selected_formats[i]["Export"]:
				self.export_path = self.parent_path + "/" + str(self.selected_formats[i]["Type"]) + "/" + i
				if not os.path.exists(self.export_path):
					os.makedirs(self.export_path)
				self.font.export(self.selected_formats[i]["Output"], FontPath=self.export_path,
				                 AutoHint=self.selected_formats[i]["Autohint"],
				                 Containers=self.selected_formats[i]["Containers"])

		Glyphs.defaults["com.eweracs.BatchExport.exportprefs"] = self.selected_formats  # write selection to saved preferences

		self.w.close()


ExportWindow()
