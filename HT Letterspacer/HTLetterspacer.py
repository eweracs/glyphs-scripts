# MenuTitle: HT Letterspacer
# -*- coding: utf-8 -*-

__doc__ = """
Runs HT Letterspacer for the current selection. Hold Option to run for all masters.
"""

from Foundation import NSEvent

import_success = False
try:
	from HTLSLibrary import *
	import_success = True
except:
	Message("Please install HTLS Manager from the plugin manager and restart Glyphs.", "HTLS Manager required")

if import_success:
	pressed_keys = NSEvent.modifierFlags()
	option_key = 524288
	option_key_pressed = pressed_keys & option_key == option_key

	HTLSScript(option_key_pressed)
