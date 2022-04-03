# MenuTitle: Delete Duplicate Nodes
# -*- coding: utf-8 -*-

__doc__ = """
Deletes duplicate nodes, helpful after converting quadratic paths to cubic.
"""

for layer in Font.selectedLayers:
	for path in layer.paths:
		for node in path.nodes:
			if node.position == node.nextNode.position:
				path.removeNodeCheckKeepShape_(node)