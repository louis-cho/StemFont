"""
2020/02/27
create by Kim Heesup

진행상황 - 18가지 케이스
"""
class notGlyph(Exception):
    def __init__(self):
        super().__init__('glyph 객체가 아닙니다.')


def getMaxXValue(glyph):
    """
    Get maximum x value about glyph
    
    Args:
        glyph : RGlyph
    Return:
        maximum x value
    """

    '''try:
        if(glyph.__class__ != RGlyph):
            raise notGlyph
    except Exception as e:
        print('예외가 발생했습니다.',e)'''

    max = -100000
    
    for con in glyph.contours:
        for p in con.points:
            if(p.type != 'offcurve'):
                if(max < p.x):
                    max = p.x

    return max

def getMinXValue(glyph):
    """
    Get minimum x value about glyph
    
    Args:
        con : RGlyph
    Return:
        minimum x value
    """

    '''try:
        if(glyph.__class__ != RGlyph):
            raise notGlyph
    except Exception as e:
        print('예외가 발생했습니다.',e)'''
    
    min = 100000

    for con in glyph.contours:
        for p in con.points:
            if(p.type != 'offcurve'):
                if(min > p.x):
                    min = p.x   
    
    return min

def getMaxYValue(glyph):
    """
    Get maximum y value about glyph
    
    Args:
        con : RGlyph
    Return:
        maximum y value
    """

    '''try:
        if(glyph.__class__ != RGlyph):
            raise notGlyph
    except Exception as e:
        print('예외가 발생했습니다.',e)'''

    max = -100000

    for con in glyph.contours:
        for p in con.points:
            if(p.type != 'offcurve'):
                if(max < p.y):
                    max = p.y
    
    return max

def getMinYValue(glyph):
    """
    Get minimum y value about glyph
    
    Args:
        con :: RGlyph
    Return:
        minimum y value
    """
    '''try:
        if(glyph.__class__ != RGlyph):
            raise notGlyph
    except Exception as e:
        print('예외가 발생했습니다.',e)'''

    min = 100000

    for con in glyph.contours:
        for p in con.points:
            if(p.type != 'offcurve'):
                if(min > p.y):
                    min = p.y
    
    return min    

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

def getContourPosition(glyph,con,kx,ky):
    """
    get contour position in glyph that is divided matrix

    Args :
        glyph :: RGlyph
        con :: RContour
        kx :: int
            value that divide x axis
        ky :: int
            value that divide y axis
    Return :: list
        point's position
                  
    """
    conGravityPosition = getGravity(con)

    maxx = getMaxXValue(glyph) + 10
    minx = getMinXValue(glyph) - 10
    maxy = getMaxYValue(glyph) + 10
    miny = getMinYValue(glyph) - 10

    dis_x = maxx - minx
    dis_y = maxy - miny 

    term_x = float(dis_x / kx)
    term_y = float(dis_y / ky)

    compart_x = []
    compart_y = []

    compart_x.append(minx)
    compart_y.append(miny)

    num = 0

    while compart_x[num] + term_x < maxx:
        compart_x.append(compart_x[num] + term_x)
        num = num+1
    compart_x.append(maxx)

    num = 0
    
    while compart_y[num] + term_y < maxy:
        compart_y.append(compart_y[num] + term_y)
        num = num+1
    compart_y.append(maxy)
    
    position_x = -1
    position_y = -1

    for i in range(0,len(compart_x)-1):
        if(compart_x[i] <= conGravityPosition[0]):
            position_x = i
        else:
            break

    for i in range(0,len(compart_y)-1):
        if(compart_y[i] <= conGravityPosition[1]):
            position_y = i
        else:
            break

    rl = [position_x, position_y]
    
    return rl