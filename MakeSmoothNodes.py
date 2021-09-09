# MenuTitle: Node Smoother
# -*- coding: utf-8 -*-

__doc__ = """
Set nodes not set to smooth that should be.
"""

for layer in Font.selectedLayers:
	for path in layer.paths:
		for node in path.nodes:
			if node.type != "offcurve":
				for i in range(2):
					curr = node.position[i]
					next = node.nextNode.position[i]
					prev = node.prevNode.position[i]
					if curr == next and curr == prev:
						node.smooth = True
