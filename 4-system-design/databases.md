# Databases

- Can we make a software application without using databases?
- We can use a simple file to store all the records on separate lines and retrieve them from the same file. But using a file for storage has some limitations:
- **Limitations of file storage:**
    - We can't offer concurrent management to separate users accessing the storage files from different locations.
    - We can't grant different access rights to different users.
    - How will the system scale and be available when adding thousands of entries?
    - How will we search content for different users in a short time?
- Above limitations can be addressed using databases.
- A **database** is an organized collection of data that can be managed and accessed easily. These are created to make it easier to store, retrieve, modify, and delete data in connection with different data-processing procedures.
- There are two basic types of databases:
    - SQL(relational databases)
    - NoSQL(non-relational databases)
- Relational databases, like phone books that record contact numbers and addresses, are organized and have predetermined schemas. 
- Non-relational databases, like file directories that store anything from a person's contact information to shopping preferences, are unstructured, scattered, and feature a dynamic schema.

## Advantages

- **Managing large data**
- **Retrieving accurate data (data consistency)**
- **Easy updation**
- **Security**
- **Data Integrity**
- **Availability**
- **Scalability**

## Types of Databases

### Relational Databases

- The data stored in relational databases has prior structure. Mostly, this model organizes data into one or more relations (also called tables), with a unique key for each tuple (instance). Each entity of the data consists of instances and attributes, where instances are stored in rows, and the attributes of each instance are stored in columns. Since each tuple has a unique key, a tuple in one table can be linked to a table in other tables by storing the primary keys in other tables, generally known as foreign keys.
- A Structured Query Language (SQL) is used for manipulating the database. THis includes insertion, deletion, and retrieval of data.
- Relational databases provide the ACID(atomicity, consistency, isolation, and durability)
- ACID is a powerful abstraction that simplifies complex interactions with the data and hides many anomalies behind a simple transaction abort.
- **Atomicity:** A transaction is considered an atomic unit. Hence, either all the statements within a transaction will successfully execute or none of them will execute. If a statement fails within a transaction, it should be aborted and rolled back.
- **Consistency:** At any given time, the database should be in a consistent state after every transaction. 
- **Isolation:** In the case of multiple transactions running concurrently, they shouldn't be affected by each other. The final state of the database should be the same as the transactions that were executed sequentially.
- **Durability:** The system should guarantee that completed transactions will survive permanently in the database even in system failure events.

**Some of the popular DBMSs are:**

- **MySQL**
- **Oracle Database**
- **Microsoft SQL Server**
- **IBM DB2**
- **Postgres**
- **SQLite**

#### Features:

- **Flexibilty:** *Data Definition Language(DDL)* is used to create and modify the structure of database objects in a database. It provides the flexibility to modify the database, including tables, columns, renaming the tables, and other changes. DDL even allows us to modify schema while other queries are happening and the database server is running.
- **Reduced Redundancy:** One of the biggest advantages of the relational database is that it eliminates data redundancy. The information related to a specific entity appears in one table while the relevant data to that specific entity appears in the other tables linked through foreign keys. This process is called normalization and has the additional benefit of removing an *inconsistent dependency*.
- **Concurrency:** 