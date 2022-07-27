# MenuTitle: HT Letterspacer for All Masters
# -*- coding: utf-8 -*-

__doc__ = """
Runs HT Letterspacer for the current selection in all masters.
"""

import_success = False
try:
	from HTLSLibrary import *
	import_success = True
except:
	Message("Please install HTLS Manager from the plugin manager and restart Glyphs.", "HTLS Manager required")


if import_success:
	HTLSScript(True)
