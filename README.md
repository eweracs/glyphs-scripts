# glyphs-scripts
Scripts for Glyphs.

## Auto-Name Instances
Names instances based on assigned names. Useful for batch-renaming large families.

## Batch Export
Opens a dialogue to choose multiple export formats. Sorts exported files into respective sub-directories (/Desktop/TTF, /Web/WOFF2, ...).

## Interpolate Anchors
Same as clicking Re-Interpolate in the layers panel, but only affects anchors.

## Instance Kerner (WIP, one axis only)
Adds Replace Feature custom parameter for every instance for kerning. Useful for hard-coded capital/sc spacing. Currently only works for single-axis setups, still trying to figure out how to make this work for multiple axes. Todo: more than two kerning values per axis

## Make Web Weights
Converts master and instance weight values into USWeightClass values based on naming. Calculates AVAR table for correct interpolation. Takes care of intermediate layer values as well.

## Write AVAR
Writes an AVAR table based on stem weights. Affects only weight, regardless of axis count.


# License

Copyright 2020 The eweracs Glyphs-Scripts Project Authors.

Some code samples by Georg Seifert (@schriftgestalt) and Rainer Scheichelbauer (@mekkablue).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use the software provided here except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
