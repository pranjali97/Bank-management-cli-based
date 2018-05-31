drop table if exists customer;
	create table customer(
		cust_id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		email CHAR(50) NOT NULL unique,
		telephone INTEGER NOT NULL,
		date_of_birth datetime NOT NULL,
		address TEXT NOT NULL,
		password CHAR(50) NOT NULL
		);

drop table if exists accounts;
	create table accounts(
		account_creation_date datetime NOT NULL,
		account_no INTEGER PRIMARY KEY AUTOINCREMENT,
		balance INTEGER NOT NULL,
		account_type CHAR(20) NOT NULL,
		account_status CHAR(20) NOT NULL,
		account_lock INTEGER DEFAULT 1 ,
		account_closing_date datetime
		);

drop table if exists logTable;
	create table logTable(
		cust_id INTEGER not null,
		account_no INTEGER NOT NULL,
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
		deposit varchar(20),
		withdraw varchar(20),
		transfer varchar (20),
		balance integer 
		);	

drop table if exists FD_table;
	create table FD_table(
		fd_no INTEGER PRIMARY KEY AUTOINCREMENT,
		account_no INTEGER NOT NULL,
		amount INTEGER NOT NULL,
		term INTEGER not null
		);

drop table if exists loan_table;
	create table loan_table(
		loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
		account_no INTEGER NOT NULL,
		amount INTEGER NOT NULL,
		term INTEGER not null
		);

