import copy
import math
from groupingTool.tMatrix.PhaseTool import *
from fwig.tools import attributetools as at
from groupingTool.clockWise.clockWiseGroup import *
from attributeTool.strokeAttribute import *
"""
	2020/02/24
	create by kim heesup
"""

def getPointOnCurveDerivation(n, p0, p1, p2, p3, front):
    x0 = p0.x
    y0 = p0.y
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y
    x3 = p3.x
    y3 = p3.y
    points = [(x0, y0)]
    for t in range(1, n):
        t = t/n
        ax = x0 + t * (x1 - x0)
        ay = y0 + t * (y1 - y0)
        bx = x1 + t * (x2 - x1)
        by = y1 + t * (y2 - y1)
        cx = x2 + t * (x3 - x2)
        cy = y2 + t * (y3 - y2)
        dx = ax + t * (bx - ax)
        dy = ay + t * (by - ay)
        ex = bx + t * (cx - bx)
        ey = by + t * (cy - by)
        fx = dx + t * (ex - dx)
        fy = dy + t * (ey - dy)
        points.append((fx, fy))
    points.append((p3.x,p3.y))
    if front is True:
        first_point = points[0]
        second_point = points[1]
    else:
        first_point = points[-2]
        second_point = points[-1]
        
    derivation = (first_point[1] - second_point[1])/(first_point[0] - second_point[0])
    return derivation

"""
line점의 좌극한 혹은 우극한의 값을 구함
"""
def getPointOnLineDerivation(n, p0, p1):
    x0 = p0.x
    y0 = p0.y
    x1 = p1.x
    y1 = p1.y

    points = [(x0, y0)]

    for t in range(1, n):
        t = t/n

        fx = x0 + t * (x1 - x0)
        fy = y0 + t * (y1 - y0)

        points.append((fx, fy))
        
    first_point = points[0]
    second_point = points[1]
    
    try:
        derivation = (first_point[1] - second_point[1])/(first_point[0] - second_point[0])
    except ZeroDivisionError:
        return float('inf')
    
    return derivation

def getLineDerivation(n,p0,clockWise):
	#증가 방향 고려
	#[우극한 값, 좌극한 값]

	if p0.type == 'offcurve':
		return None

	res = list()
	reverse_res = list()
	currentContour = p0.getParent()
	currentIndex = p0.index
	pointCount = len(currentContour.points)

	#우극한
	if (currentContour.points[(currentIndex + 1) % pointCount].type == 'offcurve'):
	    res.append(getPointOnCurveDerivation(n,p0,currentContour.points[(currentIndex + 1) % pointCount],currentContour.points[(currentIndex + 2) % pointCount],currentContour.points[(currentIndex + 3) % pointCount],True))
	else:
	    res.append(getPointOnLineDerivation(n,p0,currentContour.points[(currentIndex + 1) % pointCount]))

	#좌극한
	if (currentContour.points[(currentIndex - 1) % pointCount].type == 'offcurve'):
		res.append(getPointOnCurveDerivation(n,currentContour.points[(currentIndex - 3) % pointCount],currentContour.points[(currentIndex - 2) % pointCount],currentContour.points[(currentIndex - 1) % pointCount],p0,False))
	else:
	    res.append(getPointOnLineDerivation(n,p0,currentContour.points[(currentIndex - 1) % pointCount]))

	if clockWise == True:
		return res
	else:
		reverse_res.append(res[1])
		reverse_res.append(res[0])
		return reverse_res

def getCurveDerivation(n, p0,clockWise):

	if p0.type != 'qcurve' and p0.type != 'curve':
		return None

	currentContour = p0.getParent()
	pointCount = len(currentContour.points)
	currentIndex = p0.index
	if currentContour.points[currentIndex-1].type == 'offcurve' and clockWise is True:
		return getPointOnCurveDerivation(n, currentContour.points[currentIndex-3], currentContour.points[currentIndex-2], currentContour.points[currentIndex-1], p0, False)
	elif currentContour.points[(currentIndex+1)%pointCount].type == 'offcurve' and clockWise is not True:
		return getPointOnCurveDerivation(n, currentContour.points[(currentIndex+3)%pointCount], currentContour.points[(currentIndex+2)%pointCount], currentContour.points[(currentIndex+1)%pointCount], p0, False)
	elif currentContour.points[(currentIndex+1)%pointCount].type == 'offcurve' and clockWise is True:
		return getPointOnCurveDerivation(n, p0, currentContour.points[(currentIndex+1)%pointCount], currentContour.points[(currentIndex+2)%pointCount], currentContour.points[(currentIndex+3)%pointCount], True)
	elif currentContour.points[currentIndex-1].type == 'offcurve' and clockWise is not True:
		return getPointOnCurveDerivation(n, p0, currentContour.points[currentIndex-1], currentContour.points[currentIndex-2], currentContour.points[currentIndex-3], True)

class ClockPointPair:
	def __init__(self,point,clockDegree,index):
	    self.point = point
	    self.clockDegree = clockDegree
	    self.index = index


def calcDirection(con,point):
	"""
	포인트 데이터가 해당 컨투어의 어느쪽에 위치하고 있는지 확인하는 함수

	Args:
		con :: RContour
			조사하고자 하는 컨투어
		point :: RPoint
			RContour안에 있는 조사하고자 하는 점
	
	Returs :
		위치 정보 :: list
			[up,down,left,right]
	"""

	dr = [20,-20,0,0]
	dc = [0,0,-20,20]

	#standard direction
	checkCdirection = [0,0,0,0]
	r = point.y
	c = point.x
	for i in range(0,4):
		nr = r + dr[i]
		nc = c + dc[i]
		if con.pointInside((nc,nr)):
			checkCdirection[i] = 1

	return checkCdirection



class matrixRelocatePoint:
	"""
	점과 위치와 방향정보를 새롭게 객체를 생성하여 연산을 진행하기 위한 class

	Args:
		point :: RPoint
			재배치 하고자 하는 점
		rx :: int
			x축의 재배치 위치
		ry :: int
			y축의 재배치 위치
		direction :: list
			calcDirection함수로 인한 결과
			
	"""
	def __init__(self,point,rx,ry,direction):
		self.point = point
		self.rx = rx
		self.ry = ry
		self.direction = direction

class groupPointMatchController:
	def __init__(self,matrix,point,con):
		"""
		같은 그룹 내에서의 컨투어의 점들에 대하여 최대한 비슷한 점을 골라냄

		Args:
			matrix :: Matrix Object 
				기준 Matrix 객체

			point :: RPoint  
				매칭을 시켜줄 점

			con :: RContour 
				그룹 내에 있는 컨투어
		"""
		self.matrix = matrix
		self.point = point
		self.con = con

		self.standardCon = matrix.getCon()

	def firstFiltering(self,point,checkSdirection):
		"""
		matchPoint함수에서 적용
		1차 필터링 과정
		direction방법으로 필터링
		"""
		#direction으로 1차 필터링
		diff_count = 0
		checkCdirection = calcDirection(self.con,point)
		for j in range(0,4):
			if(checkSdirection[j] != checkCdirection[j]):
				diff_count += 1

		if diff_count > 1:
			return -1
		elif diff_count == 0:
			return 0
		elif diff_count == 1:
			return 1
	def secondFiltering(self,standardClockDegree,compareClockDegree):
		#방향이 같은 것만 고려
		# return None : 유망하지 않음
		if compareClockDegree > 0  and standardClockDegree < 0:
			return None
		elif compareClockDegree < 0  and standardClockDegree > 0:
			return None

		diff = abs(standardClockDegree - compareClockDegree)
		
		return diff



	def matchPoint(self):
		"""
		포인트를 매칭 시켜줌
		"""	 
		pointPart = self.matrix.getPointPart(self.point)
		print("기준 컨투어 = ",self.con)
		if self.matrix.con.clockwise == True:
			standard_derivation = getLineDerivation(40,self.point,True)
		else:
			standard_derivation = getLineDerivation(40,self.point,False)

		print("기준 미분값 = ",standard_derivation)

		getStandardMaxMin = GetMaxMinPointValue(self.matrix.con)

		#find all point that contour's point that is located pointPart
		originpl = [] #original points

		relocatepl = []

		checkMatrix = Matrix(self.con,self.matrix.getdivk())
		getCompareMaxMin = GetMaxMinPointValue(checkMatrix.con)

		#매트릭스 기준점을 가져옴
		standardCutLine = self.matrix.getMatrixCutLine()
		compareCutLine = checkMatrix.getMatrixCutLine()


		#additional mechanism
		dr = [20,-20,0,0]
		dc = [0,0,-20,20]

		#standard direction
		#사용하지 않는 로직
		checkSdirection = [0,0,0,0]
		r = self.point.y
		c = self.point.x
		for i in range(0,4):
			nr = r + dr[i]
			nc = c + dc[i]
			if self.matrix.con.pointInside((nc,nr)):
				checkSdirection[i] = 1

		#비교 컨투어 direction조사
		#자신의 범위와 주변 범위들을 조사
		for p in self.con.points:
			if(p.type != 'offcurve'):
				checkPart = checkMatrix.getPointPart(p)
				# 조사하는 매트릭스의 x,y차가 1 이하면 조사 범위에 포함시킨다.
				check_part_one = abs(pointPart[0] - checkPart[0])		#x
				check_part_two = abs(pointPart[1] - checkPart[1])		#y
				
				if(check_part_one <= 1) and (check_part_two <= 1):
					originpl.append(p)


		#pointPart의 첫 원소는 x부분이고 두번째 원소는 y부분이다.
		#기준컨투어에서 점의 거리를 구함
		standard_dist = math.sqrt(math.pow(self.point.x - standardCutLine[0][pointPart[0]],2) + math.pow(self.point.y - standardCutLine[1][pointPart[1]],2))
		standard_term_x = self.matrix.getTermX()
		standard_term_y = self.matrix.getTermY()
		compare_term_x = checkMatrix.getTermX()
		compare_term_y = checkMatrix.getTermY()

		#get point that get minimum distance
		dir_diff_zero_indx = -1
		dir_diff_one_indx = -1
		diff_count_mode = 0

		#시험 코드
		standardClockDegree = getPointClockDegree(self.matrix.con,self.point)

		secondResult_one = list() #두번째 필터링 까지의 결과
		secondResult_two = list()

		#originpl : 같은 그룹 내 컨투어 내 조사할 후보군 점
		for i in range(0,len(originpl)):
			print("originpl: ", originpl[i])			
			#direction으로 1차 필터링
			diff_count_mode = self.firstFiltering(originpl[i],checkSdirection)
			if diff_count_mode == -1:
				print("1차 필터링")
				continue

			#회전율로 2차 필터링
			compareClockDegree = getPointClockDegree(self.con,originpl[i])
			clock_diff = self.secondFiltering(standardClockDegree,compareClockDegree)
			if diff_count_mode == 0 and clock_diff is not None:
				temp_insert = ClockPointPair(originpl[i],clock_diff,i)
				secondResult_one.append(temp_insert)

			elif diff_count_mode == 1 and clock_diff is not None:
				temp_insert = ClockPointPair(originpl[i],clock_diff,i)
				secondResult_two.append(temp_insert)
			else:
				print("2차 필터링")



		if (self.point.type == 'curve') or (self.point.type == 'qcurve'):
			min_derivation = 1000
		elif self.point.type == 'line':
			min_derivation = 1000
			
		for i in range(0,len(secondResult_one)):

			print("조사점: ", secondResult_one[i].point)

			if secondResult_one[i].point.type == 'offcurve':
				continue

			#미분 로직
			if self.con.clockwise == True:
				compare_derivation = getLineDerivation(40,secondResult_one[i].point,True)
			else:
				compare_derivation = getLineDerivation(40,secondResult_one[i].point,False)

			if (standard_derivation[0] == float('inf')) and (compare_derivation[0] == float('inf')):
				_diff_left = 0.0
			else:
				_diff_left = abs(compare_derivation[0] - standard_derivation[0])

			if (standard_derivation[1] == float('inf')) and (compare_derivation[1] == float('inf')):
				_diff_right = 0.0
			else:
				_diff_right = abs(compare_derivation[1] - standard_derivation[1])

			_diff = _diff_left + _diff_right
			print("diff left = ", _diff_left)
			print("diff right = ", _diff_right)
			print("diff = ",_diff)
			print("compare_derivation = ", compare_derivation)
			if min_derivation > _diff:
				dir_diff_zero_indx = secondResult_one[i].index
				min_derivation = _diff
			else:
				continue

		if dir_diff_zero_indx != -1:
			return originpl[dir_diff_zero_indx]

		#추가적으로 점을 조사
		if (self.point.type == 'curve') or (self.point.type == 'qcurve'):
			min_derivation = 1000
		elif self.point.type == 'line':
			min_derivation = 1000

		for i in range(0,len(secondResult_two)):

			print("조사점: ", secondResult_two[i].point)

			if secondResult_two[i].point.type != 'offcurve':
				continue

			#미분 로직
			if self.con.clockwise == True:
				compare_derivation = getLineDerivation(40,secondResult_two[i].point,True)
			else:
				compare_derivation = getLineDerivation(40,secondResult_two[i].point,False)

			if (standard_derivation[0] == float('inf')) and (compare_derivation[0] == float('inf')):
				_diff_left = 0
			else:
				_diff_left = abs(compare_derivation[0] - standard_derivation[0])

			if (standard_derivation[1] == float('inf')) and (compare_derivation[1] == float('inf')):
				_diff_right = 0
			else:
				_diff_right = abs(compare_derivation[1] - standard_derivation[1])

			_diff = _diff_left + _diff_right

			print("diff left = ", _diff_left)
			print("diff right = ", _diff_right)
			print("diff = ",_diff)
			print("compare_derivation = ", compare_derivation)
			if min_derivation > _diff:
				dir_diff_one_indx = secondResult_two[i].index
				min_derivation = _diff
			else:
				continue


		if dir_diff_one_indx != -1:
			return originpl[dir_diff_one_indx]
		else:
			return None



	"""
	각각의 속성을 넣어주는 함수들
	"""
	def mgiveSelected(self,matchPoint):
		if matchPoint is not None:
			matchPoint.selected = True

	def mgiveAttrPenPair(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'penPair')
			if temp is not None:
				at.add_attr(matchPoint,'penPair',temp)

	def mgiveDependX(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'dependX')
			if temp is not None:
				at.add_attr(matchPoint,'dependX',temp)

	def mgiveDependY(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'dependY')
			if temp is not None:
				at.add_attr(matchPoint,'dependY',temp)

	def mgiveInnerFill(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'innerType')
			if temp is not None:
				at.add_attr(matchPoint,'innerType',temp)

	def mgiveStroke(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'stroke')
			if temp is not None:
				at.add_attr(matchPoint,'stroke',temp)

	def mdeleteAttr(self,attribute,matchPoint):
		if matchPoint is not None:
			at.del_attr(matchPoint,attribute)		