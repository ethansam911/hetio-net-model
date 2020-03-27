import os
from pathlib import Path, PureWindowsPath
# os.getcwd stands for get current working directory
DATA_DIR = os.path.join(os.getcwd(), "data")

#The four main types of nodes
node_types = ["Compound", 
              "Disease", 
              "Gene", 
              "Anatomy"
              ]

#Metaedges - Aka relationships
edge_types = ["CrC", "CtD", "CpD", 
              "CuG", "CbG", "CdG", 
              "DrD", "DuG", "DaG",
              "DdG", "DlA", "AuG", 
              "AeG", "AdG", "Gr>G", 
              "GcG", "GiG"]

#Break down the relationships to elementary key-value pairings
abbreviations = {
        "C": "Compound", 
        "D": "Disease", 
        "G": "Gene", 
        "A": "Anatomy",
        "r": "resembles", 
        "t": "treats", 
        "p": "pilliates",
        "u": "upregulates", 
        "d": "downregulates", 
        "b": "binds",
        "a": "associates", 
        "l": "localizes", 
        "e": "expresses",
        "r>": "regulates", 
        "c": "covaries", 
        "i": "interacts"
        }

#This Path exists on Windows, (Navigate using ubuntu)
NEO4J_HOME = "/mnt/c/Users/esam5/.Neo4jDesktop/neo4jDatabases/database-c173d399-1188-4720-afc0-4ced93a06bfb/installation-3.5.14"

#This is our neobolt endpoint, this will appear  
NEO4J_URL = "localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"
