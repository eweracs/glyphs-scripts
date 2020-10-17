# glyphs-scripts
Scripts for Glyphs.

## Auto-Name Instances
Names instances based on assigned names. Useful for batch-renaming large families.

## Interpolate Anchors
Same as clicking Re-Interpolate in the layers panel, but only affects anchors.

## Interpolate Kerning (WIP)
Adds Replace Feature custom parameter for every instance for kerning (editable to replace with different values). Useful for hard-coded capital/sc spacing. Currently only works for two-master setups (weight). Values and classes need to be entered directly into the script. UI in the works. Use at your own risk. Currently requires you to write the kern code to be replaced into the features. 

## Make Web Variable
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
