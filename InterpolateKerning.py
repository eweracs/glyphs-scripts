#MenuTitle: Interpolate Kerning
# -*- coding: utf-8 -*-

import vanilla
import re

__doc__="""
Interpolates custom kern feature for instances
"""

font = Glyphs.font

minWeightminWidthKern = 24
maxWeightminWidthKern = 16
minWeightmaxWidthKern = 35
maxWeightmaxWidthKern = 26

minWeight = font.masters[0].weightValue
maxWeight = font.masters[-1].weightValue
minWidth = font.masters[0].widthValue
maxWidth = font.masters[-1].widthValue

weightRange = maxWeight - minWeight
widthRange = maxWidth - minWidth

for instance in font.instances:

	kern = float((maxWeightmaxWidthKern - maxWeightminWidthKern) / widthRange * (instance.widthValue - minWidth) + (minWeightminWidthKern - maxWeightminWidthKern) / weightRange * (instance.weightValue - minWeight)) + maxWeightminWidthKern
	instance.customParameters["Replace Feature"] = """kern;
pos @Uppercase """ + str(int(kern)) + " @Smallcaps;"