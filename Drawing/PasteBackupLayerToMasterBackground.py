# MenuTitle: Paste Backup Layer to Master Background
# -*- coding: utf-8 -*-

__doc__ = """
Pastes the contents of the selected backup layer to the associated master layer background.
"""

master_layer = Layer.parent.layers[Layer.associatedMasterId]
if not Layer.isMasterLayer and not Layer.isSpecialLayer:
	master_layer.background.shapes = Layer.shapes.copy()
	master_layer.background.hints = Layer.hints.copy()
	master_layer.background.anchors = Layer.anchors.copy()
else:
	Message(title="Not a backup layer", message="Please select a backup layer from which to copy the contents.")
