

This Project contains analysis of news database and code has been written in language python3 and postgresql database. Also, there is bit of HTML to display result in web pages. 

To describe it slightly deeper, this project gives three different analysis result on news database. Project aims to analyse news database and display result of following:
1. The most popular three articles of all time
2. The most popular article authors of all time
3. Days on which more than 1% of requests led to errors

Requirements:
1. Vagrant
2. Virtualbox
Be sure to instruct the user to install Vagrant and VirtualBox, and instruct them on how to start and log into the virtual machine.
or Enviornment of your choice with following:
1. Python3
2. PostgreSQL
3. psycopg2


Set-up the news database:
User can follow this steps while using their choosen environment:
from psql console create news database by typing
CREATE DATABASE news;
also get the newsdata.sql file with the database schema and data from the path https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip 
Unzip this file after downloading. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.
To load the data, cd into the vagrant directory and use the command psql -d news -f newsdata.sql.

User can follow this steps while using Vagrant:
Next, Download data from https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip. You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.
To load the data, cd into the vagrant directory and use the command psql -d news -f newsdata.sql.

To run this project any individual should have news database and log_analysis.py file. After that run this log_analysis.py and access it through a web page as per given address. A simple Web page displays three buttons to see three different analysis.
