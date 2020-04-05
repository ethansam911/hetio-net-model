import os
from utils import file_splitter
from utils.neo4j import Neo4jController
from utils.mongodb import MongoDBController


#We start by displaying the User Interface
def main():

    # take edge and node tsv files and split them up by type
    # Having trouble writing to the correct directory on windows 
    file_splitter.write_node_files()
    file_splitter.write_edge_files()

    # Define databases for queries
    mongodb_controller = MongoDBController()
    mongodb_controller.create_database()

    neo4j_controller = Neo4jController()
    neo4j_controller.create_database()

    print(intitial_text)

    while True:
        # Receive the query user choice
        print('Query Choices:', queries)
        choice = user_input(queries, ('1', '2'))

        # Using mongoDB query
        if choice == '1':
            msg = "Please enter a disease name: "
            query = input(msg)
        else:
            neo4j_controller.query_db() 


        # Select the query, and query the choice
        if choice == '1':
            mongodb_controller.query_db(query)

        # Exit Sequence
        print()
        print('Would you like to exit?', exit)
        choice = user_input(exit, ('y', 'n'))
        if choice == 'y':
            break

    print('EXITING...')

queries = '''
1------Given a disease, what is its name, what are drug names that can treat or
palliate this disease, what are gene names that cause this disease, and where
this disease occurs?

2------Supposed that a drug can treat a disease if the drug or its similar drugs
up-regulate/down-regulate a gene, but the location down-regulates/up-regulates
the gene in an opposite direction where the disease occurs. Find all drugs
that can treat new diseases (i.e. the missing edges between drug and disease).

-------------------------PLEASE ENTER '1' OR '2'------------------------------
'''

intitial_text = '''Welcome!

This is a model of Hetio Net. Hetionet is an integrative network of biomedical
knowledge assembled from 29 different databases of genes, compounds, diseases,
and more. The network combines over 50 years of biomedical information into a
single resource, consisting of 47,031 nodes (11 types) and 2,250,197
relationships (24 types).

This simulation will answer 2 queries:'''

exit = '''
Y) Exit the program.
N) Run again.
'''

def clear():
    "Clears the screen depending on OS"
    os.system('cls' if os.name == 'nt' else 'clear')

def user_input(choice_info, choices):
    "Handle user input and validation."
    choice = None
    while True:
        choice = input("Enter your choice: ")
        if not choices or choice in choices:
            print()
            break
        print("Invalid choice, try again: ")
        print(choice_info)
    return choice


if __name__ == "__main__":
    # Run the main program
    main()
