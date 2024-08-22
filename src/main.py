import os
from pathlib import Path
import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from collections import defaultdict
from typing import List, Dict, Union
from settings import load_settings, save_settings

# Определение путей к файлам данных
ROOT_DIR: Path = Path(__file__).parent.parent
DATA_DIR: Path = ROOT_DIR / "data"
BALANCE_FILE: Path = DATA_DIR / "balance.txt"
TRANSACTIONS_FILE: Path = DATA_DIR / "transactions.csv"
FIELDNAMES: List[str] = ['date', 'amount', 'description', 'category']

def read_balance() -> Decimal:
    """
    Считывает текущий баланс из файла.

    :return: Текущий баланс
    """
    if not BALANCE_FILE.exists():
        return Decimal('0')
    with open(BALANCE_FILE, 'r') as f:
        return Decimal(f.read().strip())

def write_balance(balance: Decimal) -> None:
    """
    Записывает текущий баланс в файл.

    :param balance: Баланс для записи
    """
    with open(BALANCE_FILE, 'w') as f:
        f.write(str(balance))

def read_transactions() -> List[Dict[str, str]]:
    """
    Считывает все транзакции из файла.

    :return: Список транзакций
    """
    if not TRANSACTIONS_FILE.exists():
        return []
    with open(TRANSACTIONS_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def add_transaction(amount: Decimal, description: str, category: str) -> None:
    """
    Добавляет новую транзакцию в файл.

    :param amount: Сумма транзакции
    :param description: Описание транзакции
    :param category: Категория транзакции
    """
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

def update_balance(current_balance: Decimal, transaction_amount: Decimal) -> Decimal:
    """
    Обновляет баланс с учетом новой транзакции.

    :param current_balance: Текущий баланс
    :param transaction_amount: Сумма транзакции
    :return: Новый баланс
    """
    return current_balance + transaction_amount

def show_balance(balance: Decimal) -> None:
    """
    Отображает текущий баланс.

    :param balance: Текущий баланс
    """
    print(f"\nТекущий баланс: {balance:.2f}")

def show_transactions(transactions: List[Dict[str, str]]) -> None:
    """
    Отображает историю транзакций.

    :param transactions: Список транзакций
    """
    print("\n--- История транзакций ---")
    for transaction in transactions:
        amount = Decimal(transaction['amount'])
        print(f"{transaction['date']} - {amount:.2f} - {transaction['description']} - {transaction['category']}")

def validate_amount(amount_str: str) -> Decimal:
    """
    Валидирует введенную сумму транзакции.

    :param amount_str: Строка с суммой транзакции
    :return: Валидированная сумма
    :raises ValueError: Если сумма некорректна
    """
    try:
        amount = Decimal(amount_str)
        return amount
    except InvalidOperation:
        raise ValueError("Некорректная сумма. Пожалуйста, введите число.")

def validate_category(category: str) -> str:
    """
    Валидирует введенную категорию.

    :param category: Категория для валидации
    :return: Валидированная категория
    :raises ValueError: Если категория пуста
    """
    if not category.strip():
        raise ValueError("Категория не может быть пустой.")
    return category.strip()

def safe_input(prompt: str, validator: callable) -> Union[str, Decimal]:
    """
    Безопасно запрашивает ввод у пользователя с валидацией.

    :param prompt: Приглашение к вводу
    :param validator: Функция-валидатор
    :return: Валидированный ввод пользователя
    """
    while True:
        try:
            user_input = input(prompt)
            return validator(user_input)
        except ValueError as e:
            print(f"Ошибка: {e}")

def get_transaction_input() -> tuple[Decimal, str, str]:
    """
    Запрашивает у пользователя данные для новой транзакции.

    :return: Кортеж (сумма, описание, категория)
    """
    amount = safe_input(
        "Введите сумму транзакции (положительную для дохода, отрицательную для расхода): ",
        validate_amount
    )
    description = input("Введите описание транзакции: ")
    category = safe_input("Введите категорию транзакции: ", validate_category)
    return amount, description, category

def generate_report(transactions: List[Dict[str, str]]) -> None:
    """
    Генерирует отчет по категориям транзакций.

    :param transactions: Список транзакций
    """
    category_totals = defaultdict(Decimal)
    for transaction in transactions:
        amount = Decimal(transaction['amount'])
        category = transaction['category']
        category_totals[category] += amount

    print("\n--- Отчет по категориям ---")
    for category, total in category_totals.items():
        print(f"{category}: {total:.2f}")

def analyze_expenses(transactions: List[Dict[str, str]], settings: Dict[str, Union[str, Decimal, List[str]]]) -> None:
    """
    Анализирует расходы по категориям и сравнивает с бюджетным лимитом.

    :param transactions: Список транзакций
    :param settings: Словарь с настройками пользователя
    """
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

def edit_settings(settings: Dict[str, Union[str, Decimal, List[str]]]) -> None:
    """
    Позволяет пользователю редактировать настройки приложения.

    :param settings: Текущие настройки пользователя
    """
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

def display_menu() -> None:
    """
    Отображает главное меню приложения.
    """
    print("\n--- Меню ---")
    print("1. Показать баланс")
    print("2. Добавить транзакцию")
    print("3. Показать историю транзакций")
    print("4. Сгенерировать отчет")
    print("5. Анализ расходов")
    print("6. Редактировать настройки")
    print("7. Выйти")

def main() -> None:
    """
    Главная функция приложения, управляющая всем процессом.
    """
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