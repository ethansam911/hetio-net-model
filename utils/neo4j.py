import csv
import os
from py2neo import Graph
from py2neo.data import Node, Relationship

from utils.common import node_types, edge_types, abbreviations,\
        NEO4J_USERNAME, NEO4J_PASSWORD


class Neo4jController():
    #Our bolt connection needs to begin once we start our database in Neo4j Desktop
    def __init__(self):
        self.graph = Graph("bolt://localhost:7687", user=NEO4J_USERNAME, password=NEO4J_PASSWORD)
    #Delete all nodes and relationships in the database
    def clear_db(self):
        self.graph.delete_all()

    def create_db(self):
        query = "MATCH (n) RETURN COUNT(n);"
        result = self.graph.run(query).data()
        if result[0]['COUNT(n)'] != 0:
            print("Neo4j database found")
            return

        print("Creating Neo4j database")
        for node_type in node_types:
            print(f"Creating nodes for type: {node_type}")
            query = f"CREATE CONSTRAINT ON (n:{node_type}) ASSERT n.id is UNIQUE"
            self.graph.run(query)
        #4 Node type queries are created, but this query isn't run
            query = f"""
            USING PERIODIC COMMIT 500
            LOAD CSV WITH HEADERS FROM "file:///{node_type}.tsv" AS row FIELDTERMINATOR "\\t"
            CREATE (:{node_type} {{id:row.id, name:row.name}});
            """
            self.graph.run(query)
        # Here we are querying the relationships 
        for edge_type in edge_types:
            print(f"Creating edges for type: {edge_type}")
            source_type = abbreviations[edge_type[0]]
            target_type = abbreviations[edge_type[-1]]
            relationship = abbreviations[edge_type[1:-1]]
            #Account for Gene regulates Gene, remove the '>'
            if edge_type == 'Gr>G':
                edge_type = 'GrG'
            query = f"""
            USING PERIODIC COMMIT 500
            LOAD CSV WITH HEADERS FROM "file:///{edge_type}.tsv" AS row FIELDTERMINATOR "\\t"
            MATCH (a:{source_type} {{id:row.source}})
            MATCH (b:{target_type} {{id:row.target}})
            CREATE (a)-[:{relationship}]->(b);
            """
            self.graph.run(query)

    def query_db(self, compound):
        if compound == "":
            query = """
            MATCH (c:Compound)-[:upregulates]->(:Gene)<-[:downregulates]-(d:Disease)
            WHERE NOT (c)-[:treats]->(d)
            MATCH (c:Compound)-[:downregulates]->(:Gene)<-[:upregulates]-(d:Disease)
            WHERE NOT (c)-[:treats]->(d)
            RETURN DISTINCT c.name, d.name
            """
        else:
            #Second Query,Find all Compoung-Disease pairs 
            query = f"""
            MATCH (c:Compound {{name: "{compound}"}})-[:upregulates]->(:Gene)<-[:downregulates]-(d:Disease)
            WHERE NOT (c)-[:treats]->(d)
            MATCH (c:Compound {{name: "{compound}"}})-[:downregulates]->(:Gene)<-[:upregulates]-(d:Disease)
            WHERE NOT (c)-[:treats]->(d)
            RETURN DISTINCT c.name, d.name
            """
        results = self.graph.run(query).data()
        if not results:
            print("No Compound-Disease pairs found")
        else:
            i = 0
            print("Compound-Disease pairs:")
            for result in results:
                #New f-strings in python 3.6
                print(f"{i+1}\t{result['c.name']}-{result['d.name']}") 
                i+=1