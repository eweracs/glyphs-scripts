# MenuTitle: Set base models
# -*- coding: utf-8 -*-

__doc__ = """
Sets base zero models for Kern On.
"""

# TODO:
#  checkbox for smallcaps, small figures
#  overwrite or append models

import vanilla


class Modeller:
	def __init__(self):
		if Font is None:
			Message("No font selected", "Select a font project!")
			return

		self.font = Font

		self.prefs = {}

		self.defaults = [
			"n n",  # LC
			"v n",
			"n o",
			"o n",
			"n a",
			"i n",
			"n u",
			"l n",
			"r n",
			"l H",  # LC/UC
			"H o",
			"H n",
			"H s",
			"H x",
			"H H",
			"H O",
			"H T",
			"H V",
			"E H",
			"one zero",  # numbers
			"one one",
			"one two",
			"one three",
			"one four",
			"one n",  # numbers/LC/UC
			"one H",
			"d exclam",  # LC/spaced-off
			"d colon",
			"one comma",
			"d period",
			"H ampersand",
			"n at",
			"d hyphen",
			"d endash",  # dashes
			"d underscore",
			"endash endash",
			"d quoteright",  # quotes
			"quoteright h",
			"d quoteleft",
			"quoteleft h",
			"guilsinglleft h",
			"d parenleft",  # parens
			"pareneleft h",
			"bracketleft h",
			"h.sc h.sc",  # SC
			"e.sc h.sc",
			"h.sc o.sc",
			"o.sc h.sc",
			"h.sc v.sc",
			"v.sc h.sc",
			"h.sc parenleft.sc",
			"parenleft.sc h.sc",
			"one.sc zero.sc",
			"one.sc one.sc",
			"one.sc two.sc",
			"one.sc three.sc",
			"one.sc four.sc",
			"one.sc comma"
		]

		if Glyphs.defaults["com.eweracs.KOmodels.prefs"]:
			for key in Glyphs.defaults["com.eweracs.KOmodels.prefs"]:
				self.prefs[key] = Glyphs.defaults["com.eweracs.KOmodels.prefs"][key]
		else:
			self.prefs = {
				"allMasters": 1,
				"capitalKerning": 1,
				"modelList": self.defaults
			}

		self.master_capital_kern_values = {master: 0 for master in self.font.masters}

		self.allMasters = self.prefs["allMasters"]
		self.capitalKerning = self.prefs["capitalKerning"]

		self.models = []

		self.build_font_models()

		self.selected_master = self.font.masters[0]

		self.w = vanilla.FloatingWindow((0, 0), "Set base models")

		self.w.modelsTitle = vanilla.TextBox((10, 10, -10, 14), "Model list", sizeStyle="small")
		self.w.editModels = vanilla.TextEditor((10, 32, 145, -40), text="\n".join(self.prefs["modelList"]),
		                                       callback=self.edit_models)
		self.w.resetDefaults = vanilla.Button((10, -32, 145, 20), "Restore defaults",
		                                      callback=self.restore_defaults)
		self.w.addCapitalSpacingCheckBox = vanilla.CheckBox((165, 8, -10, 20), "Add capital kerning",
		                                                    sizeStyle="small", value=self.prefs["capitalKerning"],
		                                                    callback=self.toggle_capital_kerning)

		self.ypos = 34

		for i, master in enumerate(self.font.masters):
			setattr(self.w, "master" + str(i), vanilla.TextBox((165, self.ypos, -60, 17), master.name,
			                                                   sizeStyle="regular"))
			setattr(self.w, "kern" + str(i), vanilla.EditText((-50, self.ypos - 1, -10, 22), text="0",
			                                                  callback=self.set_master_kern_value))
			self.ypos += 28

		self.ypos += 70
		if self.ypos <= 160:
			self.ypos = 160

		self.w.allMasters = vanilla.CheckBox((165, -56, -10, 18), "Apply to all masters", sizeStyle="small",
		                                     value=self.allMasters, callback=self.select_all_masters)
		self.w.setModelsButton = vanilla.Button((165, -32, -10, 20), "Set zero models", callback=self.set_models)

		self.toggle_master_input_fields()
		self.toggle_default_button()

		self.w.setDefaultButton(self.w.setModelsButton)
		self.w.resize(320, self.ypos)
		self.w.open()
		self.w.makeKey()

	def edit_models(self, sender):
		self.prefs["modelList"] = sender.get().splitlines()
		try:
			self.build_font_models()
		except Exception as e:
			print(e)
		self.toggle_default_button()
		self.write_prefs()

	def restore_defaults(self, sender):
		self.w.editModels.set("\n".join(self.defaults))
		self.prefs["modelList"] = self.defaults
		self.w.resetDefaults.enable(False)

	def toggle_capital_kerning(self, sender):
		self.capitalKerning = sender.get()
		self.toggle_master_input_fields()
		self.write_prefs()

	def set_master_kern_value(self, sender):
		for i, master in enumerate(self.font.masters):
			if getattr(self.w, "kern" + str(i)) is sender:
				self.master_capital_kern_values[master] = sender.get()

	def toggle_default_button(self):
		if self.defaults == self.prefs["modelList"]:
			self.w.resetDefaults.enable(False)
		else:
			self.w.resetDefaults.enable(True)

	def toggle_master_input_fields(self):
		for i, master in enumerate(self.font.masters):
			getattr(self.w, "master" + str(i)).enable(self.capitalKerning)
			getattr(self.w, "kern" + str(i)).enable(self.capitalKerning)

	def build_font_models(self):
		self.models = []

		for pair in self.prefs["modelList"]:
			try:
				if pair.split(" ")[0] in self.font.glyphs and pair.split(" ")[1] in self.font.glyphs:
					self.models.append(pair)
			except:
				return

	def select_all_masters(self, sender):
		self.allMasters = sender.get()
		self.write_prefs()

	def set_models(self, sender):
		self.w.close()
		for master in self.font.masters:
			if self.allMasters == 0 and master is not self.font.selectedFontMaster:
				continue
			del master.userData["KernOnModels"]
			master.userData["KernOnModels"] = []
			for model in self.models:
				left_glyph = model.split(" ")[0]
				right_glyph = model.split(" ")[1]
				kern_value = 0
				if self.capitalKerning:
					if self.font.glyphs[left_glyph].case == 1 and self.font.glyphs[right_glyph].case == 1:
						kern_value = int(self.master_capital_kern_values[master])
				master.userData["KernOnModels"].append(model)
				self.font.setKerningForPair(master.id, model.split(" ")[0], model.split(" ")[1], kern_value)

		Glyphs.showNotification(title="Set Kern on base models",
		                        message="Zero models set in " + ["current master", "all masters"][self.allMasters] +
		                                " for " + str(len(self.models)) + " models.")

		self.write_prefs()

	def write_prefs(self):
		self.prefs["allMasters"] = self.allMasters
		self.prefs["capitalKerning"] = self.capitalKerning
		Glyphs.defaults["com.eweracs.KOmodels.prefs"] = self.prefs


Modeller()
