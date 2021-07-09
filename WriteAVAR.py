# MenuTitle: Write AVAR table
# -*- coding: utf-8 -*-

__doc__ = """
Writes an AVAR table based on current weight distribution
"""

# create a list which indexes all instance weights
instanceweights = sorted({instance.weightValue for instance in Font.instances})

axisMinimum = instanceweights[0]  # lightest stem weight
axisRange = instanceweights[-1] - axisMinimum  # axis range

# calculate and write AVAR table to custom parameters
Font.customParameters["Axis Mappings"] = {"wght": {int(axisRange/(len(instanceweights) - 1)*instance + axisMinimum):
                                                   instanceweights[instance] for instance in range(len(instanceweights))
                                                   }
                                          }

Glyphs.showNotification(title="Wrote AVAR table",
                        message="Table calculated for " + str(len(instanceweights)) + " instances")
