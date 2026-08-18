GET_ALL_PAPERS = """
MATCH (p:Paper)
RETURN p.id AS id, p.title AS title, p.year AS year,
       p.abstract AS abstract, p.citations_count AS citations_count
ORDER BY p.year DESC, p.citations_count DESC
LIMIT $limit
"""

GET_PAPER_BY_ID = """
MATCH (p:Paper {id: $id})
OPTIONAL MATCH (p)-[:AUTHORED_BY]->(a:Author)
OPTIONAL MATCH (p)-[:TAGGED_WITH]->(t:Topic)
OPTIONAL MATCH (p)-[:CITES]->(cited:Paper)
OPTIONAL MATCH (citing:Paper)-[:CITES]->(p)
RETURN p.id AS id, p.title AS title, p.year AS year,
       p.abstract AS abstract, p.citations_count AS citations_count,
       COLLECT(DISTINCT {id: a.id, name: a.name}) AS authors,
       COLLECT(DISTINCT {id: t.id, name: t.name}) AS topics,
       [x IN COLLECT(DISTINCT {id: cited.id, title: cited.title}) WHERE x.id IS NOT NULL] AS cited_papers,
       [x IN COLLECT(DISTINCT {id: citing.id, title: citing.title}) WHERE x.id IS NOT NULL] AS citing_papers
"""

GET_ALL_AUTHORS = """
MATCH (a:Author)
OPTIONAL MATCH (a)-[:AFFILIATED_WITH]->(i:Institution)
RETURN a.id AS id, a.name AS name, a.h_index AS h_index,
       i.name AS institution, i.id AS institution_id
ORDER BY a.h_index DESC
LIMIT $limit
"""

GET_AUTHOR_BY_ID = """
MATCH (a:Author {id: $id})
OPTIONAL MATCH (a)-[:AFFILIATED_WITH]->(i:Institution)
OPTIONAL MATCH (a)<-[:AUTHORED_BY]-(p:Paper)
OPTIONAL MATCH (a)<-[:AUTHORED_BY]-(p2:Paper)-[:TAGGED_WITH]->(t:Topic)
RETURN a.id AS id, a.name AS name, a.h_index AS h_index,
       i.id AS institution_id, i.name AS institution_name, i.country AS institution_country,
       COLLECT(DISTINCT {id: p.id, title: p.title, year: p.year}) AS papers,
       COLLECT(DISTINCT t.name) AS topics
"""

GET_ALL_INSTITUTIONS = """
MATCH (i:Institution)
OPTIONAL MATCH (a:Author)-[:AFFILIATED_WITH]->(i)
OPTIONAL MATCH (a)<-[:AUTHORED_BY]-(p:Paper)
RETURN i.id AS id, i.name AS name, i.country AS country, i.ranking AS ranking,
       COUNT(DISTINCT a) AS author_count,
       COUNT(DISTINCT p) AS paper_count
ORDER BY i.ranking
LIMIT $limit
"""

GET_INSTITUTION_BY_ID = """
MATCH (i:Institution {id: $id})
OPTIONAL MATCH (a:Author)-[:AFFILIATED_WITH]->(i)
OPTIONAL MATCH (a)<-[:AUTHORED_BY]-(p:Paper)
OPTIONAL MATCH (a)-[:COLLABORATES_WITH]->(collab:Author)-[:AFFILIATED_WITH]->(other:Institution)
RETURN i.id AS id, i.name AS name, i.country AS country, i.ranking AS ranking,
       COLLECT(DISTINCT {id: a.id, name: a.name, h_index: a.h_index}) AS authors,
       COLLECT(DISTINCT {id: p.id, title: p.title, year: p.year}) AS papers,
       COLLECT(DISTINCT other.name) AS collaborating_institutions
"""

GET_ALL_TOPICS = """
MATCH (t:Topic)
OPTIONAL MATCH (p:Paper)-[:TAGGED_WITH]->(t)
RETURN t.id AS id, t.name AS name, t.category AS category,
       COUNT(p) AS paper_count
ORDER BY paper_count DESC
LIMIT $limit
"""

FIND_COLLABORATION_PATH = """
MATCH path = shortestPath(
    (a1:Author {id: $from_id})-[:AUTHORED_BY|COLLABORATES_WITH*1..6]-(a2:Author {id: $to_id}
))
RETURN [n IN nodes(path) | {
    type: HEAD(labels(n)),
    id: n.id,
    name: COALESCE(n.name, n.title)
}] AS path_nodes,
[r IN relationships(path) | TYPE(r)] AS path_relationships,
length(path) AS path_length
"""

FIND_CITATION_CHAIN = """
MATCH path = (start:Paper {id: $paper_id})-[:CITES*1..5]->(end:Paper)
WHERE length(path) <= $depth
RETURN [n IN nodes(path) | {
    id: n.id,
    title: n.title,
    year: n.year
}] AS chain,
length(path) AS chain_depth
ORDER BY chain_depth
LIMIT 20
"""

FIND_PAPERS_BY_SHARED_AUTHORS = """
MATCH (a1:Author {id: $author_id})<-[:AUTHORED_BY]-(p1:Paper)
      -[:AUTHORED_BY]->(a2:Author)
      -[:AUTHORED_BY]->(p2:Paper)
WHERE p1 <> p2 AND NOT (a1)<-[:AUTHORED_BY]-(p2)
RETURN DISTINCT p2.id AS id, p2.title AS title, p2.year AS year,
       p2.citations_count AS citations_count,
       COLLECT(DISTINCT a2.name) AS connecting_authors
ORDER BY p2.citations_count DESC
LIMIT $limit
"""

FIND_INFLUENCE_NETWORK = """
MATCH (target:Paper {id: $paper_id})
MATCH path = (influencer:Paper)-[:CITES*1..3]->(target)
OPTIONAL MATCH (influencer)-[:AUTHORED_BY]->(a:Author)
OPTIONAL MATCH (influencer)-[:TAGGED_WITH]->(t:Topic)
WITH influencer, a, t, min(length(path)) AS min_depth
RETURN DISTINCT influencer.id AS id, influencer.title AS title,
       influencer.year AS year, influencer.citations_count AS citations_count,
       COLLECT(DISTINCT a.name) AS authors,
       COLLECT(DISTINCT t.name) AS topics,
       min_depth AS influence_depth
ORDER BY influence_depth, influencer.citations_count DESC
LIMIT $limit
"""

RECOMMEND_COLLABORATORS = """
MATCH (a:Author {id: $author_id})<-[:AUTHORED_BY]-(p:Paper)-[:TAGGED_WITH]->(t:Topic)
MATCH (other:Author)<-[:AUTHORED_BY]-(p2:Paper)-[:TAGGED_WITH]->(t)
WHERE other <> a
  AND NOT (a)-[:COLLABORATES_WITH]-(other)
WITH other, a, t, COUNT(DISTINCT p2) AS shared_topic_papers
WHERE NOT EXISTS {
    MATCH (a)<-[:AUTHORED_BY]-(shared:Paper)-[:AUTHORED_BY]->(other)
}
WITH other, t, shared_topic_papers
ORDER BY shared_topic_papers DESC
RETURN other.id AS id, other.name AS name, other.h_index AS h_index,
       COLLECT(DISTINCT t.name)[..5] AS shared_topics,
       SUM(shared_topic_papers) AS topic_overlap
ORDER BY topic_overlap DESC
LIMIT $limit
"""

FIND_INTERDISCIPLINARY_AUTHORS = """
MATCH (a:Author)<-[:AUTHORED_BY]-(p:Paper)-[:TAGGED_WITH]->(t:Topic)
WITH a, COLLECT(DISTINCT t.name) AS topics, COUNT(DISTINCT t) AS topic_count,
     COUNT(DISTINCT p) AS paper_count
WHERE topic_count >= $min_topics
RETURN a.id AS id, a.name AS name, a.h_index AS h_index,
       topics, topic_count, paper_count
ORDER BY topic_count DESC, paper_count DESC
LIMIT $limit
"""

GET_GRAPH_STATS = """
MATCH (p:Paper) WITH COUNT(p) AS papers
MATCH (a:Author) WITH papers, COUNT(a) AS authors
MATCH (i:Institution) WITH papers, authors, COUNT(i) AS institutions
MATCH (t:Topic) WITH papers, authors, institutions, COUNT(t) AS topics
MATCH ()-[r:CITES]->() WITH papers, authors, institutions, topics, COUNT(r) AS citations
MATCH ()-[r2:AUTHORED_BY]->() WITH papers, authors, institutions, topics, citations, COUNT(r2) AS authorships
RETURN papers, authors, institutions, topics, citations, authorships
"""

SEARCH = """
CALL db.index.fulltext.queryNodes("search_index", $query + "~")
YIELD node, score
WITH node, score
RETURN LABELS(node)[0] AS type, node.id AS id,
       COALESCE(node.title, node.name) AS label,
       score
ORDER BY score DESC
LIMIT $limit
"""
