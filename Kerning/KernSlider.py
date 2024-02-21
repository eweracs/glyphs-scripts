# MenuTitle: Kern Slider
# -*- coding: utf-8 -*-

__doc__ = """
Kern glyphs by slider input.
"""

import sys

from vanilla import FloatingWindow, Group, TextBox, EditText, Slider
from GlyphsApp import Glyphs, Message, UPDATEINTERFACE, LTR

# title at the top with the current glyph pair
# slider with the current kerning value
# change the kerning value by dragging the slider
# save the kerning value when the slider is released
# update the slider value when the kerning value is changed
# update the slider value when the glyph pair is changed
# write the kerning value below the slider


class KernSlider:
	def __init__(self):
		self.font = Glyphs.font

		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		if not self.font.currentTab:
			self.font.newTab("AV")
			self.font.currentTab.textCursor = 1

		self.minValue = -20
		self.maxValue = 20

		self.currentSliderValue = 0

		self.currentKerningValue = 0
		self.oldKerningValue = 0

		self.leftGlyph = ""
		self.rightGlyph = ""
		self.currentPair = ""

		self.w = FloatingWindow((1, 1), "Kern Slider")

		self.w.negativeRange = Group("auto")
		self.w.negativeRange.prefix = TextBox("auto", "−")
		self.w.negativeRange.entry = EditText(
			"auto",
			text=str(abs(self.minValue)),
			continuous=False,
			callback=self.update_ranges
		)

		self.w.positiveRange = Group("auto")
		self.w.positiveRange.prefix = TextBox("auto", "+")
		self.w.positiveRange.entry = EditText(
			"auto",
			text=str(self.maxValue),
			continuous=False,
			callback=self.update_ranges
		)

		self.w.currentPair = TextBox("auto", self.currentPair, alignment="center")

		self.w.slider = Slider(
			"auto",
			tickMarkCount=self.maxValue - self.minValue + 1,
			stopOnTickMarks=True,
			minValue=self.minValue,
			maxValue=self.maxValue,
			value=0,
			callback=self.enter_kern_value
		)

		self.w.currentValue = TextBox("auto", "", alignment="center")
		try:
			self.w.currentValue.set(str(int(self.currentKerningValue)))
		except:
			self.w.currentValue.set("")

		range_rules = [
			"H:|[prefix(8)]-margin-[entry(50)]|",
			"V:|[entry]|",
			"V:|[prefix]",
		]

		rules = [
			"H:|-margin-[negativeRange]-[currentPair]-[positiveRange]-margin-|",
			"H:|-margin-[slider(>=300)]-margin-|",
			"H:|-margin-[currentValue]-margin-|",
			"V:|-margin-[currentPair]-margin-[slider]-margin-[currentValue]-margin-|",
			"V:|-margin-[negativeRange]",
			"V:|-margin-[positiveRange]",
		]

		metrics = {
			"margin": 10
		}

		self.w.negativeRange.addAutoPosSizeRules(range_rules, metrics)
		self.w.positiveRange.addAutoPosSizeRules(range_rules, metrics)
		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.open()
		self.w.bind("close", self.close)

		self.ui_update()

		Glyphs.addCallback(self.ui_update, UPDATEINTERFACE)

	def enter_kern_value(self, sender):
		if sender.get() == self.currentSliderValue:
			sender.set(0)
			self.oldKerningValue = self.currentKerningValue
		self.currentSliderValue = sender.get()

		try:
			self.set_kerning_value(self.oldKerningValue + self.currentSliderValue)
		except:
			pass

	def set_kerning_value(self, value):
		try:
			right_layer = self.font.glyphs[self.rightGlyph].layers[self.font.selectedFontMaster.id]
			left_layer = self.font.glyphs[self.leftGlyph].layers[self.font.selectedFontMaster.id]
			right_layer.setPreviousKerning_forLayer_direction_(value, left_layer, LTR)
		except:
			pass

	def update_ranges(self, sender):
		if not sender.get().isnumeric():
			return
		self.minValue = -int(self.w.negativeRange.entry.get())
		self.maxValue = int(self.w.positiveRange.entry.get())
		self.w.slider.set(0)
		self.w.slider.setMinValue(self.minValue)
		self.w.slider.setMaxValue(self.maxValue)
		self.w.slider.setTickMarkCount(self.maxValue - self.minValue + 1)

	def update_kerning_value(self):
		try:
			right_layer = self.font.glyphs[self.rightGlyph].layers[self.font.selectedFontMaster.id]
			left_layer = self.font.glyphs[self.leftGlyph].layers[self.font.selectedFontMaster.id]
			self.currentKerningValue = right_layer.previousKerningForLayer_direction_(left_layer, LTR)
			if self.currentKerningValue - 1 == float(sys.maxsize):
				self.currentKerningValue = 0
		except:
			self.currentKerningValue = None

	def ui_update(self, sender=None):
		if not self.font.currentTab:
			self.w.slider.enable(False)
			self.w.currentPair.set("–")
			self.w.currentValue.set("")
			return

		if self.font.currentTab.textCursor == 0 or self.font.currentTab.textCursor == len(self.font.currentTab.text):
			self.leftGlyph = ""
			self.rightGlyph = ""

		else:
			try:
				self.leftGlyph = self.font.currentTab.text[self.font.currentTab.textCursor - 1]
			except:
				self.leftGlyph = ""
			try:
				self.rightGlyph = self.font.currentTab.text[self.font.currentTab.textCursor]
			except:
				self.rightGlyph = ""

		# if line break, reset
		if self.leftGlyph == "\n" or self.rightGlyph == "\n":
			self.leftGlyph = ""
			self.rightGlyph = ""

		# only enable slider if leftGlyph and rightGlyph are not empty
		self.w.slider.enable(len(self.leftGlyph + self.rightGlyph) > 0)

		self.currentPair = self.leftGlyph + " – " + self.rightGlyph

		self.update_kerning_value()

		self.w.currentPair.set(self.currentPair)

		try:
			self.w.currentValue.set(str(int(self.currentKerningValue)))
		except:
			self.w.currentValue.set("")

	def close(self, sender):
		Glyphs.removeCallback(self.ui_update, UPDATEINTERFACE)


KernSlider()
