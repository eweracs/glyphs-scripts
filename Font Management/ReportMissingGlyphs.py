# MenuTitle: Report Missing Glyphs
# -*- coding: utf-8 -*-

__doc__ = """
Reports glyphs missing in current font based on another font.
"""

from vanilla import *


class ReportMissingGlyphs():
	def __init__(self):

		if len(Glyphs.fonts) < 2:
			Message("Open two fonts for comparison!", "No fonts to compare")
			return

		self.font = Glyphs.fonts[0]
		self.compare_font = Glyphs.fonts[1]

		self.w = FloatingWindow((1, 1), "Report Missing Glyphs", maxSize=(300, 800))

		# add a title to display the name of the currently open font, without the extension
		self.w.source = Group("auto")
		self.w.source.title = TextBox("auto", "Font to inspect:",
		                       sizeStyle="small")
		self.w.source.select = TextBox("auto",  self.font.filepath.split("/")[-1].split(".")[0], sizeStyle="small")

		# add a vanilla group
		# add a title for the compare font
		# add a popup to select the font to compare against
		self.w.compare = Group("auto")
		self.w.compare.title = TextBox("auto", "Compare against:", sizeStyle="small")
		self.w.compare.select = PopUpButton("auto", [font.filepath.split("/")[-1].split(".")[0] for font in
		                                             Glyphs.fonts if font != self.font],
		                                    sizeStyle="small",
		                                    callback=self.select_compare_font)

		# add a divider
		self.w.divider1 = HorizontalLine("auto")

		# add a text box to display the missing glyphs
		self.missing = Group((0, 0, 0, 0))
		self.missing.text = TextBox("auto", "", selectable=True, sizeStyle="small")
		self.w.missingTitle = TextBox("auto", "Missing glyphs:", sizeStyle="small")
		self.w.missing = ScrollView("auto", self.missing.getNSView())

		# check only exporting glyphs?
		self.w.onlyExportingGlyphs = CheckBox("auto", "Only check exporting glyphs", sizeStyle="small",
		                                      callback=self.update_missing_glyphs)

		# ignore stylistic sets?
		self.w.ignoreStylisticSets = CheckBox("auto", "Ignore stylistic set glyphs", sizeStyle="small",
		                                      callback=self.update_missing_glyphs)

		# add a divider
		self.w.divider2 = HorizontalLine("auto")

		# add a checkbox to open a tab with the generated glyphs
		self.w.openTab = CheckBox("auto", "Open tab with generated glyphs", sizeStyle="small",
		                          callback=self.save_preferences)

		# add a button to generate the missing glyphs
		self.w.generate = Button("auto", "Generate missing glyphs", callback=self.generate_missing_glyphs)

		self.update_missing_glyphs()
		
		group_rules = [
			"H:|[title]-margin-[select]|",
			"V:[title]",
			"V:|[select]|",
		]

		rules = [
			"H:|-margin-[source]-margin-|",
			"H:|-margin-[compare]-margin-|",
			"H:|-margin-[onlyExportingGlyphs]-margin-|",
			"H:|-margin-[ignoreStylisticSets]-margin-|",
			"H:|-margin-[divider1]-margin-|",
			"H:|-margin-[missingTitle]-margin-|",
			"H:|-margin-[missing]-margin-|",
			"H:|-margin-[divider2]-margin-|",
			"H:|-margin-[generate]-margin-|",
			"H:|-margin-[openTab]-margin-|",
			"V:|-margin-[source]-margin-[compare]-margin-[onlyExportingGlyphs]-margin-[ignoreStylisticSets]-margin-"
			"[divider1]-margin-[missingTitle]-margin-[missing(>=100)]-margin-[divider2]-margin-[generate]-margin-"
			"[openTab]-margin-|",
		]

		metrics = {
			"margin": 10
		}

		self.w.setDefaultButton(self.w.generate)
		self.missing.addAutoPosSizeRules(["H:|-margin-[text]-margin-|", "V:|-margin-[text]-margin-|"], metrics)
		self.w.source.addAutoPosSizeRules(group_rules, metrics)
		self.w.compare.addAutoPosSizeRules(group_rules, metrics)
		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.open()
		self.w.makeKey()

		self.read_preferences()

		self.w.bind("close", self.save_preferences)

	def select_compare_font(self, sender):
		self.compare_font = Glyphs.fonts[sender.get() + 1]
		self.update_missing_glyphs()

	def update_missing_glyphs(self, sender=None):
		self.missing_glyphs = []
		for glyph in self.compare_font.glyphs:
			if glyph.name not in self.font.glyphs:
				if self.w.onlyExportingGlyphs.get() and not glyph.export:
					continue
				if self.w.ignoreStylisticSets.get() and ".ss" in glyph.name:
					continue
				self.missing_glyphs.append(glyph.name)
		self.missing.text.set("\n".join(self.missing_glyphs))
		if len(self.missing_glyphs) == 0:
			self.missing.text.set("No missing glyphs found.")

		# count the number of lines in the text box and scale the scroll view accordingly
		self.missing.resize(self.w.missing.getNSScrollView().frame().size.width, len(self.missing_glyphs) * 15)

		# enable the generate button only if there are missing glyphs
		self.w.generate.enable(len(self.missing_glyphs) > 0)

	def generate_missing_glyphs(self, sender):
		self.font.disableUpdateInterface()
		Glyphs.showMacroWindow()
		print("Generating missing glyphs:")
		for glyph in self.missing_glyphs:
			missing_glyph = GSGlyph(glyph)
			self.font.glyphs.append(missing_glyph)
			print(glyph)

		print("\n...Done.")

		self.font.enableUpdateInterface()

		for glyph in self.missing_glyphs:
			for layer in self.font.glyphs[glyph].layers:
				layer.makeComponents()

		if self.w.openTab.get():
			self.font.newTab("/" + "/".join(self.missing_glyphs))

		self.update_missing_glyphs()

	# read and write preferences
	def read_preferences(self):
		try:
			self.w.openTab.set(Glyphs.defaults["com.eweracs.MissingGlyphs.openTab"])
		except:
			self.w.openTab.set(True)
		try:
			self.w.onlyExportingGlyphs.set(Glyphs.defaults["com.eweracs.MissingGlyphs.onlyExportingGlyphs"])
		except:
			self.w.onlyExportingGlyphs.set(False)
		try:
			self.w.ignoreStylisticSets.set(Glyphs.defaults["com.eweracs.MissingGlyphs.ignoreStylisticSets"])
		except:
			self.w.ignoreStylisticSets.set(False)

	def save_preferences(self, sender):
		Glyphs.defaults["com.eweracs.MissingGlyphs.openTab"] = self.w.openTab.get()
		Glyphs.defaults["com.eweracs.MissingGlyphs.onlyExportingGlyphs"] = self.w.onlyExportingGlyphs.get()
		Glyphs.defaults["com.eweracs.MissingGlyphs.ignoreStylisticSets"] = self.w.ignoreStylisticSets.get()


ReportMissingGlyphs()
