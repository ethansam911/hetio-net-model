import os
from pathlib import Path, PureWindowsPath
from utils.common import NEO4J_HOME, node_types, edge_types
#Accessing the node_types, edge_types

# os.chdir('/mnt/c/Users/esam5/.Neo4jDesktop/neo4jDatabases/database-c173d399-1188-4720-afc0-4ced93a06bfb/installation-3.5.14')
def write_node_files():
    for node_type in node_types:
        out_file_path = os.path.join(NEO4J_HOME, "import", f"{node_type}.tsv")
        if os.path.exists(out_file_path):
            continue
        print(f"Writing file for {node_type} nodes to {out_file_path}")
        command = f"echo 'id\tname\tkind' > {out_file_path}"
        os.system(command)
        #a Unix command used to search files for the 
        #occurrence of a string of characters that matches a specified pattern.
        command = f"grep '{node_type}' data/nodes.tsv >> {out_file_path}"
        os.system(command)

def write_edge_files():
    for edge_type in edge_types:

        out_file_path = os.path.join(NEO4J_HOME, "import", 
                f"{edge_type.replace('>', '')}.tsv");
        if os.path.exists(out_file_path):
            continue
        print(f"Writing file for {edge_type} edges to {out_file_path}")
        command = f"echo 'source\tmetaedge\ttarget' > {out_file_path}"
        os.system(command)
        command = f"grep '{edge_type}' data/edges.tsv >> {out_file_path}"
        os.system(command)
