# MenuTitle: Automatically Align in All Masters
# -*- coding: utf-8 -*-

__doc__ = """
Automatically aligns all components in all masters in the selected glyphs.
"""


class AutomaticallyAlignAllMasters:
	def __init__(self):
		self.font = Font

		if self.font is None:
			Message("No font selected", "Select a font project!")
			return
		
		for selected in self.font.selectedLayers:
			glyph = selected.parent
			for layer in glyph.layers:
				for component in layer.components:
					component.automaticAlignment = True


AutomaticallyAlignAllMasters()
