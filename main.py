import sqlite3 as sql
import os
import readline
import profile
import admin_
import traceback

os.system('clear')

con = sql.connect('bank_data.db')
cur = con.cursor()

def signup_func():
    try:
        account_type = input("\nInput Account Type (s: saving account c: current account) : ")
        balance = int(input("Amount initiated : "))
        if (account_type is 'c' and balance < 5000) or (balance < 0):
            print("Invalid Amount")
            exit()        

        print("Enter your details:")
        name = input("\nFull Name : ")
        email = input("\nEmail: ")
        telephone = input("\nPhone no:")
        date_of_birth=input("\nDOB(dd/mm/yyyy):")
        address = input("\nAddress: ")
        password = input("\nPlease enter your desired password.")
        while (len(password)<8):
            password = input("Pass should have more than 8 characters. Please retry.")  

        cur.execute("INSERT INTO customer(name,email,telephone,date_of_birth,address,password) VALUES(?,?,?,?,?,?);",(name,email,telephone,date_of_birth,address,password))
    
        con.commit()
        account_status = "open"
        account_lock = 1
        cur.execute("INSERT INTO accounts(account_creation_date,balance,account_type,account_status,account_lock) VALUES(CURRENT_TIMESTAMP,?,?,?,?);",(balance,account_type,account_status,account_lock))

        con.commit()
        value=cur.execute("SELECT cust_id FROM customer order by cust_id desc limit 1;")
        for row in value:
            account_no = row[0] 

        print("\nYour Account number : ",account_no)
        val='NULL'
        cur.execute('INSERT INTO logTable(cust_id,account_no,deposit,withdraw,transfer,balance) VALUES(?,?,?,?,?,?);',(account_no,account_no,val,val,val,balance))
        con.commit()
    
    except Exception as e:
            print(e)
            traceback.print_exc()    

def signin_func():
    i=0
    while (i<3):
        try:
            account_no = int(input("Enter your Account Number : "))
            password = input("Enter Password : ")
            value = cur.execute("SELECT password FROM customer WHERE cust_id = (?);",(account_no,))
            for row in value:
                passwd = row[0]
            if (passwd == password):
                print("success")
                profile.profile_func(account_no)
                exit()
            else:
                print('Wrong credentials. Try again')
                i+=1

        except Exception as e:
            print(e)
            import traceback
            traceback.print_exc()    

    print("You have made 3 failed attemps. The account is locked")
    cur.execute("UPDATE accounts SET account_lock= WHERE account_no=(?);",(account_no,)) 
    con.commit()
    
def admin_signin_func():
        user_id = input("Enter Administrator user name.")
        password = input("Enter Administrator password.")
        if user_id == 'admin' and password == 'adminpass':
            print("Admin Login successful")
            admin_.admin_func()
            exit()
        else:
            print("Wrong credentials.Try Again")


if __name__ == '__main__':
    while(True):
        try:
            print("\n1. Sign Up\n2. Sign In\n3. Admin Sign In\n4. Quit\n")
            choice = int(input("Enter your choice :"))
            choice_dict = {
                1: signup_func,
                2: signin_func,
                3: admin_signin_func,
                4: exit 
                }
            choice_dict[choice]()
        
        except KeyError:
            print("Try Again")
