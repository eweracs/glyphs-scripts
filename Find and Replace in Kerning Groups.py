#MenuTitle: Find and Replace in Kerning Groups
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Finds and replaces text in the metrics keys of selected glyphs. Leave the Find string blank to hang the replace string at the end of the metrics keys.
"""

import vanilla

class KerningGroupReplacer( object ):
	def __init__( self ):
		self.w = vanilla.FloatingWindow( (335, 125), "Find and Replace in Kerning Groups", autosaveName="com.mekkablue.KerningGroupReplacer.mainwindow" )

		self.w.text_Find     = vanilla.TextBox( (10, 30+3, 55, 20), "Find", sizeStyle='small' )
		self.w.text_Replace  = vanilla.TextBox( (10, 55+3, 55, 20), "Replace", sizeStyle='small' )

		self.w.text_left     = vanilla.TextBox(  (70, 12, 120, 14), "Left Group", sizeStyle='small' )
		self.w.leftSearchFor = vanilla.EditText( (70, 30, 120, 20), ".tf", sizeStyle='small', placeholder='(leave these blank ...' )
		self.w.leftReplaceBy = vanilla.EditText( (70, 55, 120, 20), "", sizeStyle='small', placeholder='(empty)' )

		self.w.text_right     = vanilla.TextBox(  (200, 12, 120, 14), "Right Group", sizeStyle='small' )
		self.w.rightSearchFor = vanilla.EditText( (200, 30, 120, 20), ".tf", sizeStyle='small', placeholder='... to append)' )
		self.w.rightReplaceBy = vanilla.EditText( (200, 55, 120, 20), "", sizeStyle='small', placeholder='(empty)' )
		
		self.w.open()
		self.w.makeKey()

KerningGroupReplacer()
