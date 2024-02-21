# MenuTitle: Delete Duplicate Nodes
# -*- coding: utf-8 -*-

__doc__ = """
Deletes duplicate nodes, helpful after converting quadratic paths to cubic.
"""

from GlyphsApp import Glyphs

for layer in Glyphs.font.selectedLayers:
	for path in layer.paths:
		for node in path.nodes:
			if node.position == node.nextNode.position:
				path.removeNodeCheckKeepShape_(node)
