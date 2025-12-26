from Bank import Bank
import pickle

bank = Bank()

with open("BankStorage/Bank.pkl","wb") as bankst:
    pickle.dump(bank,bankst)