# MenuTitle: Select All Nodes Between Selected Nodes
# -*- coding: utf-8 -*-

__doc__ = """
Selects all nodes between the first and last selected node in a path.
"""


def select_all_nodes_between_selected_nodes():
	selected_nodes = [
		selection for selection in Layer.selection if isinstance(selection, GSNode)
	]  # get all the selected nodes

	if len(selected_nodes) >= 2:  # if at least two nodes are selected
		parent_path = selected_nodes[0].parent
		for selected_node in selected_nodes:  # check whether all nodes belong to the same path
			if selected_node.parent != parent_path:
				return  # if not, cancel
		node_indices = [parent_path.nodes.index(selected_node) for selected_node in
						selected_nodes]  # collect the indices of all selected nodes
		nodes_in_between = [node for node in parent_path.nodes[min(node_indices):max(
			node_indices) + 1]]  # get the nodes for all indices between the smallest and biggest selected node index
		for node in nodes_in_between:
			node.selected = True  # select all nodes in between


select_all_nodes_between_selected_nodes()