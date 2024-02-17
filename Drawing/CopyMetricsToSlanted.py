# MenuTitle: Copy Metrics to Slanted Masters
# -*- coding: utf-8 -*-

__doc__ = """
Copies the metrics from the roman masters to the slanted masters for the selected glyphs.
"""

from GlyphsApp import Glyphs, Message


class SyncMetricsForSlanted:
	def __init__(self):
		self.font = Glyphs.font

		if self.font is None:
			Message("Select a font project!", "No font selected")
			return

		# find slanted masters and their roman counterparts

		# find the one axis that is called italic or slant
		for axis in self.font.axes:
			if axis.name.lower() in ["italic", "slant"]:
				self.slantedMasterAxisIndex = self.font.axes.index(axis)
				break

		self.slantedMasters = []
		self.romanMasters = []
		for master in self.font.masters:
			for metric in master.metrics():
				if metric.name == "Italic Angle":
					if metric.position != 0:
						self.slantedMasters.append(master)
					else:
						self.romanMasters.append(master)

		self.romanToSlanted = {romanMaster.id: [] for romanMaster in self.romanMasters}

		# for every roman master, find the slanted master where all axis values except for italic or slant are the same
		for romanMaster in self.romanMasters:
			for slantedMaster in self.slantedMasters:
				match_count = 0
				for i, axis in enumerate(self.font.axes):
					if axis.name == "Italic" or axis.name == "Slant":
						continue
					if slantedMaster.axes[i] == romanMaster.axes[i]:
						match_count += 1
				if match_count == len([axis for axis in self.font.axes if axis.name != "Italic" and axis.name != "Slant"]):
					self.romanToSlanted[romanMaster.id].append(slantedMaster.id)

		# for all selected glyphs, copy the metrics from the roman masters to the slanted masters
		for selected in self.font.selectedLayers:
			for romanMaster in self.romanMasters:
				# find all special layers in the glyph that are linked to the roman masters
				roman_special_layers = [layer for layer in selected.parent.layers if layer.associatedMasterId == romanMaster.id]

				# find all special layers in the glyph that are linked to the slanted masters
				slanted_special_layers = [layer for layer in selected.parent.layers if layer.associatedMasterId in self.romanToSlanted[romanMaster.id]]

				# find the slanted special layers that have the same attributes as the roman special layers
				for roman_special_layer in roman_special_layers:
					for slanted_special_layer in slanted_special_layers:
						match_count = 0
						if "axisRules" in roman_special_layer.attributes:
							for axis in roman_special_layer.attributes["axisRules"]:
								if axis[-1] == str(self.slantedMasterAxisIndex):
									continue
								if roman_special_layer.attributes["axisRules"][axis] != slanted_special_layer.attributes["axisRules"][axis]:
									break

				for slantedCounterpart in self.romanToSlanted[romanMaster.id]:
					selected.parent.layers[slantedCounterpart].LSB = selected.parent.layers[romanMaster.id].LSB
					selected.parent.layers[slantedCounterpart].RSB = selected.parent.layers[romanMaster.id].RSB


SyncMetricsForSlanted()
