# MenuTitle: Copy models from Master
# -*- coding: utf-8 -*-

__doc__ = """
Copies Kern On models with values between masters.
"""

import vanilla


class CopyMasterModels:
	def __init__(self):
		if Font is None:
			Message("No font selected", "Select a font project!")
			return

		self.font = Font

		self.KOmasters = [master for master in Font.masters if master.userData["KernOnModels"]]

		if len(self.KOmasters) == 0:
			Message("Please set some models first.", "No Kern On models found")
			return

		self.w = vanilla.FloatingWindow((0, 0), "Copy models from Master")

		self.ypos = 10

		self.w.sourceTitle = vanilla.TextBox((10, self.ypos, -10, 14), "Source master:", sizeStyle="small")

		self.ypos += 24

		self.w.sourceSelector = vanilla.PopUpButton(
			(10, self.ypos, -100, 17), [str(i+1) + ": " + master.name for i, master in enumerate(self.font.masters)],
			callback=self.select_source)

		self.w.modelCounter = vanilla.TextBox((-90, self.ypos, -10, 17), str(len(self.font.masters[
			self.w.sourceSelector.get()].userData["KernOnModels"] or [])) + " models", sizeStyle="regular")

		self.ypos += 30

		self.w.onlyZeroModels = vanilla.CheckBox((10, self.ypos, -10, 17), "Copy only zero models")

		self.ypos += 26

		self.w.divider = vanilla.HorizontalLine((10, self.ypos, -10, 1))

		self.ypos += 10

		self.w.targetTitle = vanilla.TextBox((10, self.ypos, -10, 14), "Target masters:", sizeStyle="small")

		self.ypos += 24

		for i, master in enumerate(self.font.masters):
			setattr(self.w, master.name + str(i), vanilla.CheckBox((10, self.ypos, -10, 17), master.name,
			                                                       sizeStyle="regular"))
			if i == getattr(self.w, "sourceSelector").get():
				getattr(self.w, master.name + str(i)).enable(False)
			if master.userData["KernOnIsInterpolated"]:
				getattr(self.w, master.name + str(i)).setTitle(master.name + " (Interpolated)")
				getattr(self.w, master.name + str(i)).enable(False)
			self.ypos += 24

		self.ypos += 6

		self.w.copyButton = vanilla.Button((10, self.ypos, -10, 20), "Copy models", callback=self.copy_models)

		self.ypos += 32

		self.w.setDefaultButton(self.w.copyButton)

		self.w.resize(260, self.ypos)
		self.w.open()
		self.w.makeKey()

	def select_source(self, sender):
		self.sourceMaster = self.font.masters[sender.get()]
		for i, master in enumerate(self.font.masters):
			if master.userData["KernOnIsInterpolated"] is None:
				if i == sender.get():
					getattr(self.w, master.name + str(i)).set(False)
				getattr(self.w, master.name + str(i)).enable(i != sender.get())
		if self.sourceMaster.userData["KernOnModels"]:
			self.w.modelCounter.set(
				str(len(self.sourceMaster.userData["KernOnModels"])) + " models")
		else:
			self.w.modelCounter.set("0 models")
		self.w.copyButton.enable(self.font.masters[self.w.sourceSelector.get()].userData["KernOnModels"])

	def copy_models(self, sender):
		for i, master in enumerate(self.font.masters):
			if getattr(self.w, master.name + str(i)).get():
				master.userData["KernOnModels"] = self.sourceMaster.userData["KernOnModels"]
				for model in self.sourceMaster.userData["KernOnModels"]:

					left_glyph = model.split(" ")[0]
					right_glyph = model.split(" ")[1]
					model_kerning = self.font.kerningForPair(self.sourceMaster.id, left_glyph, right_glyph)

					if self.w.onlyZeroModels and model_kerning != 0:
						continue

					self.font.setKerningForPair(master.id, left_glyph, right_glyph, model_kerning)

		print("Copied models from master", self.font.masters[self.w.sourceSelector.get()].name, "to", ", ".join([
			master.name for i, master in enumerate(self.font.masters) if getattr(self.w, master.name + str(i)).get()]))


CopyMasterModels()
