# MenuTitle: Set Fraction Autopairs
# -*- coding: utf-8 -*-

__doc__ = """
Sets .numr–fraction and fraction–.dnom autopairs for Kern On.
"""

from GlyphsApp import Glyphs, Message

fraction_models = [
	"one.numr fraction",
	"two.numr fraction",
	"three.numr fraction",
	"four.numr fraction",
	"five.numr fraction",
	"six.numr fraction",
	"seven.numr fraction",
	"eight.numr fraction",
	"nine.numr fraction",
	"zero.numr fraction",
	"fraction one.dnom",
	"fraction two.dnom",
	"fraction three.dnom",
	"fraction four.dnom",
	"fraction five.dnom",
	"fraction six.dnom",
	"fraction seven.dnom",
	"fraction eight.dnom",
	"fraction nine.dnom",
	"fraction zero.dnom"
]

Font = Glyphs.font

required_glyphs = []
for glyph in fraction_models:
	number = glyph.replace("fraction", "").replace(" ", "")
	if number not in Font.glyphs:
		required_glyphs.append(number)
if "fraction" not in Font.glyphs:
	required_glyphs.append("fraction")
if len(required_glyphs) > 0:
	Message("Please add: " + ", ".join(required_glyphs), "Project missing required glyphs")
	exit()

for master in Font.masters:

	if master.userData["KernOnModels"]:
		auto_fraction_models = tuple(model for model in fraction_models if model not in master.userData["KernOnModels"])
	else:
		auto_fraction_models = fraction_models

	if master.userData["KernOnUserSetAutopairs"]:
		master.userData["KernOnUserSetAutopairs"] = master.userData["KernOnUserSetAutopairs"] + auto_fraction_models
	else:
		master.userData["KernOnUserSetAutopairs"] = auto_fraction_models

Glyphs.showNotification(title="Fraction autopairs set", message="Restart Kern On for changes to take effect.")
