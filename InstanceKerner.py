import vanilla


class KernWindow:

	def __init__(self):
		self.font = Font

		x = 10
		y = 10

		self.class1 = 0
		self.class2 = 0
		self.master1 = self.font.masters[0].axes[0]
		self.master2 = self.font.masters[0].axes[0]
		self.master_1_kern = 0
		self.master_2_kern = 0

		self.w = vanilla.FloatingWindow((0, 0), "Instance Kerner")

		self.w.otclass_name = vanilla.TextBox((10, y, 200, 20), "Select left and right OT Classes:", sizeStyle="small")
		y += 18

		self.ot_classes = [otclass.name for otclass in self.font.classes]
		self.masternames = [master.name for master in self.font.masters]

		self.axes_master_values = [[master.axes[a] for master in self.font.masters] for a in range(len(self.font.axes))]

		self.w.otClass1 = vanilla.PopUpButton((x, y, 140, 20), self.ot_classes, sizeStyle="small", callback=self.get_class_1)
		x += 160
		self.w.otClass2 = vanilla.PopUpButton((x, y, 140, 20), self.ot_classes, sizeStyle="small", callback=self.get_class_2)

		x -= 160
		y += 28

		self.w.master_name = vanilla.TextBox((10, y, 200, 20), "Master kerning values:", sizeStyle="small")
		y += 18

		self.w.master_1 = vanilla.PopUpButton((x, y, 92, 20), self.masternames, sizeStyle="small", callback=self.get_master_1)
		self.w.master_1_kern = vanilla.EditText((110, y, 40, 20), "", sizeStyle="small", callback=self.get_master_1_kern)
		x += 160
		self.w.master_2 = vanilla.PopUpButton((x, y, 92, 20), self.masternames, sizeStyle="small", callback=self.get_master_2)
		self.w.master_2_kern = vanilla.EditText((270, y, 40, 20), "", sizeStyle="small", callback=self.get_master_2_kern)
		y += 22
		x -= 160

		y += 10

		self.w.button = vanilla.Button((10, y, -10, 20), "Write to instances", callback=self.write_kerning)

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

	def get_master_1(self, sender):
		self.master1 = self.axes_master_values[0][sender.get()]

	def get_master_2(self, sender):
		self.master2 = self.axes_master_values[0][sender.get()]

	def write_kerning(self, sender):
		class1 = str(self.ot_classes[self.class1])
		class2 = str(self.ot_classes[self.class2])

		self.axis_1_range = self.master2 - self.master1

		if Font.features["kern"] != True:
			Font.features["kern"] = "pos @{} {} @{};".format(class1, int(self.master_1_kern), class2)

		for instance in Font.instances:

			kern = float((self.master_2_kern - self.master_1_kern)/self.axis_1_range*(instance.axes[0] - self.master1))\
			       + self.master_1_kern

			if instance.customParameters["Replace Feature"]:
				kern_text = "{}\npos @{} {} @{};".format(instance.customParameters["Replace Feature"], class1, int(kern), class2)

			else:
				kern_text = "kern;\npos @{} {} @{};".format(class1, int(kern), class2)

			instance.customParameters["Replace Feature"] = kern_text


KernWindow()
