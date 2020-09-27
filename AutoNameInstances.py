#MenuTitle: Auto-name instances
# -*- coding: utf-8 -*-
__doc__="""
Names pre-defined instances based on weight and width values
"""

for i in Font.instances:
	if i.active:
		if "Medium" in i.width:
			i.name = i.weight
		else:
			if "Regular" in i.weight:
				i.name = i.width
			else:
				if "Ultra" in i.width:
					i.name = i.weight + " Compressed"
				else:
					i.name = i.weight + ' ' + i.width