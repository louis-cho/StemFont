'''
undo/redo manager circular queue 

1. front, rear, cursor 변수를 통해 관리
2. 추가하는 경우, rear를 옮김 (cursor는 None으로 바뀜)
3. 되돌리는 경우, rear는 가만히 있고 cursor를 rear로 부터 움직이기 시작한다.(cursor가 None인 경우)
4. 복원하는 경우, cursor가 움직인다.

되돌리고 복원하는 과정에서 cursor는 front rear 경계 사이에서만 움직여야 된다.
되돌리고 복원하다가 원소를 추가하는 경우에는 rear 위치가 커서로 갱신되어야 한다.
꽉 찬 경우에 원소를 추가하는 경우 front 위치를 조정해야한다.
'''

class CircularQueue:

	def __init__(self, bufSize=5):
		self.bufSize = bufSize
		self.queue = [None]*self.bufSize
		self.front = self.rear = 0
		self.cursor = None

	def isEmpty(self):

		if self.front == self.rear:
			return True
		return False

	def isFull(self):

		if self.rear == None:
			return False

		return self.rear == self.nextIndex(self.front)

	def nextIndex(self, idx):
		return (idx+1)%self.bufSize

	def prevIndex(self, idx):
		return (idx-1)%self.bufSize

	def push(self, data):

		if self.isFull() is True:
			self.rear = self.nextIndex(self.rear)
			if self.cursor is not None:
				self.cursor = None

		self.queue[self.front] = data
		self.front = self.nextIndex(self.front)

	def peek(self):
		return self.queue[self.front]

	def pop(self):
		"""
			되돌리기 기능
		"""
		if self.isEmpty():
			return None

		if self.cursor is None:
			self.cursor = self.front-1
			return self.queue[self.cursor]
		else:
			if self.cursor is not self.rear:
				self.cursor = self.prevIndex(self.cursor)
				return self.queue[self.cursor]
			else:
				return None

	def rollback(self):
		"""
			복원하기 기능
		"""
		if self.isEmpty():
			return None

		if self.cursor is None:
			return None
		else:
			if self.cursor is not self.front:
				self.cursor = self.nextIndex(self.cursor)
				if self.queue[self.cursor] is None:
					self.cursor = None
					return None
				return self.queue[self.cursor]
			else:
				self.cursor = None
				return None

	def print(self):
		print("(front, rear, cursor) = ", self.front, self.rear, self.cursor)
