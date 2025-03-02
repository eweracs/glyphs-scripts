# MenuTitle: Report Missing Stylistic Set Variants
# -*- coding: utf-8 -*-

__doc__ = """
Analyses the existing stylistic sets and reports missing accented variants.
"""

def analyze_missing_ss_variants():
	font = Glyphs.font
	if not font:
		print("No font open")
		return

	missing_variants = []

	# Go through each glyph in the font
	for glyph in font.glyphs:
		base_name = glyph.name

		# Skip if it's already a stylistic variant
		if '.' in base_name:
			continue

		# Find all ss variants for this glyph
		ss_variants = []
		for variant in font.glyphs:
			if not variant.export:
				continue
			if variant.name.startswith(base_name + '.ss'):
				ss_variants.append(variant.name)

		# If this glyph has any ss variants
		if ss_variants:
			# Find all glyphs that use this as a component
			for composite in font.glyphs:
				if not composite.layers[0].components:
					continue

				# Check if this glyph is used as any component
				for component in composite.layers[0].components:
					if component.componentName == base_name:
						# For each ss variant of the base glyph
						for ss_variant in ss_variants:
							ss_suffix = ss_variant.split(base_name)[1]  # Get .ss0X part
							expected_ss = composite.name + ss_suffix

							# Check if the corresponding ss variant exists
							if not font.glyphs[expected_ss]:
								missing_variants.append({
									'base_glyph': base_name,
									'base_ss': ss_variant,
									'composite': composite.name,
									'missing': expected_ss
								})
						break  # Found the component, no need to check other components

	Glyphs.showMacroWindow()

	# Report results
	if missing_variants:
		print("\nMissing stylistic set variants:")
		print("================================")
		for variant in missing_variants:
			print(variant['missing'])
	else:
		print("\nNo missing stylistic set variants found!")

	return missing_variants


# Run the analysis
analyze_missing_ss_variants()
