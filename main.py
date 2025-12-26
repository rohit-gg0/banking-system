from __future__ import annotations
from Bank import Bank,AccountError,WrongPassword
from Money import Money
from Currency import Currency
import pickle

currencies = {"INR":Currency.INR, "USD":Currency.USD, "EUR":Currency.EUR}

admin_password = "1234"

with open("BankStorage/Bank.pkl","rb") as bankst:
    bank: Bank = pickle.load(bankst)

ch = input("User or Admin: ").strip().lower()

if ch=="admin":
    c=0
    while True:
        try:
            password = input("enter the Password: ")
            if password!=admin_password:
                c=c+1
                raise Exception("Wrong Password")
            break
        except Exception as ex:
            print("Wrong Password")
            if c>=3:
                print("3 wrong attempts, program terminating")
                raise ex
    
    print("Welcome Admin")

    while True:
        pass

elif ch=="user":
    print("Welcome User")
    print("List of Options")
    print("\t1 - Check Balance")
    print("\t2 - Withdraw funds")
    print("\t3 - Deposit funds")
    print("\t4 - Transfer funds")
    print("\t5 - Open new Savings Account")
    print("\t6 - Open new Current Account")
    print("\t7 - View Transaction History")
    print("\t8 - save and quit")
    print()

    while True:
        c=int(input(">>>"))

        if c==1:
            id = int(input("enter Account id: "))
            try:
                amt = bank.check_balance(id)
            except AccountError:
                print("invalid id or id doesnot exist")
                continue
            except WrongPassword:
                print("3 incorrect attempts")
                continue
            print(str(amt))

        elif c==2:
            id = int(input("enter Account id: "))
            currency = currencies[input("Enter Currency (INR/USD/EUR): ").upper()]
            amt = int(input("Enter the Amount in MINORS: "))
            amt = Money(amt,currency)

            try:
                check = bank.withdraw(id,amt)
            except AccountError:
                print("invalid id or id doesnot exist")
                continue
            except WrongPassword:
                print("3 incorrect attempts")
                continue

            if check:
                print(f"{str(amt)} was successfully withdrawn from account {id}")
            else:
                print("Transaction Failed")

        elif c==3:
            id = int(input("enter Account id: "))
            currency = currencies[input("Enter Currency (INR/USD/EUR): ").upper()]
            amt = int(input("Enter the Amount in MINORS: "))
            amt = Money(amt,currency)

            try:
                check = bank.deposit(id,amt)
            except AccountError:
                print("invalid id or id doesnot exist")
                continue
            except WrongPassword:
                print("3 incorrect attempts")
                continue
            
            if check:
                print(f"{str(amt)} was successfully deposited in account {id}")
            else:
                print(f"Transaction Failed")

        elif c==4:
            id1 = int(input("enter from Account id: "))
            id2 = int(input("enter to Account id: "))
            currency = currencies[input("Enter Currency (INR/USD/EUR): ").upper()]
            amt = int(input("Enter the Amount in MINORS: "))
            amt = Money(amt,currency)

            try:
                check = bank.transfer(id1,id2,amt)
            except AccountError:
                print("invalid id or id doesnot exist")
                continue
            except WrongPassword:
                print("3 incorrect attempts")
                continue
            
            if check:
                print(f"{str(amt)} was successfully transfered form account {id1} to account {id2}")
            else:
                print(f"Transaction Failed")

        elif c==5:
            currency = currencies[input("Enter Currency (INR/USD/EUR): ").upper()]
            while True:
                amt = int(input("Enter the Initial Balance in MINORS: "))
                if amt < bank.get_min_balance_savings_minor:
                    print(f"initial Balance cannot be less than min balance: {bank.get_min_balance_savings_minor}(MINOR)")
                else:
                    break
            
            amt = Money(amt,currency)
            
            id = bank.open_savings_account(amt)
            print(f"Account Id: {id}")
            
        elif c==6:
            currency = currencies[input("Enter Currency (INR/USD/EUR): ").upper()]
            while True:
                amt = int(input("Enter the Initial Balance in MINORS: "))
                if amt <= 0:
                    print(f"initial Balance cannot be less than or equal 00")
                else:
                    break
            
            amt = Money(amt,currency)
            
            id = bank.open_current_account(amt)
            print(f"Account Id: {id}")

        elif c==7:
            id = int(input("enter Account id: "))
            try:
                thl = bank.get_acc_transaction_history(id)
            except AccountError:
                print("invalid id or id doesnot exist")
                continue
            except WrongPassword:
                print("3 incorrect attempts")
                continue

            if not thl:
                print("Not Transaction History")
                continue
                
            for t in thl:
                print(t)
            print("End of Transaction History")

        elif c==8:
            print("Thank You")
            break

        else:
            print("INVALID CHOICE")

with open("BankStorage/Bank.pkl","wb") as bnk:
    pickle.dump(bank,bnk)
    print("Changes saved sucessfully")
print("program terminated")