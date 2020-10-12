#MenuTitle: Interpolate Kerning
# -*- coding: utf-8 -*-

import vanilla

__doc__="""
Interpolates custom kern feature for instances
"""

font = Glyphs.font

# the amount of kerning to be applied per master
M1 = 30
M2 = 20

# pos class1 [value] class2;
class1 = "@Uppercase"
class2 = "@Uppercase"

minWeight = font.masters[0].weightValue
weightRange = font.masters[-1].weightValue - minWeight

for instance in font.instances:

	kern = float((M2 - M1) / weightRange * (instance.weightValue - minWeight)) + M1

	if instance.customParameters:

		kernText = """{}
pos {} {} {};""".format(instance.customParameters["Replace Feature"], class1, str(int(kern)), class2)

	else:
		kernText = """kern;
pos {} {} {};""".format(class1, str(int(kern)), class2)

	instance.customParameters["Replace Feature"] = kernText
