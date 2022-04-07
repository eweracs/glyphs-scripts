# MenuTitle: Copy Parameters Between Masters
# -*- coding: utf-8 -*-

__doc__ = """
Copies HTLS Parameters Between Masters.
"""

# CoPilot commands
# with the vanilla library
# Make a floating window
# auto positioning
# Everything in sizeStyle small
# make a text field: "Copy from:"
# Make a check box: "Current master to"
# Make a PopUpButton with a list of all masters except the current one
# Make a check box "First half of masters to the other half"
# Make a horizontal line (separator)
# Make a button: "Copy Parameters"
# Link the two check boxes to each other
# If the first check box is selected: copy the parameters from the current master to the other master selected in the
# popupbutton
# If the second box is selected: copy the parameters from the first half of the masters to the other half of the masters
# Make the copy button the default button

from vanilla import *

class CopyParameters():
	def __init__(self):

		self.font = Font
		if self.font == None:
			Message("No font selected", "Select a font project")
			return

		self.w = FloatingWindow((1, 1), "Copy Parameters")
		self.w.title = TextBox("auto", "Copy parameters from:", sizeStyle="small")

		self.w.currentMasterTo = CheckBox("auto", "Current master to", sizeStyle="small",
		                               callback=self.link_check_boxes)
		self.w.masterSelector = PopUpButton("auto", [master.name for master in self.font.masters if master is not
		                                             self.font.selectedFontMaster], sizeStyle="small")
		self.w.firstHalfMasters = CheckBox("auto", "First half of masters to the other half", sizeStyle="small",
		                                     callback=self.link_check_boxes)
		self.w.currentMasterTo.set(1)
		self.w.firstHalfMasters.set(0)

		self.w.divider = HorizontalLine("auto")

		self.w.copyParameters = Button("auto", "Copy Parameters", sizeStyle="small", callback=self.copy_parameters)

		rules = [
			"H:|-border-[title]-border-|",
			"H:|-border-[currentMasterTo]-border-|",
			"H:|-border-[masterSelector]-border-|",
			"H:|-border-[firstHalfMasters]-border-|",
			"H:|-border-[divider]-border-|",
			"H:|-border-[copyParameters]-border-|",
			"V:|-border-[title]-border-[currentMasterTo]-border-[masterSelector]-border-[firstHalfMasters]-border-"
			"[divider]-border-[copyParameters]-border-|"
		]

		metrics = {
			"border": 10,
			"margin": 10,
		}

		self.w.setDefaultButton(self.w.copyParameters)
		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.open()
		self.w.makeKey()

	def link_check_boxes(self, sender):
		if sender == self.w.currentMasterTo:
			self.w.firstHalfMasters.set(not sender.get())
		if sender == self.w.firstHalfMasters:
			self.w.currentMasterTo.set(not sender.get())

	def copy_parameters(self, sender):
		if self.w.currentMasterTo.get():
			for master in self.font.masters:
				if master.name == self.w.masterSelector.getItem():
					master.customParameters = self.font.selectedFontMaster.customParameters

		if self.w.firstHalfMasters.get():
			for master in self.font.masters[:len(self.font.masters)//2]:
				other_master = self.font.masters[len(self.font.masters)//2 + self.font.masters.index(master)]
				other_master.customParameters = master.customParameters

CopyParameters()
