import os
from pathlib import Path

# Определение путей к файлам данных
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
BALANCE_FILE = DATA_DIR / "balance.txt"
TRANSACTIONS_FILE = DATA_DIR / "transactions.txt"

def read_balance():
    if not BALANCE_FILE.exists():
        return 0
    with open(BALANCE_FILE, 'r') as f:
        return int(f.read().strip())

def write_balance(balance):
    with open(BALANCE_FILE, 'w') as f:
        f.write(str(balance))

def read_transactions():
    if not TRANSACTIONS_FILE.exists():
        return []
    with open(TRANSACTIONS_FILE, 'r') as f:
        return f.readlines()

def add_transaction(amount, description):
    with open(TRANSACTIONS_FILE, 'a') as f:
        f.write(f"{amount},{description}\n")

def main():
    print("Добро пожаловать в приложение персонального финансового учета!")
    balance = read_balance()
    transactions = read_transactions()
    print(f"Текущий баланс: {balance}")
    print(f"Количество транзакций: {len(transactions)}")

if __name__ == "__main__":
    main()

