# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
import thulac

import sys
sys.path.append("..")
from toolkit.pre_load import neo_con

# 数据标注页面的view
# 接收GET请求数据
def showtagging_data(request):
	ctx = {}
	if 'title' in request.GET:
		# 连接数据库
		db = neo_con
		title = request.GET['title']
		answer = db.matchcsNodebyTitle(title)
		if answer == []:
			ctx['title'] = '<h1> 该实体不存在，请换一个 </h1>'
			return render(request, "tagging_data.html", ctx)
		answer = answer[0]['n']
		ctx['detail'] = answer['detail']
		ctx['title'] = answer['title']
		image = answer['image']

		ctx['image'] = '<img class="rounded card-img-top img-fluid" src="' + str(image) + '" alt="该条目无图片" style="width:30%" >'

		ctx['baseInfoValueList'] = []
		ctx['baseInfoKeyList'] = []
		List = answer['infobox'].split('##')[1:]
		for p in List:
			if len(p.split('=')) > 1:
				ctx['baseInfoKeyList'].append(p.split('=')[0])
				ctx['baseInfoValueList'].append(p.split('=')[1])

		text = ""
		List = answer['categories'].split('##')
		for p in List:
			text += '<span class="badge badge-success">' + str(p) + '</span> '
		ctx['categories'] = text

		text = ""
		keyList = ctx['baseInfoKeyList']
		valueList = ctx['baseInfoValueList']
		i = 0
		while i < len(keyList) :
			value = " "
			if i < len(valueList):
				value = valueList[i]
			text += "<tr>"
			text += '<td class="font-weight-bold">' + keyList[i] + '</td>'
			text += '<td>' + value + '</td>'
			i += 1

			if i < len(valueList):
				value = valueList[i]
			if i < len(keyList) :
				text += '<td class="font-weight-bold">' + keyList[i] + '</td>'
				text += '<td>' + value + '</td>'
			else :
				text += '<td class="font-weight-bold">' + '</td>'
				text += '<td>' + '</td>'
			i += 1
			text += "</tr>"
		ctx['baseInfoTable'] = text

		## 动态生成check控件----------------------------------

		text = ""
		tag_name_list = []
		tag_name_list.append('Invalid（不合法，不是具体的实体，或一些脏数据，或与计算机毫无关系）')
		tag_name_list.append('Person（人物，职位）')
		tag_name_list.append('Location（地点，区域）')
		tag_name_list.append('Organization（机构，会议）')
		tag_name_list.append('Political economy（政治经济名词）')
		tag_name_list.append('Theory (计算机理论基础术语，算法和数据结构，抽象)')
		tag_name_list.append('Technology (计算机工程相关术语，技术发明和应用措施，抽象)')
		tag_name_list.append('Software (计算机工程软件以及相关实体，具象)')
		tag_name_list.append('Hardware (计算机科学相关硬件，现实中存在物体)')
		tag_name_list.append('Event (计算机相关行为现象或相关事件)')
		tag_name_list.append('Game (计算机游戏)')
		tag_name_list.append('other（除上面类别之外的其它名词实体，可以与计算机无关但必须是实体）')

		count = 0
		for i in range(len(tag_name_list)):
			text += '<div class="radio"> <label class="form-check-label">'
			text += '<input type="radio" name="label" value="' + str(i) + '">'
			text +=  str(count) + '. ' + tag_name_list[i]
			text += '</label>  </div>'
			count += 1

		# 放置一个隐藏的输入框，传递title的值到缓冲页面
		text += '<input name="title" value="' + str(answer['title']) + '"  style="display:none;" ></input>'
		ctx['taggingCheck'] = text


		# 统计当前标注情况
		file_object = open('label_data/labels.txt','r')
		s = []
		sum = 0
		for i in range(17):
			s.append(set())
		for f in file_object:
			pair = f.split()
			s[int(pair[1].strip())].add(pair[0].strip())
		for i in range(17):
			sum += len(s[i])
		file_object.close()
		text = "" ##用于记录已标注样本个数
		for i in range(17):
			text += '<p>' + str(i) + '类: ' + str(len(s[i])) + '个</p>'
		text += '<p>总计: ' + str(sum) + '个</p>'
		ctx['already'] = text


	return render(request, "tagging_data.html", ctx)
