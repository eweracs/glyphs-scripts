# MenuTitle: Report Missing Automatic Alignment
# -*- coding: utf-8 -*-

__doc__ = """
Prints a tab with all layers with mixed paths/components, or more than one component with missing automatic alignment.
"""

from GlyphsApp import Glyphs, Message


class ReportMissingAutomaticAlignment:
	def __init__(self):
		self.font = Glyphs.font

		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		missing_alignment = []

		for glyph in self.font.glyphs:
			for layer in glyph.layers:
				if not layer.components:
					continue
				if not layer.isMasterLayer and not layer.isSpecialLayer:
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
				if count < len(layer.components):
					if len(layer.components) > 1:
						count_2 = 0
						for component in list(layer.components)[1:]:
							if component.automaticAlignment:
								count_2 += 1
						if count_2 < len(layer.components) - 1:
							missing_alignment.append(layer)

				# check for missing automatic alignment if only one component is present
				if len(layer.components) == 1 and not layer.components[0].automaticAlignment:
					missing_alignment.append(layer)

		if len(missing_alignment) > 0:
			self.font.newTab(missing_alignment)
		else:
			Message("No layers with missing automatic alignment found.", "All good!", OKButton="Nice.")


ReportMissingAutomaticAlignment()
