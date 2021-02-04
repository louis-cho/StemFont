from groupingTool.tTopology.topologyAssignment import *
from fwig.tools import attributetools as at

"""
    Create by Heesup Kim
"""

class topologyJudgementController:
    """
    Topology 방법을 이용하여 그룹화를 시킴

    Args: 
        sCon :: RContour
            기준이 되는 컨투어
        cCon :: RContour
            비교를 하고자 하는 컨투어
        k :: int
            margin값
    """
    def __init__(self,sCon,cCon,k):
        self.sCon = sCon
        self.cCon = cCon
        self.k = k
        
        self.sCheckCon = checkCon(sCon,self.k)
        self.cCheckCon = checkCon(cCon,self.k)
        
    def topologyJudgement(self):
        """
        비교 컨투어가 같은 그룹인지 확인해 줌
        
        Returns: 
            참이면 포함 포함을 안하면 거짓 ::Boolean
        """
        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList
        
        if(len(l1) != len(l2)):
            return False
            
            
        for i in range(0,len(l1)):
            if(l1[i].getX() != l2[i].getX()):
                return False
            if(l1[i].getY() != l2[i].getY()):
                return False
                
        return True

    def giveSelected(self):
        """
        select 속성을 추가함
        """
        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList
        
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')

        for i in range(0,len(l1)):
            if(l1[i].point.selected == True):
                 l2[i].point.selected = True    
        

    def giveAttrPenPair(self):
        """
        penpair 속성을 추가함
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')

        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList    

        for i in range(0,len(l1)):
            if(l1[i].point.selected == True):
                temp = at.get_attr(l1[i].point,'penPair')
                print(temp)
                at.add_attr(l2[i].point,'penPair',temp)
                
                                
    def giveDependX(self):
        """
        dependx 속성을 추가함
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')

        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList    

        for i in range(0,len(l1)):
            if(l1[i].point.selected == True):
                temp = at.get_attr(l1[i].point,'dependX')
                at.add_attr(l2[i].point,'dependX',temp)

    def giveDependY(self):
        """
        dependy 속성을 추가함
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')

        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList    

        for i in range(0,len(l1)):
            if(l1[i].point.selected == True):
                temp = at.get_attr(l1[i].point,'dependY')
                at.add_attr(l2[i].point,'dependY',temp)

    def giveInnerFill(self):
        """
        innerfill 속성을 추가함
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')

        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList    

        for i in range(0,len(l1)):
            if(l1[i].point.selected == True):
                temp = at.get_attr(l1[i].point,'innerFill')
                at.add_attr(l2[i].point,'innerFill',temp)

    def deleteAttr(self,attribute):
        """
        delete 속성을 추가함
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')

        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList    

        for i in range(0,len(l1)):
            if(l1[i].point.selected == True):
                at.del_attr(l2[i].point,attribute)

