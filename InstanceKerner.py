# MenuTitle: Instance Kerner
# -*- coding: utf-8 -*-

__doc__ = """
Writes Replace Feature custom parameter to instances for kern/cpsp
"""

import vanilla


class InstanceKerner:

	def __init__(self):
		self.font = Font

		# UI element indents init
		x = 10
		y = 10

		self.class1 = 0
		self.class2 = 0
		self.master1 = self.font.masters[0].axes[0]
		self.master2 = self.font.masters[-1].axes[0]
		self.master_1_kern = 0
		self.master_2_kern = 0

		self.ot_classes = [otclass.name for otclass in self.font.classes]  # List available OT classes
		self.masternames = [master.name for master in self.font.masters]  # List font master names
		self.kern_features = ["kern", "cpsp"]  # The two kerning features to write to, are more needed?

		self.feature_selection = self.kern_features[0]  # select kern as default feature

		self.w = vanilla.FloatingWindow((0, 0), "Instance Kerner")

		self.w.otclass_title = vanilla.TextBox((10, y, 200, 20), "Select left and right OT Classes:", sizeStyle="small")
		y += 18

		self.w.otClass1 = vanilla.PopUpButton((x, y, 140, 20), self.ot_classes, sizeStyle="small", callback=self.get_class_1)
		x += 160
		self.w.otClass2 = vanilla.PopUpButton((x, y, 140, 20), self.ot_classes, sizeStyle="small", callback=self.get_class_2)
		x -= 160
		y += 28

		self.w.master_title = vanilla.TextBox((10, y, 200, 20), "Master kerning values:", sizeStyle="small")
		y += 18

		self.w.master_1 = vanilla.TextBox((x + 50, y + 2, 92, 20), self.masternames[0], sizeStyle="small")
		self.w.master_1_kern = vanilla.EditText((x, y, 40, 20), "", sizeStyle="small", callback=self.get_master_1_kern)
		x += 160
		self.w.master_2 = vanilla.TextBox((x + 50, y + 2, 92, 20), self.masternames[-1], sizeStyle="small")
		self.w.master_2_kern = vanilla.EditText((x, y, 40, 20), "", sizeStyle="small", callback=self.get_master_2_kern)
		y += 28
		x -= 160

		self.w.select_feature_title = vanilla.TextBox((x, y, 200, 20), "Kern feature:", sizeStyle="small")
		y += 18

		self.w.select_feature = vanilla.PopUpButton((x, y, 80, 20), self.kern_features, sizeStyle="small",
		                                            callback=self.get_feature_selection)
		x += 90

		self.w.button = vanilla.Button((x, y, -10, 20), "Write to instances", callback=self.write_kerning)
		y += 30

		self.w.resize(320, y)
		self.w.center()
		self.w.open()
		self.w.makeKey()

	def get_class_1(self, sender):
		self.class1 = sender.get()

	def get_class_2(self, sender):
		self.class2 = sender.get()

	def get_master_1_kern(self, sender):
		self.master_1_kern = int(sender.get())

	def get_master_2_kern(self, sender):
		self.master_2_kern = int(sender.get())

	def get_feature_selection(self, sender):
		self.feature_selection = self.kern_features[sender.get()]

	def write_kerning(self, sender):
		class1 = str(self.ot_classes[self.class1])
		class2 = str(self.ot_classes[self.class2])

		self.axis_1_range = self.master2 - self.master1

		if not Font.features[self.feature_selection]:
			if self.feature_selection == "kern":
				Font.features["kern"] = "pos @{} {} @{};".format(class1, self.master_1_kern, class2)
			elif self.feature_selection == "cpsp":
				Font.features["cpsp"] = "pos @Uppercase <{} 0 {} 0>;".format(self.master_1_kern, self.master_1_kern*2)

		for instance in Font.instances:

			kern = float((self.master_2_kern - self.master_1_kern)/self.axis_1_range*(instance.axes[0] - self.master1))\
			       + self.master_1_kern

			if instance.customParameters["Replace Feature"]:
				if self.feature_selection == "kern":
					if "kern" in instance.customParameters["Replace Feature"]:
						kern_text = "{}\npos @{} {} @{};".format(instance.customParameters["Replace Feature"], class1,
						                                         int(kern), class2)
					else:
						kern_text = "{}\nkern;\npos @{} {} @{};".format(instance.customParameters["replace Feature"],
						                                                class1, int(kern), class2)

				if self.feature_selection == "cpsp":
					if "cpsp" in instance.customParameters["Replace Feature"]:
						kern_text = "{}\npos @Uppercase <{} 0 {} 0>;".format(instance.customParameters["Replace Feature"],
						                                                     int(kern), int(kern)*2)
					else:
						kern_text = "{}\ncpsp;\npos @Uppercase <{} 0 {} 0>;".format(instance.customParameters["Replace Feature"],
						                                                            int(kern), int(kern)*2)

			else:
				if self.feature_selection == "kern":
					kern_text = "kern;\npos @{} {} @{};".format(class1, int(kern), class2)
				else:
					kern_text = "cpsp;\npos @Uppercase <{} 0 {} 0>;".format(int(kern), int(kern)*2)

			instance.customParameters["Replace Feature"] = kern_text


InstanceKerner()
