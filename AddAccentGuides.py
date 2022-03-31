# MenuTitle: Add Guides for Accents
# -*- coding: utf-8 -*-

__doc__ = """
Adds guides for accents based on the current design.
"""

from vanilla import *
from Foundation import NSPoint

class AddGuides:
	def __init__(self):
		self.font = Font

		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		self.LCBaseAccents = [accent for accent in [
			"dieresiscomb",
			"dotaccentcomb",
			"gravecomb",
			"acutecomb",
			"hungarumlautcomb",
			"caroncomb.alt",
			"circumflexcomb",
			"caroncomb",
			"brevecomb",
			"ringcomb",
			"tildecomb",
			"macroncomb",
			"commaturnedabovecomb"
		] if accent in self.font.glyphs]

		self.UCBaseAccents = [accent for accent in [
			"dieresiscomb.case",
			"dotaccentcomb.case",
			"gravecomb.case",
			"acutecomb.case",
			"hungarumlautcomb.case",
			"circumflexcomb.case",
			"caroncomb.case",
			"brevecomb.case",
			"ringcomb.case",
			"tildecomb.case",
			"macroncomb.case"
		] if accent in self.font.glyphs]

		self.w = FloatingWindow((1, 1), "Add guides for accents")

		self.w.references = Group("auto")
		self.w.references.title = TextBox("auto", "Accents", sizeStyle="small")
		self.w.references.reference = TextBox("auto", "Reference", sizeStyle="small")
		self.w.LCAccents = Group("auto")
		self.w.LCAccents.title = CheckBox("auto", "Lowercase", sizeStyle="small", callback=self.update_states)
		self.w.LCAccents.reference = PopUpButton("auto", self.LCBaseAccents, sizeStyle="small")
		self.w.UCAccents = Group("auto")
		self.w.UCAccents.title = CheckBox("auto", "Uppercase", sizeStyle="small", callback=self.update_states)
		self.w.UCAccents.reference = PopUpButton("auto", self.UCBaseAccents, sizeStyle="small")

		self.w.divider = HorizontalLine("auto")

		self.w.makeButton = Button("auto", "Add guides", callback=self.add_guides)

		self.load_preferences()

		self.update_states(None)

		rules = [
			"H:|-border-[references]-border-|",
			"H:|-border-[LCAccents]-border-|",
			"H:|-border-[UCAccents]-border-|",
			"H:|-border-[makeButton]-border-|",
			"H:|-border-[divider]-border-|",
			"V:|-border-[references]-margin-[LCAccents]-margin-[UCAccents]-margin-[divider]-margin-["
			"makeButton]-border-|"
		]

		case_rules = [
			"H:|[title]-margin-[reference(130)]|",
			"V:|[reference]|",
			"V:|[title]|"
		]

		metrics = {
			"border": 10,
			"margin": 10,
		}

		self.w.setDefaultButton(self.w.makeButton)
		self.w.references.addAutoPosSizeRules(case_rules, metrics)
		self.w.LCAccents.addAutoPosSizeRules(case_rules, metrics)
		self.w.UCAccents.addAutoPosSizeRules(case_rules, metrics)
		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.open()
		self.w.makeKey()

	def update_states(self, sender):
		self.w.LCAccents.reference.enable(self.w.LCAccents.title.get())
		self.w.UCAccents.reference.enable(self.w.UCAccents.title.get())
		self.w.makeButton.enable(self.w.LCAccents.title.get() + self.w.UCAccents.title.get() > 0)
		self.save_preferences()

	def measure_reference(self, glyph):
		reference = self.font.glyphs[glyph]
		return {master.id: NSPoint(reference.layers[master.id].width / 2,
		                           reference.layers[master.id].bounds.origin.y)
		        for master in self.font.masters}

	def add_guides(self, sender):
		if self.w.LCAccents.title.get():
			lc_accents_positions = self.measure_reference(self.w.LCAccents.reference.getItem())
			for masterID in lc_accents_positions:
				lc_accents_guide = GSGuide()
				lc_accents_guide.position = lc_accents_positions[masterID]
				lc_accents_guide.angle = 0
				lc_accents_guide.name = "LC Accents"
				lc_accents_guide.locked = True
				self.font.masters[masterID].guides.append(lc_accents_guide)

		if self.w.UCAccents.title.get():
			uc_accents_positions = self.measure_reference(self.w.UCAccents.reference.getItem())
			for masterID in uc_accents_positions:
				uc_accents_guide = GSGuide()
				uc_accents_guide.position = uc_accents_positions[masterID]
				uc_accents_guide.angle = 0
				uc_accents_guide.name = "UC Accents"
				uc_accents_guide.locked = True
				self.font.masters[masterID].guides.append(uc_accents_guide)

		try:
			self.font.currentTab.redraw()
		except:
			pass

		self.save_preferences()

	def load_preferences(self):
		try:
			self.w.LCAccents.title.set(Glyphs.defaults["com.eweracs.addAccentGuides.LCselected"])
		except:
			self.w.LCAccents.title.set(1)
		self.w.LCAccents.reference.setItem(
			Glyphs.defaults["com.eweracs.addAccentGuides.LCreference"] or self.w.LCAccents.reference.getItems()[0]
		)
		try:
			self.w.UCAccents.title.set(Glyphs.defaults["com.eweracs.addAccentGuides.UCselected"])
		except:
			self.w.UCAccents.title.set(1)
		self.w.UCAccents.reference.setItem(
			Glyphs.defaults["com.eweracs.addAccentGuides.UCreference"] or self.w.UCAccents.reference.getItems()[0]
		)

	def save_preferences(self):
		Glyphs.defaults["com.eweracs.addAccentGuides.LCselected"] = self.w.LCAccents.title.get()
		Glyphs.defaults["com.eweracs.addAccentGuides.LCreference"] = self.w.LCAccents.reference.getItem()
		Glyphs.defaults["com.eweracs.addAccentGuides.UCselected"] = self.w.UCAccents.title.get()
		Glyphs.defaults["com.eweracs.addAccentGuides.UCreference"] = self.w.UCAccents.reference.getItem()


AddGuides()
