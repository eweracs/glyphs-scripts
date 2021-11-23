# MenuTitle: Interpolation Preview
# -*- coding: utf-8 -*-

__doc__ = """
Allows to visually interpolate instances or intermediate layers.
"""

import vanilla


class Interpolator:
	def __init__(self):

		if Font is None:
			Message("No font selected", "Select a font project!")
			return

		self.font = Font

		self.font.instances.append(GSInstance())
		self.font.instances[-1].name = "Interpolator Preview"

		self.w = vanilla.FloatingWindow((0, 0), "Interpolation Preview")

		self.axesRanges = []  # create a list to contain tuples with the min and max of an axis
		self.currentCoords = []
		self.sliderList = []  # create a list of the slider objects
		self.popUpButtonList = []
		self.inputFieldList = []

		self.instanceName = "Regular"
		self.selectedClasses = ["Medium (normal)", "Regular"]
		self.selectedParent = 0
		self.namePlaceholder = "Regular"

		self.styleClasses = {
			"Weight": {
				1: "Hairline",
				2: "Thin",
				3: "Extralight",
				4: "Light",
				5: "Regular",
				6: "Medium",
				7: "Semibold",
				8: "Bold",
				9: "Extrabold",
				10: "Black",
				11: "Extrablack"
			},
			"Width": {
				1: "Ultra Condensed",
				2: "Extra Condensed",
				3: "Condensed",
				4: "SemiCondensed",
				5: "Medium (normal)",
				6: "Semi Expanded",
				7: "Expanded",
				8: "Extra Expanded",
				9: "Ultra Expanded"
			}
		}

		for coord in self.font.selectedFontMaster.axes:
			self.currentCoords.append(int(coord))
		for i, axis in enumerate(self.font.axes):  # for each axis in the font, create a new slider
			self.axesRanges.append(set())  # for each axis in the font, create an empty tuple to store the axis range
			for master in self.font.masters:  # first, build a list of the axis ranges
				self.axesRanges[i].add(master.axes[i])
			self.axesRanges = [sorted(list(a)) for a in self.axesRanges]
			for axisRange in self.axesRanges:
				del axisRange[1:-1]  # delete intermediate master coordinates

			if str(Glyphs.versionNumber)[0] == "3":
				axis_tag = axis.axisTag
				axis_name = axis.name
			else:
				axis_tag = axis["Tag"]
				axis_name = axis["Name"]

			setattr(self.w, axis_tag + "title", vanilla.TextBox((10, 20 + i * 30, -10, 14),
			                                                    axis_name, sizeStyle="small"))
			s = vanilla.Slider((60, 20 + i * 30, -70, 15),
			                   minValue=sorted(self.axesRanges[i])[0],
			                   maxValue=sorted(self.axesRanges[i])[1],
			                   value=self.currentCoords[i],
			                   callback=self.axis_slider)
			setattr(self.w, axis_tag + "slider", s)
			self.sliderList.append(s)

			t = vanilla.EditText((-60, 20 + i * 30 - 1, -10, 22), callback=self.axis_input, text=self.currentCoords[i])
			self.inputFieldList.append(t)
			setattr(self.w, axis_tag + "input", t)

		self.ypos = s.getPosSize()[1] + 36

		if self.font.instances:
			self.w.selectInstanceTitle = vanilla.TextBox((10, self.ypos, -10, 14), "Copy from instance:",
			                                             sizeStyle="small")
			setattr(self.w, "instanceSelect", vanilla.PopUpButton((130, self.ypos, -10, 17),
			                                                      [i.name for i in self.font.instances],
			                                                      callback=self.instance_selector))
			self.ypos += 32

		setattr(self.w, "separator", vanilla.HorizontalLine((10, self.ypos, -10, 1)))

		self.ypos += 16

		setattr(self.w, "addMenu", vanilla.Button((155, self.ypos, -10, 20), "Instance...",
		                                          callback=self.add_instance_menu))
		setattr(self.w, "addIntermediate", vanilla.Button((10, self.ypos, -155, 20), "Intermediate...",
		                                                  callback=self.intermediate_menu))

		self.w.resize(300, self.w.addMenu.getPosSize()[1] + 30)

		self.w.open()
		self.w.makeKey()
		self.w.bind("close", self.remove_preview)

	def instance_selector(self, sender):
		for i, axis in enumerate(self.font.instances[sender.get()].axes):
			self.currentCoords[i] = axis
			self.inputFieldList[i].set(str(int(axis)))
			self.sliderList[i].set(int(axis))

	def add_instance_menu(self, sender):
		try:
			delattr(self.w, "intermediateTitle")
			delattr(self.w, "parentSelector")
			delattr(self.w, "makeIntermediate")
		except Exception:
			print()

		self.ypos = self.w.addMenu.getPosSize()[1] + 40

		try:
			setattr(self.w, "instanceName", vanilla.TextBox((10, self.ypos, 60, 14), "Name", sizeStyle="small"))
			setattr(self.w, "nameSelector", vanilla.EditText((60, self.ypos, -10, 19),
			                                                 placeholder=self.namePlaceholder, sizeStyle="small",
			                                                 callback=self.instance_name))

			self.ypos += 41

			for i, axis in enumerate(self.styleClasses):
				c = vanilla.PopUpButton((60, self.ypos + i * 30, -10, 17), list(self.styleClasses[axis].values()),
				                        callback=self.class_selector)
				c.set(4)
				setattr(self.w, axis + "classSelector", c)
				self.popUpButtonList.append(c)
				setattr(self.w, axis + "ClassTitle", vanilla.TextBox((10, self.ypos + i * 30, 60, 14), axis,
				                                                     sizeStyle="small"))
				if i == 2:
					break
			setattr(self.w, "generate", vanilla.Button((10, c.getPosSize()[1] + 30, -10, 20), "Make Instance",
			                                           callback=self.write_instance))
			self.w.setDefaultButton(self.w.generate)
			self.w.resize(300, self.w.generate.getPosSize()[1] + 30)
		except Exception:
			return

	def axis_slider(self, sender):
		for i, item in enumerate(self.sliderList):
			if item is sender:
				self.currentCoords[i] = int(sender.get())
				self.inputFieldList[i].set(str(int(sender.get())))
		self.preview_instance()

	def axis_input(self, sender):
		for i, item in enumerate(self.inputFieldList):
			if item is sender:
				try:
					if sender.get().isnumeric():
						self.currentCoords[i] = int(sender.get())
						self.sliderList[i].set(int(sender.get()))
				except Exception:
					self.currentCoords[i] = 0
					self.sliderList[i].set(0)
		self.preview_instance()

	def class_selector(self, sender):
		for i, item in enumerate(self.popUpButtonList):
			if item is sender:
				if str(Glyphs.versionNumber)[0] == "3":
					self.selectedClasses[i] = list(self.styleClasses.items())[i][1].items()[sender.get()]
				else:
					self.selectedClasses[i] = list(self.styleClasses.items())[i][1].values()[sender.get()]
		self.instance_autonamer()

	def instance_autonamer(self):  # basically copied from AutoNameInstances.py
		if len(self.w.nameSelector.get()) > 0:
			self.instanceName = self.w.nameSelector.get()
			print(len(self.w.nameSelector.get()))
		else:
			if "Medium" in self.selectedClasses[0]:
				self.namePlaceholder = self.selectedClasses[1]
				self.instanceName = self.namePlaceholder
			elif self.selectedClasses[1] == "Regular" or self.selectedClasses[1] == "Normal":
				self.namePlaceholder = self.selectedClasses[0]
				self.instanceName = self.namePlaceholder
			else:
				self.namePlaceholder = self.selectedClasses[1] + " " + self.selectedClasses[0]
				self.instanceName = self.namePlaceholder
			self.w.nameSelector.setPlaceholder(self.namePlaceholder)

	def preview_instance(self):
		self.font.instances[-1].axes = self.currentCoords
		if not self.font.currentTab:  # open up a new tab with the new instance in preview
			self.font.newTab("a")
		if self.font.currentTab.previewHeight <= 20:
			self.font.currentTab.previewHeight = 200
		self.font.currentTab.previewInstances = self.font.instances[-1]

	def instance_name(self, sender):
		self.instanceName = sender.get()
		if len(self.instanceName) == 0:
			self.instanceName = self.namePlaceholder

	def write_instance(self, sender):
		self.font.instances[-1].axes = self.currentCoords
		self.font.instances[-1].name = self.instanceName
		if str(Glyphs.versionNumber)[0] == "3":
			self.font.instances[-1].widthClass = self.selectedClasses[0]
			self.font.instances[-1].weightClass = self.selectedClasses[1]
		else:
			self.font.instances[-1].widthClass = self.selectedClasses[0]
			self.font.instances[-1].weightClass = self.selectedClasses[1]

	def intermediate_menu(self, sender):
		try:
			delattr(self.w, "nameSelector")
			delattr(self.w, "instanceName")
			for i, axis in enumerate(self.styleClasses):
				delattr(self.w, axis + "classSelector")
				delattr(self.w, axis + "ClassTitle")
				if i == 2:
					break
			delattr(self.w, "generate")

		except Exception:
			print()

		self.ypos = self.w.addIntermediate.getPosSize()[1] + 40

		try:
			setattr(self.w, "intermediateTitle",
			        vanilla.TextBox((10, self.ypos, 60, 14), "Parent Master", sizeStyle="small"))
			setattr(self.w, "parentSelector",
			        vanilla.PopUpButton((60, self.ypos, -10, 17), [master.name for master in self.font.masters],
			                            callback=self.parent_selector))
			self.ypos += 30
			setattr(self.w, "makeIntermediate", vanilla.Button((10, self.ypos, -10, 20), "Make Intermediate",
			                                                   callback=self.make_intermediate))

			self.w.setDefaultButton(self.w.makeIntermediate)
			self.w.resize(300, self.w.makeIntermediate.getPosSize()[1] + 30)

		except Exception:
			print()

	def make_intermediate(self, sender):
		for layer in self.font.selectedLayers:
			new_layer = GSLayer()
			if str(Glyphs.versionNumber)[0] == "3":
				new_layer.attributes["coordinates"] = {self.font.axes[i].axisId: coordinate for i, coordinate in
				                                      enumerate(self.currentCoords)}
			else:
				new_layer.name = "{" + ", ".join([str(axis) for axis in self.currentCoords]) + "}"
			new_layer.associatedMasterId = self.font.masters[self.selectedParent].id
			self.font.glyphs[layer.parent.name].layers.append(new_layer)
			new_layer.reinterpolate()

	def parent_selector(self, sender):
		self.selectedParent = sender.get()

	def remove_preview(self, sender):
		if "Preview" in self.font.instances[-1].name:
			del self.font.instances[-1]


Interpolator()
