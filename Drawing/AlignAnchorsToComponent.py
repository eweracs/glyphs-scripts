# MenuTitle: Align Anchors to Component
# -*- coding: utf-8 -*-

__doc__ = """
Horizontally aligns all selected anchors to the horizontal center of the selected components.
"""

from Foundation import NSPoint
from math import tan, radians
from GlyphsApp import Glyphs, Message


def calculate_italic_shift(coordinates, italic_angle, center):
	return NSPoint(coordinates[0] + int(tan(radians(italic_angle)) * (coordinates[1] - center)), coordinates[1])


def calculate_components_center(components):
	bounds = [[], []]
	for component in components:
		bounds[0].append(component.bounds.origin.x)
		bounds[1].append(component.bounds.origin.x + component.bounds.size.width)

	for i in range(2):
		bounds[i] = sum(bounds[i]) / len(bounds[i])

	return sum(bounds) / 2


def AlignAnchors():
	font = Glyphs.font

	if not font:
		Message(title="No font selected", message="Select a font project!")
		return

	for layer in font.selectedLayers:
		for anchor in layer.anchors:
			if not anchor.selected:
				continue
			position = anchor.position
			shift_center = layer.bounds.size.height / 2
			component_center = calculate_components_center([component for component in layer.components if component.selected])
			anchor.position = calculate_italic_shift([component_center, position.y], layer.italicAngle, shift_center)


AlignAnchors()
