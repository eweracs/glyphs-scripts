# MenuTitle: Copy Zero Models to Derivatives
# -*- coding: utf-8 -*-

__doc__ = """
Copies Kern On zero models from UC to SC and numbers to small figures.
"""

# TODO: Select groups

import vanilla


class CopyModels:
	def __init__(self):
		if Font is None:
			Message("No font selected", "Select a font project!")
			return

		self.font = Font

		self.smallNums = [number for number in self.font.glyphs if number.case == 4]

		self.prefs = {}

		if Glyphs.defaults["com.eweracs.CopyKOtoSC.prefs"]:
			for key in Glyphs.defaults["com.eweracs.CopyKOtoSC.prefs"]:
				self.prefs[key] = Glyphs.defaults["com.eweracs.CopyKOtoSC.prefs"][key]
		else:
			self.prefs = {
				"allMasters": 1,
				"UCtoSC": 1,
				"numToSmallFigures": 0
			}

		self.allMasters = self.prefs["allMasters"]
		self.UCtoSC = self.prefs["UCtoSC"]
		self.numToSmallFigures = self.prefs["numToSmallFigures"]

		try:
			self.master_cap_kern_values = {master: int(self.font.kerning[master.id][self.font.glyphs["H"].id][
				                                           self.font.glyphs["H"].id]) for master in self.font.masters}
		except Exception as e:
			print(e)
			self.master_cap_kern_values = {master: 0 for master in self.font.masters}

		self.w = vanilla.FloatingWindow((0, 0), "Copy zero models", minSize=(210, len(self.font.masters) * 28 + 247),
		                                maxSize=(300, len(self.font.masters) * 28 + 247))

		self.ypos = 10

		self.w.UCtoSC = vanilla.CheckBox((10, self.ypos, -10, 18), "Uppercase to smallcaps", sizeStyle="small",
		                                 value=self.UCtoSC, callback=self.select_uc_to_sc)

		self.ypos += 22

		self.w.numToSmallFigures = vanilla.CheckBox((10, self.ypos, -10, 18), "Numbers to small figures",
		                                         sizeStyle="small", value=self.numToSmallFigures,
		                                         callback=self.select_num_to_small_figures)

		self.ypos += 26

		self.w.divider = vanilla.HorizontalLine((10, self.ypos, -10, 1))

		self.ypos += 10

		self.w.capitalKerningTitle = vanilla.TextBox((10, self.ypos, -10, 14), "Uppercase base kerning (H H):",
		                                             sizeStyle="small")
		self.w.capitalKerningHelp = vanilla.HelpButton((180, self.ypos - 2, 21, 20))
		self.w.capitalKerningHelp.getNSButton().setToolTip_(
			"The amount of kerning you might have set as the standard capital spacing. "
			"Is read from the model HH, if it exists.")

		self.ypos += 28

		for i, master in enumerate(self.font.masters):
			try:
				master_cap_kern = int(self.font.kerningForPair(master.id, "H", "H"))
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

		self.w.numberTitle = vanilla.TextBox((10, self.ypos, -10, 14), "Copy from numbers:", sizeStyle="small")

		self.ypos += 26

		self.w.defaultNumberSelector = vanilla.PopUpButton((10, self.ypos, -10, 17), ["Default",
		                                                                              "Lining", "Oldstyle"])

		self.ypos += 30

		self.w.numberTargetTitle = vanilla.TextBox((10, self.ypos, -10, 14), "To small figure base set:",
		sizeStyle="small")

		self.ypos += 26

		self.w.targetNumberSelector = vanilla.PopUpButton((10, self.ypos, -10, 17),
		                                                  [".dnom", "inferior", ".numr", "superior"])

		self.ypos += 30

		self.w.dividerThree = vanilla.HorizontalLine((10, self.ypos, -10, 1))

		self.ypos += 10

		self.w.allMasters = vanilla.CheckBox((10, self.ypos, -10, 18), "Apply to all masters", sizeStyle="small",
		                                     value=self.allMasters)

		self.w.copyModelsButton = vanilla.Button((10, -30, -10, 20), "Copy zero models", callback=self.copy_models)

		self.ypos += 56

		for i, master in enumerate(self.font.masters):
			getattr(self.w, "kern" + str(i)).enable(self.w.UCtoSC.get())
		self.w.defaultNumberSelector.enable(self.w.numToSmallFigures.get())
		self.w.copyModelsButton.enable(self.w.UCtoSC.get() + self.w.numToSmallFigures.get() != 0)

		self.w.setDefaultButton(self.w.copyModelsButton)

		self.w.resize(210, self.ypos)
		self.w.open()
		self.w.makeKey()

	def select_uc_to_sc(self, sender):
		for i, master in enumerate(self.font.masters):
			getattr(self.w, "kern" + str(i)).enable(sender.get())
		self.w.copyModelsButton.enable(self.w.UCtoSC.get() + self.w.numToSmallFigures.get() != 0)
		self.write_prefs()

	def select_num_to_small_figures(self, sender):
		self.w.defaultNumberSelector.enable(sender.get())
		self.w.copyModelsButton.enable(self.w.UCtoSC.get() + self.w.numToSmallFigures.get() != 0)
		self.write_prefs()

	def set_master_cap_kern(self, sender):
		for i, master in enumerate(self.font.masters):
			if getattr(self.w, "kern" + str(i)) is sender:
				self.master_cap_kern_values[self.font.masters[i]] = sender.get()

	def copy_models(self, sender):

		self.w.close()

		global_copied_models_counter = 0
		for master in self.font.masters:

			if self.w.allMasters.get() == 0 and master is not self.font.selectedFontMaster:
				continue

			if not master.userData["KernOnIsInterpolated"] and master.userData["KernOnModels"] is None:
				Message("No models found", "Please create some models in order to copy them.")
				return

			copied_models = ""
			copied_models_counter = 0

			for model in master.userData["KernOnModels"]:
				left_glyph = model.split(" ")[0]
				right_glyph = model.split(" ")[1]

				if self.w.UCtoSC.get():
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

				if self.w.numToSmallFigures:
					if self.font.glyphs[left_glyph].case == self.w.defaultNumberSelector.get() \
							and self.font.glyphs[right_glyph].case == self.w.defaultNumberSelector.get() \
							and self.font.glyphs[left_glyph].category == "Number" \
							and self.font.glyphs[right_glyph].category == "Number" \
							and self.font.kerning[master.id][
						self.font.glyphs[left_glyph].id][self.font.glyphs[right_glyph].id] == 0:

						# if both glyphs of current pair are numbers of the selected case, and base models

						print(model)

						suffix = [".dnom", "inferior", ".numr", "superior"][self.w.targetNumberSelector.get()]
						num_model = left_glyph.split(".")[0] + suffix + " " + right_glyph.split(".")[0] + suffix
						if num_model not in master.userData["KernOnModels"]:
							master.userData["KernOnModels"].append(num_model)
							self.font.setKerningForPair(master.id, num_model.split(" ")[0],
						 	                            num_model.split(" ")[1], 0)
							copied_models += num_model + "\n"
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

		self.write_prefs()

	def write_prefs(self):
		self.prefs["allMasters"] = self.w.allMasters.get()
		self.prefs["UCtoSC"] = self.w.UCtoSC.get()
		self.prefs["numToSmallFigures"] = self.w.numToSmallFigures.get()
		Glyphs.defaults["com.eweracs.CopyKOtoSC.prefs"] = self.prefs


CopyModels()
