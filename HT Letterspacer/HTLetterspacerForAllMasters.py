# MenuTitle: HT Letterspacer for All Masters
# -*- coding: utf-8 -*-

__doc__ = """
Runs HT Letterspacer for the current selection in all masters.
"""

import_success = False
try:
	from HTLSLibrary import *
	import_success = True
except:
	Message("Please install HTLS Manager from the plugin manager and restart Glyphs.", "HTLS Manager required")


class HTLSAllMasters:
	def __init__(self):
		self.font = Font

		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		for glyph in self.font.selectedLayers:
			parent = glyph.parent
			for layer in parent.layers:
				if not layer.isMasterLayer:
					continue
				self.engine = HTLSEngine(layer)

				layer_lsb, layer_rsb = self.engine.current_layer_sidebearings() or [None, None]
				if (not layer_lsb or not layer_rsb) and (layer_lsb != 0 or layer_rsb != 0):
					continue
				layer.LSB, layer.RSB = layer_lsb, layer_rsb

				print(self.engine.output)


if import_success:
	HTLSAllMasters()
