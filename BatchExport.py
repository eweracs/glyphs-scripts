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
		self.parent_path = None
		self.export_path = None

		self.prefs = Glyphs.defaults["com.eweracs.BatchExport.exportprefs"]  # import saved preferences
		self.selected_formats = {}  # create Python dictionary to store format selection

		# if preferences exist, copy values to dict (NSDictionary doesn't work through Py-ObjC bridge)
		if self.prefs:
			for key in self.prefs:
				self.selected_formats[key] = dict(self.prefs[key])
				self.selected_formats[key]["Containers"] = list(self.selected_formats[key]["Containers"])
		else:  # build dictionary to store preferences
			self.selected_formats = {"OTF": {"Export": False, "Type": "Desktop", "Output": "OTF",
			                                 "Autohint": False, "Containers": []},
			                         "TTF": {"Export": False, "Type": "Desktop", "Output": "TTF",
			                                 "Autohint": False, "Containers": []},
			                         "VAR": {"Export": False, "Type": "Desktop", "Output": VARIABLE,
			                                 "Autohint": False, "Containers": []},
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
		                                       callback=self.format_selection, value=int(self.selected_formats["OTF"]["Export"]))
		x += 16
		y += 26
		self.w.otf_autohint = vanilla.CheckBox((x, y, 200, 18), "Autohint",
		                                       sizeStyle="small", callback=self.format_selection,
		                                       value=int(self.selected_formats["OTF"]["Autohint"]))
		x -= 16
		y += 26

		self.w.ttf_checkbox = vanilla.CheckBox((x, y, 200, 22), "TTF",
		                                       callback=self.format_selection, value=int(self.selected_formats["TTF"]["Export"]))
		x += 16
		y += 26
		self.w.ttf_autohint = vanilla.CheckBox((x, y, 200, 18), "Autohint",
		                                       sizeStyle="small", callback=self.format_selection,
		                                       value=int(self.selected_formats["TTF"]["Autohint"]))
		x -= 16
		y += 26

		self.w.var_checkbox = vanilla.CheckBox((x, y, 200, 22), "VAR",
		                                            callback=self.format_selection,
		                                            value=int(self.selected_formats["VAR"]["Export"]))
		y = 10

		x += 150
		self.w.web_title = vanilla.TextBox((x, y, 200, 20), "Web")
		y += 24

		self.w.web_source = vanilla.PopUpButton((x, y, 100, 22), ["OTF", "TTF"], callback=self.format_selection)
		self.w.web_source.set(self.selected_formats["Web"]["Output"] != "OTF")
		y += 26
		x += 16
		self.w.web_autohint = vanilla.CheckBox((x, y, 200, 18), "Autohint",
		                                       sizeStyle="small", callback=self.format_selection,
		                                       value=int(self.selected_formats["Web"]["Autohint"]))
		x -= 16
		y += 26

		self.w.woff_checkbox = vanilla.CheckBox((x, y, 200, 20), "WOFF", callback=self.format_selection,
		                                        value=WOFF in self.selected_formats["Web"]["Containers"])
		y += 26
		self.w.woff2_checkbox = vanilla.CheckBox((x, y, 200, 20), "WOFF2", callback=self.format_selection,
		                                         value=WOFF2 in self.selected_formats["Web"]["Containers"])
		y += 26
		self.w.eot_checkbox = vanilla.CheckBox((x, y, 200, 20), "EOT", callback=self.format_selection,
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
		self.w.export_button.enable(self.w.otf_checkbox.get() + self.w.ttf_checkbox.get() + self.w.var_checkbox.get() +
		                            self.w.woff_checkbox.get() + self.w.woff2_checkbox.get() + self.w.eot_checkbox.get() > 0)

	def format_selection(self, sender):  # edits the values in the dictionary based on what boxes are checked
		self.selected_formats["OTF"]["Export"] = self.w.otf_checkbox.get() == 1
		self.selected_formats["OTF"]["Autohint"] = self.w.otf_autohint.get() == 1
		self.selected_formats["TTF"]["Export"] = self.w.ttf_checkbox.get() == 1
		self.selected_formats["TTF"]["Autohint"] = self.w.ttf_autohint.get() == 1
		self.selected_formats["VAR"]["Export"] = self.w.var_checkbox.get() == 1
		if self.w.web_source.get() == 1:
			self.selected_formats["Web"]["Output"] = "TTF"
		else:
			self.selected_formats["Web"]["Output"] = "OTF"
		self.selected_formats["Web"]["Autohint"] = self.w.web_autohint.get() == 1
		if self.w.woff_checkbox.get() == 1:
			if WOFF not in self.selected_formats["Web"]["Containers"]:
				self.selected_formats["Web"]["Containers"].append(WOFF)
		elif WOFF in self.selected_formats["Web"]["Containers"]:
			self.selected_formats["Web"]["Containers"].remove(WOFF)
		if self.w.woff2_checkbox.get() == 1:
			if WOFF2 not in self.selected_formats["Web"]["Containers"]:
				self.selected_formats["Web"]["Containers"].append(WOFF2)
		elif WOFF2 in self.selected_formats["Web"]["Containers"]:
			self.selected_formats["Web"]["Containers"].remove(WOFF2)
		if self.w.eot_checkbox.get() == 1:
			if EOT not in self.selected_formats["Web"]["Containers"]:
				self.selected_formats["Web"]["Containers"].append(EOT)
		elif EOT in self.selected_formats["Web"]["Containers"]:
			self.selected_formats["Web"]["Containers"].remove(EOT)
		self.selected_formats["Web"]["Export"] = len(self.selected_formats["Web"]["Containers"]) > 0
		self.export_button_toggle()

	def export_selection(self, sender):  # iterates through the dictionary and exports fonts based on set values
		self.parent_path = GetFolder()  # open parent directory to write files to
		for output in self.selected_formats:
			if self.selected_formats[output]["Export"]:
				if self.selected_formats[output]["Containers"]:
					for container in self.selected_formats[output]["Containers"]:
						path = self.parent_path + "/" + str(self.selected_formats[output]["Type"]) + "/" + str(container) + "/"
						self.export_to_location(self.selected_formats[output]["Output"], self.selected_formats[output]["Autohint"], path, [str(container)])
				else:
					path = self.parent_path + "/" + str(self.selected_formats[output]["Type"]) + "/" + output + "/"
					self.export_to_location(self.selected_formats[output]["Output"], self.selected_formats[output]["Autohint"], path, self.selected_formats[output]["Containers"])


	def export_to_location(self, output, autohint, path, container):
		if not os.path.exists(path):  # create export directory if it doesn’t exist yet
			os.makedirs(path)
		print(container)
		self.font.export(output, FontPath=path, AutoHint=autohint, Containers=container)

		Glyphs.defaults["com.eweracs.BatchExport.exportprefs"] = self.selected_formats  # write selection to saved preferences
		# self.w.close()


ExportWindow()
