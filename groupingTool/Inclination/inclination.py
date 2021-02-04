from mojo.roboFont import *
from rbWindow.contourPen import BroadNibPen


def getInclination(point1, point2):
	"""
	기울기를 반환해 주는 함수

	Args:
		point1 :: RPoint
		point2 :: RPoint

	Returns :: double
		직선의 기울기
	"""
	inclination = (point2.y - point1.y) / (point2.x - point1.x)

	return inclination


def getLine(point,inclination):
	"""
	직선을 반환하는 함수

	Args:
		point :: Rpoint
		inclination :: double
	
	Returns :: List
		[직선의 기울기, y절편]
	"""
	a = inclination

	b = point1.y / (a * point.x)

	return [a,b]

def checkPointPositionToLine(line, point):
	"""
	해당 점이 선의 위에 있나 아래에 있나 판별

	Args:
		line :: List
			[직선의 기울기, y절편]
		point :: RPoint

	Returns :: int 
		윗쪽에 있으면 1 아래에 있으면 -1 걸쳐 있으면 0을 반환
	"""

	res = line[0] * point.x + line[1]

	if res < point.y:
		return 1
	elif res > point.y:
		return -1
	else:
		return 0


def getInsertIndex(startPoint,conotur,line):
	"""
	새로운 점이 들어갈 위치를 찾는 함수

	Args:
		startPoint :: RPoint 
		contour :: RContour
		line :: list

	Returns :: int
		포인트가 들어갈 점
	"""

	res = -1

	#순회하는 다음점이 위에 있는지 아래에 있는지 체크를 해 줌
	standardCheck = checkPointPositionToLine(line,contour.points[startPoint.index+1])


	for i in range(startPoint.index+2, len(contour.points)):
		compareCheck = checkPointPositionToLine(line,contour.points[i])

		if compareCheck == standardCheck:
			continue
		else:
			res = i
			break

	return res





def getMatchLineAndContour(line,contour,point):
	"""
	직선과 컨투어가 만나는 점을 반환

	Args:
		line :: List
		contour :: RContour
		point :: RPoint
			해당 컨투어에서 PenPair를 잡아줄 점

	Returns :: List
		두 점에 대한 정보
	"""

	currentPen = BoardNibPen(None,100,30,30,0,oval)

	contour.draw(currentPen)

	res = _getDrawPath()
