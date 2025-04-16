# Flask-ETL
Dockerized python application that implements an ETL (extract-transform-load) & data fusion pipeline on the data of a group of users, their relationships, and their owned clothes.
![image](https://github.com/user-attachments/assets/5ff0bc83-8d3a-4ada-af04-f3400659ca4f)  
Initially, the data of the clothes are present in a MySQL relational database, and the users' owned clothes and relationships are stored in a Neo4J graph database. After the execution of the pipeline, the fused data are stored in a MongoDB document database.  
  
Additionally, a Flask REST API provides methods to retrieve the fused data and to recommend a new clothe to a user depending on the clothes owned by his friends and colleagues. If all of the clothes owned by the user's friends and colleagues are already owned by the user, then the most popular clothe will be recommended.
