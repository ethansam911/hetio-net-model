import os
from utils import tsv_splitter
from utils.neo4j import Neo4jController
from utils.mongo import MongoController



QUERIES = '''
1------Given a disease, what is its name, what are drug names that can treat or
palliate this disease, what are gene names that cause this disease, and where
this disease occurs?

2------Supposed that a drug can treat a disease if the drug or its similar drugs
up-regulate/down-regulate a gene, but the location down-regulates/up-regulates
the gene in an opposite direction where the disease occurs. Find all drugs
that can treat new diseases (i.e. the missing edges between drug and disease).

-------------------------PLEASE ENTER '1' OR '2'------------------------------
'''

WELCOME_MESSAGE = '''Welcome!

This is a model of Hetio Net. Hetionet is an integrative network of biomedical
knowledge assembled from 29 different databases of genes, compounds, diseases,
and more. The network combines over 50 years of biomedical information into a
single resource, consisting of 47,031 nodes (11 types) and 2,250,197
relationships (24 types).

This simulation will attempt to answer 2 queries:'''

EXITING = '''
Y) Exit the program.
N) Run another query.
'''

def user_input(choice_details, choices):
    "Handle user input and validation."
    choice = None
    while True:
        choice = input("Enter your choice: ")
        if not choices or choice in choices:
            print()
            break
        print("Invalid response, please choose: ")
        print(choice_details)
    return choice

def clear_screen():
    "Clears the screen depending on OS"
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    "Displays UI"

    # take edge and node tsv files and split them up by type
    # Having trouble writing to the correct directory on windows 
    tsv_splitter.write_node_files()
    tsv_splitter.write_edge_files()

    # Define databases for queries
    mongo_controller = MongoController()
    mongo_controller.create_db()

    neo4j_controller = Neo4jController()
    neo4j_controller.create_db()

    print(WELCOME_MESSAGE)

    while True:
        # Receive the query user choice
        print('Query Choices:', QUERIES)
        choice = user_input(QUERIES, ('1', '2'))

        # Using mongoDB query
        if choice == '1':
            msg = "Please enter a disease name: "
        else:
            msg = "Please enter a drug name (empty for all possible drugs): "

        query = input(msg)

        # Select the query, and query the choice
        controller = mongo_controller if choice == '1' else neo4j_controller
        controller.query_db(query)

        # Exit Sequence
        print()
        print('Would you like to exit the program now?', EXITING)
        choice = user_input(EXITING, ('Y', 'N'))
        if choice == 'Y':
            break

    print('EXITING...')


if __name__ == "__main__":
    # Run main program
    main()