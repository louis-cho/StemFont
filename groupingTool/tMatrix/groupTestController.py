from groupingTool.tMatrix.PhaseTool import *
import math
import numpy as np

"""
    create by Kim heesup
"""

class groupTestController:
    def __init__(self,matrix,k):
        """
        Matrix 방법을 이용한 그룹화 진행 
        
        Args:
            matrix :: Matrix object
                기준이 되는 메트릭스

            k :: int
                오차율을 조절
        """
        self.k = k
        self.matrix = matrix

        self.standardMatrix = np.array(self.matrix.getMatrix())
    def conCheckGroup2(self,con):
        """
        현재의 메트릭스에 대하여 새로운 Contour에 대하여 같은 그룹인지 조사
        
        Args:
            con :: RContour
                조사하고자 하는 컨투어
            
        Returns:
            포함 여부 :: Boolean
                포함 - True, 포함 안함 - False
        """
        sl = self.matrix.getDivideStatus() #standard position
        
        newMatrix = Matrix(con, self.matrix.getdivk())
        
        cl = newMatrix.getDivideStatus()

        #grouping by hor,val
        compareX = []
        compareY = []

        nsl = np.array(sl)
        ncl = np.array(cl)

        ncompare = np.abs(nsl - ncl)
        

        if np.all(ncompare <= self.k) == True:
            return con
        else:
            return None

    def conCheckGroup(self,con):
        """
        2020/03/17
        create by Kim heesup

        현재의 메트릭스에 대하여 새로운 Contour에 대하여 같은 그룹인지 조사
        (한문을 위해 제작하였으나 현재는 한글, 한자 모두에 적용)

        Args:
            con :: RContour
                조사하고자 하는 컨투어
            
        Returns:
            포함 여부 :: Boolean
                포함 - True, 포함 안함 - False
        """

        compareMatrix = np.array(Matrix(con,self.matrix.getdivk()).getMatrix())

        diffMatrixCount = (self.matrix.getdivk() ** 2) * (self.k/100)

        compareStat = (self.standardMatrix == compareMatrix)

        ##########################윤려를 위한 임시 코드#############################
        compMatrix = Matrix(con, self.matrix.getdivk())
        standardCon = self.matrix.con
        compareCon = con
        if len(standardCon.points) == 4:
            if len(compareCon.points) != 4:
                return None
            isStandardHorizontal = None
            isCompareHorizontal = None
            if self.matrix.getTermX() - self.matrix.getTermY() > 50:
                isStandardHorizontal = True
            elif self.matrix.getTermY() - self.matrix.getTermX() > 50:
                isStandardHorizontal = False
            if compMatrix.getTermX() - compMatrix.getTermY() > 50:
                isCompareHorizontal = True
            elif compMatrix.getTermY() - compMatrix.getTermX() > 50:
                isCompareHorizontal = False
            if isStandardHorizontal != isCompareHorizontal and isStandardHorizontal != None:
                return None
        ########################################################################
        countDiff = compareStat[np.where(compareStat == False)]

        if len(countDiff) <= diffMatrixCount:
            return con
        else:
            return None



    def glyphCheckGroup(self,glyph):
        """
        글리프에 대햐여 해당 메크릭스와 같은 그룹인지 판별하는 함수
        
        Args:
            glyph :: RGlyph
                조사하고자 하는 클리프
            
        Returns:
            포함 여부 :: Boolean
                포함 - True, 포함 안함 - False
        """ 

        rl = []
        
        for con in glyph.contours:
            re = self.conCheckGroup(con)
            if (re != None):
                rl.append([glyph,con])

        if(len(rl) == 0):
            return None
        else:
            return rl