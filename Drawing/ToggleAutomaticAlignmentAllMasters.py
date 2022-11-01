# MenuTitle: Toggle Automatic Alignment in All Masters
# -*- coding: utf-8 -*-

__doc__ = """
Toggles automatic alignment for the selected component in all masters.
"""


def toggle_automatic_alignment_all_masters():
	layer = Layer

	if layer is None:
		return

	for i, reference in enumerate(layer.components):
		if reference.selected or len(layer.selection) == 0:
			reference.automaticAlignment = not reference.automaticAlignment

		for layer in layer.parent.layers:
			if layer is layer:
				continue

			layer.components[i].automaticAlignment = reference.automaticAlignment


toggle_automatic_alignment_all_masters()
