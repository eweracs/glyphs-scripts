# MenuTitle: Auto-name Instances
# -*- coding: utf-8 -*-

__doc__ = """
Names active instances based on set weight and width classes and user-defined exceptions.
"""

import vanilla
from GlyphsApp import Glyphs, Message


class AutoNamer:
	def __init__(self):

		self.font = Glyphs.font

		self.Exceptions = {"width": {}, "weight": {}}

		self.selectedWidthClass = None
		self.widths = []

		self.selectedWeightClass = None
		self.weights = []

		self.exceptionName = None

		self.addExceptionPopUpButtonList = []
		self.addExceptionInputList = []
		self.addExceptionButtonList = []
		self.clearExceptionButtonList = []

		self.ypos = 0

		if Glyphs.defaults["com.eweracs.AutoNameInstances.exceptionprefs"]:
			for axis in Glyphs.defaults["com.eweracs.AutoNameInstances.exceptionprefs"]:
				for key in Glyphs.defaults["com.eweracs.AutoNameInstances.exceptionprefs"][axis]:
					self.Exceptions[axis][key] = Glyphs.defaults[
						"com.eweracs.AutoNameInstances.exceptionprefs"][axis][key]

		self.update_exceptions()

		self.w = vanilla.FloatingWindow((0, 0), "Auto-name Instances")

		self.w.widthExceptionsTitle = vanilla.TextBox(
			(10, 10, -10, 14),
			"Add width name exceptions",
			sizeStyle="small"
		)

		self.new_exception_line("width", self.widths)
		self.new_exception_line("weight", self.weights)

		self.w.autoname = vanilla.Button(
			(10, self.ypos, -10, 20),
			"Auto-name instances",
			callback=self.auto_name_instances
		)

		self.redraw()

		self.w.setDefaultButton(self.w.autoname)

		self.w.open()
		self.w.makeKey()

	def pick_exception_from_list(self, sender):
		for i, item in enumerate(self.addExceptionPopUpButtonList):
			if item is sender:
				if i == 0:
					self.selectedWidthClass = self.widths[sender.get()]
				else:
					self.selectedWeightClass = self.weights[sender.get()]

				# [self.selectedWidthClass, self.selectedWeightClass][i] = [self.widths, self.weights][i][sender.get()]

	def exception_name(self, sender):
		self.exceptionName = sender.get()

	def add(self, sender):
		for i, item in enumerate(self.addExceptionButtonList):
			if item is sender:
				if self.exceptionName is not None:
					list(list(self.Exceptions.items())[i])[1][
						[self.selectedWidthClass, self.selectedWeightClass][i]
					] = self.exceptionName

		Glyphs.defaults["com.eweracs.AutoNameInstances.exceptionprefs"] = self.Exceptions

		self.update_exceptions()
		self.redraw()

	def clear(self, sender):
		for i, item in enumerate(self.clearExceptionButtonList):
			if item is sender:
				for axisnumber in range(len(self.Exceptions)):
					for exceptionnumber in range(len(list(self.Exceptions.items()))):
						i -= 1
						if i < 0:
							break
					if i < 0:
						break
				del self.Exceptions[list(self.Exceptions.items())[axisnumber][0]][
					list(self.Exceptions[list(self.Exceptions.items())[
						axisnumber
					][0]].items())[exceptionnumber][0]]

		Glyphs.defaults["com.eweracs.AutoNameInstances.exceptionprefs"] = self.Exceptions

		self.update_exceptions()
		self.redraw()

	def exception_line(self, index, origin, exception):
		origin = vanilla.TextBox((10, self.ypos, -10, 17), origin)
		arrow = vanilla.TextBox((160, self.ypos, -10, 14), u"\u2192", sizeStyle="regular")
		exception = vanilla.TextBox((190, self.ypos, 130, 22), exception)
		button = vanilla.Button((330, self.ypos, 50, 20), "Clear", callback=self.clear)

		setattr(self.w, index + "origin", origin)
		setattr(self.w, index + "arrow", arrow)
		setattr(self.w, index + "exception", exception)
		setattr(self.w, index + "button", button)

		try:
			print(getattr(self.w, "2origin").get())
		except:
			print()

		self.clearExceptionButtonList.append(button)

		self.ypos = button.getPosSize()[1] + 32

	def new_exception_line(self, type, items):
		add_exception_popup = vanilla.PopUpButton(
			(10, self.ypos, 140, 20),
			items,
			callback=self.pick_exception_from_list
		)
		add_exception_input = vanilla.EditText((190, self.ypos - 1, 130, 22), callback=self.exception_name)
		add_exception_button = vanilla.Button((330, self.ypos, 50, 20), "Add", callback=self.add)

		setattr(self.w, "add" + type + "Exception", add_exception_popup)
		setattr(self.w, "add" + type + "Arrow", vanilla.TextBox((160, self.ypos, -10, 14), u"\u2192", sizeStyle="regular"))
		setattr(self.w, "add" + type + "Name", add_exception_input)
		setattr(self.w, "add" + type + "Button", add_exception_button)

		self.addExceptionPopUpButtonList.append(add_exception_popup)
		self.addExceptionInputList.append(add_exception_input)
		self.addExceptionButtonList.append(add_exception_button)

	def redraw(self):
		try:
			for i in range(len(self.clearExceptionButtonList)):
				delattr(self.w, str(i) + "origin")
				delattr(self.w, str(i) + "arrow")
				delattr(self.w, str(i) + "exception")
				delattr(self.w, str(i) + "button")

		except Exception as e:
			print(e)

		self.ypos = 34

		self.clearExceptionButtonList = []

		for i in range(len(self.Exceptions["width"])):
			self.exception_line(
				str(i),
				list(self.Exceptions["width"])[i],
				list(self.Exceptions["width"].items())[i][1]
			)

		self.w.addwidthException.show(len(self.widths) > 0)
		self.w.addwidthArrow.show(len(self.widths) > 0)
		self.w.addwidthName.show(len(self.widths) > 0)
		self.w.addwidthButton.show(len(self.widths) > 0)

		self.w.addwidthException.setItems(self.widths)
		self.w.addwidthName.set("")

		self.w.addwidthException.setPosSize((10, self.ypos, 140, 20))
		self.w.addwidthArrow.setPosSize((160, self.ypos, -10, 14))
		self.w.addwidthName.setPosSize((190, self.ypos - 1, 130, 22))
		self.w.addwidthButton.setPosSize((330, self.ypos, 50, 20))

		if len(self.widths) > 0:
			self.ypos += 32

		for i in range(len(self.Exceptions["weight"])):
			buttonindex = i + len(self.Exceptions["width"])
			self.exception_line(
				str(buttonindex),
				list(self.Exceptions["weight"])[i],
				list(self.Exceptions["weight"].items())[i][1]
			)

		self.w.addweightException.show(len(self.weights) > 0)
		self.w.addweightArrow.show(len(self.weights) > 0)
		self.w.addweightName.show(len(self.weights) > 0)
		self.w.addweightButton.show(len(self.weights) > 0)

		self.w.addweightException.setItems(self.weights)
		self.w.addweightName.set("")

		self.w.addweightException.setPosSize((10, self.ypos, 140, 20))
		self.w.addweightArrow.setPosSize((160, self.ypos, -10, 14))
		self.w.addweightName.setPosSize((190, self.ypos - 1, 130, 22))
		self.w.addweightButton.setPosSize((330, self.ypos, 50, 20))

		if len(self.widths) > 0:
			self.ypos += 32

		self.w.autoname.setPosSize((10, self.ypos, -10, 20))

		self.w.resize(390, self.ypos + 32)

	def update_exceptions(self):
		self.widths = [width for width in [
			"Ultra Condensed",
			"Extra Condensed",
			"Condensed",
			"SemiCondensed",
			"Medium (normal)",
			"Semi Expanded",
			"Expanded",
			"Extra Expanded",
			"Ultra Expanded"
		] if width not in self.Exceptions["width"]]

		if len(self.widths) > 0:
			self.selectedWidthClass = self.widths[0]

		self.weights = [weight for weight in [
			"Thin",
			"UltraLight",
			"ExtraLight",
			"Light",
			"Normal",
			"Regular",
			"Medium",
			"DemiBold",
			"SemiBold",
			"Bold",
			"UltraBold",
			"ExtraBold",
			"Black",
			"Heavy"
		] if weight not in self.Exceptions["weight"]]

		if len(self.weights) > 0:
			self.selectedWeightClass = self.weights[0]

	def auto_name_instances(self, sender):
		self.w.close()

		if self.font is None:
			Message("Open a font file!", title="Error")
			return

		for i in self.font.instances:
			if i.active:
				if str(Glyphs.versionNumber)[0] == "3":  # Glyphs 3
					weight_name = i.weightClassName
					width_name = i.widthClassName

					if "Medium" in i.widthClassName and "Medium" not in self.Exceptions["width"]:
						width_name = ""
					if i.widthClassName in self.Exceptions["width"]:
						width_name = self.Exceptions["width"][i.widthClassName]
					if i.weightClassName in self.Exceptions["weight"]:
						weight_name = self.Exceptions["weight"][i.weightClassName]

					if i.weightClassName == "Regular" or i.weightClassName == "Normal":
						weight_name = ""
					if len(weight_name) != 0 and len(width_name) != 0:
						i.name = " ".join([weight_name, width_name])
					elif len(weight_name) > 1:
						i.name = weight_name
					elif len(width_name) > 1:
						i.name = width_name
					if i.name == "":
						i.name = "Regular"
					if i.isItalic:
						i.name += " Italic"
				else:  # Glyphs 2
					weight_name = i.weight
					width_name = i.width
					if "Medium" in i.width and "Medium" not in self.Exceptions["width"]:
						width_name = ""

					if i.width in self.Exceptions["width"]:
						width_name = self.Exceptions["width"][i.width]
					if i.weightClassName in self.Exceptions["weight"]:
						weight_name = self.Exceptions["weight"][i.weightClassName]

					if i.weight == "Regular" or i.weight == "Normal":
						weight_name = ""
					if len(weight_name) != 0 and len(width_name) != 0:
						i.name = " ".join([weight_name, width_name])
					elif len(weight_name) > 1:
						i.name = weight_name
					elif len(width_name) > 1:
						i.name = width_name
					if i.name == "":
						i.name = "Regular"
					if i.isItalic:
						i.name += " Italic"


AutoNamer()
