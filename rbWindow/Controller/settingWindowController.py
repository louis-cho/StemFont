
COLOR_GREEN = (0,1,0,0.7)

def helpCheckGlyphList(check, window):
	"""
		2020/03/23
		created by H.W. Cho

		Undo previous marked glyphs(selectedGlyphs), paint current glyphs(glyphs) from window

		Args :
			check(checkBox) : Apply mark or not
	"""
	if check.get() == 0:
		if window.selectedGlyphs is not None:
			print("B")
			for glyph in window.selectedGlyphs:
				glyph.markColor = None
			return

	if window.glyphs is None:
		print(Message("표시할 수 있는 그룹이 존재하지 않습니다."))
		return

	# rewind previous
	print("prevGlyphList : ",window.selectedGlyphs)
	if window.selectedGlyphs is not None:
		print("A")
		for glyph in window.selectedGlyphs:
			glyph.markColor = None

	window.selectedGlyphs = []

	# check current
	for glyph in window.glyphs:
		window.selectedGlyphs.append(glyph)
		glyph.markColor = COLOR_GREEN

	print(window.selectedGlyphs)

