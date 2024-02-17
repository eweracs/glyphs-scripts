# MenuTitle: Adjust Capital Kerning
# -*- coding: utf-8 -*-

__doc__ = """
Adjust the amount of base kerning between capitals.
"""

from vanilla import FloatingWindow, Group, TextBox, SegmentedButton, EditText, HorizontalLine, Button
from GlyphsApp import Glyphs, Message, UPDATEINTERFACE


class AdjustCapKern:
	def __init__(self):

		self.font = Glyphs.font
		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		# check whether font has class kerning
		try:
			if "@MMK" in self.font.kerning[self.font.masters[0].id].items()[0][0]:
				Message(
					"This script only works on projects before kerning has been generated.",
					"Font has class kerning"
				)
				return
		except:
			pass

		self.masterParams = {master.id: 0 for master in self.font.masters}

		self.w = FloatingWindow((1, 1), "Adjust Capital Kerning", maxSize=(500, 500))

		self.w.master = Group("auto")
		self.w.master.title = TextBox("auto", "Master: " + self.font.selectedFontMaster.name, sizeStyle="small")
		self.w.master.selector = SegmentedButton(
			"auto",
			[dict(title="←"), dict(title="→")],
			callback=self.master_switcher,
			sizeStyle="small"
		)

		self.w.capKern = Group("auto")
		self.w.capKern.title = TextBox("auto", "Adjust capital models by:", sizeStyle="small")

		self.w.capKern.selector = EditText(
			"auto",
			text=self.masterParams[self.font.selectedFontMaster.id],
			callback=self.set_cap_kern,
			sizeStyle="small"
		)
		self.w.capKern.selector.selectAll()

		self.w.divider = HorizontalLine("auto")

		self.w.adjustButton = Button(
			"auto",
			"Adjust models",
			callback=self.adjust_capital_models,
			sizeStyle="small"
		)

		rules = [
			"H:|-border-[master]-border-|",
			"H:|-border-[capKern]-border-|",
			"H:|-border-[adjustButton]-border-|",
			"H:|-border-[divider]-border-|",

			"V:|-border-[master]-margin-[capKern]-margin-[divider]-margin-[adjustButton]-border-|",
		]

		group_rules = [
			"H:|[title]-[selector(buttonWidth)]|",
			"V:|[selector]|"
		]

		metrics = {
			"buttonWidth": 50,
			"margin": 10,
			"border": 10
		}

		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.capKern.addAutoPosSizeRules(group_rules, metrics)
		self.w.master.addAutoPosSizeRules(group_rules, metrics)

		self.w.setDefaultButton(self.w.adjustButton)
		self.w.open()
		self.w.makeKey()
		self.w.bind("close", self.window_close)

		Glyphs.addCallback(self.ui_update, UPDATEINTERFACE)

	def master_switcher(self, sender):
		if sender.get() == 1:
			self.font.masterIndex += 1
		else:
			self.font.masterIndex -= 1

	def set_cap_kern(self, sender):
		self.masterParams[self.font.selectedFontMaster.id] = int(self.w.capKern.selector.get())

	def adjust_capital_models(self, sender):
		# for all Kern On models in the current master, check whether both glyphs are capital
		# and adjust the kerning according to the entry in the selector
		for model in self.font.selectedFontMaster.userData["KernOnModels"]:
			left = self.font.glyphs[model.split(" ")[0]]
			right = self.font.glyphs[model.split(" ")[1]]
			current_kerning = self.font.kerningForPair(self.font.selectedFontMaster.id, left.name, right.name)
			if left.case == 1 and left.category == "Letter" and right.case == 1 and right.category == "Letter":
				self.font.setKerningForPair(
					self.font.selectedFontMaster.id,
					left.name,
					right.name,
					current_kerning + self.masterParams[self.font.selectedFontMaster.id]
				)

	def ui_update(self, info):
		self.w.master.title.set("Master: " + self.font.selectedFontMaster.name)
		self.w.capKern.selector.set(self.masterParams[self.font.selectedFontMaster.id])

	def window_close(self, sender):
		Glyphs.removeCallback(self.ui_update, UPDATEINTERFACE)


AdjustCapKern()
