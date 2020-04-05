import csv
#The OS module in python provides functions for interacting with the operating system. OS, 
#comes under Python’s standard utility modules
import os
import pymongo


class MongoDBController():
    "Singleton class to control mongo db connection."

    def __init__(self):
        "Initialize variables for later usage."
        #self represents the instance of the class. By using the “self” 
        #keyword we can access the attributes and methods of the class in python
        self.data_dir = os.path.join(os.getcwd(), "data")
        self.m_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.m_db = self.m_client["hetionet"]
        self.m_col = self.m_db["data"]

    def create_database(self):
        "Populate document if it doesn't already exist."
        # count() is being deprecated, we need to check if document exists
        # this way instead of a mongo method
        cols = 0
        for _ in self.m_col.find().limit(1):
            cols += 1
        # early exit
        if cols != 0:
            print("Mongo Database Found!")
            return
        
        print("Creating MongoDB Database!")

        # Group the diseases where we have a single document per disease
        # because Create, Read, and Delete operations are fast but
        # update is costly. We have one db interaction in this method, 
        #so communication cost is lowered.
        # A disease has the following structure:


        # disease = {
        #     "id": str,
        #     "name": str,
        #     "treat": [str],
        #     "palliate": [str],
        #     "gene": [str],
        #     "where": [str],
        #     }
        diseases = {}

        # this is to splice the data in nodes.tsv so we can add the
        # relationships from edges.tsv to our nice diseases{}
        data = {
            'Anatomy': {},
            'Gene': {},
            'Disease': {},
            'Compound': {}
        }

        with open(os.path.join(self.data_dir, "nodes.tsv"), "r") as nodes_file:
            reader = csv.DictReader(nodes_file, delimiter="\t")
            for row in reader:
                data[row['kind']][row['id']] = row['name']

        for k, v in data['Disease'].items():
            diseases[k] = {
                #We identify k with kind
                'id': k,
                'name': v,
                "treat": [],
                "palliate": [],
                "gene": [],
                "c": [],
            }

    
        rel_mapping = {
            "CtD": ['target', 'source', "Compound", "treat"],
            "CpD": ['target', 'source', "Compound", "palliate"],
            "DaG": ['source', 'target', "Gene", "gene"],
            "DuG": ['source', 'target', "Gene", "gene"],
            "DdG": ['source', 'target', "Gene", "gene"],
            "DlA": ['source', 'target', "Anatomy", "where"]
        }

        with open(os.path.join(self.data_dir, "edges.tsv"), "r") as nodes_file:
            reader = csv.DictReader(nodes_file, delimiter="\t")
            for row in reader:
                edge = row['metaedge']
                if edge in rel_mapping.keys():
                    diseases[row[rel_mapping[edge][0]]][rel_mapping[edge][3]].append(
                        data[rel_mapping[edge][2]][row[rel_mapping[edge][1]]]
                        )

        # decompose diseases{} such that each disease becomes a document in the collection
        # m_col is a colleciton, we decompose the diseases{} object and insert each disease as a document
        self.m_col.insert([v for _, v in diseases.items()])

    def query_db(self, query):
        "Queries the database."
        cur_id = self.m_col.find({"id": query})

        cols = 0  # count return
        for _ in cur_id:
            if cols > 0:
                break
            cols += 1

        # choose which query was proper
        if cols == 0:
            cur = self.m_col.find({"name": query})
        else:
            cur_id.rewind()  # to iterate again, we need to reset cursor
            cur = cur_id     #cursor is a document position within the collection 

        cols = 0
        id = ""
        name = ""
        treat = []
        palliate = []
        gene = []
        where = []

        for i in cur:
            # set name and id if found
            id = i['id']
            name = i['name']
            # Create Read and Delete are fast, and Update is slow we get data split into multiple
            # documents
            #Extends 
            treat.extend(i['treat'])
            palliate.extend(i['palliate'])
            gene.extend(i['gene'])
            where.extend(i['where'])
            #Think about this like a 2D array, every column is another document 
            cols += 1

        # If nothing is found, we early exit
        if cols == 0:
            print(f'Nothing has been found for disease "{query}".')
            return

        def m_join(sep, items):
            "cleaner syntax for join to use for mapping"
            return sep.join(items)

        def m_pretty(items):
            "Turns a python list -> commas separated str 5 per line"
            # return None if list was empty
            if not items:
                return "None"

            # separate python list into groups of 10
            items = [items[i:i+10] for i in range(0, len(items), 10)]

            # join the groups of 10 to be comma delimited strs
            commas = map(lambda x: m_join(", ", x) + ',', items)

            # Join all groups with newlines and take out  commas on last line
            return m_join("\n\t", commas)[:-1]

        print(
            f'For the disease "{query}", we found...\n', f'ID:\n\t{id}\n',
            f'Name:\n\t{name}\n\n', f'Drugs that can Treat "{query}":\n\t{m_pretty(treat)}\n\n',
            f'Drugs that can Palliate "{query}":\n\t{m_pretty(palliate)}\n\n', f'Genes that cause "{query}":\n\t{m_pretty(gene)}\n\n',
            f'Where "{query}" Occurs:\n\t{m_pretty(where)}\n',
            sep='\n\n'
            )
