# MenuTitle: Toggle Automatic Alignment in All Masters
# -*- coding: utf-8 -*-

__doc__ = """
Toggles automatic alignment for the selected component in all masters.
"""


def toggle_automatic_alignment_all_masters():
	selected_components = [component for component in Layer.components if component.selected]

	for layer in Layer.parent.layers:
		for component in layer.components:
			if component.name in [selected_component.name for selected_component in selected_components]:
				component.automaticAlignment = not component.automaticAlignment


toggle_automatic_alignment_all_masters()
