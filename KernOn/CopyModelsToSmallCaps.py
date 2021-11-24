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

		try:
			self.master_cap_kern_values = {master: int(self.font.kerning[master.id][self.font.glyphs["H"].id][
				                                           self.font.glyphs["H"].id]) for master in self.font.masters}
		except Exception as e:
			print(e)
			self.master_cap_kern_values = {master: 0 for master in self.font.masters}

		self.w = vanilla.FloatingWindow((0, 0), "Copy KO models", minSize=(170, len(self.font.masters) * 28 + 170),
		                                maxSize=(300, len(self.font.masters) * 28 + 170))

		self.ypos = 10

		self.w.UCtoSC = vanilla.CheckBox((10, self.ypos, -10, 18), "Uppercase to smallcaps", sizeStyle="small", value=1)
		# value=self.allMasters, callback=self.select_UC_to_SC)

		self.ypos += 22

		self.w.numToSmallNums = vanilla.CheckBox((10, self.ypos, -10, 18), "Numbers to small figures",
		                                         sizeStyle="small", value=0)
		# value=self.allMasters, callback=self.select_num_to_small_figures)

		self.w.UCtoSC.enable(False)
		self.w.numToSmallNums.enable(False)

		self.ypos += 26

		self.w.divider = vanilla.HorizontalLine((10, self.ypos, -10, 1))

		self.ypos += 10

		self.w.capitalKerningTitle = vanilla.TextBox((10, self.ypos, -10, 14), "Capital base kerning (H H):",
		                                             sizeStyle="small")

		self.ypos += 20

		for i, master in enumerate(self.font.masters):
			try:
				master_cap_kern = int(self.font.kerning[master.id][self.font.glyphs["H"].id][self.font.glyphs["H"].id])
			except:
				master_cap_kern = 0
			setattr(self.w, "master" + str(i),
			        vanilla.TextBox((10, self.ypos, -80, 17), str(i + 1) + ": " + master.name,
			                        sizeStyle="regular"))
			setattr(self.w, "kern" + str(i), vanilla.EditText((-60, self.ypos - 1, -10, 22), text=str(
				master_cap_kern), callback=self.set_master_cap_kern))

			if master.userData["KernOnIsInterpolated"]:
				getattr(self.w, "master" + str(i)).enable(0)
				getattr(self.w, "kern" + str(i)).show(0)
				setattr(self.w, "interpolate" + str(i), vanilla.TextBox((10, self.ypos + 1, -10, 14), "Interpolated",
				                                                        alignment="right",
				                                                        sizeStyle="small"))

			self.master_cap_kern_values[master] = master_cap_kern
			self.ypos += 28

		self.w.dividerTwo = vanilla.HorizontalLine((10, self.ypos + 2, -10, 1))

		self.ypos += 10

		self.w.allMasters = vanilla.CheckBox((10, self.ypos, -10, 18), "Apply to all masters", sizeStyle="small",
		                                     value=self.allMasters, callback=self.select_all_masters)

		self.w.copyModelsButton = vanilla.Button((10, -30, -10, 20), "Copy zero models", callback=self.copy_models)

		self.ypos += 56

		self.w.setDefaultButton(self.w.copyModelsButton)

		self.w.resize(200, self.ypos)
		self.w.open()
		self.w.makeKey()

	def select_all_masters(self, sender):
		self.allMasters = sender.get()
		self.write_prefs()

	def set_master_cap_kern(self, sender):
		for i, master in enumerate(self.font.masters):
			if getattr(self.w, "kern" + str(i)) is sender:
				self.master_cap_kern_values[self.font.masters[i]] = sender.get()

	def copy_models(self, sender):

		self.w.close()

		global_copied_models_counter = 0
		for master in self.font.masters:

			if self.allMasters == 0 and master is not self.font.selectedFontMaster:
				continue

			if not master.userData["KernOnIsInterpolated"] and master.userData["KernOnModels"] is None:
				Message("No models found", "Please create some models in order to copy them.")
				return

			copied_models = ""
			copied_models_counter = 0

			for model in master.userData["KernOnModels"]:
				left_glyph = model.split(" ")[0]
				right_glyph = model.split(" ")[1]

				if self.font.glyphs[left_glyph.lower() + ".sc"] \
						and self.font.glyphs[right_glyph.lower() + ".sc"] \
						and self.font.glyphs[left_glyph].case == 1 \
						and self.font.glyphs[right_glyph].case == 1 \
						and self.font.glyphs[left_glyph].category == "Letter" \
						and self.font.glyphs[right_glyph].category == "Letter" \
						and self.master_cap_kern_values[master] == self.font.kerning[master.id][self.font.glyphs[
					left_glyph].id][self.font.glyphs[right_glyph].id]:

					# if both glyphs of current pair are uppercase letters, present as smallcaps, and base models

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
		Glyphs.defaults["com.eweracs.CopyKOtoSC.prefs"] = self.prefs


CopyModels()
