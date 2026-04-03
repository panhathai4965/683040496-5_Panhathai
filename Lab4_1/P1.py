"""
Panhathai Suporn
683040496-5
P1
"""
class BankAccount:
    branch_name = "KKU Complex"
    branch_number = 1724
    last_loan_number = 0
    last_saving_number = 0

    # Private class attributes
    # account types
    __type_saving = 1
    __type_loan = 2

    # Constructor
    def __init__(self,name,type = "saving",balance = 0):
        self.name = name
        self.type = type.lower()
        self.balance = balance
        if self.type == "saving":
            BankAccount.last_saving_number += 1
            self.account_number = f"{BankAccount.branch_number}-1-{BankAccount.last_saving_number}"
        elif self.type == "loan":
            BankAccount.last_loan_number += 1
            self.account_number = f"{BankAccount.branch_number}-2-{BankAccount.last_loan_number}"

    # Instance methods
    def change_branch_name(cls):
        cls.branch_name = input("New branch name: ")
        
    def print_customer(self):
    
        print("----- Customer Record -----")
        print(f"Name: {self.name}")
        print(f"Acccpunt number: {self.account_number}")
        print(f"Account type: {self.type}")
        print(f"Balance: {self.balance}")
        print(f"----- End Record ----")

    def withdraw(self, amount=0):
        if self.type  == "saving":
            self.balance -= amount
            return self.balance
        return False

    def deposit(self, amount=0):
        if self.type  == "saving":
            self.balance += amount
            return self.balance
        return False
    
    def pay_loan(self, amount=0):
        if self.type  == "loan":
            self.balance += amount
            return self.balance
        return False
    
    def get_loan(self, amount=0):
        if self.type  == "loan":
            if self.balance > -50000:
                self.balance += amount
                return self.balance
        return False
    
    def calc_interest(bal, int_rate, payment):
        print("----- Loan Plan -----")
        year = 0
        while True:
            bal += bal*(int_rate/100)

            chack = bal - payment
            if chack <= 0:
                payment = bal

            year += 1

            print(f"Year {year}: loan = {bal:.2f}  payment {payment:.2f}  ", end="")
            bal -= payment
            print(f"bal = {bal:.2f}")
            if bal <= 0:
                break
        print("----- End Plan -----")

    def main():
        john = BankAccount("John", "saving", balance = 500)
        john.print_customer()
        print("John asks to deposit 3,000 more and see the current balance.")
        john.deposit(3000)
        john.print_customer()

        tim = BankAccount("Tim", "loan", balance = -1000000)
        tim.print_customer()
        print("Tim wants to see the loan balance and he wants to pay half of the balance right away.")
        money = tim.balance
        tim.pay_loan((money//2)*(-1))
        tim.print_customer()

        Sarah1 = BankAccount("Sarah", "saving")
        print("Sarah wants to deposit 50,000,000")
        Sarah1.deposit(50000000)
        print("Sarah wants to open another loan account for -100,000,000")
        Sarah2 = BankAccount("Sarah", "loan", balance = -100000000)

        print("Finally, show the account information of all accounts.")
        john.print_customer()
        tim.print_customer()
        Sarah1.print_customer()
        Sarah2.print_customer()

        BankAccount.calc_interest(1000, 5, 100)
if __name__ == "__main__":
    BankAccount.main()