from parseSyllable.utility.contourDistributionChart import *
"""
2020/02/27
create by Kim Heesup

진행상황 - 18가지 케이스
""" 
def case1(glyph,contour,chars):

    conGravityPosition = getGravity(contour)

    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10

    dist_x = maxx - minx 

    temp_x = dist_x * 0.7
    lx = []
    lx.append(minx + temp_x)

    if conGravityPosition[0] <= lx[0]:
        return 0
    else:
        return 1

def case2(glyph,contour,chars):
    
    conGravityPosition = getGravity(contour)

    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10

    dist_x = maxx - minx 

    temp_x = dist_x * 0.5
    lx = []
    lx.append(minx + temp_x)

    if conGravityPosition[0] <= lx[0]:
        return 0
    else:
        return 1

def case3(glyph,contour,chars):
    
    conGravityPosition = getGravity(contour)
    
    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10

    dist_x = maxx - minx 
    
    if chars[0] != 'ㅃ':
        temp_x = dist_x * 0.65
    else:
        temp_x = dist_x * 0.689
    lx = []
    lx.append(minx + temp_x)

    if conGravityPosition[0] <= lx[0]:
        return 0
    else:
        return 1                    

def case4(glyph,contour,chars):

    conGravityPosition = getGravity(contour)

    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10

    dist_x = maxx - minx 

    temp_x = dist_x * 0.59
    lx = []
    lx.append(minx + temp_x)

    if conGravityPosition[0] <= lx[0]:
        return 0
    else:
        return 1

def case6(glyph,contour,chars):
    
    conGravityPosition = getGravity(contour)
    middle_four_prime = ['ㅚ','ㅝ','ㅟ','ㅙ']

    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10
    maxy = getMaxYValue(glyph) + 10
    miny = getMinYValue(glyph) - 10

    dist_x = maxx - minx 
    dist_y = maxy - miny 
    
    if (chars[0] == 'ㅂ') and(chars[1] not in middle_four_prime):
        temp_x = dist_x * 0.65
    else:
        temp_x = dist_x * 0.52
    temp_y = dist_y * 0.45

    lx = []
    ly = []

    lx.append(minx + temp_x)
    ly.append(miny + temp_y)

    if ((conGravityPosition[0] <= lx[0]) and (conGravityPosition[1] >= ly[0])):
        return 0
    else:
        return 1        

def case7(glyph,contour,chars):
    conGravityPosition = getGravity(contour)

    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10
    maxy = getMaxYValue(glyph) + 10
    miny = getMinYValue(glyph) - 10

    dist_x = maxx - minx 
    dist_y = maxy - miny

    lx = []
    ly = []

    temp_x = dist_x * 0.4
    lx.append(minx + temp_x)
    temp_x = dist_x * 0.6
    lx.append(minx + temp_x)
    temp_y = dist_y * 0.5
    ly.append(miny + temp_y)

    if((conGravityPosition[0] >= lx[0]) and (conGravityPosition[0] <= lx[1]) and (conGravityPosition[1] <= ly[0])):
        return 1
    else:
        return 0

def case8(glyph,contour,chars):
    
    conGravityPosition = getGravity(contour)
    

    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10
    maxy = getMaxYValue(glyph) + 10
    miny = getMinYValue(glyph) - 10

    dist_x = maxx - minx 
    dist_y = maxy - miny

    lx = []
    ly = []
    
    if chars[0] != 'ㅃ':
        temp_x = dist_x * 0.63
        lx.append(minx + temp_x)
    else:
        temp_x = dist_x * 0.735
        lx.append(minx + temp_x)
    temp_y = dist_y * 0.6
    ly.append(miny + temp_y)

    if((conGravityPosition[0] <= lx[0]) and (conGravityPosition[1] >= ly[0])):
        return 0
    else:
        return 1       

def case9(glyph,contour,chars):

    conGravityPosition = getGravity(contour)

    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10
    maxy = getMaxYValue(glyph) + 10
    miny = getMinYValue(glyph) - 10

    dist_x = maxx - minx 
    dist_y = maxy - miny

    lx = []
    ly = []

    temp_x = dist_x * 0.7
    lx.append(minx + temp_x)
    temp_y = dist_y * 0.5
    ly.append(miny + temp_y)

    if(conGravityPosition[1] >= ly[0]):
        if(conGravityPosition[0] <= lx[0]):
            return 0
        else:
            return 1
    else:
        return 2

def case10(glyph,contour,chars):
    conGravityPosition = getGravity(contour)

    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10
    maxy = getMaxYValue(glyph) + 10
    miny = getMinYValue(glyph) - 10

    dist_x = maxx - minx 
    dist_y = maxy - miny

    lx = []
    ly = []

    temp_x = dist_x * 0.5
    lx.append(minx + temp_x)
    temp_y = dist_y * 0.45
    ly.append(miny + temp_y)

    if(conGravityPosition[1] >= ly[0]):
        if(conGravityPosition[0] <= lx[0]):
            return 0
        else:
            return 1
    else:
        return 2

def case11(glyph,contour,chars):
    conGravityPosition = getGravity(contour)

    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10
    maxy = getMaxYValue(glyph) + 10
    miny = getMinYValue(glyph) - 10

    dist_x = maxx - minx 
    dist_y = maxy - miny

    lx = []
    ly = []

    temp_x = dist_x * 0.65
    lx.append(minx + temp_x)
    temp_y = dist_y * 0.5
    ly.append(miny + temp_y)

    if(conGravityPosition[1] >= ly[0]):
        if(conGravityPosition[0] <= lx[0]):
            return 0
        else:
            return 1
    else:
        return 2

def case12(glyph,contour,chars):
    conGravityPosition = getGravity(contour)

    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10
    maxy = getMaxYValue(glyph) + 10
    miny = getMinYValue(glyph) - 10

    dist_x = maxx - minx 
    dist_y = maxy - miny

    lx = []
    ly = []

    temp_x = dist_x * 0.55
    lx.append(minx + temp_x)
    temp_y = dist_y * 0.5
    ly.append(miny + temp_y)

    if(conGravityPosition[1] >= ly[0]):
        if(conGravityPosition[0] <= lx[0]):
            return 0
        else:
            return 1
    else:
        return 2

def case14(glyph,contour,chars):
    conGravityPosition = getGravity(contour)
    first_one_prime = ['ㅎ']

    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10
    maxy = getMaxYValue(glyph) + 10
    miny = getMinYValue(glyph) - 10

    dist_x = maxx - minx 
    dist_y = maxy - miny

    lx = []
    ly = []

    temp_x = dist_x * 0.4
    lx.append(minx + temp_x)
    temp_x = dist_x * 0.52
    lx.append(minx + temp_x)
    temp_y = dist_y * 0.3
    ly.append(miny + temp_y)
    temp_y = dist_y * 0.5
    ly.append(miny + temp_y)
    if chars[0] in first_one_prime:
        temp_y = dist_y * 0.566
        ly.append(miny + temp_y)
    else:
        temp_y = dist_y * 0.596
        ly.append(miny + temp_y)

    if conGravityPosition[0] <= lx[0]:
        if conGravityPosition[1] <= ly[0]:
            return 2
        elif (conGravityPosition[1] > ly[0]) and (conGravityPosition[1] <= ly[2]):
            return 1
        else:
            return 0
    elif (lx[0] < conGravityPosition[0]) and (conGravityPosition[0] < lx[1]):
        if conGravityPosition[1] <= ly[1]:
            return 2
        else:
            return 0
    else:
        if conGravityPosition[1] <= ly[1]:
            return 2
        else:
            return 1                   
  
def case16(glyph,contour,chars):
    conGravityPosition = getGravity(contour)
    
    middle_four_prime = ['ㅚ','ㅝ','ㅟ','ㅙ']
    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10
    maxy = getMaxYValue(glyph) + 10
    miny = getMinYValue(glyph) - 10

    dist_x = maxx - minx 
    dist_y = maxy - miny

    lx = []
    ly = []

    temp_x = dist_x * 0.4
    lx.append(minx + temp_x)
    if chars[1] in middle_four_prime:
        temp_x = dist_x * 0.56
        lx.append(minx + temp_x)
    else:
        temp_x = dist_x * 0.52
        lx.append(minx + temp_x)
    temp_y = dist_y * 0.3
    ly.append(miny + temp_y)
    temp_y = dist_y * 0.5
    ly.append(miny + temp_y)
    temp_y = dist_y * 0.587
    ly.append(miny + temp_y)
    if chars[1] in middle_four_prime:
        temp_y = dist_y * 0.7
        ly.append(miny + temp_y)
    
    if chars[1] not in middle_four_prime:
        if conGravityPosition[0] <= lx[0]:
            if conGravityPosition[1] <= ly[0]:
                return 2
            elif (conGravityPosition[1] > ly[0]) and (conGravityPosition[1] <= ly[2]):
                return 1
            else:
                return 0
        elif (lx[0] < conGravityPosition[0]) and (conGravityPosition[0] < lx[1]):
            if conGravityPosition[1] <= ly[1]:
                return 2
            else:
                return 0
        else:
            if conGravityPosition[1] <= ly[1]:
                return 2
            else:
                return 1
    else:
        if conGravityPosition[0] <= lx[0]:
            if conGravityPosition[1] <= ly[0]:
                return 2
            elif (conGravityPosition[1] > ly[0]) and (conGravityPosition[1] <= ly[2]):
                return 1
            else:
                return 0
        elif (lx[0] < conGravityPosition[0]) and (conGravityPosition[0] < lx[1]):
            if conGravityPosition[1] <= ly[1]:
                return 2
            else:
                return 0
        else:
            if conGravityPosition[1] <= ly[1]:
                return 2
            elif (ly[1] < conGravityPosition[1]) and (conGravityPosition[1] <= ly[3]):
                return 1
            else:
                return 0