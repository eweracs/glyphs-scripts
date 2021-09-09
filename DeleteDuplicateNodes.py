# MenuTitle: Delete Duplicate Nodes
# -*- coding: utf-8 -*-

__doc__ = """
Deletes duplicate nodes, helpful after converting quadratic paths to cubic.
"""


if Font is None:
	Message("No font selected", "Select a font project!")

for layer in Font.selectedLayers:
	for path in layer.paths:
		nodes = [node.position for node in path.nodes]
		del_nodes = []
		for i, node in enumerate(path.nodes):
			if nodes.count(node.position) > 1:
				del_nodes.append(i)
		del del_nodes[::2]
		for i, node in enumerate(del_nodes):
			path.removeNodeCheckKeepShape_(path.nodes[node - i])
