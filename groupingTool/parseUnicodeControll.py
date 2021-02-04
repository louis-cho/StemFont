class parseUnicodeController:    
    # 588 each
    first = {
        0:'ㄱ', 1:'ㄲ', 2:'ㄴ', 3:'ㄷ', 4:'ㄸ', 5:'ㄹ', 6:'ㅁ', 7:'ㅂ', 8:'ㅃ', 9:'ㅅ', 10:'ㅆ',
        11:'ㅇ', 12:'ㅈ', 13:'ㅉ', 14:'ㅊ', 15:'ㅋ', 16:'ㅌ', 17:'ㅍ', 18:'ㅎ'
    }
    # 28 each
    middle = {
        0:'ㅏ', 1:'ㅐ', 2:'ㅑ', 3:'ㅒ', 4:'ㅓ', 5:'ㅔ', 6:'ㅕ', 7:'ㅖ', 8:'ㅗ', 9:'ㅘ', 10:'ㅙ',
        11:'ㅚ', 12:'ㅛ', 13:'ㅜ', 14:'ㅝ', 15:'ㅞ', 16:'ㅟ', 17:'ㅠ', 18:'ㅡ', 19:'ㅢ', 20:'ㅣ'
    }
    # 28 each
    final = {
        0:None, 1:'ㄱ', 2:'ㄲ', 3:'ㄱㅅ', 4:'ㄴ', 5:'ㄴㅈ', 6:'ㄴㅎ', 7:'ㄷ', 8:'ㄹ', 9:'ㄹㄱ',
        10:'ㄹㅁ', 11:'ㄹㅂ', 12:'ㄹㅅ', 13:'ㄹㅌ', 14:'ㄹㅍ', 15:'ㄹㅎ', 16:'ㅁ', 17:'ㅂ', 18:'ㅂㅅ',
        19:'ㅅ', 20:'ㅆ', 21:'ㅇ', 22:'ㅈ', 23:'ㅊ', 24:'ㅋ', 25:'ㅌ', 26:'ㅍ', 27:'ㅎ'
    }

    vowel_horizontal = [8, 12, 13, 17, 18]
    vowel_horizontal_low = [8,12,18]
    vowel_vertical = [0, 1, 2, 3, 4, 5, 6, 7, 20]
    vowel_vertical_double = [5,7]
    vowel_double = [9, 10, 11, 14, 15, 16, 19]
    
    def __init__(self,code):
        self.code = code
        self.charList = self.getChars()
        
    def parseUnicode(self):
        if self.code is None:
            raise Exception("class's code is None, Please insert code by setCode() method")
            
        if not 0xAC00 <= self.code <= 0xD7A3:
            raise ValueError("Unicode is not in Korean range")
            
        first_idx = (self.code - 0xAC00) // 588
        middle_idx = (self.code - 0xAC00 - 588*first_idx) // 28
        final_idx = (self.code - 0xAC00) % 28
        
        return(first_idx,middle_idx,final_idx)
        
    def getChars(self):
        if self.code is None:
            raise Exception("class's code is None, Please insert code by setCode() method")
            
        first_idx, middle_idx, final_idx = self.parseUnicode()
        
        return [self.first[first_idx],self.middle[middle_idx],self.final[final_idx]]
        
    def setCode(self,code):
        self.code = code
        self.charList = self.getChars()

def judgeMentCandidate(spuc,cpuc):
    """
    judgement whther Contour is investigated same group

    Args:
    spuc : parseUnicodeController object about standard Rcontour unicode

    cpuc : parseUnicodeController object about compare Rcontour unicode

    Return:
    if Compare Rcontour should be investigate return True else False
    """

    for i in range(0,len(spuc.charList)):
        if(spuc.charList[i] != None):
            if(i == 0):
                if(spuc.charList[i] == cpuc.charList[i+2]):
                    return  True
            elif(i == 1):
                if(spuc.charList[i] == cpuc.charList[i]):
                    return True
            elif(i == 2):
                if(spuc.charList[i] == cpuc.charList[i-2]):
                    return True        

    return False            