
// 将zhwiki-CS-entities.csv 导入
LOAD CSV WITH HEADERS  FROM "file:///zhwiki-CS-entities.csv" AS line
CREATE (p:csNode{source:line.source,id:line.id,title:line.title,url:line.url,image:line.image,categorie:line.categorie,infobox:line.infobox,detail:line.detail})

// 创建索引
CREATE CONSTRAINT ON (c:csNode)
ASSERT c.title IS UNIQUE




// 导入新的节点
LOAD CSV WITH HEADERS FROM "file:///new_node.csv" AS line
CREATE (:NewNode { title: line.title })

//添加索引
CREATE CONSTRAINT ON (c:NewNode)
ASSERT c.title IS UNIQUE

//导入hudongItem和新加入节点之间的关系
LOAD CSV  WITH HEADERS FROM "file:///wikidata_relation2.csv" AS line
MATCH (entity1:csNode{title:line.csNode}) , (entity2:NewNode{title:line.NewNode})
CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2)

LOAD CSV  WITH HEADERS FROM "file:///wikidata_relation.csv" AS line
MATCH (entity1:csNode{title:line.csNode1}) , (entity2:csNode{title:line.csNode2})
CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2)



// 导入实体属性(数据来源: 互动百科)

// 将attributes.csv放到neo4j的import目录下，然后执行

LOAD CSV WITH HEADERS FROM "file:///attributes.csv" AS line
MATCH (entity1:csNode{title:line.Entity}), (entity2:csNode{title:line.Attribute})
CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2);

LOAD CSV WITH HEADERS FROM "file:///attributes.csv" AS line
MATCH (entity1:csNode{title:line.Entity}), (entity2:NewNode{title:line.Attribute})
CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2);

LOAD CSV WITH HEADERS FROM "file:///attributes.csv" AS line
MATCH (entity1:NewNode{title:line.Entity}), (entity2:NewNode{title:line.Attribute})
CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2);

LOAD CSV WITH HEADERS FROM "file:///attributes.csv" AS line
MATCH (entity1:NewNode{title:line.Entity}), (entity2:csNode{title:line.Attribute})
CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2)

//我们建索引的时候带了label，因此只有使用label时才会使用索引，这里我们的实体有两个label，所以一共做2*2=4次。当然，可以建立全局索引，即对于不同的label使用同一个索引


