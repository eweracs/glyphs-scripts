# MenuTitle: Kerning slider
# -*- coding: utf-8 -*-

__doc__ = """
Kerns glyphs by slider input.
"""

import vanilla


class KernSlider:
	def __init__(self):

		self.font = Font

		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		self.currentPair = ""

		self.update_current_pair()

		self.currentKerningValue = self.font.kerningForPair(self.font.selectedFontMaster.id, self.currentPair[0],
		                                                    self.currentPair[1])
		if self.currentKerningValue is None:
			self.currentKerningValue = 0
		self.oldKerningValue = int(self.currentKerningValue)

		Glyphs.addCallback(self.ui_update, UPDATEINTERFACE)

		if not self.font.currentTab:
			self.font.newTab("AV")
			self.font.currentTab.textCursor = 1

		self.w = vanilla.FloatingWindow((0, 0), "Kerning slider")

		self.ypos = 10

		self.w.pairTitle = vanilla.TextBox((10, self.ypos, -10, 17), self.currentPair[0] + " – " + self.currentPair[
			1], alignment="center")

		self.ypos += 20

		self.w.kernSlider = vanilla.Slider((10, self.ypos, -10, 23), minValue=-20,
		                                   maxValue=20, tickMarkCount=41,
		                                   value=self.currentKerningValue, stopOnTickMarks=True,
		                                   callback=self.enter_kern_value)

		self.ypos += 30

		self.update_slider_values(self.currentKerningValue, True)

		self.w.bind("close", self.window_close)
		self.w.resize(300, self.ypos)
		self.w.open()

	def enter_kern_value(self, sender):
		if sender.get() == self.currentKerningValue and self.oldKerningValue != sender.get():
			self.update_slider_values(sender.get(), True)
		self.currentKerningValue = int(sender.get())

		self.left_key = self.font.glyphs[self.currentPair[0]].leftKerningKey or self.currentPair[0]
		self.right_key = self.font.glyphs[self.currentPair[1]].leftKerningKey or self.currentPair[1]

		self.font.setKerningForPair(self.font.selectedFontMaster.id, self.left_key, self.right_key,
		                            self.currentKerningValue)

	def update_slider_values(self, value, redraw_axis):
		if redraw_axis:
			if abs(value * 2) < 20:
				new_max = 20
				new_min = -20
			else:
				new_max = abs(value) * 2
				new_min = abs(value) * -2
			self.w.kernSlider.setMaxValue(new_max)
			self.w.kernSlider.setMinValue(new_min)
			self.w.kernSlider.setTickMarkCount(new_max * 2 + 1)
		self.w.kernSlider.set(value)
		self.oldKerningValue = value

	def update_current_pair(self):
		self.currentPair = self.font.currentTab.text[
		                   self.font.currentTab.textCursor - 1:self.font.currentTab.textCursor + 1
		                   ]

		self.left_key = self.font.glyphs[self.currentPair[0]].leftKerningKey or self.currentPair[0]
		self.right_key = self.font.glyphs[self.currentPair[1]].leftKerningKey or self.currentPair[1]

		if len(self.currentPair) < 2:
			self.currentPair = "  "
		try:
			self.w.pairTitle.set(self.currentPair[0] + " – " + self.currentPair[
			1])
		except:
			return

		self.currentKerningValue = self.font.kerningForPair(self.font.selectedFontMaster.id, self.left_key,
		                                                    self.right_key)
		if self.currentKerningValue is None:
			self.currentKerningValue = 0

	def ui_update(self, info):
		try:
			if self.font.currentTab.text[self.font.currentTab.textCursor] != self.currentPair[1]:
				self.update_current_pair()
				self.w.kernSlider.set(self.currentKerningValue)
				self.update_slider_values(self.currentKerningValue, True)
		except:
			self.w.pairTitle.set("–")

	def window_close(self, sender):
		Glyphs.removeCallback(self.ui_update, UPDATEINTERFACE)

KernSlider()
