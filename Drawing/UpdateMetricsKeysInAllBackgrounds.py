# MenuTitle: Update Metrics Keys in All Backgrounds
# -*- coding: utf-8 -*-

__doc__ = """
Updates the metrics keys in all backgrounds of the selected glyphs.
"""

from GlyphsApp import Glyphs

for layer in Glyphs.font.selectedLayers:
	parent = layer.parent
	for layer in parent.layers:
		layer.background.syncMetrics()
