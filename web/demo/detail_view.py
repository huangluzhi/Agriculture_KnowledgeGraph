# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
import thulac
import re

import sys
sys.path.append("..")
from toolkit.pre_load import neo_con
from toolkit.pre_load import wv_model, tree ,predict_labels
from toolkit.NER import get_explain,get_detail_explain

# 接收GET请求数据
def showdetail(request):
	ctx = {}
	ctx['breadcrumb'] = [['Home','\\'],['命名实体识别','../'],['实体百科']]
	if 'title' in request.GET:
		# 连接数据库
		db = neo_con

		title = request.GET['title']
		answer_type = "csNode"
		answer = db.matchcsNodebyTitle(title)
		print(answer)
		if answer == []:
			answer = db.matchwikiNodebyTitle(title)
			answer_type = "wikiNode"
		if answer == []:
			return render(request, "404.html", ctx)

		if len(answer) > 0:
			answer = answer[0]['n']
		else:
			ctx['title'] = '实体条目出现未知错误'
			return

		if answer_type == "all":
			ctx['detail'] = re.sub('\\[\\[([^\\[\\]]*)\\]\\]','<a href="detail.html?title=\\1">\\1</a>',answer['detail'])
		else:
			ctx['detail'] = re.sub('[\\[\\]]','',answer['detail'])
		ctx['title'] = answer['title']
		image = answer['image']

		if image != "":
			ctx['image'] = '<img src="' + str(image) + '" alt="该条目无图片" height="100%" width="100%" >'

		ctx['baseInfoValueList'] = []
		ctx['baseInfoKeyList'] = []
		List = answer['infobox'].split('##')[1:]
		if answer_type == "csNode":
			for p in List:
				if len(p.split('=')) > 1:
					ctx['baseInfoKeyList'].append(p.split('=')[0])
					ctx['baseInfoValueList'].append(re.sub('\\[\\[([^\\[\\]]*)\\]\\]','<a href="detail.html?title=\\1">\\1</a>',p.split('=')[1]))
		else:
			for p in List:
				if len(p.split('=')) > 1:
					ctx['baseInfoKeyList'].append(p.split('=')[0])
					ctx['baseInfoValueList'].append(re.sub('[\\[\\]]','',p.split('=')[1]))


		text = ""
		keyList = ctx['baseInfoKeyList']
		valueList = ctx['baseInfoValueList']
		List = answer['categories'].split('##')
		for p in List:
			text += '<span class="badge bg-important">' + str(p) + '</span> '
		ctx['categories'] = text

		text = '<table class="table table-striped table-advance table-hover"> <tbody>'
		i = 0
		while i < len(keyList) :
			value = " "
			if i < len(valueList):
				value = valueList[i]
			text += "<tr>"
			text += '<td><strong>' + keyList[i] + '</strong></td>'
			text += '<td>' + value + '</td>'
			i += 1

			if i < len(valueList):
				value = valueList[i]
			if i < len(keyList) :
				text += '<td><strong>' + keyList[i] + '</strong></td>'
				text += '<td>' + value + '</td>'
			else :
				text += '<td><strong>' + '</strong></td>'
				text += '<td>' + '</td>'
			i += 1
			text += "</tr>"
		text += " </tbody> </table>"
		if answer['infobox'].strip() == '':
			text = ''
		ctx['baseInfoTable'] = text

		if answer_type == "csNode":
			tagcloud = ""
			taglist = wv_model.get_simi_top(answer['title'], 10)
			for tag in taglist:
				tagcloud += '<a href= "./detail.html?title=' + str(tag) + '"> '
				tagcloud += str(tag) + "</a>"
#			print(tag)
			ctx['tagcloud'] = tagcloud

		agri_type = ""
		ansList = tree.get_path(answer['title'], True)
		for List in ansList:
			agri_type += '<p >'
			flag = 1
			for p in List:
				if flag == 1:
					flag = 0
				else:
					agri_type += ' / '
				agri_type += str(p)

			agri_type += '</p>'
		if len(ansList) == 0:
			agri_type = '<p > 暂无类型</p>'
		ctx['agri_type'] = agri_type

		if answer_type == "csNode":
			entity_type = ""
			explain = get_explain(predict_labels[answer['title']])
			detail_explain = get_detail_explain(predict_labels[answer['title']])
			entity_type += '<p > [' + explain + "]: "
			entity_type += detail_explain + "</p>"
			ctx['entity_type'] = entity_type

	else:
		return render(request, "404.html", ctx)

	return render(request, "detail.html", ctx)

#
## -*- coding: utf-8 -*-
#from django.http import HttpResponse
#from django.shortcuts import render_to_response
#import thulac
#
#import sys
#sys.path.append("..")
#from neo4jModel.models import Neo4j
#
#def search_detail(request):
#	return render_to_response('detail.html')
#
## 接收GET请求数据
#def showdetail(request):
#	request.encoding = 'utf-8'
#	if 'title' in request.GET:
#		# 连接数据库
#		db = Neo4j()
#		db.connectDB()
#		title = request.GET['title']
#		answer = db.matchItembyTitle(title)
#		message = answer['detail']
#
#	return HttpResponse(message)
