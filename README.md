# hetio-net
Big Data Project  
Project I: Model of HetioNet

Sam_Eldesouki: Ethan Sam/Merna Eldesouki


### Dependencies

- Python 3+
- mongo 4+
- neo4j 3.5+
- pymongo 3.10.1
- py2neo 4.3.0

### Setup

### How to run - (Windows Subsystem for Linux )

- start the MongoDB service:
    - `sudo systemctl enable mongodb.service`
- start the neo4j service:
  - For Windows 10 
        - Run neo4J Desktop and create a new database 
  - For Ubuntu
        - `sudo systemctl start newo4j.service`

![](https://media.discordapp.net/attachments/688449265227268174/692893417289678908/unknown.png)
![](https://media.discordapp.net/attachments/688449265227268174/692895470854471730/unknown.png)

- For Ubuntu, use `sudo systemctl start neo4j.service`
- In the file `<neo4j-home>\conf\neo4j.conf` make sure that `dbms.directories.import` is set to `<neo4j-home>\import`.
  - To see this through the GUI Client, use 
  ![](https://media.discordapp.net/attachments/688449265227268174/695981233267539998/unknown.png?width=555&height=704)
- the directory `<neo4j-home>\import` should exist and your user should have read and write access to it:

- Change `utils/common.py` to match the neo4j username and password, in the GUI this can be changed here:


```bash terminal 
 python3 app.py 
```

### edges.tsv relationships

#### Disease
- DrD = Disease Resembles Disease
- DlA = Disease Localizes Anatomy
- DuG = Disease Upregulates Gene
- DaG = Disease Associates Genes
- DdG = Disease Downregulates Genes

#### Compound
- CrC = Compound Resembles Compound
- CtD = Compound Treats Disease
- CpD= Compound Palliates Diseases
- CuG = Compound Upregulates Genes
- CbG = Compound Binds Genes
- CdG = Compound Downregulates Gene

#### Anatomy
- AuG = Anatomy Upregulates Genes
- AeG = Anatomy Expresses Gene
- AdG = Anatomy Downregulates Genes

#### Gene
- Gr>G = Gene Regulates Gene
- GcG = Gene Covaries Gene
- GiG = Gene Interacts Gene

### Goals

Queries

1. Given a disease, what is its name, what are drug names
that can treat or palliate this disease, what are gene
names that cause this disease, and the location in which this disease
occurs? Obtain and output this information in a single
query.
    - In order to do this, we  create a MongoDB database that stores 
    every disease in a document with relevant information

1. Supposed that a drug can treat a disease if the drug or
its similar drugs up-regulate/down-regulate a gene, but
the location down-regulates/up-regulates the gene in
an opposite direction where the disease occurs. Find all
drugs that can treat new diseases (i.e. the missing
edges between drug and disease). Obtain and output
the drug-disease pairs in a single query.

    - In order to do this, we create a neo4j database 
    modelling a graph of Hetionet and then querying the relevant paths


