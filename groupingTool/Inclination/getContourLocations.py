from mojo.roboFont import *

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

