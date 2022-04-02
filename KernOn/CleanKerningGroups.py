# MenuTitle: Clean Kerning Groups
# -*- coding: utf-8 -*-

__doc__ = """
Cleans up the kerning file to remove all occurences of "KO_".
"""

import vanilla


class CleanGroups:
	def __init__(self):
		self.font = Font

		self.filePath = self.font.filepath

		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		self.w = vanilla.FloatingWindow((0, 0), "Clean kerning groups")

		self.ypos = 10

		self.w.helperText = vanilla.TextBox((10, self.ypos, -10, 50),
		                                    "This will remove all occurences of \"KO_\" in your kerning groups."
		                                    "\nYour file will close.", sizeStyle="small")

		self.ypos += 48

		self.w.reopen = vanilla.CheckBox((14, self.ypos, -10, 17), "Reopen file afterwards", sizeStyle="small")

		self.ypos += 26

		self.w.cleanButton = vanilla.Button((10, self.ypos, -10, 20), "Clean kerning", callback=self.clean_groups)

		self.ypos += 30

		self.w.setDefaultButton(self.w.cleanButton)

		self.w.resize(196, self.ypos)
		self.w.open()
		self.w.makeKey()

	def clean_groups(self, sender):
		self.w.close()

		self.font.save()

		f = open(self.font.filepath, "r")
		filedata = f.read()
		f.close()

		newdata = filedata.replace("KO_", "")

		f = open(self.font.filepath, "w")
		f.write(newdata)
		f.close()

		self.font.close()
		if self.w.reopen.get():
			Glyphs.open(self.filePath)


CleanGroups()
