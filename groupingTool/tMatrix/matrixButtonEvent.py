from groupingTool.tMatrix.PhaseTool import *
from groupingTool.tMatrix.groupPointMatch import *
from jsonConverter.converter import *
from rbWindow.ExtensionSetting import extensionValue
from rbWindow.ExtensionSetting.extensionValue import *
from mojo.extensions import *
from mojo.roboFont import CurrentGlyph
from attributeTool.strokeAttribute import *
"""
2020/02/24
Created by heesup Kim
"""
def mselectAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []
    prevPointList = list()
    restoreStack = getExtensionDefault(DefaultKey+".restoreStack")

    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        if(standardMatrix.con != contoursList[i]):
            for sp in standardMatrix.con.points:
                if(sp.selected == True):
                    controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        mPoint = controllerList[i].matchPoint()
        if mPoint is not None:
            controllerList[i].mgiveSelected(mPoint)
            tmp = list()
            tmp.append(mPoint); tmp.append(mPoint.name)
            prevPointList.append(tmp)
        

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name)
        prevPointList.append(tmp)



    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)
    CurrentFont().update()
    CurrentFont().save(CurrentFont().path)

def mpenPairAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []
    prevPointList = list()
    restoreStack = getExtensionDefault(DefaultKey+".restoreStack")




    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        if(standardMatrix.con != contoursList[i]):
            for sp in standardMatrix.con.points:
                if(sp.selected == True):
                    controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        mPoint = controllerList[i].matchPoint()
        controllerList[i].mgiveAttrPenPair(mPoint)

        if mPoint is not None:
            
            tmp = list()
            tmp.append(mPoint); tmp.append(mPoint.name)
            prevPointList.append(tmp)
        

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name)
        prevPointList.append(tmp)

    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)
    
    CurrentFont().update()
    CurrentFont().save(CurrentFont().path)

def mdependXAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []
    prevPointList = list()
    restoreStack = getExtensionDefault(DefaultKey+".restoreStack")



    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        if(standardMatrix.con != contoursList[i]):
            for sp in standardMatrix.con.points:
                if(sp.selected == True):
                    controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        mPoint = controllerList[i].matchPoint()
        controllerList[i].mgiveDependX(mPoint)

        if mPoint is not None:
            
            tmp = list()
            tmp.append(mPoint); tmp.append(mPoint.name)
            prevPointList.append(tmp)
        


    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name)
        prevPointList.append(tmp)

    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)
    CurrentFont().update()
    CurrentFont().save(CurrentFont().path)

def mdependYAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []
    prevPointList = list()
    restoreStack = getExtensionDefault(DefaultKey+".restoreStack")


    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        if(standardMatrix.con != contoursList[i]):
            for sp in standardMatrix.con.points:
                if(sp.selected == True):
                    controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        mPoint = controllerList[i].matchPoint()
        if mPoint is not None:
            controllerList[i].mgiveDependY(mPoint)
            tmp = list()
            tmp.append(mPoint); tmp.append(mPoint.name)
            prevPointList.append(tmp)
        


    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name)
        prevPointList.append(tmp)

    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

    CurrentFont().update()
    CurrentFont().save(CurrentFont().path)

def minnerFillAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []
    prevPointList = list()
    restoreStack = getExtensionDefault(DefaultKey+".restoreStack")



    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        if(standardMatrix.con != contoursList[i]):
            for sp in standardMatrix.con.points:
                if(sp.selected == True):
                    controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        mPoint = controllerList[i].con.points[0]
        controllerList[i].mgiveInnerFill(mPoint)    
        tmp = list()
        tmp.append(mPoint); tmp.append(mPoint.name)
        prevPointList.append(tmp)
    

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name)
        prevPointList.append(tmp)

    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

    CurrentFont().update()
    CurrentFont().save(CurrentFont().path)
        
def mdeleteAttribute(groupDict,standardMatrix,attribute):
    controllerList = []
    contoursList = []
    prevPointList = list()
    restoreStack = getExtensionDefault(DefaultKey+".restoreStack")

    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        for sp in standardMatrix.con.points:
            if(sp.selected == True):
                controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    if attribute == "innerType" or attribute == "sound" or attribute == "char" or attribute == "formType":
        for i in range(0,len(controllerList)):
            mPoint = controllerList[i].con.points[0]
            controllerList[i].mdeleteAttr(attribute,mPoint)
            if mPoint is not None:
                tmp = list()
                tmp.append(mPoint); tmp.append(mPoint.name)
                prevPointList.append(tmp)
    else:
        for i in range(0,len(controllerList)):
            mPoint = controllerList[i].matchPoint()
            controllerList[i].mdeleteAttr(attribute,mPoint)
            if mPoint is not None:
                tmp = list()
                tmp.append(mPoint); tmp.append(mPoint.name)
                prevPointList.append(tmp)
        

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name)
        prevPointList.append(tmp)

    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

    CurrentFont().update()
    CurrentFont().save(CurrentFont().path)

def mgiveStrokeAttribute(groupDict,standardMatrix):

    controllerList = []
    contoursList = []
    prevPointList = list()
    restoreStack = getExtensionDefault(DefaultKey+".restoreStack")

    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        for sp in standardMatrix.con.points:
            if(sp.selected == True):
                controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        mPoint = controllerList[i].matchPoint()
        controllerList[i].mgiveStroke(mPoint)
        
        if mPoint is not None:
            
            tmp = list()
            tmp.append(mPoint); tmp.append(mPoint.name)
            prevPointList.append(tmp)
        

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name)
        prevPointList.append(tmp)
    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

    CurrentFont().update()
    CurrentFont().save(CurrentFont().path)