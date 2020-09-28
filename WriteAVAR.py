#MenuTitle: Write AVAR table
# -*- coding: utf-8 -*-
import vanilla

__doc__="""
Writes an AVAR table based on current weight distribution
"""

font = Glyphs.font

# create a list which indexes all instances by weight
instancelist = sorted({font.instances[i].weightValue for i in range(len(font.instances))})

axisMinimum = instancelist[0] # lightest stem weight
axisRange = instancelist[-1] - axisMinimum # axis range 

# calculate and write AVAR table to custom parameters
font.customParameters["Axis Mappings"] = {"wght": {int(axisRange/(len(instancelist)-1)*l+axisMinimum):instancelist[l] for l in range(len(instancelist))}}
