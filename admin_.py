import sqlite3 as sql
con = sql.connect("bank_data.db")
cur = con.cursor()

def display_close_accounts():
	value = cur.execute("SELECT account_no, account_closing_date FROM accounts WHERE account_status=(?);",("closed",))
	for row in value:
		print("Account number",row[0])
		print("Closing Date", row[1])

def FD_report():
	try:
		account_no = int(input("Enter the customer ID"))
		a = cur.execute("SELECT cust_id FROM customer WHERE cust_id = (?);", (account_no,))		
		if (a):
			value = cur.execute("SELECT fd_no, amount, term FROM FD_table WHERE account_no =(?);", (account_no,))
			for row in value:
				print("FD number", row[0])
				print("Amount", row[1])
				print("Term", row[2])

			if(value == 'NULL'):
				print("N.A")
	
	except Exception as e:
		print(e)

def FD_customer():
	try:
		account_no = int(input("Enter the customer ID"))
		a = cur.execute("SELECT cust_id FROM customer WHERE cust_id = (?);", (account_no,))
		if (a):
			amt = 0
			value = cur.execute("SELECT SUM(amount) FROM FD_table WHERE account_no = (?);", (account_no,))
			for row  in value:
				amt = row[0] 
				print(amt)
			
			value = cur.execute("SELECT * FROM FD_table WHERE amount > (?);", (amt,))
			for row in value:
				print("Account no", row[0])
				print("FD number", row[1])
				print("Amount", row[2])
				print("Term", row[3])
		else:
			print("Account number is invalid")

	except Exception as e:
		print(e)
	

def FD_amount():
	try:
		amount = int(input("Enter the amount"))
		if(amount>0 and not amount%100):
			value = cur.execute("SELECT * FROM FD_table WHERE amount > (?);", (amount,))
			for row in value:
				print("Account Number", row[0])
				print("FD number", row[1])
				print("Amount", row[2])
				print("Term", row[3])
		else:
			print("Enter amount in multiples of 1000")
			exit() 	
	except Exception as e:
		print(e)
	
def loan_report():
	try:
		account_no = int(input("Enter the customer ID"))
		a = cur.execute("SELECT cust_id FROM customer WHERE cust_id = (?);",(account_no,))		
		if (a):
			value = cur.execute("SELECT loan_id, amount, term FROM loan_table WHERE account_no =(?);",(account_no,))
			for row in value:
				print("Loan number", row[0])
				print("Amount", row[1])
				print("Term", row[2])

			if(value == 'NULL'):
				print("N.A")
		else:
			print("Incorrect customer ID")

	except Exception as e:
		print(e)
	
def loan_customer():
	try:
		account_no = int(input("Enter the customer ID"))
		a = cur.execute("SELECT cust_id FROM customer WHERE cust_id = (?);", (account_no,))
		if (a):
			amt = 0
			value = cur.execute("SELECT SUM(amount) FROM loan_table WHERE account_no = (?);", (account_no,))
			for row  in value:
				amt = row[0] 
				print(amt)
			
			value = cur.execute("SELECT * FROM loan_table WHERE amount > (?);", (amt,))
			for row in value:
				print("Account no", row[0])
				print("FD number", row[1])
				print("Amount", row[2])
				print("Term", row[3])
		else:
			print("Account number is invalid")

	except Exception as e:
		print(e)
	

def loan_amount():
	try:
		amount = int(input("Enter the amount"))
		if(amount>0 and not amount%100):
			value = cur.execute("SELECT * FROM loan_table WHERE amount > (?);", (amount,))
			for row in value:
				print("Account Number", row[0])
				print("Loan number", row[1])
				print("Amount", row[2])
				print("Term", row[3])	
		
	except Exception as e:
		print(e)


def loan_fd_report():
	try:
		value = cur.execute("SELECT ln.account_no FROM loan_table as ln GROUP BY account_no HAVING SUM(ln.amount) > (SELECT SUM(fd.amount) FROM FD_table as fd WHERE fd.account_no = ln.account_no);")
		for row in value:
			print("Account Number: ", row[0])
	except Exception as e:
		raise

def cust_yet_to_avail_loan():
	try:
		value = cur.execute("SELECT account_no FROM accounts WHERE account_no NOT IN(SELECT account_no FROM loan_table);")
		for row in value:
			print("Account Number: ",row[0])

	except Exception as e:
		print(e)

def cust_yet_to_get_FD():
	try:
		value = cur.execute("SELECT account_no FROM accounts WHERE account_no NOT IN(SELECT account_no FROM FD_table);")
		for row in value:
			print("Account Number: ",row[0])
		
	except Exception as e:
		print(e)

def cust_no_fd_laon():
	try:
		value = cur.execute("SELECT account_no FROM accounts WHERE account_no NOT IN(SELECT account_no FROM loan_table) and account_no NOT IN(SELECT account_no FROM FD_table );")
		for row in value:
			print("Account number", row[0])
	except Exception as e:
		raise
			
		
def admin_logout():
	exit()

def admin_func():
	while True:
		li=["Print closed accounts","FD report of customer","FD report of customer vis-a-vis another customer","FD report w.r.t amount","Loan report of customer","Loan report of customer vis-a-vis another customer","Loan repost w.r.t loan amount","Loan-FD Report","Report of customers yeet to avail a loan"," Report of customer who are yet to open an FD acccount"," Report of customer with neither laon nor FD account","Admin Logout"]
		for n,val in enumerate(li):
			print(n+1,val)

		choice_dict={1:display_close_accounts,2:FD_report,3:FD_customer,4:FD_amount,5:loan_report,6:loan_customer,7:loan_amount,8:loan_fd_report,9:cust_yet_to_avail_loan,10:cust_yet_to_get_FD,11:cust_no_fd_laon,12:admin_logout}
		choice = int(input("Enter your choice : "))
		choice_dict[choice]()