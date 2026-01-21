# MenuTitle: Print Models in All Masters
# -*- coding: utf-8 -*-

__doc__ = """
Prints a tab with all Kern On models for each master.
"""

from GlyphsApp import Glyphs, Message, LTR


class ModelsForGlyph:
	def __init__(self):

		self.font = Glyphs.font

		if self.font is None:
			return

		did_something = False

		for i, master in enumerate(self.font.masters):
			if master.userData["KernOnIsInterpolated"]\
				or not master.userData["KernOnModels"]\
				or len(master.userData["KernOnModels"]) == 0:
				continue

			negative_models = []
			zero_models = []
			positive_models = []

			for model in master.userData["KernOnModels"]:
				lglyph = self.font.glyphs[model.split(" ")[0]]
				rglyph = self.font.glyphs[model.split(" ")[1]]
				new_model = "/" + lglyph.name + "/" + rglyph.name
				model_kerning = rglyph.layers[i].previousKerningForLayer_direction_(lglyph.layers[i], LTR)
				if model_kerning == 0 or model_kerning is None:
					zero_models.append(new_model)
				elif model_kerning > 0:
					positive_models.append(new_model)
				elif model_kerning < 0:
					negative_models.append(new_model)

			text = master.name + " (" + str(len(master.userData["KernOnModels"])) + " models)\n\nZero:\n" + \
				"/space".join(zero_models) + "\n\nPositive:\n" + "/space".join(positive_models) + \
				"\n\nNegative:\n" + "/space".join(negative_models)

			self.font.newTab(text)
			self.font.currentTab.masterIndex = i

			did_something = True

		if not did_something:
			Message("This project does not appear to contain any Kern On models.", "No models found")


ModelsForGlyph()
