from groupingTool.parseUnicodeControll import *
from parseSyllable.configVersion1 import *
from parseSyllable.configVersion2 import *
from parseSyllable.configVersion3 import *

def getConfigure(RGlyph):

	resultList = list()
	resultDict = dict()

	middle_one = ['ㅏ','ㅑ','ㅓ','ㅕ','ㅣ','ㅐ']
	middle_two = ['ㅔ','ㅖ','ㅒ']
	middle_three = ['ㅗ','ㅛ','ㅜ','ㅠ','ㅡ']
	middle_four = ['ㅘ','ㅚ','ㅟ', 'ㅢ','ㅙ']
	middle_five = ['ㅝ']
	middle_six = ['ㅞ']

	#print("RGlyph : ", RGlyph)
	puc = parseUnicodeController(RGlyph.unicode)
	chars = puc.getChars()


	if chars[2] is None:
		if chars[1] in middle_one:
			resultList = case1(RGlyph)
		elif chars[1] in middle_two:
			resultList = case3(RGlyph)
		elif chars[1] in middle_three:
			resultList = case5(RGlyph)
		elif chars[1] in middle_four:
			resultList = case7(RGlyph)
		elif chars[1] in middle_five:
			resultList = case9(RGlyph)
		elif chars[1] in middle_six:
			resultList = case11(RGlyph)
	else:
		if chars[1] in middle_one:
			resultList = case2(RGlyph)
		elif chars[1] in middle_two:
			resultList = case4(RGlyph)
		elif chars[1] in middle_three:
			resultList = case5(RGlyph)
		elif chars[1] in middle_four:
			resultList = case8(RGlyph)
		elif chars[1] in middle_five:
			resultList = case10(RGlyph)
		elif chars[1] in middle_six:
			resultList = case12(RGlyph)

	resultDict[str(RGlyph.unicode)] = resultList

	return resultDict