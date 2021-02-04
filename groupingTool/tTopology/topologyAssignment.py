"""
create by Heesup Kim
"""

class topologicalRpoint:
    def __init__(self,point):
        """
        point에 대한 정보와 x, y축에 대한 위상값에 대한 정보를 저장

        Args:
            point :: RPoint
        """
        self.point = point
        self.x = -1
        self.y = -1
        
    def setX(self,num):
        self.x = num
    def setY(self,num):
        self.y = num
    def getX(self):
        return self.x
    def getY(self):
        return self.y        
            


class checkCon:
    """
    topology 방법으로 컨투어에 대한 정보를 분석하는 클래스

    Args:
            con :: RContour
                분석하고자 하는 컨투어
            k :: int
                위상에 대한 margin값 할당
    """
    def __init__(self,con,k):
        self.con = con
        self.k = k
        self.pointList = list(con.points)
        
        self.consistClockWise()
        self.slist = self.sortByStartingPoint()
        self.tpPointList = self.assignmentTopological(self.k) 
    
    def consistClockWise(self):
        """
        컨투어의 점의 순서가 시계방향인지 반 시계방향인지 확인 후 반시계 방향이면 일괄적으로 시계 방향으로 돌려줌
        """
        
        if(self.con.clockwise == False):
            self.pointList.reverse()
            rp = self.pointList[-1]
            self.pointList.insert(0,rp)
            del(self.pointList[-1])
            
    def sortByStartingPoint(self):
        """
        리스트의 점의 시작을 일괄적으로 고정하기 위하여 y값이 가장 작은 점을 시작점으로 분류하고 만약 y값이 같이면 x값이 가장 작은 것으로 설정
        이 이후에 topology분석을 시작함

        Returns: 
            시작점이 설정된 리스트 ::List
        """
        minY = 10000000000
        minX = 10000000000
        
        candidatePoints = []
        startPoint = None
        slist = []
        
        for i in range(0,len(self.pointList)):
            if(self.pointList[i].type != "offcurve"):
                if(minX > self.pointList[i].x):
                    minX = self.pointList[i].x
                
        for i in range(0,len(self.pointList)):
            if(self.pointList[i].type != "offcurve"):
                if(minX == self.pointList[i].x):
                    candidatePoints.append(self.pointList[i])
                
        for i in range(0,len(candidatePoints)):
            if(candidatePoints[i].type != "offcurve"):
                if(minY > candidatePoints[i].y):
                    minY = candidatePoints[i].y
                
        for i in range(0,len(candidatePoints)):
            if(candidatePoints[i].type != "offcurve"):
                if(minY == candidatePoints[i].y):
                    startPoint = candidatePoints[i]
                
                        
        num = -1
        for i in range(0,len(self.pointList)):
            if((startPoint.x == self.pointList[i].x) and (startPoint.y == self.pointList[i].y)):
                num = i;
                break;
                
        ll = self.pointList[i:len(self.pointList)]
        rl = self.pointList[0:i]
        
        offSlist = ll + rl
        #remove offCurvce
        for i in range(0,len(offSlist)):
            if(offSlist[i].type != "offcurve"):
                slist.append(offSlist[i])
        return slist
        
             
    def assignmentTopological(self,num):
        """
        위상을 최종적으로 계산하여 할당해 주는 함수

        Args:
            num :: int
                margin값
                
        Returns:
            topologicalRpoint인스턴스에 대한 리스트 반환 :: list
        """
        sortByX = sorted(self.pointList,key = lambda RPoint: RPoint.x)
        sortByY = sorted(self.pointList,key = lambda RPoint: RPoint.y)
        
        sortByXNone = []
        sortByYNone = []
        tpRpl =[]
        
        idx = 1

        sortByXNone.append(sortByX[0])
        
        
        while(idx < len(sortByX)):
            if(sortByX[idx].x - sortByX[idx-1].x < num):
                sortByXNone.append(sortByX[idx])
                idx += 1
            else:
                sortByXNone.append(None)
                sortByXNone.append(sortByX[idx])
                idx += 1

        
        idx = 1

        sortByYNone.append(sortByY[0])
        
        
        while(idx < len(sortByY)):
            if(sortByY[idx].y - sortByY[idx-1].y < num):
                sortByYNone.append(sortByY[idx])
                idx += 1
            else:
                sortByYNone.append(None)
                sortByYNone.append(sortByY[idx])
                idx += 1
                           
                
        #assign topological
        for i in range(0,len(self.slist)):
            intpPoint = topologicalRpoint(self.slist[i])
            #assign x topological
            for j in range(0,len(sortByXNone)):
                if(sortByXNone[j] == None):
                    continue
                if((intpPoint.point.x == sortByXNone[j].x) and (intpPoint.point.y == sortByXNone[j].y)):
                    intpPoint.setX(j)
            #assign y topological
            for j in range(0,len(sortByYNone)):
                if(sortByYNone[j] == None):
                    continue
                if((intpPoint.point.x == sortByYNone[j].x) and (intpPoint.point.y == sortByYNone[j].y)):
                    intpPoint.setY(j)
            tpRpl.append(intpPoint)
            
        return tpRpl