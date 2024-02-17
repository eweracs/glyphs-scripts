# MenuTitle: Find Mirrored Components
# -*- coding: utf-8 -*-

__doc__ = """
Prints a tab with all layers with mirrored components.
"""

# go through all glyphs and their layers, excluding backup layers and layers with no components
# print a tab with all layers with mirrored components

from GlyphsApp import Glyphs, Message


class FindMirroredComponents:
	def __init__(self):
		self.font = Glyphs.font

		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		mirrored_component_layers = []

		for glyph in self.font.glyphs:
			for layer in glyph.layers:
				if not layer.components or not layer.isMasterLayer:
					continue

				# check for mirrored components
				for component in layer.components:
					if component.transform[0] == -1 and component.transform[3] != -1:
						mirrored_component_layers.append(layer)
						break
					elif component.transform[0] != -1 and component.transform[3] == -1:
						mirrored_component_layers.append(layer)
						break

		if len(mirrored_component_layers) > 0:
			self.font.newTab(mirrored_component_layers)
		else:
			Message("No layers with mirrored components found.", "All good!", OKButton="Nice.")


FindMirroredComponents()
