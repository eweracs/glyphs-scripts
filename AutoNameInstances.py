#MenuTitle: Auto-name instances
# -*- coding: utf-8 -*-
__doc__="""
Names pre-defined instances based on set weight and width names
"""

for i in Glyphs.font.instances:
	if i.active:
		if "Medium" in i.width:
			i.name = i.weight
		else:
			if i.weight == "Regular" or i.weight == "Normal":
				i.name = i.width
			else:
				if i.width == "Ultra Condensed":
					i.name = i.weight + " Compressed"
				else:
					i.name = i.weight + " " + i.width
