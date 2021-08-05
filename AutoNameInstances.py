# MenuTitle: Auto-name instances
# -*- coding: utf-8 -*-
__doc__ = """
Names pre-defined instances based on set weight and width classes.
"""

import vanilla


class AutoNamer:
	def __init__(self):
		try:
			self.font = Font
		except Exception:
			print("Open a font file!")
			quit()
		self.prefs = []
		self.widthExceptions = {}
		self.selectedWidthClass = None
		self.widths = []

		if Glyphs.defaults["com.eweracs.AutoNameInstances.exceptionprefs"]:
			for key in Glyphs.defaults["com.eweracs.AutoNameInstances.exceptionprefs"]:
				self.widthExceptions[key] = Glyphs.defaults["com.eweracs.AutoNameInstances.exceptionprefs"][key]

		self.update_widths()

		# self.widths = [width for width in {i.width for i in self.font.instances} if width not in
		#               [item for item in self.widthExceptions]]

		self.exceptionName = None  # Exception title set by the user

		self.w = vanilla.FloatingWindow((0, 0), "Instance Autonamer")
		self.widthExTitleList = []
		self.widthExArrowList = []
		self.widthExEditList = []
		self.widthExButtonList = []

		setattr(self.w, "widthExceptionsTitle", vanilla.TextBox((10, 10, -10, 14), "Add width name exceptions",
		                                                        sizeStyle="small"))

		self.ypos = 32
		for i, exception in enumerate(self.widthExceptions):
			n = vanilla.TextBox((10, self.ypos + i * 32, -10, 17), str(list(self.widthExceptions.items())[i][0]))
			a = vanilla.TextBox((160, self.ypos + i * 32, -10, 14), u"\u2192", sizeStyle="regular")
			e = vanilla.TextBox((190, self.ypos + i * 32, 130, 22), str(list(self.widthExceptions.items())[i][1]))
			b = vanilla.Button((330, self.ypos + i * 32, 50, 20), "Clear", callback=self.clear_exception)
			setattr(self.w, exception + "Selection", n)
			self.widthExTitleList.append(n)
			setattr(self.w, exception + "Arrow", a)
			self.widthExArrowList.append(a)
			setattr(self.w, exception + "Name", e)
			self.widthExEditList.append(e)
			setattr(self.w, exception + "Clear", b)
			self.widthExButtonList.append(b)

		try:
			self.ypos = n.getPosSize()[1] + 32
		except Exception:
			self.ypos = 32

		if len(self.widths) > 0:
			self.selectedWidthClass = self.widths[0]
			setattr(self.w, "widthExceptions", vanilla.PopUpButton((10, self.ypos, 140, 20), self.widths,
			                                                       callback=self.list_exceptions))
			setattr(self.w, "widthExceptionsArrow", vanilla.TextBox((160, self.ypos, -10, 14), u"\u2192",
			                                                        sizeStyle="regular"))

			setattr(self.w, "widthExceptionName", vanilla.EditText((190, self.ypos - 1, 130, 22),
			                                                       callback=self.exception_name))
			setattr(self.w, "addWidthException", vanilla.Button((330, self.ypos, 50, 20), "Add",
			                                                    callback=self.add_exception))

			self.ypos = self.w.widthExceptions.getPosSize()[1] + 32

		setattr(self.w, "generate", vanilla.Button((10, self.ypos, -10, 20), "Auto-name instances",
		                                           callback=self.auto_name_instances))

		self.ypos += 32

		self.w.resize(390, self.ypos)
		self.w.open()
		self.w.makeKey()

	def list_exceptions(self, sender):
		self.selectedWidthClass = self.widths[sender.get()]

	def exception_name(self, sender):
		self.exceptionName = sender.get()

	def add_exception(self, sender):
		self.widthExceptions[self.selectedWidthClass] = self.exceptionName
		n = vanilla.TextBox((10, self.ypos, -10, 17), self.selectedWidthClass)
		a = vanilla.TextBox((160, self.ypos, -10, 14), u"\u2192", sizeStyle="regular")
		e = vanilla.TextBox((190, self.ypos -1, 130, 22), str(self.widthExceptions[self.selectedWidthClass]))
		b = vanilla.Button((330, self.ypos, 50, 20), "Clear", callback=self.clear_exception)

		setattr(self.w, self.selectedWidthClass + "Selection", n)
		self.widthExTitleList.append(n)
		setattr(self.w, self.selectedWidthClass + "Arrow", a)
		self.widthExArrowList.append(a)
		setattr(self.w, self.selectedWidthClass + "Name", e)
		self.widthExEditList.append(e)
		setattr(self.w, self.selectedWidthClass + "Clear", b)
		self.widthExButtonList.append(b)

		self.update_widths()
		self.redraw_items()
		Glyphs.defaults["com.eweracs.AutoNameInstances.exceptionprefs"] = self.widthExceptions

	def clear_exception(self, sender):

		for i, item in enumerate(self.widthExButtonList):
			if item is sender:
				delattr(self.w, list(self.widthExceptions.items())[i][0] + "Selection")
				del self.widthExTitleList[i]
				delattr(self.w, list(self.widthExceptions.items())[i][0] + "Arrow")
				del self.widthExArrowList[i]
				delattr(self.w, list(self.widthExceptions.items())[i][0] + "Name")
				del self.widthExEditList[i]
				delattr(self.w, list(self.widthExceptions.items())[i][0] + "Clear")
				del self.widthExButtonList[i]
				del self.widthExceptions[list(self.widthExceptions.items())[i][0]]

		self.update_widths()
		self.redraw_items()
		Glyphs.defaults["com.eweracs.AutoNameInstances.exceptionprefs"] = self.widthExceptions

	def update_widths(self):
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
		] if width not in self.widthExceptions]

		self.selectedWidthClass = self.widths[0]

	def redraw_items(self):
		self.ypos = 32
		for i in range(len(self.widthExceptions)):
			self.widthExTitleList[i].setPosSize((10, self.ypos + i * 32, -10, 17))
			self.widthExArrowList[i].setPosSize((160, self.ypos + i * 32, -10, 14))
			self.widthExEditList[i].setPosSize((190, self.ypos + i * 32 - 1, 130, 22))
			self.widthExButtonList[i].setPosSize((330, self.ypos + i * 32, 50, 20))
		try:
			self.ypos = self.widthExTitleList[i].getPosSize()[1] + 32
		except Exception as e:
			print(e)

		self.w.widthExceptions.setItems(self.widths)
		self.w.widthExceptions.setPosSize((10, self.ypos, 140, 20))
		self.w.widthExceptionsArrow.setPosSize((160, self.ypos, -10, 14))
		self.w.widthExceptionName.set("")
		self.w.widthExceptionName.setPosSize((190, self.ypos - 1, 130, 22))
		self.w.addWidthException.setPosSize((330, self.ypos, 50, 20))

		self.ypos += 32

		self.w.generate.setPosSize((10, self.ypos, -10, 20))

		self.ypos += 32

		self.w.resize(390, self.ypos)

	def auto_name_instances(self, sender):
		for i in self.font.instances:
			if i.active:
				if "Medium" in i.width:
					i.name = i.weight
				elif i.weight == "Regular" or i.weight == "Normal":
					i.name = i.width
				for exception in self.widthExceptions:
					if str(exception) in i.width:
						i.name = i.weight + " " + self.widthExceptions[exception]
				if i.isItalic:
					i.name += " Italic"
					if "Regular" in i.name:
						i.name = i.name.replace("Regular ", "")

		Glyphs.defaults["com.eweracs.AutoNameInstances.exceptionprefs"] = self.widthExceptions


AutoNamer()
