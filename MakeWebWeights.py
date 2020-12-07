# MenuTitle: Make Web Weights
# -*- coding: utf-8 -*-

import re

__doc__ = """
Prepares a file for web use, assigning USWeightClass values.
"""

cssdict = {
	"Thin": 100,
	"Hair": 100,
	"ExtraLight": 200,
	"UltraLight": 200,
	"Light": 300,
	"Regular": 400,
	"Normal": 400,
	"Medium": 500,
	"SemiBold": 600,
	"DemiBold": 600,
	"Bold": 700,
	"ExtraBold": 800,
	"UltraBold": 800,
	"Black": 900,
	"Heavy": 900,
}

font = Font

# create a list which indexes all masters by weight
weightlist = sorted({master.axes[0] for master in font.masters})

axisMinimum = weightlist[0]  # lightest stem weight
axisRange = weightlist[-1] - axisMinimum  # axis range

# set USWeightClass values for masters based on naming
for master in font.masters:
	if "Thin" in master.name or "Hair" in master.name:
		master.weightValue = 100
	if "Light" in master.name:
		master.axes[0] = 300
	if "ExtraLight" in master.name or "UltraLight" in master.name:
		master.axes[0] = 200
	if "Regular" in master.name or "Normal" in master.name:
		master.axes[0] = 400
	if "Medium" in master.name:
		master.axes[0] = 500
	if "Bold" in master.name:
		master.axes[0] = 700
	if "SemiBold" in master.name or "DemiBold" in master.name:
		master.axes[0] = 600
	if "ExtraBold" in master.name or "UltraBold" in master.name:
		master.axes[0] = 800
	if "Black" in master.name or "Heavy" in master.name:
		master.axes[0] = 900

cssweightlist = sorted({master.axes[0] for master in font.masters})

cssMinimum = cssweightlist[0]  # lightest USWeightClass value
cssRange = cssweightlist[-1] - cssMinimum  # USWeightClass range


# input_weight is old stem weight
def convert_weight(input_weight):
	output_weight = (input_weight - axisMinimum)/axisRange*cssRange + cssMinimum
	return int(output_weight)  # calculate reference USWeightClass weight for old stem weight


# recalculate values in intermediate layers
for glyph in font.glyphs:
	for layer in glyph.layers:
		if layer.isSpecialLayer:
			# rename the layer by converting the old number to new weight assignment
			# convert the layer name by reading only the digits from the layer
			layer.name = re.sub(r'\d+', str(convert_weight(int("".join([char for char in layer.name if char.isdigit()])))), layer.name)

# calculate AVAR table and write to custom parameters
print(int(cssRange/100 + 1))
font.customParameters["Axis Mappings"] = {
	"wght": {cssdict[i.weight]: convert_weight(sorted({instance.axes[0] for instance in font.instances})[index]) for
	         index, i in enumerate(font.instances)}}

# set USWeightClass values for instances based on weight assignment
for instance in font.instances:
	instance.axes[0] = cssdict[instance.weight]

Glyphs.showNotification(title="Converted to web weights",
                        message="AVAR table calculated for " + str(len(font.instances)) + " instances")
