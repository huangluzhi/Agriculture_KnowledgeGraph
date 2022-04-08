# coding: utf-8

from py2neo import Graph,Node,Relationship,NodeMatcher
from read_csv import readCSV2
from hudong_class import csNode


class Neo4j():
	graph = None
	matcher = None
	def __init__(self):
		print("create neo4j class ...")

	def connectDB(self):
		self.graph = Graph("http://localhost:7474", auth=("neo4j", "zasqwe"))
		self.matcher = NodeMatcher(self.graph)

	def matchItembyTitle(self,value):
		answer = self.matcher.match("Item", title=value).first()
		# answer = self.graph.find_one(label="Item",property_key="title",property_value=value)
		return answer

	# 根据title值返回互动百科item
	def matchcsNodebyTitle(self,value):
		answer = self.matcher.match("csNode", title=value).first()
		# answer = self.graph.find_one(label="csNode",property_key="title",property_value=value)
		return answer

	# 返回所有已经标注过的互动百科item   filename为labels.txt
	def getLabeledcsNode(self, filename):
		labels = readCSV2(filename)
		List = []
		i = 0
		for line in labels:
			ctx = self.matcher.match("csNode", title=line[0]).first()
			# ctx = self.graph.find_one(label="csNode",property_key="title",property_value=line[0])
			if ctx == None:
				continue;
			cur = csNode(ctx)
			cur.label = line[1]
			List.append(cur)

		print('load LabeledcsNode over ...')
		return List

	# 返回限定个数的互动百科item
	def getAllcsNode(self, limitnum):
		List = []
		ge = self.graph.find(label="csNode", limit=limitnum)
		for g in ge:
			List.append(csNode(g))

		print('load AllcsNode over ...')
		return List


#test = Neo4j()
#test.connectDB()
#answer = test.graph.find_one(label="csNode",property_key="title",property_value='火龙果')
#print(answer)
#a = test.getLabeledcsNode('labels.txt')
#print(a[10].categories)
