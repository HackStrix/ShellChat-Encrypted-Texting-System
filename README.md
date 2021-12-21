# encrypted-texting-system


## Setup

```pip install -r requirements.txt```

### mysql commands for server.py before running

```create database userdata;```

```CREATE USER sankalp IDENTIFIED BY 123456;```

``` GRANT ALL PRIVILEGES ON userdata.* TO 'sankalp'@'localhost';```

``` CREATE TABLE history (chat_id int, to_user varchar(255) NOT NULL, from_user varchar(255) NOT NULL, message varchar(10000));```

```insert into history values ("lool", "lool", "dkjnfkjnkjfnkjf", 0);```

```CREATE TABLE userkeys (username varchar(255) primary key not null,public_n varchar(1000) not null, public_e int not null);```

