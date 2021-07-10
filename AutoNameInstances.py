# MenuTitle: Auto-name instances
# -*- coding: utf-8 -*-
__doc__ = """
Names pre-defined instances based on set weight and width classes.
"""

import vanilla


class AutoNamer:
	def __init__(self):
		self.font = Font
		self.prefs = []
		self.widthExceptions = {"Medium (normal)": "Hello", "Extra Condensed": "Hey"}
		self.widths = [width for width in {i.width for i in self.font.instances} if width not in
		               [item for item in self.widthExceptions]]
		self.exceptionName = None

		self.w = vanilla.FloatingWindow((0, 0), "Instance Autonamer")
		self.widthExTitleList = []
		self.widthExArrowList = []
		self.widthExEditList = []
		self.widthExButtonList = []

		self.ypos = 32

		setattr(self.w, "widthExceptionsTitle", vanilla.TextBox((10, 10, -10, 14), "Add width name exceptions",
		                                                        sizeStyle="small"))

		for i, exception in enumerate(self.widthExceptions):
			n = vanilla.TextBox((10, self.ypos + i * 32, -10, 17), str(list(self.widthExceptions.items())[i][0]))
			a = vanilla.TextBox((160, self.ypos + i * 32, -10, 14), u"\u2192", sizeStyle="regular")
			e = vanilla.EditText((190, self.ypos - 1 + i * 32, 130, 22),
			                     text=str(list(self.widthExceptions.items())[i][1]))
			b = vanilla.Button((330, self.ypos + i * 32, 50, 20), "Clear", callback=self.clear_exception)
			setattr(self.w, exception + "Selection", n)
			self.widthExTitleList.append(n)
			setattr(self.w, exception + "Arrow", a)
			self.widthExArrowList.append(a)
			setattr(self.w, exception + "Name", e)
			self.widthExEditList.append(e)
			setattr(self.w, exception + "Clear", b)
			self.widthExButtonList.append(b)
			self.ypos = n.getPosSize()[1]

		self.ypos += 32

		if len(self.widths) > 0:
			self.selectedWidthClass = self.widths[0]
			setattr(self.w, "widthExceptions", vanilla.PopUpButton((10, self.ypos, 140, 20), self.widths,
			                                                       callback=self.list_width_exceptions))
			setattr(self.w, "widthExceptionsArrow", vanilla.TextBox((160, self.ypos, -10, 14), u"\u2192",
			                                                        sizeStyle="regular"))

			setattr(self.w, "widthExceptionName", vanilla.EditText((190, self.ypos - 1, 130, 22),
			                                                       callback=self.width_exception_name))
			setattr(self.w, "addWidthException", vanilla.Button((330, self.ypos, 50, 20), "Add",
			                                                    callback=self.add_width_exception))

			self.ypos = self.w.widthExceptions.getPosSize()[1] + 30

		self.w.resize(390, self.ypos)
		self.w.open()
		self.w.makeKey()

	def list_width_exceptions(self, sender):
		self.selectedWidthClass = self.widths[sender.get()]

	def width_exception_name(self, sender):
		self.exceptionName = sender.get()

	def add_width_exception(self, sender):
		self.widthExceptions[self.selectedWidthClass] = self.exceptionName

	def clear_exception(self, sender):
		for i, item in enumerate(self.widthExTitleList):
			if item is sender:
				sender.get()

AutoNamer()

# for i in Font.instances:
# 	if i.active:
# 		if "Medium" in i.width:
# 			i.name = i.weight
# 		elif i.weight == "Regular" or i.weight == "Normal":
# 			i.name = i.width
# 		elif i.width == "Ultra Condensed":
# 			i.name = i.weight + " Compressed"
# 		else:
# 			i.name = i.weight + " " + i.width
# 		if i.isItalic:
# 			i.name += " Italic"
# 			if "Regular" in i.name:
# 				i.name = i.name.replace("Regular ", "")
