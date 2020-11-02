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

		self.otf_checkbox_status = 0
		self.ttf_checkbox_status = 0
		self.variable_checkbox_status = 0
		self.woff_checkbox_status = 0
		self.woff2_checkbox_status = 0
		self.eot_checkbox_status = 0
		self.otf_autohint_checkbox_status = 0
		self.ttf_autohint_checkbox_status = 0
		self.web_autohint_checkbox_status = 0
		self.web_source_selector_status = 0

		self.selected_formats = {}

		if Glyphs.defaults["com.eweracs.BatchExport.exportprefs"]:
			for key1 in Glyphs.defaults["com.eweracs.BatchExport.exportprefs"]:
				for key2 in Glyphs.defaults["com.eweracs.BatchExport.exportprefs"][key1]:
					self.selected_formats[key1] = dict(Glyphs.defaults["com.eweracs.BatchExport.exportprefs"][key1])
					self.selected_formats[key1][key2] = Glyphs.defaults["com.eweracs.BatchExport.exportprefs"][key1][key2]

			# self.selected_formats = copy.copy(dict(Glyphs.defaults["com.eweracs.BatchExport.exportprefs"]))
			if self.selected_formats["Web"]["Output"] == "OTF":
				self.web_source_selector_status = 0
			else:
				self.web_source_selector_status = 1
			if WOFF in self.selected_formats["Web"]["Containers"]:
				self.woff_checkbox_status = 1
			if WOFF2 in self.selected_formats["Web"]["Containers"]:
				self.woff2_checkbox_status = 1
			if EOT in self.selected_formats["Web"]["Containers"]:
				self.eot_checkbox_status = 1
		else:
			self.selected_formats = {"OTF": {"Export": False, "Type": "Desktop", "Output": "OTF", "Autohint": False, "Containers": [PLAIN]},
			                         "TTF": {"Export": False, "Type": "Desktop", "Output": "TTF", "Autohint": False, "Containers": [PLAIN]},
			                         "VAR": {"Export": False, "Type": "Desktop", "Output": VARIABLE, "Autohint": False, "Containers": [PLAIN]},
			                         "Web": {"Export": False, "Type": "Web", "Output": "OTF", "Autohint": False, "Containers": []}
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
		self.w.web_source.set(self.web_source_selector_status)
		y += 26
		x += 16
		self.w.web_autohint = vanilla.CheckBox((x, y, 200, 18), "Autohint",
		                                       sizeStyle="small", callback=self.web_autohint_select,
		                                       value=int(self.selected_formats["Web"]["Autohint"]))
		x -= 16
		y += 26

		self.w.woff_checkbox = vanilla.CheckBox((x, y, 200, 20), "WOFF", callback=self.woff_select,
		                                        value=self.woff_checkbox_status)
		y += 26
		self.w.woff2_checkbox = vanilla.CheckBox((x, y, 200, 20), "WOFF2", callback=self.woff2_select,
		                                         value=self.woff2_checkbox_status)
		y += 26
		self.w.eot_checkbox = vanilla.CheckBox((x, y, 200, 20), "EOT", callback=self.eot_select,
		                                       value=self.eot_checkbox_status)
		y += 30

		self.w.export_button = vanilla.Button((10, y, -10, 20), "Export...", callback=self.export_selection)
		y = 200

		self.export_button_toggle()
		self.w.resize(320, y)
		self.w.center()
		self.w.open()
		self.w.makeKey()

	def export_button_toggle(self):
		if self.w.otf_checkbox.get() + self.w.ttf_checkbox.get() + self.w.variable_checkbox.get() + \
		   self.w.woff_checkbox.get() + self.w.woff2_checkbox.get() + self.w.eot_checkbox.get() > 0:
			self.w.export_button.enable(True)
		else:
			self.w.export_button.enable(False)

	def otf_select(self, sender):
		self.selected_formats["OTF"]["Export"] = sender.get() == 1
		self.export_button_toggle()
		return

	def otf_autohint_select(self, sender):
		self.selected_formats["OTF"]["Autohint"] = sender.get() == 1
		return

	def ttf_select(self, sender):
		self.selected_formats["TTF"]["Export"] = sender.get() == 1
		self.export_button_toggle()
		return

	def ttf_autohint_select(self, sender):
		self.selected_formats["TTF"]["Autohint"] = sender.get() == 1
		return

	def variable_select(self, sender):
		self.selected_formats["VAR"]["Export"] = sender.get() == 1
		self.export_button_toggle()
		return

	def web_source_select(self, sender):
		if sender.get() == 1:
			self.selected_formats["Web"]["Output"] = "TTF"
		else:
			self.selected_formats["Web"]["Output"] = "OTF"
		return

	def web_autohint_select(self, sender):
		self.selected_formats["Web"]["Autohint"] = sender.get() == 1
		return

	def woff_select(self, sender):
		if sender.get() == 1:
			self.selected_formats["Web"]["Containers"].append(WOFF)
		else:
			self.selected_formats["Web"]["Containers"].remove(WOFF)
		self.selected_formats["Web"]["Export"] = len(self.selected_formats["Web"]["Containers"]) > 0
		self.export_button_toggle()
		return

	def woff2_select(self, sender):
		if sender.get() == 1:
			self.selected_formats["Web"]["Containers"].append(WOFF2)
		else:
			self.selected_formats["Web"]["Containers"].remove(WOFF2)
		self.selected_formats["Web"]["Export"] = len(self.selected_formats["Web"]["Containers"]) > 0
		self.export_button_toggle()
		return

	def eot_select(self, sender):
		if sender.get() == 1:
			self.selected_formats["Web"]["Containers"].append(EOT)
		else:
			self.selected_formats["Web"]["Containers"].remove(EOT)
		self.selected_formats["Web"]["Export"] = len(self.selected_formats["Web"]["Containers"]) > 0
		self.export_button_toggle()
		return

	def export_selection(self, sender):
		self.export_path = GetFolder()  # open parent directory to write files to
		for i in self.selected_formats:
			if self.selected_formats[i]["Export"]:
				if self.selected_formats[i]["Type"] == "Desktop":
					if not os.path.exists(self.export_path + "/Desktop/" + i):
						os.makedirs(self.export_path + "/Desktop/" + i)
					self.font.export(self.selected_formats[i]["Output"], FontPath=self.export_path + "/Desktop/" + i,
					                 AutoHint=self.selected_formats[i]["Autohint"],
					                 Containers=[PLAIN])
				else:
					if not os.path.exists(self.export_path + "/Web/"):
						os.makedirs(self.export_path + "/Web/")
					self.font.export(self.web_source_status, FontPath=self.export_path + "/Web/",
					                 AutoHint=self.selected_formats[i]["Autohint"],
					                 Containers=self.selected_formats["Web"]["Containers"])

		Glyphs.defaults["com.eweracs.BatchExport.exportprefs"] = self.selected_formats  # write selection to saved preferences

		self.w.close()


ExportWindow()
