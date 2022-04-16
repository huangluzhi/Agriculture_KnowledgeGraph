- wiki.zh.bin 用于保存词向量的模型

- wiki.zh.vec用于保存词向量

- adjust_parameter用于进行交叉验证和网格搜索，最后得到的结果存在mylog.log中

  （注意，模型过大没有上传，请自行下载中文模型：http://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.zh.zip）



## 计算机科学分类

0. Invalid（不合法，不是具体的实体，或一些脏数据，或与农业毫无关系）
1. Person（人物，职位）
2. Location（地点，区域）
3. Organization（机构，会议）
4. Political economy（政治经济名词）
5. Theory (计算机理论基础术语，算法和数据结构，抽象)
6. Technology (计算机工程相关术语，技术发明和应用措施，抽象)
7. Software (计算机工程软件以及相关实体，具象)
8. Hardware (计算机科学相关硬件，现实中存在物体)
9. Event (计算机相关行为现象)
10. Game (计算机游戏)
11. History (计算机科学相关事件)
17. other（除上面类别之外的其它名词实体，可以与农业无关但必须是实体）
