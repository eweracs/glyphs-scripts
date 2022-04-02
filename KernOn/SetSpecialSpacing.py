# MenuTitle: Set special spacing groups
# -*- coding: utf-8 -*-

__doc__ = """
Sets special spacing groups for Kern On.
"""

found_special_spacing = True
for glyph in Font.glyphs:
	if not glyph.userData["KernOnSpecialSpacing"]:
		continue
	found_special_spacing = False
	break

if found_special_spacing:
	Message("Please run Kern On once to build basic special spacing, as it will otherwise not be written.",
	        "No existing special spacing found")
else:
	defaults = {
		# No kerning on both sides
		"periodcentered.loclCAT": {"L": "NoKerning", "R": "NoKerning"},
		"periodcentered.loclCAT.case": {"L": "NoKerning", "R": "NoKerning"},
		"paragraph": {"L": "NoKerning", "R": "NoKerning"},
		"section": {"L": "NoKerning", "R": "NoKerning"},
		"copyright": {"L": "NoKerning", "R": "NoKerning"},
		"registered": {"L": "NoKerning", "R": "NoKerning"},
		"published": {"L": "NoKerning", "R": "NoKerning"},
		"trademark": {"L": "NoKerning", "R": "NoKerning"},
		"degree": {"L": "NoKerning", "R": "NoKerning"},
		"bar": {"L": "NoKerning", "R": "NoKerning"},
		"brokenbar": {"L": "NoKerning", "R": "NoKerning"},
		"dagger": {"L": "NoKerning", "R": "NoKerning"},
		"daggerdbl": {"L": "NoKerning", "R": "NoKerning"},
		"estimated": {"L": "NoKerning", "R": "NoKerning"},
		"numero": {"L": "NoKerning", "R": "NoKerning"},
		"servicemark": {"L": "NoKerning", "R": "NoKerning"},
		"florin": {"L": "NoKerning", "R": "NoKerning"},
		"euro": {"L": "NoKerning", "R": "NoKerning"},
		"lira": {"L": "NoKerning", "R": "NoKerning"},
		"bitcoin": {"L": "NoKerning", "R": "NoKerning"},
		"cent": {"L": "NoKerning", "R": "NoKerning"},
		"currency": {"L": "NoKerning", "R": "NoKerning"},
		"dollar": {"L": "NoKerning", "R": "NoKerning"},
		"sterling": {"L": "NoKerning", "R": "NoKerning"},
		"yen": {"L": "NoKerning", "R": "NoKerning"},
		"logicalnot": {"L": "NoKerning", "R": "NoKerning"},
		"asciicircum": {"L": "NoKerning", "R": "NoKerning"},
		"infinity": {"L": "NoKerning", "R": "NoKerning"},
		"emptyset": {"L": "NoKerning", "R": "NoKerning"},
		"integral": {"L": "NoKerning", "R": "NoKerning"},
		"increment": {"L": "NoKerning", "R": "NoKerning"},
		"product": {"L": "NoKerning", "R": "NoKerning"},
		"summation": {"L": "NoKerning", "R": "NoKerning"},
		"radical": {"L": "NoKerning", "R": "NoKerning"},
		"mu": {"L": "NoKerning", "R": "NoKerning"},
		"partialdiff": {"L": "NoKerning", "R": "NoKerning"},
		"upArrow": {"L": "NoKerning", "R": "NoKerning"},
		"northEastArrow": {"L": "NoKerning", "R": "NoKerning"},
		"rightArrow": {"L": "NoKerning", "R": "NoKerning"},
		"southEastArrow": {"L": "NoKerning", "R": "NoKerning"},
		"downArrow": {"L": "NoKerning", "R": "NoKerning"},
		"southWestArrow": {"L": "NoKerning", "R": "NoKerning"},
		"leftArrow": {"L": "NoKerning", "R": "NoKerning"},
		"northWestArrow": {"L": "NoKerning", "R": "NoKerning"},
		"leftRightArrow": {"L": "NoKerning", "R": "NoKerning"},
		"upDownArrow": {"L": "NoKerning", "R": "NoKerning"},

		# No kerning, left only
		"Jacute": {"L": "NoKerning"},
		"jacute": {"L": "NoKerning"},
		"jacute.sc": {"L": "NoKerning"},

		# No kerning, right only
		"Ldot": {"R": "NoKerning"},
		"ldot": {"R": "NoKerning"},
		"ldot.sc": {"R": "NoKerning"},

		# Special Spacing
		"zero.dnom": {"L": "small nums", "R": "small nums"},
		"one.dnom": {"L": "small nums", "R": "small nums"},
		"two.dnom": {"L": "small nums", "R": "small nums"},
		"three.dnom": {"L": "small nums", "R": "small nums"},
		"four.dnom": {"L": "small nums", "R": "small nums"},
		"five.dnom": {"L": "small nums", "R": "small nums"},
		"six.dnom": {"L": "small nums", "R": "small nums"},
		"seven.dnom": {"L": "small nums", "R": "small nums"},
		"eight.dnom": {"L": "small nums", "R": "small nums"},
		"nine.dnom": {"L": "small nums", "R": "small nums"},
		"zero.subs": {"L": "small nums", "R": "small nums"},
		"one.subs": {"L": "small nums", "R": "small nums"},
		"two.subs": {"L": "small nums", "R": "small nums"},
		"three.subs": {"L": "small nums", "R": "small nums"},
		"four.subs": {"L": "small nums", "R": "small nums"},
		"five.subs": {"L": "small nums", "R": "small nums"},
		"six.subs": {"L": "small nums", "R": "small nums"},
		"seven.subs": {"L": "small nums", "R": "small nums"},
		"eight.subs": {"L": "small nums", "R": "small nums"},
		"nine.subs": {"L": "small nums", "R": "small nums"},
		"zeroinferior": {"L": "small nums", "R": "small nums"},
		"oneinferior": {"L": "small nums", "R": "small nums"},
		"twoinferior": {"L": "small nums", "R": "small nums"},
		"threeinferior": {"L": "small nums", "R": "small nums"},
		"fourinferior": {"L": "small nums", "R": "small nums"},
		"fiveinferior": {"L": "small nums", "R": "small nums"},
		"sixinferior": {"L": "small nums", "R": "small nums"},
		"seveninferior": {"L": "small nums", "R": "small nums"},
		"eightinferior": {"L": "small nums", "R": "small nums"},
		"nineinferior": {"L": "small nums", "R": "small nums"},
		"zero.numr": {"L": "small nums", "R": "small nums"},
		"one.numr": {"L": "small nums", "R": "small nums"},
		"two.numr": {"L": "small nums", "R": "small nums"},
		"three.numr": {"L": "small nums", "R": "small nums"},
		"four.numr": {"L": "small nums", "R": "small nums"},
		"five.numr": {"L": "small nums", "R": "small nums"},
		"six.numr": {"L": "small nums", "R": "small nums"},
		"seven.numr": {"L": "small nums", "R": "small nums"},
		"eight.numr": {"L": "small nums", "R": "small nums"},
		"nine.numr": {"L": "small nums", "R": "small nums"},
		"zero.sups": {"L": "small nums", "R": "small nums"},
		"one.sups": {"L": "small nums", "R": "small nums"},
		"two.sups": {"L": "small nums", "R": "small nums"},
		"three.sups": {"L": "small nums", "R": "small nums"},
		"four.sups": {"L": "small nums", "R": "small nums"},
		"five.sups": {"L": "small nums", "R": "small nums"},
		"six.sups": {"L": "small nums", "R": "small nums"},
		"seven.sups": {"L": "small nums", "R": "small nums"},
		"eight.sups": {"L": "small nums", "R": "small nums"},
		"nine.sups": {"L": "small nums", "R": "small nums"}
		"zerosuperior": {"L": "small nums", "R": "small nums"},
		"onesuperior": {"L": "small nums", "R": "small nums"},
		"twosuperior": {"L": "small nums", "R": "small nums"},
		"threesuperior": {"L": "small nums", "R": "small nums"},
		"foursuperior": {"L": "small nums", "R": "small nums"},
		"fivesuperior": {"L": "small nums", "R": "small nums"},
		"sixsuperior": {"L": "small nums", "R": "small nums"},
		"sevensuperior": {"L": "small nums", "R": "small nums"},
		"eightsuperior": {"L": "small nums", "R": "small nums"},
		"ninesuperior": {"L": "small nums", "R": "small nums"}
	}

	print("Setting special spacing groups for:\n")

	set_glyphs = []
	for exception in defaults:
		if exception in Font.glyphs:
			Font.glyphs[exception].userData["KernOnSpecialSpacing"] = defaults[exception]
			set_glyphs.append(exception)
			print(exception, "–", ", ".join([side + ": " + defaults[exception][side] for side in defaults[exception]]))

	print("\n...Done.")

	Glyphs.showNotification(title="Set special spacing groups",
	                        message="Special spacing groups set for "
	                                + str(len(set_glyphs)) + " glyphs. Detailed report in Macro window.")
