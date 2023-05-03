
#Mysql

sudo mysql -u username\root -p
#Type the password .

CREATE DATABASE db_name;

SHOW DATABASES;

to create new user and grant permission:
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON * . * TO 'username'@'localhost';


USE db_name;

CREATE TABLE tablename (
Column_a VARCHAR(50) NOT NULL,
Column_b VARCHAR(30) NOT NULL,
Column_c VARCHAR(60) NOT NULL,
Column_d INT NOT NULL, PRIMARY KEY(Column_a));

Describe table_Name;

INSERT INTO tablename VALUE  ("Value1", "value 2", "value 3", 1234);

SELECT * FROM tablename;

#To Display  Column Data
SELECT Column_name FROM tablename;

#To Create a View
CREATE VIEW view_name AS SELECT column FROM tablename WHERE column_1 > condition;
SELECT * FROM view_name;
ALTER VIEW view_name AS SELECT column FROM movies WHERE column_1 < condition;

#To run script :
sudo mysql -u root -p < script1.sql>



