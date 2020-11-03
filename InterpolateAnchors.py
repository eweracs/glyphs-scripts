#MenuTitle: Re-interpolate anchors
# -*- coding: utf-8 -*-
__doc__="""
Re-interpolates anchors for currently selected layer.
"""

for thisLayer in Font.selectedLayers:
	copyLayer = thisLayer.copy()
	thisLayer.reinterpolate()
	thisLayer.paths = copyLayer.paths
	thisLayer.components = copyLayer.components
	thisLayer.width = copyLayer.width
	thisLayer.hints = copyLayer.hints