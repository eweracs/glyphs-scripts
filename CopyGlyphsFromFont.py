# MenuTitle: Copy Glyphs Between Fonts
# -*- coding: utf-8 -*-

__doc__ = """
Copies a selection of glyphs from a source font to a target font.
"""

from vanilla import *


# Build a vanilla UI that has a selector for the source font and a selector for the target font
# Add a scrolling text field where you can enter the glyphs you want to copy
# make sure that all entered glyphs exist in the target font
# add a check box for overwriting existing glyphs
# add a button which copies the selected glyphs

class CopyGlyphs:
	def __init__(self):
		self.font = Font

		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		# check that more than one font is open
		if len(Glyphs.fonts) < 2:
			Message("Please open another font and try again.", "Two fonts required")
			return

		self.w = FloatingWindow((1, 1), "")
		self.w.sourceFont = Group("auto")
		self.w.sourceFont.title = TextBox("auto", "Source font:")
		self.w.sourceFont.selector = PopUpButton("auto", [font.familyName for font in Glyphs.fonts],
		                                         callback=self.check_source_target)

		self.w.targetFont = Group("auto")
		self.w.targetFont.title = TextBox("auto", "Target font:")
		self.w.targetFont.selector = PopUpButton("auto", [font.familyName for font in Glyphs.fonts],
		                                         callback=self.check_source_target)
		self.w.targetFont.selector.set(1)

		self.w.glyphs = Group("auto")
		self.w.glyphs.title = TextBox("auto", "Glyphs to copy (space separated):")
		self.w.glyphs.text = TextEditor("auto", "", callback=self.check_glyphs)

		# add a text box listing the glyphs missing in the source font
		self.w.missing = TextBox("auto", "", sizeStyle="small")

		self.w.overwrite = CheckBox("auto", "Overwrite existing glyphs")
		self.w.divider = HorizontalLine("auto")
		self.w.copyGlyphs = Button("auto", "Copy glyphs", callback=self.copy_glyphs)

		self.check_glyphs(self.w.glyphs.text)

		self.w.setDefaultButton(self.w.copyGlyphs)

		font_rules = [
			"H:|[title]|",
			"H:|[selector]|",
			"V:|[title]-margin-[selector]|",
		]

		glyph_rules = [
			"H:|[title]|",
			"H:|[text]|",
			"V:|[title]-margin-[text(>=80)]|",
		]

		rules = [
			"H:|-border-[sourceFont]-border-|",
			"H:|-border-[targetFont]-border-|",
			"H:|-border-[glyphs]-border-|",
			"H:|-border-[missing(200)]",
			"H:|-border-[overwrite]-border-|",
			"H:|-border-[divider]-border-|",
			"H:|-border-[copyGlyphs]-border-|",
			"V:|-border-[sourceFont]-margin-[targetFont]-margin-[glyphs]-[missing]-margin-[overwrite]-margin-["
			"divider]-margin"
			"-[copyGlyphs]-border-|",
		]

		metrics = {
			"border": 10,
			"margin": 10
		}

		self.w.sourceFont.addAutoPosSizeRules(font_rules, metrics)
		self.w.targetFont.addAutoPosSizeRules(font_rules, metrics)
		self.w.glyphs.addAutoPosSizeRules(glyph_rules, metrics)
		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.open()
		self.w.makeKey()

	# make sure that the source font is not the same as the target font
	# deactivate the copy button if the source and target font are the same

	def check_source_target(self, sender):
		self.w.copyGlyphs.enable(self.w.sourceFont.selector.get() != self.w.targetFont.selector.get())

	# make sure that the entered glyphs exist in the source font
	# deactivate the copy button if any of the entered glyphs do not exist in the source font

	def check_glyphs(self, sender):
		# make a list of the missing glyphs and write it in the text box
		# show the text box only if there are missing glyphs
		missing = []
		for glyph in sender.get().split(" "):
			if glyph not in Glyphs.fonts[self.w.targetFont.selector.get()].glyphs:
				if glyph != "":
					missing.append(glyph)

		self.w.missing.set("Missing in source font: " + ", ".join(missing))
		self.w.missing.show(len(missing) > 0)

		self.w.copyGlyphs.enable(len(missing) == 0)


	# show the macro window
	# copy the selected glyphs from the source font to the target font
	# print a log in the macro window of the process

	def copy_glyphs(self, sender):
		Glyphs.showMacroWindow()
		source_font = Glyphs.fonts[self.w.sourceFont.selector.get()]
		target_font = Glyphs.fonts[self.w.targetFont.selector.get()]
		glyphs = self.w.glyphs.text.get().split(" ")
		overwrite = self.w.overwrite.get()
		print("Copying glyphs from %s to %s:" % (source_font.familyName, target_font.familyName))
		for glyph in source_font.glyphs:
			if glyph.name in glyphs:
				if not overwrite:
					if glyph.name in target_font.glyphs:
						continue
					print("%s: %s" % (glyph.name, "glyph already exists in target font"))
					target_font.glyphs.append(glyph.copy())
				else:
					target_font.glyphs[glyph.name] = glyph.copy()
					print(glyph)
		print("...Done.")


CopyGlyphs()
