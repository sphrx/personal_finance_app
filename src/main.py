import os
from pathlib import Path
import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from collections import defaultdict
from settings import load_settings, save_settings

# Определение путей к файлам данных
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
BALANCE_FILE = DATA_DIR / "balance.txt"
TRANSACTIONS_FILE = DATA_DIR / "transactions.csv"
FIELDNAMES = ['date', 'amount', 'description', 'category']

def read_balance():
    if not BALANCE_FILE.exists():
        return Decimal('0')
    with open(BALANCE_FILE, 'r') as f:
        return Decimal(f.read().strip())

def write_balance(balance):
    with open(BALANCE_FILE, 'w') as f:
        f.write(str(balance))

def read_transactions():
    if not TRANSACTIONS_FILE.exists():
        return []
    with open(TRANSACTIONS_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def add_transaction(amount, description, category):
    file_exists = TRANSACTIONS_FILE.exists()

    with open(TRANSACTIONS_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'amount': str(amount),
            'description': description,
            'category': category
        })

def get_transaction_input():
    while True:
        try:
            amount = Decimal(input("Введите сумму транзакции (положительную для дохода, отрицательную для расхода): "))
            description = input("Введите описание транзакции: ")
            category = input("Введите категорию транзакции: ")
            return amount, description, category
        except InvalidOperation:
            print("Ошибка: Введите корректное число для суммы.")

def update_balance(current_balance, transaction_amount):
    return current_balance + transaction_amount

def display_menu():
    print("\n--- Меню ---")
    print("1. Показать баланс")
    print("2. Добавить транзакцию")
    print("3. Показать историю транзакций")
    print("4. Выйти")

def show_balance(balance):
    print(f"\nТекущий баланс: {balance:.2f}")

def show_transactions(transactions):
    print("\n--- История транзакций ---")
    for transaction in transactions:
        amount = Decimal(transaction['amount'])
        print(f"{transaction['date']} - {amount:.2f} - {transaction['description']} - {transaction['category']}")

def validate_amount(amount_str):
    try:
        amount = Decimal(amount_str)
        return amount
    except InvalidOperation:
        raise ValueError("Некорректная сумма. Пожалуйста, введите число.")

def validate_category(category):
    if not category.strip():
        raise ValueError("Категория не может быть пустой.")
    return category.strip()

def safe_input(prompt, validator):
    while True:
        try:
            user_input = input(prompt)
            return validator(user_input)
        except ValueError as e:
            print(f"Ошибка: {e}")

def get_transaction_input():
    amount = safe_input(
        "Введите сумму транзакции (положительную для дохода, отрицательную для расхода): ",
        validate_amount
    )
    description = input("Введите описание транзакции: ")
    category = safe_input("Введите категорию транзакции: ", validate_category)
    return amount, description, category

def generate_report(transactions):
    category_totals = defaultdict(Decimal)
    for transaction in transactions:
        amount = Decimal(transaction['amount'])
        category = transaction['category']
        category_totals[category] += amount

    print("\n--- Отчет по категориям ---")
    for category, total in category_totals.items():
        print(f"{category}: {total:.2f}")


def analyze_expenses(transactions, settings):
    category_totals = defaultdict(Decimal)
    for transaction in transactions:
        amount = Decimal(transaction['amount'])
        if amount < 0:  # только расходы
            category = transaction['category']
            category_totals[category] -= amount  # меняем знак, чтобы расходы были положительными

    print("\n--- Анализ расходов ---")
    total_expenses = sum(category_totals.values())
    budget_limit = Decimal(settings['budget_limit'])

    for category, total in category_totals.items():
        percentage = (total / total_expenses) * 100 if total_expenses > 0 else 0
        print(f"{category}: {total:.2f} {settings['currency']} ({percentage:.1f}%)")

    print(f"\nОбщие расходы: {total_expenses:.2f} {settings['currency']}")
    print(f"Бюджетный лимит: {budget_limit:.2f} {settings['currency']}")

    if total_expenses > budget_limit:
        overspend = total_expenses - budget_limit
        print(f"Превышение бюджета на {overspend:.2f} {settings['currency']}!")
    else:
        underspend = budget_limit - total_expenses
        print(f"Вы сэкономили {underspend:.2f} {settings['currency']}.")


def edit_settings(settings):
    print("\n--- Редактирование настроек ---")
    settings['currency'] = input(f"Введите валюту (текущая: {settings['currency']}): ") or settings['currency']

    while True:
        try:
            new_limit = input(f"Введите новый бюджетный лимит (текущий: {settings['budget_limit']}): ")
            if new_limit:
                settings['budget_limit'] = Decimal(new_limit)
            break
        except InvalidOperation:
            print("Пожалуйста, введите корректное число.")

    print("Текущие категории:")
    for i, category in enumerate(settings['categories'], 1):
        print(f"{i}. {category}")

    new_category = input("Введите новую категорию (или нажмите Enter, чтобы пропустить): ")
    if new_category:
        settings['categories'].append(new_category)

    save_settings(settings)
    print("Настройки сохранены.")


def display_menu():
    print("\n--- Меню ---")
    print("1. Показать баланс")
    print("2. Добавить транзакцию")
    print("3. Показать историю транзакций")
    print("4. Сгенерировать отчет")
    print("5. Анализ расходов")
    print("6. Редактировать настройки")
    print("7. Выйти")


def main():
    print("Добро пожаловать в приложение персонального финансового учета!")
    settings = load_settings()

    while True:
        balance = read_balance()
        transactions = read_transactions()

        display_menu()
        choice = safe_input("Выберите действие (1-7): ",
                            lambda x: x if x in ['1', '2', '3', '4', '5', '6', '7'] else ValueError("Неверный выбор"))

        if choice == '1':
            show_balance(balance)
        elif choice == '2':
            amount, description, category = get_transaction_input()
            add_transaction(amount, description, category)
            new_balance = update_balance(balance, amount)
            write_balance(new_balance)
            print(f"Транзакция добавлена. Новый баланс: {new_balance:.2f} {settings['currency']}")
        elif choice == '3':
            show_transactions(transactions)
        elif choice == '4':
            generate_report(transactions)
        elif choice == '5':
            analyze_expenses(transactions, settings)
        elif choice == '6':
            edit_settings(settings)
        elif choice == '7':
            print("Спасибо за использование приложения. До свидания!")
            break


if __name__ == "__main__":
    main()


