# MenuTitle: Save with Version
# -*- coding: utf-8 -*-

__doc__ = """
Saves a copy of the current file as a .glyphs file with a version number.
"""

new_filepath = "%s %s.glyphs" % (".".join(Font.filepath.split(".")[:-1]), Glyphs.font.version())

Font.save(new_filepath, makeCopy=True)