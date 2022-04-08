
import json
import codecs
import time
newfile = open("newentities.json", "w", encoding='utf-8')
with open("entities.json", "r", encoding='utf-8') as fr:
    for line in fr.readlines():
        entity = json.loads(line)
        entity['entityOriginName'] = entity['entityOriginName'].rstrip('\n')
        entity['jsonItem']['searchinfo']['search'] = entity['jsonItem']['searchinfo']['search'].rstrip('\n')
        newline = json.dumps(entity, ensure_ascii=False)
        newfile.writelines(newline + '\n')
