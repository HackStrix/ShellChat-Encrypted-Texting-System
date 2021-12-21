# encrypted-texting-system

This is a chatting sytem created using python and mysql, this allows users to communicate over an encrypted channel using rsa(512). The server.py mantains a database of public keys of the every username on the network along with the encrypted chats of the users. These chats are encrypted using rsa and base64 which can only be decrypted using the rsa private key stored locally on the users computer. This allows encypted and secure flow of messages over the internet without violating the message privacy.

## Setup

```pip install -r requirements.txt```

### mysql commands for server.py before running

```create database userdata;```

```CREATE USER sankalp IDENTIFIED BY 123456;```

``` GRANT ALL PRIVILEGES ON userdata.* TO 'sankalp'@'localhost';```

``` CREATE TABLE history (chat_id int, to_user varchar(255) NOT NULL, from_user varchar(255) NOT NULL, message varchar(10000));```

```insert into history values ("lool", "lool", "dkjnfkjnkjfnkjf", 0);```

```CREATE TABLE userkeys (username varchar(255) primary key not null,public_n varchar(1000) not null, public_e int not null);```

