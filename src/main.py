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

def get_transaction_input():
    while True:
        try:
            amount = int(input("Введите сумму транзакции (положительную для дохода, отрицательную для расхода): "))
            description = input("Введите описание транзакции: ")
            return amount, description
        except ValueError:
            print("Ошибка: Введите целое число для суммы.")

def update_balance(current_balance, transaction_amount):
    return current_balance + transaction_amount

def display_menu():
    print("\n--- Меню ---")
    print("1. Показать баланс")
    print("2. Добавить транзакцию")
    print("3. Показать историю транзакций")
    print("4. Выйти")

def show_balance(balance):
    print(f"\nТекущий баланс: {balance}")

def show_transactions(transactions):
    print("\n--- История транзакций ---")
    for transaction in transactions:
        amount, description = transaction.strip().split(',', 1)
        print(f"{amount} - {description}")

def main():
    print("Добро пожаловать в приложение персонального финансового учета!")

    while True:
        balance = read_balance()
        transactions = read_transactions()

        display_menu()
        choice = input("Выберите действие (1-4): ")

        if choice == '1':
            show_balance(balance)
        elif choice == '2':
            amount, description = get_transaction_input()
            add_transaction(amount, description)
            new_balance = update_balance(balance, amount)
            write_balance(new_balance)
            print(f"Транзакция добавлена. Новый баланс: {new_balance}")
        elif choice == '3':
            show_transactions(transactions)
        elif choice == '4':
            print("Спасибо за использование приложения. До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите число от 1 до 4.")

if __name__ == "__main__":
    main()

