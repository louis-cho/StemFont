import os
import json
from xml.etree import ElementTree as et
from fontParts.fontshell.contour import RContour
from fontParts.fontshell.glyph import RGlyph

def set_stroke(point,value) -> bool:
    """
    획에 대한 정보를 저장해주는 함수
    
    Args:
        path :: str
            폰트 파일의 경로
        point:: RPoint
    """
    #폰트 파일의 경로를 찾아줌
    contour = point.getParent()
    glyph = contour.getParent()
    font = glyph.getParent()
    
    path = font.path
    path += "/glyphs"

    value = str(value)
    
    #파일들을 받아오고 해당 point가 들어있는 파일을 가져옴
    files = os.listdir(path)
    for i in range(0, len(files)):
        search_file = files[i]
        tree = et.parse(path + "/" + search_file)
        glyph_info = tree.getroot()
        glyph_name = glyph_info.get("name")
        
        if glyph.name == glyph_name:
            break
    
    
    outline = glyph_info.find("outline")
    
    contours_info = outline.getchildren()
    
    for contour_info in contours_info:
        for point_info in contour_info.getchildren():
            if (float(point_info.get('x')) != point.x) or (float(point_info.get('y')) != point.y):
                continue
            else:
                information = point_info.get("stroke")
                if information is not None and value in information:
                    return True
                if information is not None:
                    value = information  + "," + value
                else:
                    vlaue = information
                point_info.set("stroke",value)
                tree.write(path + "/" + search_file, encoding="UTF-8", xml_declaration=True)
                return True
            
    return False

def get_stroke(point) -> list:
    """
    획에 대한 정보를 가져오는 함수
    
    Args :
        point :: RPoint
    """
    #폰트 파일의 경로를 찾아줌
    contour = point.getParent()
    glyph = contour.getParent()
    font = glyph.getParent()
    
    path = font.path
    path += "/glyphs"
    
    #파일들을 받아오고 해당 point가 들어있는 파일을 가져옴
    files = os.listdir(path)
    for i in range(0, len(files)):
        search_file = files[i]
        tree = et.parse(path + "/" + search_file)
        glyph_info = tree.getroot()
        glyph_name = glyph_info.get("name")
        
        if glyph.name == glyph_name:
            break
    
    
    outline = glyph_info.find("outline")
    
    contours_info = outline.getchildren()
    
    for contour_info in contours_info:
        for point_info in contour_info.getchildren():
            if (float(point_info.get('x')) != point.x) or (float(point_info.get('y')) != point.y):
                continue
            else:
                stroke_info = point_info.get("stroke")
                if stroke_info is not None:
                    return stroke_info.split(',')
                else:
                    return list()
            
    return list()

def delete_stroke(point,value) -> bool:
    """
    획에 대한 정보를 삭제하는 함수
    
    Args :
        point :: RPoint
        value :: str
            삭제하고자 하는 값
    """
    #폰트 파일의 경로를 찾아줌
    contour = point.getParent()
    glyph = contour.getParent()
    font = glyph.getParent()
    
    path = font.path
    path += "/glyphs"
    
    #파일들을 받아오고 해당 point가 들어있는 파일을 가져옴
    files = os.listdir(path)
    for i in range(0, len(files)):
        search_file = files[i]
        tree = et.parse(path + "/" + search_file)
        glyph_info = tree.getroot()
        glyph_name = glyph_info.get("name")
        
        if glyph.name == glyph_name:
            break
    
    
    outline = glyph_info.find("outline")
    
    contours_info = outline.getchildren()
    
    for contour_info in contours_info:
        for point_info in contour_info.getchildren():

            if (float(point_info.get('x')) != point.x) or (float(point_info.get('y')) != point.y):
                continue
            else:
                stroke_info = point_info.get("stroke")
                print(stroke_info)
                stroke_remove = value + ','
                print(stroke_remove)
                stroke_info = stroke_info.replace(value + ',' , '')
                print(stroke_info)
                point_info.set("stroke",stroke_info)
                tree.write(path + "/" + search_file, encoding="UTF-8", xml_declaration=True)
                return True
            
    return False