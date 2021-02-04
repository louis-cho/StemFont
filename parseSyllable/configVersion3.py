import pandas as pd 
import matplotlib.pylab as plt
from groupingTool.parseUnicodeControll import *
from parseSyllable.utility.contourDistributionChart import *

def getGravity(con):
    """
    Get contour's points Gravity
    
    Args:
        con :: RContour
    Return:
        List
            gravity position[x,y]   
    """

    totalX = 0
    totalY = 0
    cnt = 0

    for p in con.points:
        if(p.type != 'offcurve'):
            totalX += p.x
            totalY += p.y
            cnt += 1    

    averageX = int(totalX / cnt)
    averageY = int(totalY / cnt)

    return [averageX,averageY]
    
class PositionState:
    def __init__(self,con,conNumber):
        self.con = con
        self.conNumber = conNumber
        
"""
output configure : [[first] , [middle], [final]]
"""
    
def case1(glyph):
    """
    middle one , no final
    """
    
    point_list = list()
    
    first = list()
    middle = list()
    final = list()
    output = list()
    
    maxx = glyph.bounds[2]
    minx = glyph.bounds[0]
    
    dist_x = maxx - minx
    
    for i in range(0,len(glyph.contours)):
        #temp_list = getGravity(glyph.contours[i])
        temp_object = PositionState(glyph.contours[i],i)
        point_list.append(temp_object)
    
    result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
    middle.append(result[-1].conNumber)
    
    for i in range(0, len(result) - 1):
        first.append(result[i].conNumber)
    
    output.append(first)
    output.append(middle)
    output.append(final)
    
    return output
    
def case2(glyph):
    """
    middle one, exist final
    """
    
    point_list = list()
    
    first = list()
    middle = list()
    final = list()
    output = list()
    
    maxx = glyph.bounds[2]
    minx = glyph.bounds[0]
    miny = glyph.bounds[1]
    maxy = glyph.bounds[3]
    
    dist_y = maxy - miny
    dist_x = maxx - minx
    
    temp_x1 = dist_x * 0.4
    temp_x2 = dist_x * 0.7
    
    temp_y1 = dist_y * 0.45
    temp_y2 = dist_y * 0.5
    
    for i in range(0,len(glyph.contours)):
        temp_list = getGravity(glyph.contours[i])
        if (temp_list[0] >= minx + temp_x1) and (temp_list[0] <= minx + temp_x2):
            if temp_list[1] <= miny + temp_y2:
                final.append(i)
            else:
                temp_object = PositionState(glyph.contours[i],i)
                point_list.append(temp_object)
        else:
            if temp_list[1] <= miny + temp_y1:
                final.append(i)
            else:
                temp_object = PositionState(glyph.contours[i],i)
                point_list.append(temp_object)
                
    result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
    middle.append(result[-1].conNumber)
    
    for i in range(0, len(result) - 1):
        first.append(result[i].conNumber)
    
    output.append(first)
    output.append(middle)
    output.append(final)
    
    return output
    
def case3(glyph):
    """
    middle two, no final
    """
    
    point_list = list()
    
    first = list()
    middle = list()
    final = list()
    output = list()
    
    maxx = glyph.bounds[2]
    minx = glyph.bounds[0]
    
    dist_x = maxx - minx
    
    for i in range(0,len(glyph.contours)):
        #temp_list = getGravity(glyph.contours[i])
        temp_object = PositionState(glyph.contours[i],i)
        point_list.append(temp_object)
    
    result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
    middle.append(result[-1].conNumber)
    middle.append(result[-2].conNumber)
    
    for i in range(0, len(result) - 2):
        first.append(result[i].conNumber)
    
    output.append(first)
    output.append(middle)
    output.append(final)
    
    return output
    
def case4(glyph):
    """
    middle two, exist final
    """
    
    point_list = list()
    
    first = list()
    middle = list()
    final = list()
    output = list()
    
    maxx = glyph.bounds[2]
    minx = glyph.bounds[0]
    miny = glyph.bounds[1]
    maxy = glyph.bounds[3]
    
    dist_y = maxy - miny
    dist_x = maxx - minx
    
    temp_x1 = dist_x * 0.4
    temp_x2 = dist_x * 0.7
    
    temp_y1 = dist_y * 0.45
    temp_y2 = dist_y * 0.5
    
    for i in range(0,len(glyph.contours)):
        temp_list = getGravity(glyph.contours[i])
        if (temp_list[0] >= minx + temp_x1) and (temp_list[0] <= minx + temp_x2):
            if temp_list[1] <= miny + temp_y2:
                final.append(i)
            else:
                temp_object = PositionState(glyph.contours[i],i)
                point_list.append(temp_object)
        else:
            if temp_list[1] <= miny + temp_y1:
                final.append(i)
            else:
                temp_object = PositionState(glyph.contours[i],i)
                point_list.append(temp_object)
                
    result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
    middle.append(result[-1].conNumber)
    middle.append(result[-2].conNumber)
    
    for i in range(0, len(result) - 2):
        first.append(result[i].conNumber)
    
    output.append(first)
    output.append(middle)
    output.append(final)
    
    return output
    

def case5(glyph):
    """
    middle three, does not matter final
    """
    
    point_list = list()
    
    first = list()
    middle = list()
    final = list()
    output = list()
    
    
    for i in range(0,len(glyph.contours)):
        #temp_list = getGravity(glyph.contours[i])
        temp_object = PositionState(glyph.contours[i],i)
        point_list.append(temp_object)
                
    result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
    #값이 가장 큰 것이 중성
    #중성 컨투어 중 miny값 이하면 종성 아니면 초성
    middle.append(result[-1].conNumber)
    cut_line = result[-1].con.bounds[1]
    del(result[-1])
    
    for i in range(0, len(result)):
        if result[i].con.bounds[1] >= cut_line:
            first.append(result[i].conNumber)
        else:
            final.append(result[i].conNumber)
    
    output.append(first)
    output.append(middle)
    output.append(final)
    
    return output
    

def case7(glyph):
    """
    middle four, exist final
    """
    
    point_list = list()
    
    first = list()
    middle = list()
    final = list()
    output = list()
    
    
    for i in range(0,len(glyph.contours)):
        #temp_list = getGravity(glyph.contours[i])
        temp_object = PositionState(glyph.contours[i],i)
        point_list.append(temp_object)
    
    result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
    middle.append(result[-1].conNumber)
    
    for i in range(0,len(result)-1):
        first.append(result[i].conNumber)
    
    output.append(first)
    output.append(middle)
    output.append(final)
    
    return output
    
    
def case8(glyph):
    """
    middle four, exist final
    """
    
    point_list = list()
    
    first = list()
    middle = list()
    final = list()
    output = list()
    
    miny = glyph.bounds[1]
    maxy = glyph.bounds[3]
    
    dist_y = maxy - miny
    
    temp_y = dist_y * 0.4
    
    for i in range(0,len(glyph.contours)):
        temp_list = getGravity(glyph.contours[i])
        if temp_list[1] <= miny + temp_y:
            final.append(i)
        else:
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
                
    result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
    middle.append(result[-1].conNumber)
    
    for i in range(0, len(result) - 1):
        first.append(result[i].conNumber)
    
    output.append(first)
    output.append(middle)
    output.append(final)
    
    return output

def case9(glyph):
    """
    middle five, no final
    """
    
    point_list = list()
    
    first = list()
    middle = list()
    final = list()
    output = list()
    
    
    for i in range(0,len(glyph.contours)):
        #temp_list = getGravity(glyph.contours[i])
        temp_object = PositionState(glyph.contours[i],i)
        point_list.append(temp_object)
    
    #중성을 찾는 과정            
    result1 = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    middle.append(result1[-1].conNumber)
    del(result1[-1])
    
    result2 = sorted(result1, key = lambda PositionState: PositionState.con.bounds[1])
    middle.append(result2[0].conNumber)
    del(result2[0])
    
    for i in range(0, len(result2)):
        first.append(result2[i].conNumber)
    
    output.append(first)
    output.append(middle)
    output.append(final)
    
    return output
    
def case10(glyph):
    """
    middle five, exist final
    """
    
    point_list = list()
    
    first = list()
    middle = list()
    final = list()
    output = list()
    
    miny = glyph.bounds[1]
    maxy = glyph.bounds[3]
    minx = glyph.bounds[0]
    maxx = glyph.bounds[2]
    
    dist_y = maxy - miny
    dist_x = maxx - minx
    
    temp_y1 = dist_y * 0.42
    temp_y2 = dist_y * 0.3
    temp_x = dist_x * 0.5
    
    for i in range(0,len(glyph.contours)):
        temp_list = getGravity(glyph.contours[i])
        if (temp_list[1] <= miny + temp_y2) and (temp_list[0] <= minx + temp_x):
            final.append(i)
        elif(temp_list[1] <= miny + temp_y1) and (temp_list[0] > minx + temp_x):
            final.append(i)
        else:
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
    
    #중성을 찾는 과정            
    result1 = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    middle.append(result1[-1].conNumber)
    del(result1[-1])
    
    result2 = sorted(result1, key = lambda PositionState: PositionState.con.bounds[1])
    middle.append(result2[0].conNumber)
    del(result2[0])
    
    for i in range(0, len(result2)):
        first.append(result2[i].conNumber)
    
    output.append(first)
    output.append(middle)
    output.append(final)
    
    return output


def case11(glyph):
    """
    middle six, no final
    """
    
    point_list = list()
    
    first = list()
    middle = list()
    final = list()
    output = list()
    
    miny = glyph.bounds[1]
    maxy = glyph.bounds[3]
    minx = glyph.bounds[0]
    maxx = glyph.bounds[2]
    
    dist_y = maxy - miny
    dist_x = maxx - minx
    
    temp_y1 = dist_y * 0.42
    temp_y2 = dist_y * 0.3
    temp_x = dist_x * 0.5
    
    for i in range(0,len(glyph.contours)):
        temp_object = PositionState(glyph.contours[i],i)
        point_list.append(temp_object)
    
    #중성을 찾는 과정            
    result1 = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    middle.append(result1[-1].conNumber)
    del(result1[-1])
    middle.append(result1[-1].conNumber)
    del(result1[-1])
    
    result2 = sorted(result1, key = lambda PositionState: PositionState.con.bounds[1])
    middle.append(result2[0].conNumber)
    del(result2[0])
    
    for i in range(0, len(result2)):
        first.append(result2[i].conNumber)
    
    output.append(first)
    output.append(middle)
    output.append(final)
    
    return output
    

def case12(glyph):
    """
    middle five, exist final
    """
    
    point_list = list()
    
    first = list()
    middle = list()
    final = list()
    output = list()
    
    miny = glyph.bounds[1]
    maxy = glyph.bounds[3]
    minx = glyph.bounds[0]
    maxx = glyph.bounds[2]
    
    dist_y = maxy - miny
    dist_x = maxx - minx
    
    temp_y1 = dist_y * 0.42
    temp_y2 = dist_y * 0.3
    temp_x = dist_x * 0.4
    
    for i in range(0,len(glyph.contours)):
        temp_list = getGravity(glyph.contours[i])
        if (temp_list[1] <= miny + temp_y2) and (temp_list[0] <= minx + temp_x):
            final.append(i)
        elif(temp_list[1] <= miny + temp_y1) and (temp_list[0] > minx + temp_x):
            final.append(i)
        else:
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
    
    #중성을 찾는 과정            
    result1 = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    middle.append(result1[-1].conNumber)
    del(result1[-1])
    middle.append(result1[-1].conNumber)
    del(result1[-1])
    
    result2 = sorted(result1, key = lambda PositionState: PositionState.con.bounds[1])
    middle.append(result2[0].conNumber)
    del(result2[0])
    
    for i in range(0, len(result2)):
        first.append(result2[i].conNumber)
    
    output.append(first)
    output.append(middle)
    output.append(final)
    
    return output
    

#testFont = CurrentFont()

# g = CurrentGlyph()

# l = case2(g)

# print(l)

#first_one = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ','ㄲ','ㄸ','ㅃ','ㅆ','ㅉ']

#middle_one = ['ㅏ','ㅑ','ㅓ','ㅕ','ㅣ','ㅐ']
#middle_two = ['ㅔ','ㅖ','ㅒ']
#middle_three = ['ㅗ','ㅛ','ㅜ','ㅠ','ㅡ']
#middle_four = ['ㅘ','ㅚ','ㅟ', 'ㅢ','ㅙ']
#middle_five = ['ㅝ']
#middle_six = ['ㅞ']


#final_one = ['ㄱ','ㄲ','ㄱㅅ','ㄴ','ㄴㅈ','ㄴㅎ','ㄷ','ㄹ','ㄹㄱ','ㄹㅁ','ㄹㅂ','ㄹㅅ','ㄹㅌ','ㄹㅍ','ㄹㅎ','ㅁ','ㅂ','ㅂㅅ','ㅅ','ㅆ','ㅇ','ㅈ','ㅋ','ㅌ','ㅍ','ㅊ','ㅎ']

#check = 0

#for gly in testFont:
    #print(check)
    #check = check + 1
    #puc = parseUnicodeController(gly.unicode)
    #chars = puc.getChars()
    #print(chars)
    #if (chars[0] in first_one) and (chars[1] in middle_three):
        #print(chars)
        #l = case5(gly)
        #for i in l[1]:
            #gly.contours[i].selected = True
            
            
#g = CurrentGlyph()
#puc = parseUnicodeController(g.unicode)
#chars = puc.getChars()

#print(chars)
#if(chars[2] )

                


    
        