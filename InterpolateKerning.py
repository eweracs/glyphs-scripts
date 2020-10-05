#MenuTitle: Interpolate Kerning
# -*- coding: utf-8 -*-

import vanilla

__doc__="""
Interpolates custom kern feature for instances
"""

font = Glyphs.font

M1 = 30
M2 = 20

class1 = "@Uppercase"
class2 = "@Uppercase"

minWeight = font.masters[0].weightValue
maxWeight = font.masters[-1].weightValue

weightRange = maxWeight - minWeight

for instance in font.instances:

	kern = float((M2 - M1) / weightRange * (instance.weightValue - minWeight)) + M1

	if instance.customParameters:

		kernText = """{}
pos {} {} {};""".format(instance.customParameters["Replace Feature"], class1, str(int(kern)), class2)

	else:
		kernText = """kern;
pos {} {} {};""".format(class1, str(int(kern)), class2)

	instance.customParameters["Replace Feature"] = kernText