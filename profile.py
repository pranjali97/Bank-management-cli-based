from datetime import datetime
import sqlite3 as sql
con = sql.connect("bank_data.db")
cur = con.cursor()
import traceback

global account_no
global cust_id

def change_addr():
    address = input("Enter address : ")
    cur.execute('UPDATE customer SET address = (?) WHERE cust_id = (?);',(address, cust_id))
    print("Address successfully changed\n")
    con.commit()

def open_account():
    try:
        li=["Savings Account","Current Account","Fixed Deposit Account"]
        for n,val in enumerate(li):
            print(n+1,val)
        amount = int(input("Enter Amount to be deposited in the FD : "))
        if amount > 0 and not amount%100:
            pass
        else:
            print("Enter amount in multiples of 1000")
            exit()    
        term = int(input("Enter the term for the FD(in terms of years): "))
        if (not term > 1) :
            print("Enter term period greater than 12 months")
            exit()
        cur.execute('INSERT INTO FD_table(account_no,amount,term) VALUES(?,?,?);',(account_no,amount,term))
        con.commit()
        value = cur.execute("SELECT fd_no FROM FD_table order by fd_no desc limit 1;")
        for row in value:
            fd_no = row[0] 
            print("Your fixed deposit number is :", fd_no)

        value=cur.execute("SELECT * FROM FD_table WHERE account_no=(?);",(account_no,))
        for row in value:
            print("FD number: ",row[0])
            print("Customer ID: ",row[1])
            print("Amount: ", row[2])
            print("Term: ", row[3])


    except Exception as e:
        print(e)
        traceback.print_exc() 
    


def deposit():
    amount = int(input("Enter Amount to be deposited : "))
    value = cur.execute('SELECT balance FROM accounts WHERE account_no = (?);', (account_no,))
    for row in value:
        bal=row[0]

    bal = bal + amount
    print("New balance is : ",bal)
    cur.execute('UPDATE accounts SET balance = (?) WHERE account_no = (?);', (bal, account_no))
    con.commit()
    cur.execute('INSERT INTO logTable(cust_id,account_no,deposit,withdraw,transfer,balance) VALUES (?,?,?,?,?,?);', (account_no,account_no,amount,'NULL','NULL', bal))
    con.commit()
    value = cur.execute('SELECT transaction_id FROM logTable ORDER BY transaction_id DESC limit 1;')
    for row in value:
        print("Your transaction ID is : ", row[0])


def withdraw():
    amount = int(input("Enter Amount to be withdrawl : "))
    value = cur.execute('SELECT balance FROM accounts WHERE account_no = (?);', (account_no,))
    for row in value:
        bal = row[0]

    if (bal - amount < 0):
        print('Not enough balance')
        exit()
    else:
        bal = bal-amount
        print("New balance is : ",bal)
        cur.execute('UPDATE accounts SET balance = (?) WHERE account_no = (?);', (bal, account_no))
        cur.execute('INSERT INTO logTable(cust_id,account_no,deposit,withdraw,transfer,balance) VALUES (?,?,?,?,?,?);',(account_no, account_no,"NULL", amount,"NULL", bal))
        con.commit()
        value = cur.execute('SELECT transaction_id FROM logTable ORDER BY transaction_id DESC limit 1;')
        for row in value:
            print("Your transaction ID is : ", row[0])


def get_statement():
    value = cur.execute('SELECT account_no, transaction_id, deposit, withdraw, transfer, balance FROM logTable WHERE account_no = (?);',(account_no,))
    for row in value:
        print("Account_no",row[0])
        print("Transaction_id",row[1])
        print("Deposit", row[2])
        print("Withdraw", row[3])
        print("Transfer", row[4])
        print("Balance", row[5])
       
            
def transfer_money():
    acc2 = int(input('Enter Account No. to transfer money : '))
    a = cur.execute('SELECT account_no FROM accounts WHERE account_no = (?);', (acc2,))
    value = cur.execute('SELECT balance FROM accounts WHERE account_no = (?);', (acc2,))
    for row in value:
        bal = row[0]   
        print(bal)
    if(a):
        amount = int(input('Enter amount to Transfer : '))
        value = cur.execute('SELECT balance FROM accounts WHERE account_no = (?);', (account_no,))
        for row in value:
            my = row[0]

        if ((my - amount) < 0):
            print('Not enough balance')
        else:
            my = my - amount
            bal = bal + amount
            cur.execute('UPDATE accounts SET balance = (?) WHERE account_no = (?);', (my, account_no))
            cur.execute('INSERT INTO logTable(cust_id,account_no,deposit,withdraw,transfer,balance) VALUES (?,?,?,?,?,?);',(account_no,account_no,"NULL","NULL",amount,my))
            cur.execute('UPDATE accounts SET balance = (?) WHERE account_no = (?);', (bal, acc2))
            print("Transfer Complete")
            con.commit()
            value = cur.execute('SELECT transaction_id FROM logTable ORDER BY transaction_id DESC limit:1;')
            for row in value:
                print("Your trabsaction ID is : ", row[0])
    else:
        exit()

    
def close_account():
    cur.execute('UPDATE accounts SET account_status=(?), account_closing_date =CURRENT_TIMESTAMP WHERE account_no = (?);', ("closed", account_no,))
    con.commit()
    print("Account closed")



def get_loan():
    amount = int(input("Enter Amount of loan to be issued : "))
    if(amount>0 and not amount%100):
        pass
    else:
        print("Enter amount in multiples of 1000")
        exit()    
    term = int(input("Enter the term of the loan(in terms of years): "))
    cur.execute('INSERT INTO loan_table(account_no,amount,term) VALUES(?,?,?);',(account_no,amount,term))
    con.commit()
    value = cur.execute("SELECT loan_id FROM loan_table order by loan_id desc limit 1;")
    for row in value:
        loan_id = row[0] 
        print("Your Loan ID is :", loan_id)  
    value = cur.execute("SELECT * FROM loan_table WHERE account_no=(?);",(account_no,))
    for row in value:
        print("Loan number: ",row[0])
        print("Customer ID: ",row[1])
        print("Amount: ", row[2])
        print("Term: ", row[3])
                      


def logout():
    print("logging out")
    exit()            
    
       
def profile_func(acc):
    global account_no
    account_no = acc
    global cust_id
    cust_id = acc
    li = ["Address Change","Open New Acccount", "Money Deposit","Money Withdrawal", "Transfer Money","Print Statement","Account Closure","Avail Loan","Customer Logout"]
    for n,val in enumerate(li):
        print(n+1,val)
    choice_dict={
                    1:change_addr,
                    2:open_account,
                    3:deposit,
                    4:withdraw,
                    5:transfer_money,
                    6:get_statement,
                    7:close_account,
                    8:get_loan,
                    9:logout
                }
    choice = int(input("Enter your choice : "))
    choice_dict[choice]()
            
