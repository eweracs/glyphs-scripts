import lighttable as lt
from GlyphsApp import *
from Foundation import NSAffineTransform, NSColor

font = Glyphs.font

glyph = font.glyphs[0]

restoration_font = None

if info := lt.RestorationInfo.info_for(glyph):
	restoration_font = info.restoration_font

selected_font_master_index = font.masters.index(font.selectedFontMaster)

master_kerning = font.kerning[font.selectedFontMaster.id]

left_layer, right_layer = (font.currentTab.layers[font.currentTab.layersCursor - 1],
                           font.currentTab.layers[font.currentTab.layersCursor])

left_glyph, right_glyph = left_layer.parent, right_layer.parent

info_left_layer, info_right_layer = (restoration_font.glyphs[left_glyph.name].layers[left_layer.associatedMasterId],
                                     restoration_font.glyphs[right_glyph.name].layers[right_layer.associatedMasterId])

if (current_kerning := right_layer.previousKerningForLayer_direction_(left_layer, LTR)) > 1000:
	current_kerning = 0

info_kerning = info_right_layer.previousKerningForLayer_direction_(info_left_layer, LTR)

kerning_difference = info_kerning - current_kerning

path = right_layer.bezierPath.copy()

transform = NSAffineTransform.transform()
transform.translateXBy_yBy_(kerning_difference, 0)

path.transformUsingAffineTransform_(transform)

if kerning_difference < 0:
	NSColor.redColor().colorWithAlphaComponent_(0.6).set()
else:
	NSColor.greenColor().colorWithAlphaComponent_(0.6).set()

path.fill()
