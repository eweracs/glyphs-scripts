# glyphs-scripts
Scripts for Glyphs.

## Auto-Name Instances
Names instances based on assigned names. Useful for batch-renaming large families.

## Interpolate Anchors
Same as clicking Re-Interpolate in the layers panel, but only affects anchors.

## Interpolate Kerning
Adds Replace Feature custom parameter for every instance for kerning (editable to replace with different values). Useful for hard-coded capital/sc spacing.

## Make Web Variable
Converts master and instance weight values into USWeightClass values based on naming. Calculates AVAR table for correct interpolation. Tales care of intermediate layer values as well.

## Write AVAR
Writes an AVAR table based on stem weights. Affects only weight, regardless of axis count.
