# MenuTitle: Interpolation Preview
# -*- coding: utf-8 -*-

__doc__ = """
Allows to visually interpolate instances or intermediate layers.
"""

import vanilla


class Interpolator:
	def __init__(self):

		self.font = Font

		self.w = vanilla.FloatingWindow((0, 0), "Interpolation Preview")

		self.axesRanges = []  # create a list to contain tuples with the min and max of an axis
		self.currentCoords = []
		self.sliderList = []  # create a list of the slider objects

		self.initialLayers = []

		for self.thisLayer in self.font.selectedLayers:
			self.initialLayers.append(self.thisLayer)

		for glyph in self.initialLayers:
			self.copyLayer = glyph.copy()
			self.copyLayer.name = "Preview {" + ", ".join([str(axis) for axis in self.currentCoords]) + "}"
			self.font.glyphs[glyph.parent.name].layers.append(self.copyLayer)

		for coord in self.font.selectedFontMaster.axes:
			self.currentCoords.append(int(coord))
		for i, axis in enumerate(self.font.axes):  # for each axis in the font, create a new slider
			self.axesRanges.append(set())  # for each axis in the font, create an empty tuple to store the axis range
			for master in self.font.masters:  # first, build a list of the axis ranges
				self.axesRanges[i].add(master.axes[i])
			setattr(self.w, axis["Tag"] + "title", vanilla.TextBox((10, 20 + i * 30, -10, 14),
			                                                       axis["Name"], sizeStyle="small"))
			s = vanilla.Slider((60, 20 + i * 30, -10, 15),
			                   minValue=sorted(self.axesRanges[i])[0],
			                   maxValue=sorted(self.axesRanges[i])[1],
			                   value=self.currentCoords[i],
			                   callback=self.axis_selector)
			setattr(self.w, axis["Tag"] + "slider", s)
			self.sliderList.append(s)

		self.w.resize(300, s.getPosSize()[1] + 30)

		self.w.open()
		self.w.makeKey()

	def axis_selector(self, sender):
		for i, item in enumerate(self.sliderList):
			if item is sender:
				self.currentCoords[i] = int(sender.get())
		self.interpolate_glyph()

	def interpolate_glyph(self):
		for i, glyph in Font.selectedLayers:
			self.font.glyphs[glyph.parent.name].layers[-1].name = "Preview {200}"
			print(", ".join([str(axis) for axis in self.currentCoords]))
			self.font.glyphs[glyph.parent.name].layers[-1].reinterpolate()
			# self.font.selectedLayers[i].paths = self.copyLayer.paths
			# self.font.selectedLayers[i].components = self.copyLayer.components
			# self.font.selectedLayers[i].width = self.copyLayer.width
			# self.font.selectedLayers[i].hints = self.copyLayer.hints


Interpolator()
