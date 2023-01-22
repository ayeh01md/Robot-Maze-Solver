import heapq
import sys

class Graph:
	def __init__(self):
		self.vertices = {}
		
	def add_vertex(self, name, edges):
		self.vertices[name] = edges
	
	def get_shortest_path(self, startpoint, endpoint):
		#distances使用字典的方式儲存每一個頂點到startpoint點的距離
		distances = {}
		
		#從startpoint到某點的最優路徑的前一個結點
		#eg:startpoint->B->D->E,則previous[E]=D,previous[D]=B,等等
		previous = {}
		
		#用來儲存圖中所有頂點的到startpoint點的距離的優先佇列
		#這個距離不一定是最短距離
		nodes = []
		
		#Dikstra演算法 資料初始化
		for vertex in self.vertices:
			if vertex == startpoint:
				#將startpoint點的距離初始化為0
				distances[vertex] = 0
				heapq.heappush(nodes, [0, vertex])
			elif vertex in self.vertices[startpoint]:
				#把與startpoint點相連的結點距離startpoint點的距離初始化為對應的弧長/路權
				distances[vertex] = self.vertices[startpoint][vertex]
				heapq.heappush(nodes, [self.vertices[startpoint][vertex], vertex])
				previous[vertex] = startpoint
			else:
				#把與startpoint點不直接連線的結點距離startpoint的距離初始化為sys.maxsize
				distances[vertex] = sys.maxsize
				heapq.heappush(nodes, [sys.maxsize, vertex])
				previous[vertex] = None
		
		while nodes:
			#取出佇列中最小距離的結點
			smallest = heapq.heappop(nodes)[1]
			if smallest == endpoint:
				shortest_path = []
				lenPath = distances[smallest]
				temp = smallest
				while temp != startpoint:
					shortest_path.append(temp)
					temp = previous[temp]
				#將startpoint點也加入到shortest_path中
				shortest_path.append(temp)
			if distances[smallest] == sys.maxsize:
				#所有點不可達
				break
			#遍歷與smallest相連的結點，更新其與結點的距離、前繼節點
			for neighbor in self.vertices[smallest]:
				dis = distances[smallest] + self.vertices[smallest][neighbor]
				if dis < distances[neighbor]:
					distances[neighbor] = dis
					#更新與smallest相連的結點的前繼節點
					previous[neighbor] = smallest
					for node in nodes:
						if node[1] == neighbor:
							#更新與smallest相連的結點到startpoint的距離
							node[0] = dis
							break
					heapq.heapify(nodes)
		return shortest_path, lenPath
if __name__ == '__main__':
	g = Graph()
	g.add_vertex('a', {'b':6, 'd':2, 'f':5})
	g.add_vertex('b', {'a':6, 'c':4, 'd':5})
	g.add_vertex('c', {'b':4, 'e':4, 'h':6})
	g.add_vertex('d', {'a':2, 'b':5, 'e':6, 'f':4})
	g.add_vertex('e', {'d':6, 'c':4, 'g':5, 'h':4})
	g.add_vertex('f', {'a':5, 'd':4, 'g':9})
	g.add_vertex('g', {'f':9, 'e':5, 'h':5})
	g.add_vertex('h', {'c':6, 'e':4, 'g':5})
	start = 'c'
	end = 'f'
	shortestPath, len = g.get_shortest_path(start, end)
	print('{}->{} the shortest path:{},the shortest distance:{}'.format(start, end, shortestPath, len))