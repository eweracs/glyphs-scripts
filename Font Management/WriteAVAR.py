# MenuTitle: Write AVAR table
# -*- coding: utf-8 -*-

__doc__ = """
Writes an AVAR table based on current weight distribution.
"""

from GlyphsApp import Glyphs, Message

Font = Glyphs.font

if Font is None:
	Message("No font selected.", "Select a font project!")

if str(Glyphs.versionNumber)[0] == "2":
	instanceweights = sorted({instance.weightValue for instance in Font.instances})
	instancewidths = sorted({instance.widthValue for instance in Font.instances})
else:
	for i, a in enumerate(Font.axes):
		if a.axisTag == "wght":
			weightindex = i
	instanceweights = sorted({instance.axes[weightindex] for instance in Font.instances if instance.type == 0})
	for j, a in enumerate(Font.axes):
		if a.axisTag == "wdth":
			widthindex = j
	instancewidths = sorted({instance.axes[widthindex] for instance in Font.instances if instance.type == 0})

axisMinimum = instanceweights[0]  # lightest stem weight
axisRange = instanceweights[-1] - axisMinimum  # axis range

# calculate and write AVAR table to custom parameters
Font.customParameters["Axis Mappings"] = {
	"wght": {
		int(axisRange / (len(instanceweights) - 1) * instance + axisMinimum):
		instanceweights[instance] for instance in range(len(instanceweights))
	},
	"wdth": {
		int(axisRange / (len(instancewidths) - 1) * instance + axisMinimum):
		instancewidths[instance] for instance in range(len(instancewidths))
	}
}

Glyphs.showNotification(
	title="Wrote AVAR table",
	message="Table calculated for " + str(len(instanceweights)) + " instances"
)
