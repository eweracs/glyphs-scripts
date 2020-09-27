#MenuTitle: Make Web Variable
# -*- coding: utf-8 -*-
import vanilla
import re

__doc__="""
Prepares a file for web use, calculating an AVAR table and assigning USWeightClass values.
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

font = Glyphs.font

axisMinimum = font.masters[0].weightValue # lightest master stem weight
axisRange = font.masters[-1].weightValue - axisMinimum # boldest master stem weight

# set USWeightClass values for masters based on naming
for master in font.masters:
	if "Thin" in master.name or "Hair" in master.name:
		master.weightValue = 100
	if "Light" in master.name:
		master.weightValue = 300
	if "ExtraLight" in master.name or "UltraLight" in master.name:
		master.weightValue = 200
	if "Regular" in master.name or "Normal" in master.name:
		master.weightValue = 400
	if "Medium" in master.name:
		master.weightValue = 500
	if "Bold" in master.name:
		master.weightValue = 700
	if "SemiBold" in master.name or "DemiBold" in master.name:
		master.weightValue = 600
	if "ExtraBold" in master.name or "UltraBold" in master.name:
		master.weightValue = 800
	if "Black" in master.name or "Heavy" in master.name:
		master.weightValue = 900

cssMinimum = font.masters[0].weightValue # get lightest USWeightClass value
cssMaximum = font.masters[-1].weightValue # get boldest USWeightClass value
cssRange = cssMaximum - cssMinimum

# inputWeight is old stem weight
def convertWeight(inputWeight):
	outputWeight = ((inputWeight - axisMinimum)/axisRange)*cssRange + cssMinimum
	return int(round(outputWeight, 0)) # calculate reference USWeightClass weight for old stem weight

# read only number from a string
def int_from_string(string):
	chars = [char for char in string]		
	digits = []		
	for char in chars:
		if char.isdigit():
			digits.append(char)		
	number="".join(digits)
	return int(number)

# check whether layer is intermediate layer (has numbers)
def hasNumbers(layerName):
	return any(char.isdigit() for char in layerName)

# recalculate values in intermediate layers
for glyph in font.glyphs:
	for layer in glyph.layers:
		if hasNumbers(layer.name):
			newWeight = str(convertWeight(int_from_string(layer.name)))
			layer.name = re.sub(r'\d+', newWeight,layer.name)

# calculate AVAR table and write to custom parameters
font.customParameters["Axis Mappings"] = {"wght" : {l*100+cssMinimum:convertWeight(sorted({font.instances[i].weightValue for i in range(len(font.instances))})[l]) for l in range(int(cssRange/100+1))}}

# set USWeightClass values for instances based on weight assignment
for instance in font.instances:
	instance.weightValue = cssdict[instance.weight]

# Rename font family
if "Variable" not in font.familyName:
	font.familyName = font.familyName + " Variable"