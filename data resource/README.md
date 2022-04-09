## neo4j

### node:

1. √ csNode (zhwiki-CS-entities.csv)：计算机科学相关实体
2. wikiNode：计算机科学无关实体
3. singleNode：无属性（wiki中不存在）实体
4. wikiSynoNode：维基同义词（redirect）

newNode = wikiNode + wikiSynoNode + singleNode

all nodes in neo4j = csNode + newNode = csNode + wikiNode + wikiSynoNode + singleNode

### relation:

1. √ wikidata_relation.csv：node1->node1。csNode中从wikidata提取的自身关系
2. √ wikidata_relation2.csv：node1->node2&node3。csNode中从wikidata提取的外部关系
3. √ zhwiki-CS-relationAttribute.csv：node1->node1&node2。csNode中infobox提取的关系。
4. √ zhwiki-CS-normalAttribute.csv：node1->node3。csNode中infobox提取的普通属性。
5. zhwiki-wiki-attribute.csv：node2->node1&node2。wikiNode中infobox提取的关系。
6. zhwiki-wiki-normalAttribute.csv：node2->node3。wikiNode中infobox提取的普通属性。
7. zhwiki-synonym.csv：node