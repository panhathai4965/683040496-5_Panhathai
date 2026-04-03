"""
Panhathai Suporn
683040496-5
P1
"""

class BankAccount: # class 
    saving_run = 0 # class Attribute
    loaning_run = 0
    branch_name = "KKU Complex"
    branch_num = 1724

    #__type_saivng = 1 
    #__type_loan = 2

    def __init__(self, name, acc_type="saving", balance=0): # constructor
        if not name:
           raise ValueError("Name is required") #if there are no name 
       
        self.name = name # instance
        self.type = acc_type
        self.balance = balance

        if self.type == "saving": # saving type
           BankAccount.saving_run += 1
           #type_code = 1
           self.acc_num = f"{BankAccount.branch_num}-1-{BankAccount.saving_run}"
        
        elif self.type == "loan": # loaning type
           BankAccount.loaning_run += 1
           #type_code = 2
           self.acc_num = f"{BankAccount.branch_num}-2-{BankAccount.loaning_run}"

        else:
           raise ValueError("Invalid account type") # check the acc_type
       
    def get_balance(self): # get balance 
       return self.balance
    
    def deposit(self, amount=0): # deposit money
        if self.type == "saving":
            self.balance += amount
        else:
           return None
        return self.balance

    def withdraw(self, amount=0): # withdraw money
        if self.type == "loan":         
            self.balance -= amount
        else:
           return None
        return self.balance
    
    def pay_loan(self, amount=0): # loan paying 
        if self.type == "loan":
           self.balance += amount
        else:
           return None
        return self.balance 
    
    def get_loan(self, amount=0): # get the loan 
        if self.type == "loan":
            if self.balance <= -50000:
                self.balance -= amount
            else:
                return None 
        return self.balance
        
          
    # PRINT FUNCTION 
    def print_customer(self):
       print("----- Customer Record -----")
       print(f"Name: {self.name}")
       print(f"Account number: {self.acc_num}")
       print(f"Account type: {self.type}")
       print(f"Balance: {self.balance}")
       print("----- End Record -----")



    @classmethod # class that change the branch name by input
    def change_branch_name(cls):
       cls.branch_name = input("Branch name: ")
       return cls.branch_name
    
    @staticmethod # calculate 
    def cal_interest(bal, interest_rate, payment):
        year = 0
        print("----- Loan Plan -----")

        while bal > 0:
            year += 1
            loan = bal + (bal * interest_rate / 100)

            bal = bal + (bal * interest_rate / 100)

            bal = bal - payment

            if bal < 0:
               bal = 0

            print(f"Year {year}: loan = {loan:.2f} payment = {payment:.2f} balance = {bal:.2f}")
        print("----- End Plan -----")


# Test Function
C1 = BankAccount("John", "saving", 500)
C1.print_customer()
C1.withdraw(500)
C1.print_customer()
BankAccount.cal_interest(1000, 5, 100)


       