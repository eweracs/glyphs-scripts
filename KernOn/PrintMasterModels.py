# MenuTitle: Print master models
# -*- coding: utf-8 -*-

__doc__ = """
Prints a tab with all Kern On models for each master.
"""

for i, master in enumerate(Font.masters):

	negativeModels = []
	zeroModels = []
	positiveModels = []

	for model in master.userData["KernOnModels"]:
		Lglyph = Font.glyphs[model.split(" ")[0]]
		Rglyph = Font.glyphs[model.split(" ")[1]]
		newModel = Lglyph.string + Rglyph.string
		model_kerning = Font.kerningForPair(master.id, Lglyph.name, Rglyph.name)
		if model_kerning == 0:
			zeroModels.append(newModel)
		elif model_kerning > 0:
			positiveModels.append(newModel)
		elif model_kerning < 0:
			negativeModels.append(newModel)

	text = "Zero models:\n" + " ".join(zeroModels) + "\n\nPositive models:\n" \
	       + " ".join(positiveModels) + "\n\nNegative models:\n" + " ".join(negativeModels)

	Font.newTab(text)
	Font.currentTab.masterIndex = i
