# MenuTitle: Print mMster Models
# -*- coding: utf-8 -*-

__doc__ = """
Prints a tab with all Kern On models for each master.
"""

for i, master in enumerate(Font.masters):
	if master.userData["KernOnIsInterpolated"]:
		continue

	negativeModels = []
	zeroModels = []
	positiveModels = []

	for model in master.userData["KernOnModels"]:
		Lglyph = Font.glyphs[model.split(" ")[0]]
		Rglyph = Font.glyphs[model.split(" ")[1]]
		newModel = "/" + Lglyph.name + "/" + Rglyph.name
		model_kerning = Rglyph.layers[i].previousKerningForLayer_direction_(Lglyph.layers[i], LTR)
		if model_kerning == 0 or model_kerning is None:
			zeroModels.append(newModel)
		elif model_kerning > 0:
			positiveModels.append(newModel)
		elif model_kerning < 0:
			negativeModels.append(newModel)

	text = master.name + " (" + str(len(master.userData["KernOnModels"])) + " models)\n\nZero:\n" + \
	       "/space".join(
		zeroModels) + "\n\nPositive:\n" \
	    + "/space".join(positiveModels) + "\n\nNegative:\n" + "/space".join(negativeModels)

	Font.newTab(text)
	Font.currentTab.masterIndex = i
