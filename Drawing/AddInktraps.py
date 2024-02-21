# MenuTitle: Add Inktraps
# -*- coding: utf-8 -*-

__doc__ = """
Adds rudimentary inktraps for the selected nodes.
"""

from vanilla import FloatingWindow, Group, TextBox, EditText, HorizontalLine, Button
from math import dist, sin, acos, radians, degrees, sqrt
from Foundation import NSPoint
from GlyphsApp import Glyphs, GSNode, Message


class AddInktraps:
	def __init__(self):
		self.font = Glyphs.font

		if self.font is None:
			Message("No font selected", "Select a font project!")
			return

		self.aperture = 20
		self.depth = 0.5

		self.w = FloatingWindow((1, 1), "Add Inktraps")
		self.w.aperture = Group("auto")
		self.w.aperture.title = TextBox("auto", "Aperture")
		self.w.aperture.entry = EditText("auto", text="20", callback=self.aperture_callback)
		self.w.depth = Group("auto")
		self.w.depth.title = TextBox("auto", "Depth")
		self.w.depth.entry = EditText("auto", text="0.5", callback=self.depth_callback)
		self.w.divider = HorizontalLine("auto")
		self.w.addInktraps = Button("auto", "Add Inktraps", callback=self.add_inktraps)

		group_rules = [
			"H:|[title(60)]-margin-[entry(40)]|",
			"V:|[title]",
			"V:|[entry]|",
		]

		rules = [
			"H:|-margin-[aperture]-margin-|",
			"H:|-margin-[depth]-margin-|",
			"H:|-margin-[divider]-margin-|",
			"H:|-margin-[addInktraps]-margin-|",
			"V:|-margin-[aperture]-margin-[depth]-margin-[divider]-margin-[addInktraps]-margin-|"
		]

		metrics = {
			"margin": 10
		}

		self.w.aperture.addAutoPosSizeRules(group_rules, metrics)
		self.w.depth.addAutoPosSizeRules(group_rules, metrics)
		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.setDefaultButton(self.w.addInktraps)
		self.w.open()
		self.w.makeKey()

	def aperture_callback(self, sender):
		try:
			self.aperture = float(sender.get())
		except:
			Message(title="Invalid value", message="Aperture must be a number.")
			return

	def depth_callback(self, sender):
		try:
			self.depth = float(sender.get())
		except:
			Message(title="Invalid value", message="Depth must be a number.")
			return

	def add_inktraps(self, sender):
		for layer in self.font.selectedLayers:
			for path in layer.paths:
				for node in path.nodes:
					if node.selected:
						self.create_inktrap_for_node(node)

	def create_inktrap_for_node(self, node):
		# there are three nodes that form a triangle. A center node ("node") and one left and one right node ("left_node" and
		# "right_node")

		path = node.parent
		layer = node.layer

		prev_node = node.prevNode
		next_node = node.nextNode

		if prev_node is None or next_node is None:
			print("Node is not connected to other nodes.")
			return
		if prev_node.type == "offcurve" or next_node.type == "offcurve":
			print("Node is an offcurve node.")
			return

		# calculate the distance between the left and right nodes
		a = dist([prev_node.position.x, prev_node.position.y], [next_node.position.x, next_node.position.y])
		# calculate the distance between the left node and the selected node
		b = dist([node.position.x, node.position.y], [prev_node.position.x, prev_node.position.y])
		# calculate the distance between the right node and the selected node
		c = dist([node.position.x, node.position.y], [next_node.position.x, next_node.position.y])

		# calculate the angle at the selected node
		angle_at_node = degrees(acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)))

		# see how far into my angle the circle can be pushed, then calculate the intersections with b and c
		# if the angle is less than 90 degrees, the circle can be pushed inwards
		if angle_at_node < 90:
			# calculate the size of the other two equal angles in the triangle consisting of the intersection points of the
			# pushed-in circle and the selected node
			other_angles = (180 - angle_at_node) / 2
			# make a right triangle using the diameter of the circle as the hypotenuse. The right angle will be at the
			# intersection of the circle with line c.
			# calculate the angle on in the triangle at the intersection of the circle with line c
			circle_angle = 90 - other_angles
			# calculate the distance from the intersection of the circle with line c to the hypotenuse
			circle_line_b = sin(circle_angle)
			# calculate the distance from the intersection of the circle with line c to the intersection with line b
			line_between_intersections = sqrt(self.aperture ** 2 - circle_line_b ** 2)

			# using the angle A and the two other angles, as well as line_a as the line opposite angle A, calculate the
			# distance of the intersections to the selected node
			distance_to_intersections = line_between_intersections * sin(radians(other_angles)) / sin(
				radians(angle_at_node))

			# calculate the path time at which the intersection with line b is reached
			factor_b = distance_to_intersections / b
			# calculate the coordinates of intersection b using the coordinates of the selected node and of the left node
			intersection_b = NSPoint(
				node.position.x + (prev_node.position.x - node.position.x) * factor_b,
				node.position.y + (prev_node.position.y - node.position.y) * factor_b
			)
			# calculate the path time at which the intersection with line c is reached
			factor_c = distance_to_intersections / c
			# calculate the coordinates of intersection c using the coordinates of the selected node and of the right node
			intersection_c = NSPoint(
				node.position.x + (next_node.position.x - node.position.x) * factor_c,
				node.position.y + (next_node.position.y - node.position.y) * factor_c
			)

			path.insertNode_atIndex_(GSNode(intersection_b), node.index)
			path.insertNode_atIndex_(GSNode(intersection_c), node.index + 1)

			# open a corner at the node
			layer.openCornerAtNode_offset_(node, distance_to_intersections * self.depth)
			# find the middle between the two new nodes
			node_1_position = path.nodes[node.index].position
			node_2_position = path.nodes[node.index - 1].position
			middle_node = GSNode()
			middle_node.position = NSPoint(
				node_1_position.x + (node_2_position.x - node_1_position.x) / 2,
				node_1_position.y + (node_2_position.y - node_1_position.y) / 2
			)
			path.insertNode_atIndex_(middle_node, node.index)
			path.removeNodeAtIndex_(node.index - 2)
			path.removeNodeAtIndex_(node.index)


AddInktraps()
