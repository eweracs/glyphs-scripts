# MenuTitle: Toggle Special Layer
# -*- coding: utf-8 -*-

__doc__ = """
Toggles the activation state of special layers (intermediate or alternate).
"""

from GlyphsApp import Glyphs, Message


def toggle_special_layer(layer):
	if layer.attributes:
		layer.userData["attributes"] = {}
		if "axisRules" in layer.attributes:
			layer.userData["attributes"]["axisRules"] = {}
			for axis in layer.attributes["axisRules"].keys():
				layer.userData["attributes"]["axisRules"][axis] = {}
				for rule in layer.attributes["axisRules"][axis].keys():
					layer.userData["attributes"]["axisRules"][axis][rule] = layer.attributes["axisRules"][axis][rule]
			del layer.attributes["axisRules"]
		if "coordinates" in layer.attributes:
			layer.userData["attributes"]["coordinates"] = {}
			for axis in layer.attributes["coordinates"].keys():
				layer.userData["attributes"]["coordinates"][axis] = layer.attributes["coordinates"][axis]
			del layer.attributes["coordinates"]
		layer.name = "(Deactivated)"
	else:
		if not layer.userData["attributes"]:
			Message("No restorable attributes were found for the selected layer.", "No attributes to restore")
			return
		for key in layer.userData["attributes"]:
			layer.attributes[key] = layer.userData["attributes"][key]
		del layer.userData["attributes"]


for layer in Glyphs.font.selectedLayers:
	toggle_special_layer(layer)
