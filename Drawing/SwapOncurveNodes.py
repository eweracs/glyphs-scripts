# MenuTitle: Swap On-curve Nodes
# -*- coding: utf-8 -*-

__doc__ = """
Swaps two selected on-curve nodes, moving their handles accordingly.
"""

from Foundation import NSPoint


def swap_oncurve_node_positions_keep_offcurves():
	# get selected on-curve nodes
	selected_nodes = [selected for selected in Layer.selection if
	                  type(selected) == GSNode and selected.type != "offcurve"]

	# check that exactly two nodes are selected
	if len(selected_nodes) != 2:
		return

	# collect the off-curve nodes for each selected node
	nodes_offcurves = [
		[attached_node for attached_node in [node.prevNode, node.nextNode] if attached_node.type == "offcurve"] for node
		in selected_nodes]

	# swap the on-curve node positions
	for index, position in enumerate([node.position for node in selected_nodes]):
		selected_nodes[index - 1].position = position

	# move the off-curve nodes by the change in on-curve node position
	for index, node_offcurves in enumerate(nodes_offcurves):
		x_diff = selected_nodes[index].x - selected_nodes[index - 1].x
		y_diff = selected_nodes[index].y - selected_nodes[index - 1].y
		for offcurve in node_offcurves:
			offcurve.position = NSPoint(offcurve.position.x + x_diff, offcurve.position.y + y_diff)


swap_oncurve_node_positions_keep_offcurves()
