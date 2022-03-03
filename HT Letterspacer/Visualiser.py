# MenuTitle: Visualiser
# -*- coding: utf-8 -*-

__doc__ = """
Visually adjust HT Letterspacer parameters.
"""

import vanilla
from AppKit import NSColor

try:
	from HT_LetterSpacer_script import *
except:
	Message("Please run HT Letterspacer once before starting the script.", "External import required")

try:
	from importlib import reload
except:
	pass
reload(HT_LetterSpacer_script)


class HTLSVisualiser:
	def __init__(self):
		if Font is None:
			Message("No font selected", "Select a font project!")
			return

		self.font = Font

		self.glyphList = [glyph.name for glyph in self.font.glyphs]

		self.currentMasterId = self.font.selectedFontMaster.id
		self.originalParams = []
		self.originalSidebearings = []
		self.force_update = False

		for i, master in enumerate(Font.masters):
			if not master.customParameters["paramArea"]:
				master.customParameters["paramArea"] = round(
					Font.glyphs["idotless"].layers[i].LSB * master.xHeight / 100)
			if not master.customParameters["paramDepth"]:
				master.customParameters["paramDepth"] = 10
			self.originalParams.append([master.customParameters["paramArea"], master.customParameters["paramDepth"]])

			master_sidebearings = {glyph.name: [self.font.glyphs[glyph.name].layers[master.id].LSB, self.font.glyphs[
				glyph.name].layers[master.id].RSB] for glyph in self.font.glyphs
			}

			self.originalSidebearings.append(master_sidebearings)

		self.areaValueForMaster = int(self.font.selectedFontMaster.customParameters["paramArea"])
		self.depthValueForMaster = int(self.font.selectedFontMaster.customParameters["paramDepth"])

		if not self.font.currentTab:
			self.font.newTab("nnnnonononooo")

		self.font.currentTab.textCursor = 0
		self.font.currentTab.textRange = len(Font.currentTab.text)

		self.space_glyphs()

		self.w = vanilla.FloatingWindow((0, 0), "HT Letterspacer Visualiser")

		self.ypos = 10

		self.w.areaTtitle = vanilla.TextBox((10, self.ypos, -10, 14), "Area (" + str(self.originalParams[
			self.font.masterIndex][0]) + ")",
		                                    sizeStyle="small")
		self.w.areaEntry = vanilla.EditText((-60, self.ypos, -10, 19),
		                                    self.areaValueForMaster,
		                                    sizeStyle="small", callback=self.enter_area_value)

		self.ypos += 24

		self.w.areaSlider = vanilla.Slider((10, self.ypos, -10, 23), minValue=1,
		                                   maxValue=self.areaValueForMaster*1.5,
		                                   value=self.areaValueForMaster, callback=self.area_slider_callback)

		self.ypos += 30

		self.w.depthTtitle = vanilla.TextBox((10, self.ypos, -10, 14), "Depth (" + str(self.originalParams[
			self.font.masterIndex][1]) + ")", sizeStyle="small")
		self.w.depthEntry = vanilla.EditText((-60, self.ypos, -10, 19),
		                                    self.depthValueForMaster,
		                                    sizeStyle="small", callback=self.enter_depth_value)

		self.ypos += 24

		self.w.depthSlider = vanilla.Slider((10, self.ypos, -10, 23), minValue=1,
		                                   maxValue=20,
		                                   value=self.depthValueForMaster, callback=self.depth_slider_callback)

		self.ypos += 30

		self.w.resetButton = vanilla.Button((10, self.ypos, 100, 20), "Reset", callback=self.reset_values)

		self.ypos += 32

		self.w.divider = vanilla.HorizontalLine((10, self.ypos, -10, 1))

		self.ypos += 16

		self.w.leftOriginalLSB = vanilla.TextBox((30, self.ypos, 110, 14),
		                                      "(" + str(self.originalSidebearings[self.font.masterIndex]["n"][0]) + ")",
		                                      sizeStyle="small", alignment="left")
		self.w.leftOriginalRSB = vanilla.TextBox((30, self.ypos, 110, 14),
		                                      "(" + str(self.originalSidebearings[self.font.masterIndex]["n"][1]) + ")",
		                                      sizeStyle="small", alignment="right")

		self.w.rightOriginalLSB = vanilla.TextBox((160, self.ypos, -30, 14),
		                                      "(" + str(self.originalSidebearings[self.font.masterIndex]["o"][0]) + ")",
		                                      sizeStyle="small", alignment="left")
		self.w.rightOriginalRSB = vanilla.TextBox((160, self.ypos, -30, 14),
		                                      "(" + str(self.originalSidebearings[self.font.masterIndex]["o"][1]) + ")",
		                                      sizeStyle="small", alignment="right")

		self.ypos += 25

		color = NSColor.clearColor()
		self.w.leftView = GlyphView((20, self.ypos, 130, 100),
		                                    layer=self.font.glyphs["n"].layers[self.font.selectedFontMaster.id],
		                            backgroundColor=color)

		self.w.rightView = GlyphView((150, self.ypos, 130, 100),
		                                     layer=self.font.glyphs["o"].layers[self.font.selectedFontMaster.id],
		                             backgroundColor=color)

		self.ypos += 40

		self.w.leftNewLSB = vanilla.TextBox((30, self.ypos, 110, 14),
		                                 self.font.glyphs["n"].layers[self.font.masterIndex].LSB,
		                                 sizeStyle="small", alignment="left")
		self.w.leftNewRSB = vanilla.TextBox((30, self.ypos, 110, 14),
		                                 self.font.glyphs["n"].layers[self.font.masterIndex].RSB,
		                                 sizeStyle="small", alignment="right")

		self.w.rightNewLSB = vanilla.TextBox((160, self.ypos, -30, 14),
		                                 self.font.glyphs["o"].layers[self.font.masterIndex].LSB,
		                                 sizeStyle="small", alignment="left")
		self.w.rightNewRSB = vanilla.TextBox((160, self.ypos, -30, 14),
		                                 self.font.glyphs["o"].layers[self.font.masterIndex].RSB,
		                                 sizeStyle="small", alignment="right")

		self.ypos += 66

		self.w.leftGlyphSelector = vanilla.ComboBox((20, self.ypos, 120, 19), self.glyphList, sizeStyle="small",
		                                            callback=self.ui_update)
		self.w.rightGlyphSelector = vanilla.ComboBox((160, self.ypos, -20, 19), self.glyphList, sizeStyle="small",
		                                             callback=self.ui_update)

		self.w.leftGlyphSelector.set("n")
		self.w.rightGlyphSelector.set("o")

		self.ypos += 30

		self.w.bind("close", self.window_close)
		self.w.resize(300, self.ypos)
		self.w.open()
		self.w.makeKey()

		Glyphs.addCallback(self.ui_update, UPDATEINTERFACE)

	def enter_area_value(self, sender):
		try:
			if sender.get().isnumeric() and int(sender.get()) > 0:
				self.font.selectedFontMaster.customParameters["paramArea"] = int(sender.get())
				self.areaValueForMaster = int(sender.get())
				self.w.areaSlider.set(int(sender.get()))
				self.space_glyphs()
		except Exception as e:
			print(e)

	def area_slider_callback(self, sender):
		self.font.selectedFontMaster.customParameters["paramArea"] = int(sender.get())
		self.areaValueForMaster = int(sender.get())
		self.w.areaEntry.set(int(sender.get()))
		self.space_glyphs()

	def enter_depth_value(self, sender):
		if sender.get().isnumeric() and int(sender.get()) > 0:
			self.font.selectedFontMaster.customParameters["paramDepth"] = int(sender.get())
			self.depthValueForMaster = int(sender.get())
			self.w.depthSlider.set(int(sender.get()))
			self.space_glyphs()

	def depth_slider_callback(self, sender):
		self.font.selectedFontMaster.customParameters["paramDepth"] = int(sender.get())
		self.depthValueForMaster = int(sender.get())
		self.w.depthEntry.set(int(sender.get()))
		self.space_glyphs()

	def reset_values(self, sender):
		self.font.selectedFontMaster.customParameters["paramArea"] = int(self.originalParams[self.font.masterIndex][0])
		self.font.selectedFontMaster.customParameters["paramDepth"] = int(self.originalParams[self.font.masterIndex][1])
		self.force_update = True
		self.ui_update(None)
		self.force_update = False
		self.space_glyphs()


	def space_glyphs(self):
		self.font.currentTab.textCursor = 0
		self.font.currentTab.textRange = len(Font.currentTab.text)
		try:
			HT_LetterSpacer_script.HTLetterspacerScript(ui=False, all_masters=False)
		except:
			HT_LetterSpacer_script.HTLetterspacerScript(ui=False)
		for layer in self.font.selectedLayers:
			layer.syncMetrics()

	def ui_update(self, info):
		self.w.leftNewLSB.set(self.font.glyphs[self.w.leftGlyphSelector.get()].layers[self.font.masterIndex].LSB)
		self.w.leftNewRSB.set(self.font.glyphs[self.w.leftGlyphSelector.get()].layers[self.font.masterIndex].RSB)
		self.w.rightNewLSB.set(self.font.glyphs[self.w.rightGlyphSelector.get()].layers[self.font.masterIndex].LSB)
		self.w.rightNewRSB.set(self.font.glyphs[self.w.rightGlyphSelector.get()].layers[self.font.masterIndex].RSB)

		if self.w.leftGlyphSelector.get() in self.glyphList:
			self.w.leftView.layer = self.font.glyphs[self.w.leftGlyphSelector.get()].layers[
				self.font.selectedFontMaster.id
			]
			if self.font.glyphs[self.w.leftGlyphSelector.get()].string not in self.font.currentTab.text:
				self.font.currentTab.text += "/" + self.w.leftGlyphSelector.get()
		if self.w.rightGlyphSelector.get() in self.glyphList:
			self.w.rightView.layer = self.font.glyphs[self.w.rightGlyphSelector.get()].layers[
				self.font.selectedFontMaster.id
			]
			if self.font.glyphs[self.w.rightGlyphSelector.get()].string not in self.font.currentTab.text:
				self.font.currentTab.text += "/" + self.w.rightGlyphSelector.get()
			
		self.w.leftOriginalLSB.set("(" + str(self.originalSidebearings[self.font.masterIndex][
			                                  self.w.leftGlyphSelector.get()][0]) + ")")
		self.w.leftOriginalRSB.set("(" + str(self.originalSidebearings[self.font.masterIndex][
			                                  self.w.leftGlyphSelector.get()][1]) + ")")
		self.w.rightOriginalLSB.set("(" + str(self.originalSidebearings[self.font.masterIndex][
			                                  self.w.rightGlyphSelector.get()][0]) + ")")
		self.w.rightOriginalRSB.set("(" + str(self.originalSidebearings[self.font.masterIndex][
			                                  self.w.rightGlyphSelector.get()][1]) + ")")

		if self.currentMasterId == self.font.selectedFontMaster.id and self.force_update is False:
			return

		self.w.areaTtitle.set("Area (" + str(self.originalParams[self.font.masterIndex][0]) + ")")
		self.areaValueForMaster = int(self.font.selectedFontMaster.customParameters["paramArea"])
		self.w.areaEntry.set(self.areaValueForMaster)
		self.w.areaSlider.setMaxValue(self.areaValueForMaster * 1.5)
		self.w.areaSlider.set(self.areaValueForMaster)

		self.w.depthTtitle.set("Depth (" + str(self.originalParams[self.font.masterIndex][1]) + ")")
		self.depthValueForMaster = int(self.font.selectedFontMaster.customParameters["paramDepth"])
		self.w.depthEntry.set(self.depthValueForMaster)
		self.w.depthSlider.set(self.depthValueForMaster)
		self.currentMasterId = self.font.selectedFontMaster.id

	def window_close(self, sender):
		Glyphs.removeCallback(self.ui_update, UPDATEINTERFACE)


HTLSVisualiser()
