# MenuTitle: Delete Nodes in All Masters
# -*- coding: utf-8 -*-

__doc__ = """
Deletes the selected node(s) in all masters.
"""

for glyph in Font.selectedLayers:
	for layer in glyph.parent.layers:
		for path in layer.paths:
			for node in path.nodes:
				if node.selected:
					path.removeNodeCheckKeepShape_(node)
