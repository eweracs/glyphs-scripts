# MenuTitle: Copy Shapes From First Half of Masters
# -*- coding: utf-8 -*-

__doc__ = """
Copies shapes from the first half of the masters to the second half. Includes special layers.
"""

from GlyphsApp import Glyphs, Message


class CopyShapesFromFirstHalf:
	def __init__(self):
		self.font = Glyphs.font

		# check that the font has an even amount of masters
		if len(self.font.masters) % 2 != 0:
			Message("An even amount of masters is required to copy between two halves.", "Uneven amount of masters")
			return

		for glyph in self.font.selectedLayers:
			# make a list of all master layers, not special layers
			master_layers = [layer for layer in glyph.parent.layers if layer.isMasterLayer]

			# make a list of all special layers
			special_layers = [layer for layer in glyph.parent.layers if layer.isSpecialLayer]

			# check that the glyph has exactly one special layer per master
			copy_special_layers = len(special_layers) > 0

			for i, layer in enumerate(special_layers):
				if layer.associatedMasterId != master_layers[i].associatedMasterId:
					print(
						"%s: Special layers not copied. An amount of exactly one special layer per master is "
						"required." %
						glyph.parent.name
					)
					copy_special_layers = False
					break

			for i in range(int(len(master_layers) / 2)):
				# copy the shapes from the first half of the masters to the second half
				master_layers[i + int(len(master_layers) / 2)].shapes = master_layers[i].shapes.copy()
				if copy_special_layers:
					special_layers[i + int(len(master_layers) / 2)].shapes = special_layers[i].shapes.copy()


CopyShapesFromFirstHalf()
