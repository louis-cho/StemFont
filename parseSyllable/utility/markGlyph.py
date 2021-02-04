from groupingTool.parseUnicodeController import *


COLOR_RED = (1,0,0,1)
COLOR_GREEN = (0,1,0,1)
COLOR_BLUE = (0,0,1,1)

def markGlyph(RGlyph):
    
    unicodeObj = parseUnicodeController(RGlyph.unicode)
    uniCodeIdx = unicodeObj.parseUnicode()
    uniCodeData = unicodeObj.getChars()

    # 종성이 존재하지 않는 경우
    if uniCodeData[2] is None:

            if uniCodeIdx[1] in parseUnicodeController.vowel_vertical:
                RGlyph.markColor = COLOR_RED         
        
            elif uniCodeIdx[1] in parseUnicodeController.vowel_horizontal:
                RGlyph.markColor = COLOR_GREEN        
  
            elif uniCodeIdx[1] in parseUnicodeController.vowel_double:
                RGlyph.markColor = COLOR_BLUE
        
                
    # 종성이 존재하는 경우    
    elif uniCodeData[2] is not None:
        
        if uniCodeIdx[1] in parseUnicodeController.vowel_horizontal:
            RGlyph.markColor = COLOR_RED
            
        elif uniCodeIdx[1] in parseUnicodeController.vowel_vertical:
            RGlyph.markColor =COLOR_GREEN
        
        elif uniCodeIdx[1] in parseUnicodeController.vowel_double:
            RGlyph.markColor = COLOR_BLUE