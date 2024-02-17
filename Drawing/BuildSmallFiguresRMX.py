# MenuTitle: Build Small Figures RMX
# -*- coding: utf-8 -*-

__doc__ = """
Builds small figures with RMX added to base glyphs.
"""

from vanilla import FloatingWindow, TextBox, Group, PopUpButton, HorizontalLine, SegmentedButton, EditText, CheckBox, Button
from Foundation import NSPoint
from GlyphsApp import Glyphs, GSGlyph, GSComponent, Message, UPDATEINTERFACE


class BuildFigures:
	def __init__(self):

		self.font = Glyphs.font
		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		self.currentMaster = self.font.selectedFontMaster

		self.base_suffixes = [".dnom", "inferior", ".numr", "superior"]

		self.w = FloatingWindow((0, 0), "Build Small Figures RMX")

		self.w.descriptionText = TextBox(
			"auto",
			"After defining RMX values for the base figures, these values will be "
			"written to the glyphs. Open RMX Scaler on these afterwards to scale "
			"them accordingly.",
			sizeStyle="small"
		)

		self.w.source = Group("auto")
		self.w.source.title = TextBox("auto", "Source figures:", sizeStyle="small")
		self.w.source.selector = PopUpButton(
			"auto", ["Default", "Proportional .lf", "Tabular .tf"], sizeStyle="small", callback=self.select_source
		)

		self.w.default = Group("auto")
		self.w.default.title = TextBox("auto", "Target figures:", sizeStyle="small")
		self.w.default.selector = PopUpButton(
			"auto", self.base_suffixes, sizeStyle="small", callback=self.select_default
		)

		self.w.divider1 = HorizontalLine("auto")

		self.w.master = Group("auto")
		self.w.master.title = TextBox(
			"auto", "Master: " + self.font.selectedFontMaster.name, sizeStyle="small"
		)
		self.w.master.selector = SegmentedButton(
			"auto", [dict(title="←"), dict(title="→")], callback=self.master_switcher
		)

		self.w.paramTitles = Group("auto")
		self.w.paramTitles.width = TextBox("auto", "Width %", sizeStyle="small")
		self.w.paramTitles.height = TextBox("auto", "Height %", sizeStyle="small")
		self.w.paramTitles.weight = TextBox("auto", "Weight", sizeStyle="small")

		self.w.paramEntries = Group("auto")
		self.w.paramEntries.width = EditText("auto", sizeStyle="small", text="0", callback=self.param_input)
		self.w.paramEntries.height = EditText("auto", sizeStyle="small", text="0", callback=self.param_input)
		self.w.paramEntries.weight = EditText("auto", sizeStyle="small", text="0", callback=self.param_input)

		self.w.divider2 = HorizontalLine("auto")

		self.w.componentTitles = Group("auto")
		self.w.componentTitles.figures = TextBox(
			"auto", "Build components:", sizeStyle="small"
		)

		self.w.componentTitles.yShift = TextBox(
			"auto", "y shift:", sizeStyle="small", alignment="left"
		)

		self.w.dnom = Group("auto")
		self.w.dnom.select = CheckBox("auto", ".dnom", sizeStyle="small")
		self.w.dnom.shift = EditText("auto", text="0", sizeStyle="small")

		self.w.inferior = Group("auto")
		self.w.inferior.select = CheckBox("auto", "inferior", sizeStyle="small")
		self.w.inferior.shift = EditText("auto", text="-100", sizeStyle="small")

		self.w.numr = Group("auto")
		self.w.numr.select = CheckBox("auto", ".numr", sizeStyle="small")
		self.w.numr.shift = EditText("auto", text="300", sizeStyle="small")

		self.w.superior = Group("auto")
		self.w.superior.select = CheckBox("auto", "superior", sizeStyle="small")
		self.w.superior.shift = EditText("auto", text="350", sizeStyle="small")

		self.w.divider3 = HorizontalLine("auto")

		# self.w.allMasters = Group("auto")
		# self.w.allMasters.select = CheckBox("auto", "Apply to all masters", sizeStyle="small")
		# self.w.allMasters.shift = TextBox("auto", "")

		self.w.writeButton = Button("auto", "Make figures", callback=self.make_figures)

		self.load_preferences()

		self.masterParams = {master.id: {
			"width": self.w.paramEntries.width.get(),
			"height": self.w.paramEntries.height.get(),
			"weight": self.w.paramEntries.weight.get()
		} for master in self.font.masters}

		self.select_default(None)
		self.param_input(None)

		rules = [
			"H:|-border-[" + item + "]-border-|" for item in [
				"descriptionText", "source", "default", "divider1", "master", "paramTitles", "paramEntries",
				"divider2", "componentTitles", "dnom", "inferior", "numr", "superior", "divider3",
				"writeButton"
			]
		]

		rules.append(
			"V:|-border-[descriptionText]-space-[source]-margin-[default(==source)]-margin-[divider1]-margin-"
			"[master]-margin-[paramTitles]-margin-[paramEntries]-margin-[divider2]-margin-"
			"[componentTitles]-margin-[dnom]-thin-[inferior]-thin-[numr]-thin-[superior]-margin-[divider3]"
			"-margin-[writeButton]-border-|"
		)

		metrics = {
			"buttonWidth": 70,
			"border": 10,
			"margin": 10,
			"thin": 5,
			"space": 16
		}

		popup_rules = [
			"H:|[title]-[selector(buttonWidth)]|",
			"V:|[title]|",
			"V:|[selector]|"
		]

		param_rules = [
			"H:|[width(buttonWidth)]-[height(==buttonWidth)]-[weight(==buttonWidth)]|",
			"V:|[width]|",
			"V:|[height]|",
			"V:|[weight]|"
		]

		component_rules = [
			"H:|[figures]-[yShift(buttonWidth)]|",
			"V:|[figures]|",
			"V:|[yShift]|"
		]

		select_nums_rules = [
			"H:|[select]-[shift(buttonWidth)]|",
			"V:|[select]|",
			"V:|[shift]|"
		]

		self.w.source.addAutoPosSizeRules(popup_rules, metrics)
		self.w.default.addAutoPosSizeRules(popup_rules, metrics)
		self.w.master.addAutoPosSizeRules(popup_rules, metrics)
		self.w.paramTitles.addAutoPosSizeRules(param_rules, metrics)
		self.w.paramEntries.addAutoPosSizeRules(param_rules, metrics)
		self.w.componentTitles.addAutoPosSizeRules(component_rules, metrics)
		self.w.dnom.addAutoPosSizeRules(select_nums_rules, metrics)
		self.w.inferior.addAutoPosSizeRules(select_nums_rules, metrics)
		self.w.numr.addAutoPosSizeRules(select_nums_rules, metrics)
		self.w.superior.addAutoPosSizeRules(select_nums_rules, metrics)
		# self.w.allMasters.addAutoPosSizeRules(select_nums_rules, metrics)

		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.setDefaultButton(self.w.writeButton)

		self.w.open()
		self.w.makeKey()
		self.w.bind("close", self.window_close)

		Glyphs.addCallback(self.ui_update, UPDATEINTERFACE)

	def filter_for_name(self, name):
		for filter in Glyphs.filters:
			if filter.__class__.__name__ == name:
				return filter

	def param_input(self, sender):
		self.masterParams[self.font.selectedFontMaster.id] = {
			"width": self.w.paramEntries.width.get(),
			"height": self.w.paramEntries.height.get(),
			"weight": self.w.paramEntries.weight.get()
		}

	def select_source(self, sender):
		missing_numbers = []
		for number in ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]:
			suffix = ["", ".lf", ".tf"][self.w.source.selector.get()]
			if number + suffix not in self.font.glyphs:
				missing_numbers.append(number + suffix)
		if len(missing_numbers) > 0:
			Message("Please add " + ", ".join(missing_numbers) + " to glyph set.", "Missing source glyphs for scaling")
			return False

	def select_default(self, sender):
		selection = self.base_suffixes[self.w.default.selector.get()]
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
		self.select_source(None)
		if not self.select_source(None):
			return

		RMX_layers = []
		base_suffix = self.base_suffixes[self.w.default.selector.get()]
		source_suffix = ["", ".lf", ".tf"][self.w.source.selector.get()]
		for glyph in self.font.glyphs:
			if base_suffix in glyph.name:
				if not glyph.userData["RMXScaler"]:
					glyph.userData["RMXScaler"] = {}
				glyph.userData["RMXScaler"]["source"] = glyph.name.replace(base_suffix, source_suffix)

				for layer in glyph.layers:
					layer.userData["RMXScaler"] = {}
					for name in self.masterParams[layer.master.id]:
						layer.userData["RMXScaler"][name] = int(self.masterParams[layer.master.id][name])
					RMX_layers.append(layer)

		try:
			RMXScaler = self.filter_for_name("RMXScaler")
			RMXScaler.runFilterWithLayers_error_(RMX_layers, None)
		except:
			Message("Please run the RMX scaler manually for all %s figures." % base_suffix, "Couldn’t run RMX Scaler")

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
		]]

		print("Building components:\n")
		for glyph in component_targets:
			glyph_name = glyph.replace("/", "")
			component_shift = int(Glyphs.defaults[
				self.domain(glyph.split("/")[1].replace(".", "") + "Shift")
			])
			print(
				glyph.replace("/", ""), "from",
				glyph.split("/")[0] + base_suffix, "with y shift", component_shift
			)
			if glyph_name not in self.font.glyphs:
				self.font.glyphs.append(GSGlyph(glyph_name))
			for layer in self.font[glyph_name].layers:
				if layer is not self.font.glyphs[glyph_name].layers[self.font.selectedFontMaster.id]:
					continue
				layer.clear()
				layer.shapes.append(GSComponent(glyph.split("/")[0] + base_suffix, NSPoint(0, component_shift)))
		print("\n...Done.")

	def master_switcher(self, sender):
		if sender.get() == 1:
			self.font.masterIndex += 1
		else:
			self.font.masterIndex -= 1

	def ui_update(self, info):
		if self.currentMaster != self.font.selectedFontMaster:
			self.w.master.title.set("Master: " + self.font.selectedFontMaster.name)
			for name in self.masterParams[self.font.selectedFontMaster.id]:
				getattr(self.w.paramEntries, name).set(self.masterParams[self.font.selectedFontMaster.id][name])
		self.currentMaster = self.font.selectedFontMaster

	def window_close(self, sender):
		Glyphs.removeCallback(self.ui_update, UPDATEINTERFACE)

	def domain(key):
		return "com.eweracs.BuildSmallFiguresRMX." + key

	def write_preferences(self):
		Glyphs.defaults[self.domain("source")] = self.w.source.selector.get()
		Glyphs.defaults[self.domain("default")] = self.w.default.selector.get()
		Glyphs.defaults[self.domain("width")] = int(self.w.paramEntries.width.get())
		Glyphs.defaults[self.domain("height")] = int(self.w.paramEntries.height.get())
		Glyphs.defaults[self.domain("weight")] = int(self.w.paramEntries.weight.get())

		for suffix in self.base_suffixes:
			suffix = suffix.replace(".", "")
			Glyphs.defaults[self.domain(suffix)] = getattr(self.w, suffix).select.get()
			Glyphs.defaults[self.domain(suffix + "Shift")] = getattr(self.w, suffix).shift.get()

		# Glyphs.defaults[self.domain("allMasters"] = self.w.allMasters.select.get()

	def load_preferences(self):
		self.w.source.selector.set(Glyphs.defaults[self.domain("source")] or 0)
		self.w.default.selector.set(Glyphs.defaults[self.domain("default")] or 0)
		self.w.paramEntries.width.set(Glyphs.defaults[self.domain("width")] or 0)
		self.w.paramEntries.height.set(Glyphs.defaults[self.domain("height")] or 0)
		self.w.paramEntries.weight.set(Glyphs.defaults[self.domain("weight")] or 0)

		for i, suffix in enumerate(self.base_suffixes):
			suffix = suffix.replace(".", "")
			control = getattr(self.w, suffix)
			control.select.set(Glyphs.defaults[self.domain(suffix)] or 0)
			control.shift.set(Glyphs.defaults[self.domain(suffix + "Shift")] or [0, -150, 280, 320][i])

		# self.w.allMasters.select.set(Glyphs.defaults[self.domain("allMasters"] or 1)


BuildFigures()
