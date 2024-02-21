# MenuTitle: Show Current Glyph Models
# -*- coding: utf-8 -*-

__doc__ = """
Prints models in the current master that include the selected glyph(s).
"""

# check if current master has Kern On models, if not, show a message
# show the models in the current master that include the currently selected glyph, open a new tab and list all models
# if no models are found, show a message

from GlyphsApp import Glyphs, Message


def ModelsForGlyph(Font):
	if Font is None:
		return
	master = Font.selectedFontMaster
	if master.userData["KernOnModels"] is None:
		Message("This master doesn’t contain any Kern On models.", "No models found")
		return

	no_models = []

	for layer in Font.selectedLayers:
		models = []
		glyph_name = layer.parent.name
		for model in master.userData["KernOnModels"]:
			if glyph_name == model.split(" ")[0] or glyph_name == model.split(" ")[1]:
				models.append(model.replace(" ", "/"))

		if len(models) > 0:
			Font.newTab(
				"Models with glyph %s in master %s:\n" % (glyph_name, master.name) + "\n/".join(models)
			)
		else:
			no_models.append(glyph_name)

	if len(no_models) > 0:
		Message("No models found for glyphs: " + ", ".join(no_models), "No models found")


ModelsForGlyph(Glyphs.font)
