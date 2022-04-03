# MenuTitle: Re-interpolate anchors
# -*- coding: utf-8 -*-
__doc__ = """
Re-interpolates anchors for currently selected layer.
"""

for layer in Font.selectedLayers:
	copy_layer = layer.copy()
	layer.reinterpolate()
	if str(Glyphs.versionNumber)[0] == "3":
		layer.shapes = copy_layer.shapes
	else:
		layer.paths = copy_layer.paths
		layer.components = copy_layer.components
	layer.width = copy_layer.width
	layer.hints = copy_layer.hints
