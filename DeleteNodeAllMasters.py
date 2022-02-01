# MenuTitle: Delete Nodes in All Masters
# -*- coding: utf-8 -*-

__doc__ = """
Deletes the selected node(s) in all masters.
"""

for glyph in Font.selectedLayers:
	for layer in glyph.parent.layers:
		for path in layer.paths:
			delete_nodes = []
			for node in path.nodes:
				if node.selected:
					delete_nodes.append(node)
			for delete_node in delete_nodes:
				path.removeNodeCheckKeepShape_(delete_node)
