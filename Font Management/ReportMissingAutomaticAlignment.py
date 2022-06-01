# MenuTitle: Report Missing Automatic Alignment
# -*- coding: utf-8 -*-

__doc__ = """
Prints a tab with all layers with mixed paths/components, or more than one component with missing automatic alignment.
"""

from vanilla import *


class ReportMissingAutomaticAlignment:
	def __init__(self):
		self.font = Font

		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		missing_alignment = []

		for glyph in self.font.glyphs:
			for layer in glyph.layers:
				if not layer.components:
					continue
				if not layer.isMasterLayer or not layer.isSpecialLayer:
					continue

				# check for mixed paths/components
				if layer.paths and layer.components:
					missing_alignment.append(layer)
					continue

				# check for multiple components without automatic alignment
				count = 0
				for component in layer.components:
					if component.automaticAlignment:
						count += 1
				if count < len(layer.components) - 1:
					missing_alignment.append(layer)

		if len(missing_alignment) > 0:
			self.font.newTab(missing_alignment)
		else:
			Message("No layers with missing automatic alignment found.", "All good!", OKButton="Nice.")


ReportMissingAutomaticAlignment()
