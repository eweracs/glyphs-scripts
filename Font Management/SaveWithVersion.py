# MenuTitle: Save with Version
# -*- coding: utf-8 -*-

__doc__ = """
Saves a copy of the current file as a .glyphs file with a version number.
"""

italic_masters = 0
for master in Glyphs.font.masters:
    if master.italicAngle:
        italic_masters += 1

is_italic = ""
if italic_masters:
    is_italic = "Italic "

new_filename = "%s %s%s.glyphs" % (Glyphs.font.familyName, is_italic, Glyphs.font.version())

new_filepath = Font.filepath.replace(Glyphs.font.filepath.split("/")[-1], new_filename)

Glyphs.font.save(new_filepath, makeCopy=True)