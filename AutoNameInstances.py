#MenuTitle: Auto-name instances
# -*- coding: utf-8 -*-
__doc__="""
Names pre-defined instances based on weight and width values
"""

for i in Glyphs.font.instances:
	if i.active:
		if i"Medium" in i.width:
			i.name = i.weight
		else:
			if i.weight == "Regular" or i.weight == "Normal":
				i.name = i.width
			else:
				if i.width == "Ultra Condensed":
					i.name = i.weight + " Compressed"
				else:
					i.name = i.weight + " " + i.width