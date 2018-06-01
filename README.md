# Bank-management-cli-based
Command line based bank management system with sqlite database 

main.py 
This is the driver program that allows the user to select one of the following things
1.signup
2.signin
3.admin login
4.quit

main.py holds the codes for the validation in signin, signup and admin login 

On successful login, main.py redirects to profile.py which holds the following list of functions
1.Address Change
2.Open New Acccount
3.Money Deposit
4.Money Withdrawal
5.Transfer Money
6.Print Statement
7.Account Closure
8.Avail Loan
9.Customer Logout

On successful admin login, main.py redirects to admin_.py which holds the following list of functions
1.Print closed accounts
2.FD report of customer
3.FD report of customer vis-a-vis another customer
4.FD report w.r.t amount
5.Loan report of customer
6.Loan report of customer vis-a-vis another customer
7.Loan repost w.r.t loan amount
8.Loan-FD Report
9.Report of customers yet to avail a loan
10.Report of customer who are yet to open an FD acccount
11.Report of customer with neither laon nor FD account
12.Admin Logout
