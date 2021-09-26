# MenuTitle: Interpolate Letterspacer
# -*- coding: utf-8 -*-

__doc__ = """
Interpolate HT Letterspacer values for different masters.
"""

import vanilla


class InterpolateLetterspacer:
	def __init__(self):

		if Font is None:
			Message("No font selected.", "Select a font project!")
			return

		if len(Font.axes) > 1:
			Message("You can still use it to interpolate along the first axis of your project.",
			        "This script only works for singe-axis setups for the moment.")

		self.font = Font

		self.master_list = [master for master in self.font.masters]
		self.selected_targets = {}

		for master in self.font.masters:
			self.selected_targets[master] = 0

		self.source_one = self.master_list[0]
		self.source_two = self.master_list[1]

		self.checkBoxList = []
		self.popUpButtonList = []

		self.ypos = 10

		self.w = vanilla.FloatingWindow((0, 0), "Interpolate Letterspacer")

		self.w.sourcesTitle = vanilla.TextBox((10, 10, -10, 14), "Source masters", sizeStyle="small")

		self.w.areaTitle = vanilla.TextBox((180, self.ypos + 3, 40, 14), "Area", alignment="center", sizeStyle="small")
		self.w.depthTitle = vanilla.TextBox((226, self.ypos + 3, 40, 14), "Depth", alignment="center",
		                                    sizeStyle="small")
		self.w.overTitle = vanilla.TextBox((272, self.ypos + 3, 40, 14), "Over", alignment="center", sizeStyle="small")

		self.ypos += 24

		self.w.sourceOneTitle = vanilla.TextBox((10, self.ypos + 3, -10, 14), "1:", sizeStyle="small")
		self.w.sourceOneSelector = vanilla.PopUpButton((32, self.ypos, 140, 20),
		                                               [master.name for master in self.font.masters],
		                                               callback=self.pick_first_master)

		self.w.sourceOneArea = vanilla.TextBox((180, self.ypos + 3, 40, 14),
		                                       str(self.source_one.customParameters["paramArea"] or "0"),
		                                       alignment="center", sizeStyle="small")
		self.w.sourceOneDepth = vanilla.TextBox((226, self.ypos + 3, 40, 14),
		                                        str(self.source_one.customParameters["paramDepth"] or "0"),
		                                        alignment="center", sizeStyle="small")
		self.w.sourceOneOver = vanilla.TextBox((272, self.ypos + 3, 40, 14),
		                                       str(self.source_one.customParameters["paramOver"] or "0"),
		                                       alignment="center", sizeStyle="small")

		self.ypos += 32

		self.w.sourceTwoTitle = vanilla.TextBox((10, self.ypos + 3, -10, 14), "2:", sizeStyle="small")
		self.w.sourceTwoSelector = vanilla.PopUpButton((32, self.ypos, 140, 20),
		                                               [master.name for master in self.font.masters],
		                                               callback=self.pick_second_master)

		self.w.sourceTwoSelector.set(1)

		self.w.sourceTwoArea = vanilla.TextBox((180, self.ypos + 3, 40, 14),
		                                       str(self.source_two.customParameters["paramArea"] or "0"),
		                                       alignment="center", sizeStyle="small")
		self.w.sourceTwoDepth = vanilla.TextBox((226, self.ypos + 3, 40, 14),
		                                        str(self.source_two.customParameters["paramDepth"] or "0"),
		                                        alignment="center", sizeStyle="small")
		self.w.sourceTwoOver = vanilla.TextBox((272, self.ypos + 3, 40, 14),
		                                       str(self.source_two.customParameters["paramOver"] or "0"),
		                                       alignment="center", sizeStyle="small")

		self.ypos += 32

		self.w.divider = vanilla.HorizontalLine((10, self.ypos, -10, 1))

		self.ypos += 10

		self.w.interpolationTitle = vanilla.TextBox((10, self.ypos, -10, 14), "Target masters", sizeStyle="small")

		self.ypos += 24

		for i, master in enumerate(self.master_list):
			check_box = vanilla.CheckBox((10, self.ypos, 162, 20), str(i + 1) + ") " + self.master_list[i].name,
			                             callback=self.select_interpolation_targets, value=True)
			pop_up_button = vanilla.PopUpButton((180, self.ypos, -10, 20),
			                                    ["Interpolate", "Copy from 1", "Copy from 2"],
			                                    callback=self.pick_interpolation_type)
			setattr(self.w, str(i) + "CheckBox", check_box)
			setattr(self.w, str(i) + "PopUpButton", pop_up_button)

			self.checkBoxList.append(check_box)
			self.popUpButtonList.append(pop_up_button)
			self.ypos += 32

		self.w.writeParameters = vanilla.Button((10, self.ypos, -10, 20), "Write parameters",
		                                        callback=self.write_parameters)

		self.update_states()

		self.w.setDefaultButton(self.w.writeParameters)
		self.w.resize(320, self.ypos + 32)
		self.w.open()
		self.w.makeKey()

	def update_states(self):
		for i in range(len(self.checkBoxList)):
			self.checkBoxList[i].enable(True)
			self.popUpButtonList[i].enable(True)

			if self.master_list[i].name == self.source_one.name or self.master_list[i].name == self.source_two.name:
				self.checkBoxList[i].enable(False)
				self.popUpButtonList[i].enable(False)

	def pick_first_master(self, sender):
		self.source_one = self.master_list[sender.get()]
		self.w.sourceOneArea.set(str(self.source_two.customParameters["paramArea"] or "0"))
		self.w.sourceTwoDepth.set(str(self.source_two.customParameters["paramDepth"] or "0"))
		self.w.sourceTwoOver.set(str(self.source_two.customParameters["paramOver"] or "0"))

		self.update_states()

	def pick_second_master(self, sender):
		self.source_two = self.master_list[sender.get()]
		self.w.sourceTwoArea.set(str(self.source_two.customParameters["paramArea"] or "0"))
		self.w.sourceTwoDepth.set(str(self.source_two.customParameters["paramDepth"] or "0"))
		self.w.sourceTwoOver.set(str(self.source_two.customParameters["paramOver"] or "0"))

		self.update_states()

	def select_interpolation_targets(self, sender):
		for i, item in enumerate(self.checkBoxList):
			if item is sender:
				if sender.get() == 1:
					self.selected_targets[self.master_list[i]] = self.popUpButtonList[i].get()
				else:
					del self.selected_targets[self.master_list[i]]

	def pick_interpolation_type(self, sender):
		for i, item in enumerate(self.popUpButtonList):
			if item is sender:
				self.selected_targets[self.master_list[i]] = sender.get()
				print(self.selected_targets)

	def write_parameters(self, sender):
		for target in self.selected_targets:
			if target.name != self.source_one.name and target.name != self.source_two.name:
				if self.selected_targets[target] == 0 and self.source_one == self.source_two:
					Message("Cannot interpolate between two identical masters.", "Select two different masters.")
					return
				for parameter in ["paramArea", "paramDepth", "paramOver"]:
					try:
						target.customParameters[parameter] = self.calculate_values(
							self.selected_targets[target],
							self.source_one.axes[0],
							self.source_two.axes[0],
							float(self.source_one.customParameters[parameter]),
							float(self.source_two.customParameters[parameter]),
							target.axes[0]
						)

					except Exception:
						print("Parameter " + parameter + " not used.")

	def calculate_values(self, mode, master_one, master_two, value_one, value_two, target):
		if mode == 0:
			return int(value_two + (target - master_two) * ((value_two - value_one) / (master_two - master_one)))
		if mode == 1:
			return value_one
		if mode == 2:
			return value_two


InterpolateLetterspacer()
