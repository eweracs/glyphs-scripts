import lighttable as lt

glyph = Font.glyphs[0]

print(Font.currentTab.layers[Font.currentTab.textCursor])

restoration_font = None

if info := lt.RestorationInfo.info_for(glyph):
	restoration_font = info.restoration_font

selected_font_master_index = Font.masters.index(Font.selectedFontMaster)

master_kerning = Font.kerning[Font.selectedFontMaster.id]

left_layer, right_layer = (Font.currentTab.layers[Font.currentTab.textCursor - 1],
                           Font.currentTab.layers[Font.currentTab.textCursor])

left_glyph, right_glyph = left_layer.parent, right_layer.parent

info_left_layer, info_right_layer = (restoration_font.glyphs[left_glyph.name].layers[left_layer.associatedMasterId],
                                     restoration_font.glyphs[right_glyph.name].layers[right_layer.associatedMasterId])

if (current_kerning := right_layer.previousKerningForLayer_direction_(left_layer, LTR)) > 1000:
	current_kerning = 0

info_kerning = info_right_layer.previousKerningForLayer_direction_(info_left_layer, LTR)

print("Pair: %s%s\nCurrent kerning: %s\nOld kerning: %s\nDifference: %s\n" %
      (left_glyph.name, right_glyph.name, int(current_kerning), int(info_kerning), int(current_kerning - info_kerning)))