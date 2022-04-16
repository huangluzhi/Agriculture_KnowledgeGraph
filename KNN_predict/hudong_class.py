# coding: utf-8

class csNode:
    title = None
    detail = None
    image = None
    categories = None
    baseInfoKeyList = None
    baseInfoValueList = None
    label = None  # label值从文件中读取
    # 初始化，将字典answer赋值给类成员
    def __init__(self,answer):
        self.title = answer['title']
        self.detail = answer['detail']
        self.image = answer['image']
        self.categories = []
        self.baseInfoKeyList = []
        self.baseInfoValueList = []
        label = -1
        # print(answer)

        if len(answer['categories']) > 0:
            List = answer['categories'].split('##')
            for p in List:
                self.categories.append(p)

        if len(answer['infobox']) > 0:
            List = answer['infobox'].split('##')[1:]
            for p in List:
                if len(p.split('=')) > 1:
                    self.baseInfoKeyList.append(p.split('=')[0])
                    self.baseInfoValueList.append(p.split('=')[1])
