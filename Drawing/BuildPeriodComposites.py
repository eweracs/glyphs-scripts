# MenuTitle: Build Period Composites
# -*- coding: utf-8 -*-

__doc__ = """
Builds colon, semicolon and ellipsis from glyphs period and comma.
"""

from vanilla import *
from Foundation import NSPoint
from math import *


class BuildPeriodComposites:
	def __init__(self):
		self.font = Font

		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		self.w = FloatingWindow((1, 1), "Period Composites")

		self.w.descriptionText = TextBox("auto", "Build:", sizeStyle="small")

		self.w.colon = CheckBox("auto", "Colon", sizeStyle="small")
		self.w.semicolon = CheckBox("auto", "Semicolon", sizeStyle="small")
		self.w.ellipsis = CheckBox("auto", "Ellipsis", sizeStyle="small")
		self.w.divider = HorizontalLine("auto")
		self.w.makeBackup = CheckBox("auto", "Back up old shapes in background", sizeStyle="small")
		self.w.build = Button("auto", "Build", callback=self.build_glyphs)

		self.w.setDefaultButton(self.w.build)

		rules = [
			"H:|-margin-[descriptionText]-margin-|",
			"H:|-margin-[colon]-margin-|",
			"H:|-margin-[semicolon]-margin-|",
			"H:|-margin-[ellipsis]-margin-|",
			"H:|-margin-[divider]-margin-|",
			"H:|-margin-[makeBackup]-margin-|",
			"H:|-margin-[build]-margin-|",
			"V:|-margin-[descriptionText]-margin-[colon]-margin-[semicolon]-margin-[ellipsis]-margin-[divider]-margin-"
			"[makeBackup]-margin-[build]-margin-|",
		]

		metrics = {
			"margin": 10
		}

		self.read_preferences()

		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.open()
		self.w.makeKey()

	def build_glyphs(self, sender):
		glyphs_to_build = {}
		required_glyphs = set()
		required_anchors = {"period": set(), "comma": set()}

		# colon requires period, semicolon requires comma and period, ellipsis requires period. Add required to list
		# if not already present
		if self.w.colon.get():
			glyphs_to_build["colon"] = ["period", "period"]
			required_glyphs.add("period")
			required_anchors["period"].add("colon_exit")
			required_anchors["period"].add("colon_entry")
		if self.w.semicolon.get():
			glyphs_to_build["semicolon"] = ["comma", "period"]
			required_glyphs.add("comma")
			required_glyphs.add("period")
			required_anchors["period"].add("colon_exit")
			required_anchors["period"].add("colon_entry")
			required_anchors["comma"].add("colon_exit")
		if self.w.ellipsis.get():
			glyphs_to_build["ellipsis"] = ["period", "period", "period"]
			required_glyphs.add("period")
			required_anchors["period"].add("_ellipsis")
			required_anchors["period"].add("ellipsis")

		missing = [glyph for glyph in required_glyphs if glyph not in self.font.glyphs]

		if len(missing) > 0:
			Message("Missing glyphs: " + ", ".join(missing), "Missing glyphs")
			return

		for glyph in required_glyphs:
			working_glyph = self.font.glyphs[glyph]
			period = self.font.glyphs["period"]
			print("Setting anchors in %s..." % working_glyph.name)

			# set anchors: use dict to find coordinates, then use calculate_italic_shift to shift coordinates for italic
			for layer in working_glyph.layers:
				period_layer = period.layers[layer.associatedMasterId]
				coordinates = {"colon_entry": (layer.bounds.origin.x + layer.bounds.size.width / 2,
				                          layer.bounds.origin.y + layer.bounds.size.height),
				               "colon_exit": (layer.bounds.origin.x + layer.bounds.size.width / 2,
				                         period_layer.master.xHeight - period_layer.bounds.origin.y),
				               "_ellipsis": (0, 0),
				               "ellipsis": (layer.bounds.origin.x + layer.bounds.size.width, 0)}

				for anchor in required_anchors[glyph]:
					center = layer.bounds.size.height / 2
					if anchor == "_ellipsis":
						center = layer.master.xHeight / 2
					layer.anchors[anchor] = GSAnchor(name=anchor,
					                                 pt=self.calculate_italic_shift(coordinates[anchor],
					                                                                layer.master.italicAngle,
					                                                                center)
					                                 )

		for glyph in glyphs_to_build.keys():

			# make sure glyph exists
			if glyph not in self.font.glyphs:
				self.font.glyphs.append(GSGlyph(glyph))

			working_glyph = self.font.glyphs[glyph]

			print("Building %s..." % working_glyph.name)

			for layer in working_glyph.layers:
				if self.w.makeBackup.get():
					layer.background = layer.copyDecomposedLayer()
				layer.clear()
				for component in glyphs_to_build[glyph]:
					new_component = GSComponent(component)

					if glyph.endswith("colon"):
						new_component.anchor = "colon_exit"
					if glyph == "ellipsis":
						new_component.anchor = "ellipsis"
					layer.components.append(new_component)

		print("\n...Done!")

		self.font.newTab("/" + "/".join([glyph for glyph in required_glyphs] + [key for key in glyphs_to_build.keys()]))

		self.write_preferences()

	def calculate_italic_shift(self, coordinates, italic_angle, center):
		return NSPoint(coordinates[0] + int(tan(radians(italic_angle)) * (coordinates[1] - center)),
		               coordinates[1])

	def write_preferences(self):
		Glyphs.defaults["com.eweracs.buildPeriodComposites.colon"] = self.w.colon.get()
		Glyphs.defaults["com.eweracs.buildPeriodComposites.semicolon"] = self.w.semicolon.get()
		Glyphs.defaults["com.eweracs.buildPeriodComposites.ellipsis"] = self.w.ellipsis.get()
		Glyphs.defaults["com.eweracs.buildPeriodComposites.makeBackup"] = self.w.makeBackup.get()

	def read_preferences(self):
		try:
			self.w.colon.set(Glyphs.defaults["com.eweracs.buildPeriodComposites.colon"])
			self.w.semicolon.set(Glyphs.defaults["com.eweracs.buildPeriodComposites.semicolon"])
			self.w.ellipsis.set(Glyphs.defaults["com.eweracs.buildPeriodComposites.ellipsis"])
			self.w.makeBackup.set(Glyphs.defaults["com.eweracs.buildPeriodComposites.makeBackup"])
		except:
			pass


BuildPeriodComposites()
