# MenuTitle: Build Small Figures RMX
# -*- coding: utf-8 -*-

__doc__ = """
Builds small figures with RMX added to base glyphs.
"""

import vanilla
from Foundation import NSPoint


class BuildFigures:
	def __init__(self):

		self.font = Font
		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		self.w = vanilla.FloatingWindow((0, 0), "Build Small Figures RMX")

		self.w.descriptionText = vanilla.TextBox("auto",
		                                         "After defining RMX values for the base figures, these values will be "
		                                         "written to the glyphs. Open RMX Scaler on these afterwards to scale "
		                                         "them accordingly.",
		                                         sizeStyle="small")

		self.w.source = vanilla.Group("auto")
		self.w.source.title = vanilla.TextBox("auto", "Source figures:", sizeStyle="small")
		self.w.source.selector = vanilla.PopUpButton("auto", ["Default", "Proportional .lf", "Tabular .tf"],
		                                             sizeStyle="small")

		self.w.default = vanilla.Group("auto")
		self.w.default.title = vanilla.TextBox("auto", "Base small figures:", sizeStyle="small")
		self.w.default.selector = vanilla.PopUpButton("auto", [".dnom", "inferior", ".numr", "superior"],
		                                              sizeStyle="small",
		                                              callback=self.selection_change)

		self.w.paramTitles = vanilla.Group("auto")
		self.w.paramTitles.width = vanilla.TextBox("auto", "Width", sizeStyle="small")
		self.w.paramTitles.height = vanilla.TextBox("auto", "Height", sizeStyle="small")
		self.w.paramTitles.weight = vanilla.TextBox("auto", "Weight", sizeStyle="small")

		self.w.paramEntries = vanilla.Group("auto")
		self.w.paramEntries.width = vanilla.EditText("auto", sizeStyle="small", text="0")
		self.w.paramEntries.height = vanilla.EditText("auto", sizeStyle="small", text="0")
		self.w.paramEntries.weight = vanilla.EditText("auto", sizeStyle="small", text="0")

		self.w.divider1 = vanilla.HorizontalLine("auto")

		self.w.componentTitles = vanilla.Group("auto")
		self.w.componentTitles.figures = vanilla.TextBox("auto", "Build components:",
		                                                 sizeStyle="small")

		self.w.componentTitles.yShift = vanilla.TextBox("auto", "y shift:",
		                                                sizeStyle="small", alignment="left")

		self.w.dnom = vanilla.Group("auto")
		self.w.dnom.select = vanilla.CheckBox("auto", ".dnom", sizeStyle="small")
		self.w.dnom.shift = vanilla.EditText("auto", text="0", sizeStyle="small")

		self.w.inferior = vanilla.Group("auto")
		self.w.inferior.select = vanilla.CheckBox("auto", "inferior", sizeStyle="small")
		self.w.inferior.shift = vanilla.EditText("auto", text="-100", sizeStyle="small")

		self.w.numr = vanilla.Group("auto")
		self.w.numr.select = vanilla.CheckBox("auto", ".numr", sizeStyle="small")
		self.w.numr.shift = vanilla.EditText("auto", text="300", sizeStyle="small")

		self.w.superior = vanilla.Group("auto")
		self.w.superior.select = vanilla.CheckBox("auto", "superior", sizeStyle="small")
		self.w.superior.shift = vanilla.EditText("auto", text="350", sizeStyle="small")

		self.w.divider2 = vanilla.HorizontalLine("auto")

		self.w.allMasters = vanilla.Group("auto")
		self.w.allMasters.select = vanilla.CheckBox("auto", "Apply to all masters", sizeStyle="small")
		self.w.allMasters.shift = vanilla.TextBox("auto", "")


		self.w.writeButton = vanilla.Button("auto", "Make figures", callback=self.make_figures)


		self.load_preferences()
		self.selection_change(None)

		rules = [
			"H:|-border-[descriptionText]-border-|",
			"H:|-border-[source]-border-|",
			"H:|-border-[default]-border-|",
			"H:|-border-[paramTitles]-border-|",
			"H:|-border-[paramEntries]-border-|",
			"H:|-border-[divider1]-border-|",
			"H:|-border-[componentTitles]-border-|",
			"H:|-border-[dnom]-border-|",
			"H:|-border-[inferior]-border-|",
			"H:|-border-[numr]-border-|",
			"H:|-border-[superior]-border-|",
			"H:|-border-[divider2]-border-|",
			"H:|-border-[allMasters]-border-|",
			"H:|-border-[writeButton]-border-|",

			"V:|-border-[descriptionText]-space-[source]-margin-[default(==source)]-space-[paramTitles]-margin-"
			"[paramEntries]-margin-[divider1]-margin-[componentTitles]-margin-[dnom]-thin-[inferior]-thin-[numr]"
			"-thin-[superior]-margin-[divider2]-margin-[allMasters]-margin-[writeButton]-border-|"

		]

		metrics = {
			"width": 70,
			"border": 10,
			"margin": 10,
			"thin": 5,
			"space": 16
		}

		popup_rules = [
			"H:|[title]-[selector(width)]|",
			"V:|[title]|",
			"V:|[selector]|"
		]

		param_rules = [
			"H:|[width(width)]-[height(==width)]-[weight(==width)]|",
			"V:|[width]|",
			"V:|[height]|",
			"V:|[weight]|"
		]

		component_rules = [
			"H:|[figures]-[yShift(width)]|",
			"V:|[figures]|",
			"V:|[yShift]|"
		]

		select_nums_rules = [
			"H:|[select]-[shift(width)]|",
			"V:|[select]|",
			"V:|[shift]|"
		]

		self.w.source.addAutoPosSizeRules(popup_rules, metrics)
		self.w.default.addAutoPosSizeRules(popup_rules, metrics)
		self.w.paramTitles.addAutoPosSizeRules(param_rules, metrics)
		self.w.paramEntries.addAutoPosSizeRules(param_rules, metrics)
		self.w.componentTitles.addAutoPosSizeRules(component_rules, metrics)
		self.w.dnom.addAutoPosSizeRules(select_nums_rules, metrics)
		self.w.inferior.addAutoPosSizeRules(select_nums_rules, metrics)
		self.w.numr.addAutoPosSizeRules(select_nums_rules, metrics)
		self.w.superior.addAutoPosSizeRules(select_nums_rules, metrics)
		self.w.allMasters.addAutoPosSizeRules(select_nums_rules, metrics)

		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.setDefaultButton(self.w.writeButton)

		self.w.open()
		self.w.makeKey()

	def filter_for_name(self, name):
		for filter in Glyphs.filters:
			if filter.__class__.__name__ == name:
				return filter

	def selection_change(self, sender):
		selection = [".dnom", "inferior", ".numr", "superior"][self.w.default.selector.get()]
		self.w.dnom.select.enable(self.w.dnom.select.getTitle() != selection)
		self.w.inferior.select.enable(self.w.inferior.select.getTitle() != selection)
		self.w.numr.select.enable(self.w.numr.select.getTitle() != selection)
		self.w.superior.select.enable(self.w.superior.select.getTitle() != selection)

		self.w.dnom.shift.enable(self.w.dnom.select.getTitle() != selection)
		self.w.inferior.shift.enable(self.w.inferior.select.getTitle() != selection)
		self.w.numr.shift.enable(self.w.numr.select.getTitle() != selection)
		self.w.superior.shift.enable(self.w.superior.select.getTitle() != selection)

	def make_figures(self, sender):

		self.write_preferences()

		RMX_layers = []
		base_suffix = [".dnom", "inferior", ".numr", "superior"][self.w.default.selector.get()]
		source_suffix = ["", ".lf", ".tf"][self.w.source.selector.get()]
		for glyph in self.font.glyphs:
			if base_suffix in glyph.name:
				if not glyph.userData["RMXScaler"]:
					glyph.userData["RMXScaler"] = {}
				glyph.userData["RMXScaler"]["source"] = glyph.name.replace(base_suffix, source_suffix)

				for layer in glyph.layers:
					if self.w.allMasters.select.get() == 0 and layer is not glyph.layers[
						self.font.selectedFontMaster.id]:
						continue
					layer.userData["RMXScaler"] = {}
					layer.userData["RMXScaler"]["width"] = int(self.w.paramEntries.width.get())
					layer.userData["RMXScaler"]["height"] = int(self.w.paramEntries.height.get())
					layer.userData["RMXScaler"]["weight"] = int(self.w.paramEntries.weight.get())
					RMX_layers.append(layer)

		try:
			RMXScaler = self.filter_for_name("RMXScaler")
			RMXScaler.runFilterWithLayers_error_(RMX_layers, None)
		except:
			Message("Please run the RMX scaler manually for all %s figures." %base_suffix, "Couldn’t run RMX Scaler")

		selected_targets = []
		if self.w.dnom.select:
			selected_targets.append(".dnom")
		if self.w.inferior.select:
			selected_targets.append("inferior")
		if self.w.numr.select:
			selected_targets.append(".numr")
		if self.w.superior.select:
			selected_targets.append("superior")

		component_groups = [figure for figure in selected_targets if figure != base_suffix]
		component_targets = [number + "/" + suffix for suffix in component_groups for number in [
			"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"
		]
		                     ]

		for glyph in component_targets:
			glyph_name = glyph.replace("/", "")
			component_shift = int(Glyphs.defaults[
				                      "com.eweracs.BuildSmallFiguresRMX." + glyph.split("/")[1].replace(".",
				                                                                                        "") + "Shift"
				                      ])
			print(glyph.replace("/", ""), glyph.split("/")[0] + base_suffix, component_shift)
			if glyph_name not in self.font.glyphs:
				self.font.glyphs.append(GSGlyph(glyph_name))
			for layer in self.font[glyph_name].layers:
				if self.w.allMasters.select.get() == 0 and layer is not self.font.glyphs[
					glyph_name].layers[self.font.selectedFontMaster.id]:
					print("h")
					continue
				layer.clear()
				layer.shapes.append(GSComponent(glyph.split("/")[0] + base_suffix, NSPoint(0, component_shift)))

	def write_preferences(self):
		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.source"] = self.w.source.selector.get()
		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.default"] = self.w.default.selector.get()
		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.width"] = int(self.w.paramEntries.width.get())
		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.height"] = int(self.w.paramEntries.height.get())
		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.weight"] = int(self.w.paramEntries.weight.get())

		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.dnom"] = self.w.dnom.select.get()
		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.inferior"] = self.w.inferior.select.get()
		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.numr"] = self.w.numr.select.get()
		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.superior"] = self.w.superior.select.get()

		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.dnomShift"] = self.w.dnom.shift.get()
		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.inferiorShift"] = self.w.inferior.shift.get()
		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.numrShift"] = self.w.numr.shift.get()
		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.superiorShift"] = self.w.superior.shift.get()

		Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.allMasters"] = self.w.allMasters.select.get()

	def load_preferences(self):
		self.w.source.selector.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.source"] or 0)
		self.w.default.selector.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.default"] or 0)
		self.w.paramEntries.width.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.width"] or 0)
		self.w.paramEntries.height.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.height"] or 0)
		self.w.paramEntries.weight.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.weight"] or 0)

		self.w.dnom.select.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.dnom"] or 0)
		self.w.inferior.select.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.inferior"] or 0)
		self.w.numr.select.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.numr"] or 0)
		self.w.superior.select.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.superior"] or 0)

		self.w.dnom.shift.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.dnomShift"] or 0)
		self.w.inferior.shift.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.inferiorShift"] or 0)
		self.w.numr.shift.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.numrShift"] or 0)
		self.w.superior.shift.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.superiorShift"] or 0)

		self.w.allMasters.select.set(Glyphs.defaults["com.eweracs.BuildSmallFiguresRMX.allMasters"] or 0)


BuildFigures()
