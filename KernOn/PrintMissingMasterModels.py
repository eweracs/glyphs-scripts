# MenuTitle: Print Missing Master Models
# -*- coding: utf-8 -*-

__doc__ = """
Prints a tab for each master with missing models from all other masters.
"""

# create a list of all Kern On models across all masters of the current font
# for each master, check which models are missing and open a new tab with the missing models

if Font is None:
	Message("Please open a font project!", "No font selected")
	exit()

all_models = []

for master in Font.masters:
	if master.userData["KernOnAutoKernedFrom"] or master.userData["KernOnIsInterpolated"] or not master.userData["KernOnModels"]:
		continue
	for model in master.userData["KernOnModels"]:
		if model not in all_models:
			all_models.append(model)

for master in Font.masters:
	if master.userData["KernOnAutoKernedFrom"] or master.userData["KernOnIsInterpolated"]:
		continue
	missing_models = []
	for model in all_models:
		if model not in master.userData["KernOnModels"]:
			missing_models.append(model)

	if len(missing_models) > 0:
		# replace the space in the model name with a slash
		# add a slash as the first character of the model name
		missing_models = [model.replace(" ", "/") for model in missing_models]
		missing_models = ["/" + model for model in missing_models]
		Font.newTab(master.name + ":\n\n" + "\n".join(missing_models))

		# find the current master's index
		Font.currentTab.masterIndex = Font.masters.index(master)
