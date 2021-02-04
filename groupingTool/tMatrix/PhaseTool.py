
import numpy as np

"""
modify by Kim heesup
"""

class GetMaxMinPointValue:
    """
    컨투어의 영역을 구하는 함수(이미 속성으로 정의가 되어 있어 사용하지 않음)
    
    Args:
        con:: RContour
            영역을 구하고자 하는 컨투어
    """
    def __init__(self,con):
        self.con = con
        self.p_list = []

        for p in self.con.points:
            if(p.type != "offcurve"):
                self.p_list.append(p)

        self.sortByX = sorted(self.p_list,key = lambda RPoint : RPoint.x)
        self.sortByY = sorted(self.p_list,key = lambda RPoint : RPoint.y)

    def getMaxXValue(self):
        return self.sortByX[-1].x
    def getMinXValue(self):
        return self.sortByX[0].x
    def getMaxYValue(self):
        return self.sortByY[-1].y
    def getMinYValue(self):
        return self.sortByY[0].y     

class Matrix:   
    """
    영역을 일정 구간 만큼 나눈 후 나눈 영역의 특정 범위에 점이 몇개가 존재하는지 판단

    Args:
        con :: RContour
            조사 하고자 할 RContour
        divk :: int
            영역을 몇개의 구간으로 나눌지 지정
    """
    def __init__(self,con,divk):
        self.divk = divk
        self.con = con
        self.matrix = None
                            
    def getdivk(self):
        return self.divk

    def getCon(self):
        return self.con

    def getTermX(self):
        maxx = self.con.bounds[2] + 10
        minx = self.con.bounds[0] - 10

        term_x = float((maxx - minx) / self.divk)

        return term_x

    def getTermY(self):
        maxy = self.con.bounds[3] + 10
        miny = self.con.bounds[1] - 10

        term_y = float((maxy - miny) / self.divk)

        return term_y


    def getMatrixCutLine(self):
        """
        매트릭스틑 쪼갤 때 나뉘어지는 포인트를 리턴해 줌
        (point 매칭시 거리계산시 사용)
        
        Return:
            나뉘어지는 포인트 :: list
                [[x축 기준 포인트], [y축 기준 포인트]]
        """

        divided_x = list()
        divided_y = list()
        res_divided = list()

        maxx = self.con.bounds[2] + 10
        minx = self.con.bounds[0] - 10
        maxy = self.con.bounds[3] + 10
        miny = self.con.bounds[1] - 10

        term_x = float((maxx - minx) / self.divk)
        term_y = float((maxy - miny) / self.divk)


        divided_pointx = minx
        divided_pointy = miny

        for i in range(0,self.divk):
            #print("i : ",i)
            #print("divided_pointx + (term_x * i) :", divided_pointx + (term_x * i))
            divided_x.append(divided_pointx + (term_x * i))
            #print(divided_x)
            #print("divided_pointy + (term_y * i) : ",divided_pointy + (term_y * i))
            divided_y.append(divided_pointy + (term_y * i))
            #print(divided_y)

        res_divided.append(divided_x)
        res_divided.append(divided_y)

        return res_divided            

    def getPointPart(self,p):
        """
        하나의 점에 대하여 어느 영역에 있는지 판별해 줌
        Args:
            p : Rpoint

        Return:
            점의 위치 :: list
        """
        maxx = self.con.bounds[2] + 10
        minx = self.con.bounds[0] - 10
        maxy = self.con.bounds[3] + 10
        miny = self.con.bounds[1] - 10
    
        term_x = float((maxx - minx) / self.divk)
        term_y = float((maxy - miny) / self.divk)      
        

        position_x = int((p.x - minx) // term_x);
        position_y = int((p.y - miny) // term_y);

        if(position_x >= self.divk):
            position_x = position_x - 1;
        if(position_y >= self.divk):
            position_y = position_y - 1;
        
        rl = [position_x, position_y]
    
        return rl     
    
    
    def getPointCnt(self):
        """
        메크릭스에 총 점이 몇개가 있는지 반환
        """
        res = 0
        for m in self.matrix:
            for j in m:
                res += j
        
        return res
        
    
    def getDivideStatus(self):
        """
        각각의 점에 대하여 matrix의 어느 영역에 있는지에 대한 정보를 계산
        
        Returns :
            [행에 대한 정보, 열에 대한 정보] :: list   
        """
    
        point_stat = []
    
        rl = []
        xrl = np.zeros(self.divk)
        yrl = np.zeros(self.divk)
    
    
        for p in self.con.points:
            if(p.type != "offcurve"):
                point_stat.append(self.getPointPart(p))
    
        for st in point_stat:
            cx = st[0]
            cy = st[1]

            xrl[cx] += 1
            yrl[cy] += 1

        rl.append(xrl.tolist())
        rl.append(yrl.tolist())
        
        return rl

    def getMatrix(self):
        """
        특정 위치에 몇개의 점이 위치하는지 matrix에 정보를 저장하고 그에 대한 정보를 반환
        """

        if(self.matrix is None):

            self.matrix = []

            for i in range(0,self.divk):
                self.matrix.append([])
            
            for i in range(0,len((self.matrix))):
                for j in range(0,self.divk):
                    self.matrix[i].append(0)

            pl= []

            for p in self.con.points:
                if(p.type != "offcurve"):
                    pl.append(self.getPointPart(p))

            for li in pl:
                self.matrix[li[0]][li[1]] = self.matrix[li[0]][li[1]] + 1

            return self.matrix
        else:
            return self.matrix




