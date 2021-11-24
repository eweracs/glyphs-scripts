# MenuTitle: Copy zero models to small caps
# -*- coding: utf-8 -*-

__doc__ = """
Copies Kern On zero models from uppercase to smallcaps.
"""

# TODO: Select groups

import vanilla


class CopyModels:
	def __init__(self):
		if Font is None:
			Message("No font selected", "Select a font project!")
			return

		self.font = Font

		self.prefs = {}

		if Glyphs.defaults["com.eweracs.CopyKOtoSC.prefs"]:
			for key in Glyphs.defaults["com.eweracs.CopyKOtoSC.prefs"]:
				self.prefs[key] = Glyphs.defaults["com.eweracs.CopyKOtoSC.prefs"][key]
		else:
			self.prefs = {
				"allMasters": 1,
				# "UCtoSC": 1,
				# "numToSmallFigures": 0
			}

		self.allMasters = self.prefs["allMasters"]
		# self.allMasters = self.prefs["UCtoSC"]
		# self.allMasters = self.prefs["numToSmallFigures"]

		self.w = vanilla.FloatingWindow((0, 0), "Copy KO models")

		self.w.UCtoSC = vanilla.CheckBox((10, 10, -10, 18), "Uppercase to smallcaps", sizeStyle="small", value=1)
		# value=self.allMasters, callback=self.select_UC_to_SC)

		self.w.numToSmallNums = vanilla.CheckBox((10, 32, -10, 18), "Numbers to small figures", sizeStyle="small",
		                                         value=0)
		# value=self.allMasters, callback=self.select_num_to_small_figures)

		self.w.UCtoSC.enable(False)
		self.w.numToSmallNums.enable(False)

		self.w.divider = vanilla.HorizontalLine((10, 60, -10, 1))

		self.w.allMasters = vanilla.CheckBox((10, 70, -10, 18), "Apply to all masters", sizeStyle="small",
		                                     value=self.allMasters, callback=self.select_all_masters)
		self.w.copyModelsButton = vanilla.Button((10, -30, -10, 20), "Copy models", callback=self.copy_models)

		self.w.resize(174, 128)
		self.w.open()
		self.w.makeKey()

	def select_all_masters(self, sender):
		self.allMasters = sender.get()
		self.write_prefs()

	def copy_models(self, sender):
		global_copied_models_counter = 0
		for master in self.font.masters:
			if master.userData["KernOnModels"] is None:
				Message("No models found", "Please create some models in order to copy them.")
				return
			copied_models = ""
			copied_models_counter = 0
			for model in master.userData["KernOnModels"]:
				left_glyph = model.split(" ")[0]
				right_glyph = model.split(" ")[1]
				if self.font.glyphs[left_glyph].case == 1 and self.font.glyphs[right_glyph].case == 1:
					sc_model = left_glyph.lower() + ".sc " + right_glyph.lower() + ".sc"
					if sc_model not in master.userData["KernOnModels"]:
						master.userData["KernOnModels"].append(sc_model)
						self.font.setKerningForPair(master.id, left_glyph.lower() + ".sc",
						                            right_glyph.lower() + ".sc", 0)
						copied_models += sc_model + "\n"
						copied_models_counter += 1
			if copied_models_counter > 0:
				print("Copied", copied_models_counter, "model(s) for master", master.name, ":\n", copied_models)
			global_copied_models_counter += copied_models_counter

		if global_copied_models_counter > 0:
			Glyphs.showNotification(title="Models copied",
			                        message="Copied " + str(global_copied_models_counter)
			                                + " models. Detailed report in Macro window.")
		else:
			Glyphs.showNotification(title="No models copied",
			                        message="All models already present.")

	def write_prefs(self):
		self.prefs["allMasters"] = self.allMasters
		Glyphs.defaults["com.eweracs.KOmodels.prefs"] = self.prefs


CopyModels()
