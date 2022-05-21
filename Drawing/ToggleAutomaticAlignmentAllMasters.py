# MenuTitle: Toggle Automatic Alignment in All Masters
# -*- coding: utf-8 -*-

__doc__ = """
Toggles automatic alignment for the selected component in all masters.
"""


class ToggleAutomaticAlignmentAllMasters:
	def __init__(self):
		self.layer = Layer

		if self.layer is None:
			return

		for i, reference in enumerate(self.layer.components):
			if reference.selected:
				reference.automaticAlignment = not reference.automaticAlignment

			for layer in self.layer.parent.layers:
				if layer is self.layer:
					continue

				layer.components[i].automaticAlignment = reference.automaticAlignment


ToggleAutomaticAlignmentAllMasters()
