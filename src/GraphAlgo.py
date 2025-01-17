import json
import matplotlib.pyplot as plt
from typing import List
import numpy as np
import math
from queue import PriorityQueue
from src.GraphAlgoInterface import GraphAlgoInterface
from src.GraphInterface import GraphInterface
from src.DiGraph import DiGraph
from src.Node import Node


class GraphAlgo(GraphAlgoInterface):
	def __init__(self, g=None):
		self.graph = g
	
	def init(self, g):
		self.graph = g
	
	def get_graph(self) -> GraphInterface:
		return self.graph
		"""
		*Returns the directed graph on which the algorithm works on.
		"""
	
	def load_from_json(self, file_name: str) -> bool:
		try:
			with open(file_name) as f:
				json_obj = json.load(f)
			graph = DiGraph()
			for node in json_obj['Nodes']:
				temp = []
				_id = node['id']
				try:
					for i in node['pos'].split(","):
						temp.append((float)(i))
						pos = tuple(temp)
				except:
					pos = None
				graph.add_node(_id, pos)
			for edge in json_obj['Edges']:
				graph.add_edge(edge['src'], edge['dest'], edge['w'])
			self.graph = graph
			return True
		except:
			return False
		
		"""
		Loads a graph from a json file, returns True if the loading was successful, False o.w .
		"""
	
	def save_to_json(self, file_name: str) -> bool:
		try:
			graph = self.graph
			Nodes = []
			Edges = []
			nodes = list(graph.get_all_v().values())
			for node in nodes:
				Nodes.append(node.toJson())
				src = node.id
				for _id, w in node.getStart().items():
					edge = {'src': src, 'w': w, 'dest': _id}
					Edges.append(edge)
			json_object = {'Edges': Edges, 'Nodes': Nodes}
			
			with open(file_name, 'w') as f:
				json.dump(json_object, f)
			return True
		except:
			return False
		"""
		Saves the graph in JSON format to a file, returns True if the save was successful, False o.w.
		"""
	
	def shortest_path(self, id1: int, id2: int) -> (float, list):
		graph = self.graph
		try:
			graph.get_node(id1)
			graph.get_node(id2)
			if (graph.v_size() != 2):
				q = PriorityQueue()
				q.put((0, id1))
				prev = {}
				prev.update({id1: id1})
				weight = {}
				weight.update({id1: 0})
				visited = set([])
				while (not q.empty()):
					_id = q.get()[1]
					if (not visited.__contains__(_id)):
						visited.add(_id)
					if (_id == id2):
						curr_id = _id
						path = [curr_id]
						while (curr_id != id1):
							curr_id = prev.get(curr_id)
							path.append(curr_id)
						path.reverse()
						output = (weight[id2], path)
						return output
					edges = graph.all_out_edges_of_node(_id)
					for i, w in edges.items():
						if (i in visited):
							continue
						dist = weight[_id]
						dist += w
						if (weight.__contains__(i)):
							if (weight[i] > dist):
								prev.update({i: _id})
								weight.update({i: dist})
								q.put((dist, i))
						else:
							prev.update({i: _id})
							weight.update({i: dist})
							q.put((dist, i))
				return (float('inf'), [])
		except:
			return (float('inf'), [])
		"""
		* Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm, returns the distance of the path and a list of the nodes ids that the path goes through .
		"""
	
	def DFS(self, node: int) -> Node:
		counter = 0
		stack = []
		stack.insert(0, self.graph.get_node(node))
		stack[0].setStatus(True)
		stack[0].setInfo(counter)
		counter += 1
		while (len(stack) is not 0):
			if (not self.hasNext(stack[0])):
				stack[0].setInfo(counter)
				poped = stack.pop(0)
				counter += 1
				continue
			stack.insert(0, self.getNext(stack[0]))
			stack[0].setStatus(True)
			stack[0].setInfo(counter)
			counter += 1
		return poped
	
	"""
	*Implementation of DFS algorithm on a weighted directed graph.
	"""
	
	def hasNext(self, node: Node) -> bool:
		edges = self.graph.all_out_edges_of_node(node.getId())
		s = []
		for i in edges:
			if (not self.graph.get_node(i).getStatus()):
				s.append(i)
		if (len(s) != 0):
			return True
		return False
	
	"""
	*Tells if the received node has a unvisited child.
	"""
	
	def getNext(self, node: Node) -> Node:
		edges = self.graph.all_out_edges_of_node(node.getId())
		for i in edges:
			if (not self.graph.get_node(i).getStatus()):
				return self.graph.get_node(i)
		pass
	
	"""
	*Returns the unvisited child of the received node .
	"""
	
	def connected_component(self, id1: int) -> list:
		self.setAllNodeComponentsToDefaultValue()
		self.DFS(id1)
		self.fCc()
		self.get_graph().setTranspose()
		self.DFS(id1)
		list = self.listOfConnectedComponent()
		self.setAllNodeComponentsToDefaultValue()
		self.get_graph().setTranspose()
		return list
	
	"""
	*Finds the Strongly Connected Component(SCC) that node id1 is a part of, using DFS algorithm, then a transposition for the verticies, and then performing another DFS algorithm, returns The list of nodes in the SCC .
	"""
	
	def fCc(self):
		for each in self.get_graph().get_all_v():
			node = self.graph.get_node(each)
			node.setStatus(not node.getStatus())
			node.setInfo(-1)
		pass
	
	"""
	*After performing the first DFS algorithm run, we need to make sure that in the next running of the DFS algorithm we will check only the components that were declared as "somehow connected" to the received node.
	"""
	
	def setAllNodeComponentsToDefaultValue(self):
		for _id, node in self.get_graph().get_all_v().items():
			node.setStatus(False)
			node.setInfo(-1)
		pass
	
	"""
	*Sets all the status and info parameters of each node to its default value .
	"""
	
	def listOfConnectedComponent(self) -> list:
		list = []
		for each in self.get_graph().get_all_v():
			node = self.graph.get_node(each)
			if (node.getInfo() != -1):
				list.append(each)
		return list
	
	"""
	*Returns a list of all the connected component .
	"""
	
	def connected_components(self) -> List[list]:
		graph = self.graph
		try:
			nodes = graph.get_all_v()
			s = set([])
			output = []
			for i in nodes:
				if (not s.__contains__(i)):
					s.add(i)
					l = self.connected_component(i)
					output.append(l)
					for j in l:
						s.add(j)
			return output
		except:
			return []
		
		"""
		*Finds all the Strongly Connected Component(SCC) in the graph, returns a list with all of the SCC lists .
		"""
	
	def plot_graph(self) -> None:
		graph = self.graph
		size = self.graph.v_size()
		np.random.seed(0)
		ax = plt.gca()
		plt.axis("scaled")
		nodes = list(graph.get_all_v().values())
		for node in nodes:
			pos = self.getPos(size, node.getId())
			node.setPos(pos)
			node.incPos(size)
		max_x = nodes[0].getPos()[0]
		min_x = max_x
		max_y = nodes[0].getPos()[1]
		min_y = max_y
		for node in nodes:
			for _id in node.getStart():
				node2 = graph.get_node(_id)
				pos1 = node.getPos()
				pos2 = node2.getPos()
				dis = self.distance(pos1, pos2)
				a = plt.Arrow(x=pos1[0], y=pos1[1], dx=dis[0], dy=dis[1], width=0.05, color='k')
				ax.add_patch(a)
			pos = node.getPos()
			if (max_x < pos[0]):
				max_x = pos[0]
			elif (min_x > pos[0]):
				min_x = pos[0]
			if (max_y < pos[1]):
				max_y = pos[1]
			elif (min_y > pos[1]):
				min_y = pos[1]
			
			c = plt.Circle((pos[0], pos[1]), 0.05)
			plt.text(pos[0] + 0.05, pos[1] + 0.05, node.getId(), fontsize=10, color='g')
			ax.add_patch(c)
		dx = (max_x - min_x) / 10
		dy = (max_y - min_y) / 10
		ax.set_ylim(min_y - dy, max_y + dy)
		ax.set_xlim(min_x - dx, max_x + dx)
		for node in nodes:
			node.dicPos(size)
		plt.show()
		
		"""
		*Plots the graph, if the nodes have a position, the nodes will be placed there, otherwise, they will be placed in a random but elegant manner .
		"""
	
	def getPos(self, size, id1):
		if (id1 % 4 == 0):
			return ((-1 * size), id1, 0.0)
		if (id1 % 4 == 1):
			return ((size), id1, 0.0)
		if (id1 % 4 == 2):
			return (id1 / 10, (size), 0.0)
		return (id1, (-1 * size), 0.0)
	
	"""
	*Generates a pos in a shape of a square.
	"""
	
	def distance(self, pos1, pos2):
		_pos = self.des(pos1[0], pos1[1], pos2[0], pos2[1])
		return (_pos[0] - pos1[0], _pos[1] - pos1[1], pos2[2] - pos1[2])
	
	"""
	* Calculates the distance an arrow need to be for connecting between two nodes .
	"""
	
	def des(self, x1, y1, x2, y2):
		dy = y2 - y1
		dx = x2 - x1
		if (dy == 0):
			return (x2 - 0.05 * (abs(dx) / dx), y2)
		if (dx == 0):
			return (x2, y2 - 0.05 * (abs(dy) / dy))
		te = math.atan(dx / dy)
		te2 = math.radians(90 - math.degrees(te))
		_x = math.cos(te2) * 0.05
		_y = math.sin(te2) * 0.05
		if (dy < 0):
			return (x2 + _x, y2 + _y)
		else:
			return (x2 - _x, y2 - _y)
	
	"""
	*Finds the correct distance .
	"""
