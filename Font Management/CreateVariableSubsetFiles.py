# MenuTitle: Create Variable Subset Files
# -*- coding: utf-8 -*-

__doc__ = """
Create glyphs files to export subset variable fonts.
"""

import vanilla
import itertools


class CreateSubsets:
	def __init__(self):

		Message("This script is still heavily experimental, especially for managing special layers. Use at your own "
		        "risk.",
		        "Warning")

		if Font is None:
			Message("No font selected", "Select a font project!")
			return

		self.font = Font

		self.preferred_directory = Glyphs.defaults["com.eweracs.subsetVariableFont.saveLocation"] or None

		self.axisRanges = {axis.name: sorted(set(master.axes[i] for master in self.font.masters))
		                   for i, axis in enumerate(self.font.axes)}

		self.axisIndices = {axisIndex: axis.axisTag for axisIndex, axis in enumerate(self.font.axes)}

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

		if self.preferred_directory:
			items = [
				"📁 " + self.preferred_directory.split("/")[-1],
				"Current file directory",
				"Choose..."
			]
			self.w.locationPicker.entry.setItems(items)

		# read preferences for text field
		self.w.enterRecipe.set(Glyphs.defaults["com.eweracs.subsetVariableFont.recipes"] or "")

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
		self.w.bind("close", self.write_preferences)

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
			if sender is getattr(getattr(self.w, axis.axisTag), "reset"):
				getattr(getattr(self.w, axis.axisTag), "min").set(self.axisRanges[axis.name][0])
				getattr(getattr(self.w, axis.axisTag), "max").set(self.axisRanges[axis.name][1])
				getattr(getattr(self.w, axis.axisTag), "default").set(self.variable_font_origin_master.axes[i])

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
		if sender.getItem() == "Current file directory":
			self.preferred_directory = self.font.filepath.replace("/" + self.font.filepath.split("/")[-1], "")
			print(self.preferred_directory)

		self.write_preferences(None)

	def master_manager(self, subset_values, family_name):
		self.current_font.disableUpdateInterface()

		# Calculate necessary extremes and intermediates
		axes_ranges = [[subset_values[axis][0], subset_values[axis][1]] for axis in subset_values]
		for i, axis in enumerate(axes_ranges):
			for master in self.current_font.masters:
				if axes_ranges[i][0] < master.axes[i] < axes_ranges[i][1]:
					if master.axes[i] in axes_ranges[i]:
						continue
					axes_ranges[i].append(master.axes[i])

		necessary_extremes = list(itertools.product(*axes_ranges))
		missing_extremes = []
		for extreme in necessary_extremes:
			if extreme not in [master.axes for master in self.current_font.masters]:
				if extreme not in missing_extremes:
					missing_extremes.append(extreme)
					print("Adding missing extreme master:", extreme)

		# Add missing extreme masters
		for extreme in missing_extremes:
			extreme_instance = GSInstance()
			extreme_instance.name = "Extreme " + str(extreme)
			self.current_font.instances.append(extreme_instance)
			self.current_font.instances[-1].axes = extreme
			self.current_font.instances[-1].addAsMaster()
			self.current_font.masters[-1].axes = extreme

		# Find/add missing origin master
		try:
			for master in self.current_font.masters:
				match_count = 0
				for i, axis in enumerate(subset_values):
					if master.axes[i] == subset_values[axis][2]:
						match_count += 1
				if match_count == len(self.current_font.axes):
					origin_master = master
			print("Origin exists:", origin_master)
			self.current_font.customParameters["Variable Font Origin"] = origin_master.id

		except:
			origin_instance = GSInstance()
			origin_instance.name = "Variable Font Origin"
			self.current_font.instances.append(origin_instance)
			self.current_font.instances[-1].axes = [subset_values[axis][2] for axis in subset_values]
			self.current_font.instances[-1].addAsMaster()
			self.current_font.masters[-1].axes = [subset_values[axis][2] for axis in subset_values]
			self.current_font.customParameters["Variable Font Origin"] = self.current_font.masters[-1].id
			print("New origin master:", self.current_font.masters[-1])

		# Remove unused instances
		remove_list = []
		for instance in self.current_font.instances:
			if instance.type == 1:
				continue
			for i, axis in enumerate(self.current_font.axes):
				if instance.axes[i] < subset_values[axis.name][0] or instance.axes[i] > subset_values[axis.name][1]:
					remove_list.append(instance)
		for instance in remove_list:
			self.current_font.instances.remove(instance)

		for instance in self.current_font.instances:
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

		self.current_font.enableUpdateInterface()

	def fix_special_layers(self):
		self.current_font.disableUpdateInterface()
		Glyphs.showMacroWindow()

		for glyph in self.current_font.glyphs:
			if glyph.mastersCompatible:
				continue
			print("Fixing layers:", glyph.name + "...")
			duplicate = glyph.duplicate(name=glyph.name + "specialLayers")

			master_layers = [master.id for master in self.current_font.masters]
			for layer in duplicate.layers:
				if not layer.isSpecialLayer:
					continue
				axis_rules = layer.attributes["axisRules"]
				duplicate.layers[layer.associatedMasterId] = layer.copy()
				master_layers.remove(layer.associatedMasterId)
			for id in master_layers:
				duplicate.layers[id].reinterpolate()
				append_layer = duplicate.layers[id]
				append_layer.attributes["axisRules"] = axis_rules
				glyph.layers.append(append_layer)

			del self.current_font.glyphs[glyph.name + "specialLayers"]

		self.current_font.enableUpdateInterface()

	def check_empty_glyphs(self):
		for glyph in self.current_font.glyphs:
			if glyph.mastersCompatible:
				continue
			remove_layers = []
			for layer in glyph.layers:
				if layer.shapes:
					continue
				remove_layers.append(layer)
			for layer in remove_layers:
				glyph.layers.remove(layer)
		self.fix_special_layers()

	def order_special_layers(self, subset_values):
		for glyph in self.current_font.glyphs:
			make_master_layers = False
			delete_special_layers = False
			for layer in glyph.layers:
				if not layer.isSpecialLayer:
					continue
				for i, axis in enumerate(self.current_font.axes):
					try:
						axis_max = subset_values[axis.name][1]
						axis_min = subset_values[axis.name][0]
						layer_attributes_max = layer.attributes["axisRules"]["a0" + str(i + 1)]["max"]
						if axis_min < layer_attributes_max < axis_max:
							continue
						if layer_attributes_max > axis_min:
							make_master_layers = True
						if layer_attributes_max < axis_min:
							delete_special_layers = True

					except:
						pass

				if make_master_layers:  # makes the special layers to master layers
					copy_layer = layer.copy()
					del copy_layer.attributes["axisRules"]
					glyph.layers[layer.associatedMasterId] = copy_layer
					del layer.attributes["axisRules"]

				if delete_special_layers:  # deactivates special layers
					del layer.attributes["axisRules"]

	def remove_unused_masters(self, subset_values):

		# Remove unnecessary masters
		remove_list = []
		for master in self.current_font.masters:
			for i, axis in enumerate(self.current_font.axes):
				if master.axes[i] < subset_values[axis.name][0] or master.axes[i] > subset_values[axis.name][1]:
					remove_list.append(master)

		for master in remove_list:
			self.current_font.masters.remove(master)

	def remove_axes(self):

		# Remove unused axes
		axisranges = [[] for axis in self.current_font.axes]
		for i, axis in enumerate(self.current_font.axes):
			for master in self.current_font.masters:
				if master.axes[i] in axisranges[i]:
					continue
				axisranges[i].append(master.axes[i])

		remove_axes = []
		remove_master_parameters = {master: [] for master in self.current_font.masters}
		for i, axis in enumerate(axisranges):
			if len(axisranges[i]) == 1:
				for master in self.current_font.masters:
					try:
						remove_master_parameters[master].append(master.customParameters["Axis Location"][i])
					except:
						pass
				remove_axes.append(self.current_font.axes[i])

		for axis in remove_axes:
			print("Removing unused axis:", axis)
			self.current_font.axes.remove(axis)

		for master in remove_master_parameters:
			print("Master:", master.name)
			for i, parameter in enumerate(remove_master_parameters[master]):
				print("Removing Axis Location parameter for axis:", parameter["Axis"])
				master.customParameters["Axis Location"].remove(parameter)

	def remove_unused_instances(self):
		remove_instances = []
		for instance in self.current_font.instances:
			if instance.type:
				continue
			if "Extreme" in instance.name or "Origin" in instance.name:
				remove_instances.append(instance)

		for instance in remove_instances:
			self.current_font.instances.remove(instance)

	def remove_in_instance_names(self, name):
		if name == "-":
			name = ""
		for instance in self.current_font.instances:
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
			self.current_font = Glyphs.openDocumentWithContentsOfFile_display_(original_font_file_path, False).font
			if recipe == "":
				continue
			family_name = recipe.split("\n")[0]
			replace_name = recipe.split("\n")[len(recipe.split("\n")) - 1]
			subset_values = {}
			for i, line in enumerate(recipe.split("\n")[1:len(recipe.split("\n")) - 1]):
				subset_values[self.current_font.axes[i].name] = [int(line.split(":")[0]),
				                                                           int(line.split(":")[1].split("[")[0]),
				                                                           int(line.split("[")[1].replace("]", ""))]

			print("\nNew family name:", family_name)

			self.master_manager(subset_values, family_name)

			filename = self.preferred_directory + "/" + family_name + ".glyphs"
			print("Writing file to:", filename)
			self.current_font.save(path=filename)
			self.current_font.save()

			self.fix_special_layers()
			self.remove_unused_masters(subset_values)
			self.current_font.save()
			self.check_empty_glyphs()
			self.order_special_layers(subset_values)
			self.remove_axes()
			self.remove_unused_instances()
			self.remove_in_instance_names(replace_name)

			self.current_font.save()
			self.current_font.close()

		self.w.close()

	def write_preferences(self, sender):
		# save text field to prefs
		Glyphs.defaults["com.eweracs.subsetVariableFont.recipes"] = self.w.enterRecipe.get()
		Glyphs.defaults["com.eweracs.subsetVariableFont.saveLocation"] = self.preferred_directory


CreateSubsets()