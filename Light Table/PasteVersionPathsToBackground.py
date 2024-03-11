# MenuTitle: Paste Version Paths to Background
# -*- coding: utf-8 -*-

__doc__ = """
Pastes the decomposed layers from the selected version into the background of each layer.
"""

import lighttable as lt

Font.disableUpdateInterface()
for selection in Font.selectedLayers:
	for layer in selection.parent.layers:
		if info := lt.RestorationInfo.info_for(layer):
			plan = lt.ComponentIntegrationPlan(
				strategies={},
				fallback=lt.ComponentIntegrationStrategy.INTEGRATE_AS_PATHS
			)
			restored_background = info.restore_layer_as_background(plan)
Font.enableUpdateInterface()