# MenuTitle: Visualiser
# -*- coding: utf-8 -*-

__doc__ = """
Visually adjust HT Letterspacer parameters.
"""

import vanilla

try:
	import HT_LetterSpacer_script
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

		self.currentMasterId = self.font.selectedFontMaster.id
		self.originalParams = []
		self.force_update = False

		for i, master in enumerate(Font.masters):
			if not master.customParameters["paramArea"]:
				master.customParameters["paramArea"] = round(
					Font.glyphs["idotless"].layers[i].LSB * master.xHeight / 100)
			if not master.customParameters["paramDepth"]:
				master.customParameters["paramDepth"] = 10
			self.originalParams.append([master.customParameters["paramArea"], master.customParameters["paramDepth"]])

		self.areaValueForMaster = int(self.font.selectedFontMaster.customParameters["paramArea"])
		self.depthValueForMaster = int(self.font.selectedFontMaster.customParameters["paramDepth"])

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
		if self.currentMasterId == self.font.selectedFontMaster.id and self.force_update is False:
			return
		print("h")
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
