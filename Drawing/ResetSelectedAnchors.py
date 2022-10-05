# MenuTitle: Reset Selected Anchors
# -*- coding: utf-8 -*-

__doc__ = """
Resets only selected anchors for the current layer.
"""


def reset_selected_anchors(layer):
	ghost_layer = layer.copy()
	for ghost_anchor in ghost_layer.anchors:
		if layer.anchors[ghost_anchor.name].selected:
			ghost_anchor.selected = True
	layer.anchors = []
	layer.addMissingAnchors()
	for ghost_anchor in ghost_layer.anchors:
		if not ghost_anchor.selected:
			layer.anchors[ghost_anchor.name] = GSAnchor(ghost_anchor.name, ghost_anchor.position)


reset_selected_anchors(Layer)
