# MenuTitle: Recompose from Components
# -*- coding: utf-8 -*-

__doc__ = """
Recompose the selected glyph from its components.
"""


def recompose_from_components():
	parent = Layer.parent

	base_glyph = Layer.components[0].component

	# Duplicate glyph with new name
	component_glyph = parent.copy()
	component_glyph.name = AskString("Please pick a valid name for the component:", value="_%s." % parent.name,
	                                 title="Component Name", OKButton="Next", placeholder="_component.name")

	if not component_glyph.name:
		print("No glyph name provided")
		return
	if component_glyph.name in Font.glyphs:
		print("Glyph already in font.")
		return

	# Set to non-exporting
	component_glyph.export = False

	# Remove all components, leave paths
	anchor_name = AskString("Please pick an anchor name:", value="center", title="Anchor Name",
	                        OKButton="Make Component", placeholder="_component.name")
	if not anchor_name:
		return
	for layer in component_glyph.layers:
		associated_base_layer = base_glyph.layers[layer.associatedMasterId]

		base_offset = layer.components[0].position
		
		parent_layer = parent.layers[layer.associatedMasterId]
		parent_layer.leftMetricsKey = "==+%s" % int(base_offset.x) if base_offset.x else None

		for component in [remove for remove in layer.components]:
			layer.shapes.remove(component)
		if not associated_base_layer.anchors[anchor_name]:
			if anchor_name == "bottom":
				associated_base_layer.anchors[anchor_name] = GSAnchor(
					pt=(associated_base_layer.bounds.size.width / 2 + associated_base_layer.bounds.origin.x + base_offset.x, base_offset.y))
			if anchor_name == "center":
				associated_base_layer.anchors[anchor_name] = GSAnchor(pt=(
				associated_base_layer.bounds.size.width / 2 + associated_base_layer.bounds.origin.x + base_offset.x,
				associated_base_layer.bounds.size.height / 2 + base_offset.y))
			if anchor_name == "bottomright":
				associated_base_layer.anchors[anchor_name] = GSAnchor(
					pt=(associated_base_layer.bounds.size.width + associated_base_layer.bounds.origin.x + base_offset.x, base_offset.y))
			if anchor_name == "topright":
				associated_base_layer.anchors[anchor_name] = GSAnchor(pt=(
				associated_base_layer.bounds.size.width + associated_base_layer.bounds.origin.x + base_offset.x,
				associated_base_layer.bounds.size.height + base_offset.y))
		if associated_base_layer.anchors[anchor_name]:
			base_anchor = associated_base_layer.anchors[anchor_name]
			new_anchor = GSAnchor()
			new_anchor.name = "_%s" % anchor_name
			new_anchor.position = (base_anchor.position.x + base_offset.x, base_anchor.position.y + base_offset.y)
			layer.anchors.append(new_anchor)



	# Add glyph to font
	Font.glyphs.append(component_glyph)

	for layer in parent.layers:
		layer.background = layer.copyDecomposedLayer()
		for remove_path in [path for path in layer.paths]:
			layer.shapes.remove(remove_path)
		layer.components.append(GSComponent(Font.glyphs[component_glyph.name]))

	component_glyph.leftMetricsKey = "=40"
	component_glyph.rightMetricsKey = "=40"

	for layer in component_glyph.layers:
		layer.syncMetrics()
	component_glyph.leftKerningGroup = None
	component_glyph.rightKerningGroup = None
	component_glyph.setCategory_(None)
	component_glyph.setSubCategory_(None)
	component_glyph.updateGlyphInfo()


recompose_from_components()