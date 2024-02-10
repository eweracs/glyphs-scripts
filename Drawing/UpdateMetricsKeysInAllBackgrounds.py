# MenuTitle: Update Metrics Keys in All Backgrounds
# -*- coding: utf-8 -*-

__doc__ = """
Updates the metrics keys in all backgrounds of the selected glyphs.
"""

for layer in Font.selectedLayers:
	parent = layer.parent
	for layer in parent.layers:
		layer.background.syncMetrics()
