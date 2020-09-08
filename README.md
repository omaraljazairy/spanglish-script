# Spanglish Script

A basic local python script that has a quiz section to ask about Spanish Words & sentences. 

# Features 
  - Add Spanish words + translations in English.
  - Add Spanish sentences + translations in English.
  - Add words per category.
  - If the category is a verb, it will ask to add all the subject pronouns + the tenses.
  - Word quiz or sentence quiz, 10 questions per session.
  - If any word or sentence is answered correctly from the first time, it will not be repeated for the next sessions of the current day.
  - An overview of the results per word.

# Tech
  - Docker image with docker-compose 3.3
  - Python 3.8
  - Postgres DB
  - PgAdmin4

# Installation

  1- Pull the image from dockerhub after logging in from the command line using the folowing command: ``` $ docker pull onha2001/spanglishscript:latest ```.
  2- Run the image containers with the command ``` $ docker-compose up ``` .
  3- The credentials to connect with the database and pgadmin are in the docker-compose.yml file. When modied, change the credentials in the config.py file. Otherwise the script will not be able to connect with the database.
  4- The database schema file is included.
  5- Access the script by connecting to it's container.
  6- Run editor.py script to add words or sentences.
  7- Run quiz.py to start the quiz questions.

### PgAdmin setup

To use the pgadmin interface after runing its container, do the following:

```sh
a- open the browser with the url localhost:8080 .
b- login with the credentials set in the docker-compose.yml file.
c- create a new connection to the postgres server.
d- use the Gateway Ipaddress of postgres container.
e- to get the Gateway IPAddress, inspect the postgres <containername>.
f- when the connection is established, create the database spanglish_script .
g- the database schema.sql file is included in the spanglish folder.
```

### Todos

 - include the tests
 - write more instructions here.

### Author

 - Omar Aljazairy
 - omar@fedal.nl
 

License
----

[MIT](https://choosealicense.com/licenses/mit/)

