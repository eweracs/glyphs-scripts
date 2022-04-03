# MenuTitle: Create Variable Subset File
# -*- coding: utf-8 -*-

__doc__ = """
Creates a file to export a subset variable font.
"""

import vanilla
import os
import itertools


class CreateSubset:
	def __init__(self):
		if Font is None:
			Message("No font selected", "Select a font project!")
			return

		self.font = Font

		self.preferred_directory = Glyphs.defaults["com.eweracs.subsetVariableFont.saveLocation"] or None

		self.axisRanges = {axis.name: sorted(set(master.axes[i] for master in self.font.masters))
		                   for i, axis in enumerate(self.font.axes)}

		for axis in self.axisRanges:
			del self.axisRanges[axis][1:-1]

		self.variable_font_origin_master = self.font.masters[0]
		for master in self.font.masters:
			if master.id == self.font.customParameters["Variable Font Origin"]:
				self.variable_font_origin_master = master

		self.subsetValues = {}

		self.w = vanilla.FloatingWindow((1, 1), "Create Variable Subset File", maxSize=(400, 1200))

		self.w.newName = vanilla.Group("auto")
		self.w.newName.title = vanilla.TextBox("auto", "Family name", sizeStyle="small")
		self.w.newName.entry = vanilla.EditText("auto", text=self.font.familyName, sizeStyle="small")
		self.w.divider = vanilla.HorizontalLine("auto")

		self.w.axisTitles = vanilla.Group("auto")
		self.w.axisTitles.title = vanilla.Group("auto")
		self.w.axisTitles.min = vanilla.TextBox("auto", "Min", alignment="center", sizeStyle="small")
		self.w.axisTitles.max = vanilla.TextBox("auto", "Max", alignment="center", sizeStyle="small")
		self.w.axisTitles.separator = vanilla.Group("auto")
		self.w.axisTitles.bracketleft = vanilla.Group("auto")
		self.w.axisTitles.default = vanilla.TextBox("auto", "Default", alignment="center", sizeStyle="small")
		self.w.axisTitles.bracketright = vanilla.Group("auto")
		self.w.axisTitles.reset = vanilla.Group("auto")

		for i, axis in enumerate(self.font.axes):
			axis_group = vanilla.Group("auto")

			axis_group.title = vanilla.TextBox("auto", axis.name, sizeStyle="small")
			axis_group.min = vanilla.EditText("auto", text=self.axisRanges[axis.name][0], sizeStyle="small",
			                             callback=self.define_axis_ranges)
			axis_group.max = vanilla.EditText("auto", text=self.axisRanges[axis.name][1], sizeStyle="small",
			                           callback=self.define_axis_ranges)
			axis_group.separator = vanilla.TextBox("auto", ":", alignment="center")
			axis_group.bracketleft = vanilla.TextBox("auto", "[", alignment="center")
			axis_group.default = vanilla.EditText("auto",
			                                text=self.variable_font_origin_master.axes[i], sizeStyle="small",
			                                callback=self.define_axis_ranges)
			axis_group.bracketright = vanilla.TextBox("auto", "]", alignment="center")
			axis_group.reset = vanilla.SquareButton("auto", u"↺", sizeStyle="small",
			                              callback=self.reset_value)

			setattr(self.w, axis.axisTag, axis_group)

			self.subsetValues[axis.name] = [int(axis_group.min.get()),
			                                int(axis_group.max.get()),
			                                int(axis_group.default.get())]

		self.w.removeName = vanilla.Group("auto")
		self.w.removeName.title = vanilla.TextBox("auto", "Remove in instance names:", sizeStyle="small")
		self.w.removeName.entry = vanilla.EditText("auto", sizeStyle="small")

		self.w.addRecipeButton = vanilla.Button("auto", "Add recipe", callback=self.add_recipe)
		self.w.recipeHelp = vanilla.HelpButton("auto", callback=self.recipe_help)
		self.w.enterRecipe = vanilla.TextEditor("auto", callback=self.edit_recipes)
		self.w.locationPicker = vanilla.Group("auto")
		self.w.locationPicker.title = vanilla.TextBox("auto", "Save files in:", sizeStyle="small")
		self.w.locationPicker.entry = vanilla.PopUpButton("auto", ["Current file directory", "Choose..."],
		                                                  sizeStyle="small",
		                                                  callback = self.file_chooser)
		self.w.makeButton = vanilla.Button("auto", "Bake recipe", callback=self.make_subset_file)
		self.w.makeButton.enable(len(self.w.enterRecipe.get()) > 0)

		rules = [
			"H:|-border-[" + axis.axisTag + "]-border-|"for axis in self.font.axes
		]

		rules += [
			"H:|-border-[newName]-border-|",
			"H:|-border-[divider]-border-|",
			"H:|-border-[axisTitles]-border-|",
			"H:|-border-[removeName]-border-|",
			"H:|-border-[addRecipeButton(90)]-margin-[recipeHelp]",
			"H:|-border-[enterRecipe]-border-|",
			"H:|-border-[locationPicker]-border-|",
			"H:|-border-[makeButton]-border-|",
			"V:|-border-[newName]-margin-[divider]-[axisTitles]-["
			+ "]-small-[".join([axis.axisTag for axis in self.font.axes]) +
			"]-margin-[removeName]-margin-[addRecipeButton]-margin-[enterRecipe(>=120)]-margin-[locationPicker]-margin-"
			"[makeButton]-border-|",
			"V:[removeName]-[recipeHelp]-[enterRecipe]"
		]

		axis_group_rules = [
			"H:|[title(40)]-[min(>=48)][separator(8)][max(==min)][bracketleft(8)][default(==min)][bracketright(8)]["
			"reset(20)]|",

			"V:|-2-[title]-2-|",
			"V:|[min]|",
			"V:|[max]|",
			"V:|[separator]|",
			"V:|[bracketleft]|",
			"V:|[default]|",
			"V:|[bracketright]|",
			"V:|[reset]|"
		]

		new_name_rules = [
			"H:|[title]-margin-[entry]|",
			"V:|[entry]|"
		]

		metrics = {
			"border": 10,
			"margin": 10,
			"small": 6
		}

		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.newName.addAutoPosSizeRules(new_name_rules, metrics)
		self.w.removeName.addAutoPosSizeRules(new_name_rules, metrics)
		self.w.axisTitles.addAutoPosSizeRules(axis_group_rules, metrics)
		self.w.locationPicker.addAutoPosSizeRules(new_name_rules, metrics)
		for axis in self.font.axes:
			getattr(self.w, axis.axisTag).addAutoPosSizeRules(axis_group_rules, metrics)

		self.w.setDefaultButton(self.w.makeButton)
		self.w.open()
		self.w.makeKey()
		self.w.bind("close", self.write_prefences)

	def add_recipe(self, sender):
		recipe_text = self.w.newName.entry.get() + "\n"
		for axis in self.font.axes:
			recipe_text += str(self.subsetValues[axis.name][0]) + ":" \
			               + str(self.subsetValues[axis.name][1]) + "[" \
			               + str(self.subsetValues[axis.name][2]) + "]" \
			               + "\n"
		remove_entry = self.w.removeName.entry.get()
		if remove_entry == "":
			remove_entry = "-"
		recipe_text += remove_entry + "\n\n"
		self.w.enterRecipe.set(self.w.enterRecipe.get() + recipe_text)
		self.w.makeButton.enable(len(self.w.enterRecipe.get()) > 0)

	def recipe_help(self, sender):
		self.helpView = vanilla.Popover((1, 1))
		self.helpView.description = vanilla.TextBox("auto", "Recipe structure:\n\n"
		                                                    "New family name\n"
		                                                    "min : max [ default ] for each axis\n"
		                                                    "Particle to remove in instance names\n"
		                                                    "(write \"-\" for none)\n\n"
		                                                    "Leave blank line before new file")

		rules = [
			"H:|-border-[description]-border-|",
			"V:|-border-[description]-border-|"
		]

		metrics= {
			"border": 10
		}

		self.helpView.addAutoPosSizeRules(rules, metrics)
		self.helpView.open(parentView=self.w.recipeHelp, preferredEdge="right")

	def edit_recipes(self, sender):
		self.w.makeButton.enable(len(sender.get()) > 0)

	def define_axis_ranges(self, sender):
		if not sender.get().isnumeric() or len(sender.get()) == 0:
			return
		for axis in self.font.axes:
			self.subsetValues[axis.name] = [int(getattr(self.w, axis.axisTag).min.get() or 0),
			                                int(getattr(self.w, axis.axisTag).max.get() or 0),
			                                int(getattr(self.w, axis.axisTag).default.get() or 0)]

	def reset_value(self, sender):
		for i, axis in enumerate(Font.axes):
			if sender is getattr(self.w, axis.axisTag + "Button"):
				getattr(self.w, axis.axisTag + "Min").set(self.axisRanges[axis.name][0])
				getattr(self.w, axis.axisTag + "Max").set(self.axisRanges[axis.name][1])
				getattr(self.w, axis.axisTag + "Default").set(self.variable_font_origin_master.axes[i])

	def file_chooser(self, sender):
		if sender.getItem() == "Choose...":
			self.preferred_directory = GetFolder()
			if not self.preferred_directory:
				sender.setItem("Current file directory")
				return
			items = [
				"📁 " + self.preferred_directory.split("/")[-1],
				"Current file directory",
				"Choose..."
			]
			sender.setItems(items)
			print(self.preferred_directory)
		if sender.getItem() == "Current file directory":
			self.preferred_directory = self.font.filepath.replace("/" + self.font.filepath.split("/")[-1], "")
			print(self.preferred_directory)

		self.write_prefences(None)

	def master_manager(self, subset_values, family_name):
		current_font = Glyphs.currentDocument.font
		current_font.disableUpdateInterface()

		# Calculate necessary extremes and intermediates
		axes_ranges = [[subset_values[axis][0], subset_values[axis][1]] for axis in subset_values]
		for i, axis in enumerate(axes_ranges):
			for master in current_font.masters:
				if master.axes[i] > axes_ranges[i][0] and master.axes[i] < axes_ranges[i][1]:
					if master.axes[i] in axes_ranges[i]:
						continue
					axes_ranges[i].append(master.axes[i])

		necessary_extremes = list(itertools.product(*axes_ranges))
		missing_extremes = []
		for extreme in necessary_extremes:
			if extreme not in [master.axes for master in current_font.masters]:
				if extreme not in missing_extremes:
					missing_extremes.append(extreme)
					print("Adding missing extreme master:", extreme)

		# Add missing extreme masters
		for extreme in missing_extremes:
			extreme_instance = GSInstance()
			extreme_instance.name = "Extreme" + str(extreme)
			current_font.instances.append(extreme_instance)
			current_font.instances[-1].axes = extreme
			current_font.instances[-1].addAsMaster()
			current_font.instances.remove(current_font.instances[-1])
			current_font.masters[-1].axes = extreme

		for instance in current_font.instances:
			if instance.name == "Extreme":
				current_font.instances.remove(instance)

		# Find/add missing origin master
		try:
			for master in current_font.masters:
				match_count = 0
				for i, axis in enumerate(subset_values):
					if master.axes[i] == subset_values[axis][2]:
						match_count += 1
				if match_count == len(current_font.axes):
					origin_master = master
			print("Origin exists:", origin_master)
			current_font.customParameters["Variable Font Origin"] = origin_master.id

		except:
			origin_instance = GSInstance()
			origin_instance.name = "Variable Font Origin"
			current_font.instances.append(origin_instance)
			current_font.instances[-1].axes = [subset_values[axis][2] for axis in subset_values]
			current_font.instances[-1].addAsMaster()
			current_font.masters[-1].axes = [subset_values[axis][2] for axis in subset_values]
			current_font.customParameters["Variable Font Origin"] = current_font.masters[-1].id
			print("New origin master:", current_font.masters[-1])
			for instance in current_font.instances:
				if instance.name == "Variable Font Origin":
					current_font.instances.remove(instance)

		# Remove unnecessary masters
		remove_list = []
		for master in current_font.masters:
			for i, axis in enumerate(current_font.axes):
				if master.axes[i] < subset_values[axis.name][0] or master.axes[i] > subset_values[axis.name][1]:
					remove_list.append(master)

		for master in remove_list:
			current_font.masters.remove(master)

		# Remove unused instances
		remove_list = []
		for instance in current_font.instances:
			if instance.type == 1:
				continue
			for i, axis in enumerate(current_font.axes):
				if instance.axes[i] < subset_values[axis.name][0] or instance.axes[i] > subset_values[axis.name][1]:
					remove_list.append(instance)
		for instance in remove_list:
			current_font.instances.remove(instance)

		for instance in current_font.instances:
			if instance.type:
				for fontInfo in instance.properties:
					if fontInfo.key == "familyNames":
						for value in fontInfo.values:
							if value.languageTag == "dflt":
								value.value = family_name
				if "Desktop" in instance.customParameters["fileName"]:
					suffix = "Desktop"
				if "Web" in instance.customParameters["fileName"]:
					suffix = "Web"
				instance.customParameters["fileName"] = family_name.replace(" ", "-")
				try:
					if suffix:
						instance.customParameters["fileName"] = instance.customParameters["fileName"] + "-" + suffix
				except:
					pass

		current_font.enableUpdateInterface()

	def fix_special_layers(self):
		Glyphs.currentDocument.font.disableUpdateInterface()
		Glyphs.showMacroWindow()

		for glyph in Glyphs.currentDocument.font.glyphs:
			remove_layers = []
			for layer in glyph.layers:
				if layer.isSpecialLayer:
					for i, axis in enumerate(layer.attributes["axisRules"]):
						axis_range = sorted(set([master.axes[i] for master in Glyphs.currentDocument.font.masters]))
						if layer.attributes["axisRules"][axis]["max"] > axis_range[-1]:
							remove_layers.append(layer)
			for layer in remove_layers:
				glyph.layers.remove(layer)

		for glyph in Glyphs.currentDocument.font.glyphs:
			if glyph.mastersCompatible:
				continue
			print("Fixing special layers:", glyph.name)
			backup_glyph = glyph.duplicate(name=glyph.name + ".specialLayers")
			for layer in backup_glyph.layers:
				if layer.isSpecialLayer:
					copy_layer = layer.copy()
					del copy_layer.attributes["axisRules"]
					backup_glyph.layers[layer.associatedMasterId] = copy_layer
			for layer in backup_glyph.layers:
				if layer.name == "Variable Font Origin" or "Extreme" in layer.name:
					layer.reinterpolate()
					final_layer = layer
					final_layer.attributes["axisRules"] = glyph.layers[-1].attributes["axisRules"]
			glyph.layers.append(final_layer.copy())
			del Glyphs.currentDocument.font.glyphs[glyph.name + ".specialLayers"]
		Glyphs.currentDocument.font.enableUpdateInterface()

	def remove_axes(self, family_name):

		# Remove unused axes
		current_font = Glyphs.currentDocument.font
		axisranges = [[] for a in current_font.axes]
		for i, axis in enumerate(current_font.axes):
			for master in current_font.masters:
				if master.axes[i] in axisranges[i]:
					continue
				axisranges[i].append(master.axes[i])

		remove_axes = []
		remove_master_parameters = {master: [] for master in current_font.masters}
		for i, axis in enumerate(axisranges):
			if len(axisranges[i]) == 1:
				for glyph in Glyphs.currentDocument.font.glyphs:
					remove_layers = []
					for layer in glyph.layers:
						if not layer.attributes:
							continue
						try:
							if layer.attributes["axisRules"]["a0" + str(i + 1)]:
								del layer.attributes["axisRules"]["a0" + str(i + 1)]
							if len(layer.attributes["axisRules"]) == 0:
								del layer.attributes["axisRules"]
						except Exception as e:
							print(e, family_name)
					for layer in remove_layers:
						glyph.layers.remove(layer)

				for master in current_font.masters:
					remove_master_parameters[master].append(master.customParameters["Axis Location"][i])

				remove_axes.append(current_font.axes[i])

		for axis in remove_axes:
			print("Removing unused axis:", axis)
			current_font.axes.remove(axis)

		for master in remove_master_parameters:
			print("Master:", master.name)
			for i, parameter in enumerate(remove_master_parameters[master]):
				print("Removing Axis Location parameter for axis:", parameter["Axis"])
				master.customParameters["Axis Location"].remove(parameter)

	def remove_in_instance_names(self, name):
		if name == "-":
			name = ""
		for instance in Glyphs.currentDocument.font.instances:
			if instance.type:
				continue
			instance.name = instance.name.replace(name, "")
			if instance.name.replace(" ", "") == name.replace(" ", "") or instance.name == "":
				instance.name = "Regular"
			if instance.name[0] == " ":
				instance.name = instance.name[1::]

	def make_subset_file(self, sender):
		original_font_file_path = self.font.filepath

		for recipe in self.w.enterRecipe.get().split("\n\n"):
			if recipe == "":
				continue
			family_name = recipe.split("\n")[0]
			replace_name = recipe.split("\n")[len(recipe.split("\n")) - 1]
			subset_values = {}
			for i, line in enumerate(recipe.split("\n")[1:len(recipe.split("\n")) - 1]):
				subset_values[self.font.axes[i].name] = [int(line.split(":")[0]), int(line.split(":")[1].split("[")[0]),
				                                         int(line.split("[")[1].replace("]", ""))]

			print("\nNew family name:", family_name)

			self.master_manager(subset_values, family_name)

			filename = self.preferred_directory + "/" + family_name + ".glyphs"
			print("Writing file to:", filename)
			# NS_url = NSURL.fileURLWithPath_(filename)
			# Glyphs.currentDocument.font.saveToURL_type_error_(NS_url, 1, None)
			Glyphs.currentDocument.font.save(
				path=filename)
			Glyphs.currentDocument.font.save()

			self.fix_special_layers()
			self.remove_axes(family_name)
			self.remove_in_instance_names(replace_name)

			Glyphs.currentDocument.font.save()
			Glyphs.currentDocument.font.close()
			Glyphs.open(original_font_file_path)
			Glyphs.currentDocument.font.save()

		self.w.close()

		self.e = vanilla.FloatingWindow((1, 1))
		self.e.exportSubsets = vanilla.Button("auto", "Export subset files", callback=self.export_subset_TTFs)

		rules = [
			"H:|-border-[exportSubsets]-border-|",
			"V:|-border-[exportSubsets]-border-|"
		]

		metrics = {
			"border": 10
		}

		self.e.addAutoPosSizeRules(rules, metrics)

		self.e.open()
		self.e.makeKey()

	def export_subset_TTFs(self, sender):
		Glyphs.currentDocument.font.disableUpdateInterface()
		for filename in os.listdir(self.preferred_directory):
			if ".glyphs" not in filename:
				continue
			Glyphs.open(self.preferred_directory + "/" + filename)
			for instance in Glyphs.currentDocument.font.instances:
				if instance.type == 1:
					instance.generate(Format=VARIABLE,
					                  FontPath="/Users/sebastiancarewe/Repositories/"
					                           "optimo-Futurista/OTVAR/TT/filename")
			Glyphs.currentDocument.font.close()
		Glyphs.currentDocument.font.enableUpdateInterface()
		self.e.close()

	def write_prefences(self, sender):
		Glyphs.defaults["com.eweracs.subsetVariableFont.saveLocation"] = self.preferred_directory


CreateSubset()
