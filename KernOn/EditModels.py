# MenuTitle: Edit Kern On Models in Master
# -*- coding: utf-8 -*-

__doc__ = """
Allows for simplified editing of Kern On models in each master.
"""

from vanilla import *


class EditModels:
	def __init__(self):
		self.font = Font
		if self.font is None:
			Message("Please open a font project!", "No font selected")
			return

		# check whether font has class kerning
		try:
			if "@MMK" in self.font.kerning[self.font.masters[0].id].items()[0][0]:
				Message("This script only works on projects before kerning has been generated.",
				        "Font has class kerning")
				return
		except:
			pass

		# check whether all masters have kern on models
		for master in self.font.masters:
			if "KernOnModels" not in master.userData:
				master.userData["KernOnModels"] = []

		self.currentMaster = self.font.selectedFontMaster

		self.w = FloatingWindow((1, 1), "Edit Kern On Models")

		# add a segmented button: left button has a left arrow, right button has a right arrow

		self.w.master = Group("auto")
		self.w.master.title = TextBox("auto", "Master: " + self.font.selectedFontMaster.name, sizeStyle="small")
		self.w.master.selector = SegmentedButton("auto", [dict(title="←"), dict(title="→")],
		                                         callback=self.master_switcher)

		# add a divider

		self.w.divider = HorizontalLine("auto")

		# make a vanilla group with a combo box with all models in the current master's KernOnModels user data,
		# an editable text field with the model's kerning value and a button to delete the model

		self.w.model = Group("auto")
		self.w.model.title = TextBox("auto", "Model: ", sizeStyle="small")
		self.w.model.selector = ComboBox("auto",
		                                 [model for model in self.font.selectedFontMaster.userData["KernOnModels"]],
		                                 sizeStyle="small",
		                                 callback=self.model_selector)
		self.w.model.value = EditText("auto", sizeStyle="small")
		self.w.model.button = Button("auto", "−", sizeStyle="small", callback=self.delete_model)

		# make a vanilla group with a button to add a new model

		self.w.addModel = Group("auto")
		self.w.addModel.title = TextBox("auto", "Add: ", sizeStyle="small")

		# make a group with two combo boxes, one for the first glyph of the model and one for the second glyph of the model

		self.w.addModel.selector = Group("auto")
		self.w.addModel.selector.first = ComboBox("auto", [glyph.name for glyph in self.font.glyphs],
		                                          sizeStyle="small", callback=self.check_model)
		self.w.addModel.selector.second = ComboBox("auto", [glyph.name for glyph in self.font.glyphs],
		                                           sizeStyle="small", callback=self.check_model)

		self.w.addModel.value = EditText("auto", "0", sizeStyle="small")
		self.w.addModel.button = Button("auto", "+", sizeStyle="small", callback=self.add_model)

		selector_rules = [
			"H:|[first]-margin-[second(==first)]|",
			"V:|[first]|",
			"V:|[second]|",
		]

		model_rules = [
			"H:|[title(36)]-margin-[selector(120)]-margin-[value(>=40)]-margin-[button]|",
			"V:|[selector]|",
			"V:|[title]|",
			"V:|[value]|",
			"V:|[button]|",
		]

		master_rules = [
			"H:|[title]-[selector(70)]|",
			"V:[title]",
			"V:|[selector]|"
		]

		rules = [
			"H:|-border-[master]-border-|",
			"H:|-border-[divider]-border-|",
			"H:|-border-[model]-border-|",
			"H:|-border-[addModel]-border-|",
			"V:|-border-[master]-margin-[divider]-margin-[model]-margin-[addModel]-border-|",
		]

		metrics = {
			"border": 10,
			"margin": 10
		}

		self.set_models_items()
		self.check_model(None)

		self.w.master.addAutoPosSizeRules(master_rules, metrics)
		self.w.model.addAutoPosSizeRules(model_rules, metrics)
		self.w.addModel.addAutoPosSizeRules(model_rules, metrics)
		self.w.addModel.selector.addAutoPosSizeRules(selector_rules, metrics)
		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.open()
		self.w.makeKey()
		self.w.bind("close", self.window_close)

		Glyphs.addCallback(self.ui_update, UPDATEINTERFACE)

	def master_switcher(self, sender):
		if sender.get() == 1:
			self.font.masterIndex += 1
		else:
			self.font.masterIndex -= 1

	def delete_model(self, sender):
		self.font.removeKerningForPair(self.font.selectedFontMaster.id,
		                               self.w.model.selector.get().split(" ")[0],
		                               self.w.model.selector.get().split(" ")[1])
		self.font.selectedFontMaster.userData["KernOnModels"].remove(self.w.model.selector.get())
		self.set_models_items()

	def set_models_items(self):
		if len(self.font.selectedFontMaster.userData["KernOnModels"]) > 0:
			self.w.model.selector.setItems(self.font.selectedFontMaster.userData["KernOnModels"])
			self.w.model.selector.set(self.font.selectedFontMaster.userData["KernOnModels"][0])
			self.w.model.value.set(self.font.kerningForPair(self.font.selectedFontMaster.id,
			                                                self.w.model.selector.get().split(" ")[0],
			                                                self.w.model.selector.get().split(" ")[1]))
		else:
			self.w.model.selector.setItems(["No models"])
			self.w.model.selector.set("No models")
			self.w.model.selector.enable(False)
			self.w.model.value.set("")
			self.w.model.value.enable(False)
			self.w.model.button.enable(False)

	def edit_model(self, sender):
		if not sender.get().isdigit():
			return
		self.font.setKerningForPair(self.font.selectedFontMaster.id,
		                            self.w.model.selector.get().split(" ")[0],
		                            self.w.model.selector.get().split(" ")[1],
		                            self.w.model.value.get())

	def check_model(self, sender):
		# check whether both glyphs of the model exist in the font
		if self.w.addModel.selector.first.get() in self.font.glyphs \
				and self.w.addModel.selector.second.get() in self.font.glyphs:
			self.w.addModel.button.enable(True)
			self.w.addModel.value.enable(True)
		else:
			self.w.addModel.button.enable(False)
			self.w.addModel.value.enable(False)

	def add_model(self, sender):
		# check whether the model is already in the font
		model = self.w.addModel.selector.first.get() + " " + self.w.addModel.selector.second.get()
		if model in self.font.selectedFontMaster.userData["KernOnModels"]:
			Message("Please select a different model.", "Model already present")
			return
		self.font.selectedFontMaster.userData["KernOnModels"].append(model)
		self.font.setKerningForPair(self.font.selectedFontMaster.id,
		                            self.w.addModel.selector.first.get(),
		                            self.w.addModel.selector.second.get(),
		                            int(self.w.addModel.value.get()))

		self.w.model.selector.setItems(self.font.selectedFontMaster.userData["KernOnModels"])

		self.w.addModel.selector.first.set("")
		self.w.addModel.selector.second.set("")
		self.w.addModel.value.set("0")

		# check if there are kern on models in the current master, if yes, enable the model selector
		if len(self.font.selectedFontMaster.userData["KernOnModels"]) > 0:
			self.w.model.selector.enable(True)
			self.w.model.selector.set(self.font.selectedFontMaster.userData["KernOnModels"][0])
			self.w.model.value.enable(True)
			self.w.model.value.set(self.font.kerningForPair(self.font.selectedFontMaster.id,
			                                                self.w.model.selector.get().split(" ")[0],
			                                                self.w.model.selector.get().split(" ")[1]))
			self.w.model.button.enable(True)

	def model_selector(self, sender):
		try:
			self.w.model.value.set(self.font.kerningForPair(self.font.selectedFontMaster.id,
			                                                self.w.model.selector.get().split(" ")[0],
			                                                self.w.model.selector.get().split(" ")[1]))
		except:
			pass

	def ui_update(self, info):
		if self.currentMaster != self.font.selectedFontMaster:
			self.set_models_items()
		self.currentMaster = self.font.selectedFontMaster

	def window_close(self, sender):
		Glyphs.removeCallback(self.ui_update, UPDATEINTERFACE)

		# remove kern on models user data for each master if no models are left
		for master in self.font.masters:
			if len(master.userData["KernOnModels"]) == 0:
				del master.userData["KernOnModels"]


EditModels()
