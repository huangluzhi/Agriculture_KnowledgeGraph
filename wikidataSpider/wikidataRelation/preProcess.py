# 预处理entities.json,原来的entities.json是每个搜索词搜索返回的json文件，一个搜索词包含多个结果，现在只取搜索词和json数据中的text完全一样的数据,得到readytoCrawl.json，做进一步爬取

import json
import codecs
import time

resultJsonFile = codecs.open('readytoCrawl.json', 'w', encoding='utf-8')
with open("entities.json", "r") as fr:
    for line in fr.readlines():
        entity = json.loads(line)
        originname = entity['entityOriginName'].rstrip('\n')
        isMatched = False
        for repository in entity['jsonItem']['search']:
            # if (repository['match']['language'] in ['zh', 'en', 'zh-hans', 'zh-hant', 'zh-cn', 'en-gb']) and repository['match']['text'] == originname :
            if repository['match']['text'] == originname :
                resultJson = dict()
                resultJson['entity']  = repository
                resultJson['entityOriginName']  = originname
                resultJson['jsonNumber'] = entity['jsonNumber']
                resultJson = json.dumps(dict(resultJson),ensure_ascii=False) + '\n'
                resultJsonFile.write(resultJson)
                isMatched = True
                break
        if not isMatched:
            for repository in entity['jsonItem']['search']:
                if repository['match']['text'].lower() == originname.lower() :
                    resultJson = dict()
                    resultJson['entity']  = repository
                    resultJson['entityOriginName']  = repository['match']['text']
                    resultJson['jsonNumber'] = entity['jsonNumber']
                    resultJson = json.dumps(dict(resultJson),ensure_ascii=False) + '\n'
                    resultJsonFile.write(resultJson)
                    isMatched = True
                    break
        if not isMatched:
            print(originname, " ", entity['jsonItem']['search'][0]['match']['text'])
