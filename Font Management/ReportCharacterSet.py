# MenuTitle: Report Character Set
# -*- coding: utf-8 -*-

__doc__ = """
Reports the character set of the current font.
"""

from vanilla import FloatingWindow, CheckBox, Group, TextBox, EditText, HorizontalLine, Button
from GlyphsApp import Glyphs, Message

# Report the glyph names in the current font to the console.
# Options to exclude non-exporting glyphs, stylistic sets. and suffixed glyphs.
# auto alignment in vanilla attributes


class ReportCharacterSet:
	def __init__(self):
		self.font = Glyphs.font

		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		self.w = FloatingWindow((1, 1), "Report Character Set", maxSize=(300, 500))

		self.w.excludeNonExporting = CheckBox("auto", "Only exporting glyphs", value=True, sizeStyle="small")
		self.w.excludeStylisticSets = CheckBox("auto", "Ignore stylistic sets", value=True, sizeStyle="small")
		self.w.excludeSuffixedGlyphs = CheckBox("auto", "Ignore suffixed glyphs", value=True, sizeStyle="small")

		self.w.includeSuffixes = Group("auto")
		self.w.includeSuffixes.title = TextBox("auto", "Except:", sizeStyle="small")
		self.w.includeSuffixes.suffixes = EditText(
			"auto",
			text="case tf dnom numr loclCAT alt notdef",
			sizeStyle="small"
		)

		self.w.divider = HorizontalLine("auto")

		self.w.report = Button("auto", "Report in Macro Window", callback=self.report_glyphs)

		self.w.setDefaultButton(self.w.report)

		group_rules = [
			"H:|-margin-[title]-margin-[suffixes(>=200)]-margin-|",
			"V:[title]",
			"V:|[suffixes]|",
		]

		rules = [
			"H:|-margin-[excludeNonExporting]-margin-|",
			"H:|-margin-[excludeStylisticSets]-margin-|",
			"H:|-margin-[excludeSuffixedGlyphs]-margin-|",
			"H:|-margin-[includeSuffixes]-margin-|",
			"H:|-margin-[divider]-margin-|",
			"H:|-margin-[report]-margin-|",
			"V:|-margin-[excludeNonExporting]-margin-[excludeStylisticSets]-margin-[excludeSuffixedGlyphs]-margin-"
			"[includeSuffixes]-margin-[divider]-margin-[report]-margin-|"
		]

		metrics = {
			"margin": 10
		}

		self.w.includeSuffixes.addAutoPosSizeRules(group_rules, metrics)
		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.open()
		self.w.makeKey()

	def report_glyphs(self, sender):
		character_set = []
		for glyph in self.font.glyphs:
			if self.w.excludeNonExporting.get() and not glyph.export:
				continue
			if self.w.excludeStylisticSets.get() and ".ss" in glyph.name:
				continue
			if self.w.excludeSuffixedGlyphs.get() and "." in glyph.name:
				for suffix in self.w.includeSuffixes.suffixes.get().split(" "):
					if glyph.name.endswith(suffix):
						character_set.append(glyph.name)
						break
				continue
			character_set.append(glyph.name)

		Glyphs.clearLog()
		Glyphs.showMacroWindow()
		print("Character set (%s glyphs):\n\n%s" % (len(character_set), "\n".join(character_set)))


ReportCharacterSet()
