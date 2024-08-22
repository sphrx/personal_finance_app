import unittest
from decimal import Decimal
from pathlib import Path
import json
import csv
import os
import sys

# Добавляем путь к директории src в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import (
    read_balance, write_balance, read_transactions, add_transaction,
    update_balance, validate_amount, validate_category, generate_report,
    analyze_expenses, edit_settings
)
from settings import load_settings, save_settings, DEFAULT_SETTINGS


class TestFinanceApp(unittest.TestCase):
    def setUp(self):
        # Создаем временную директорию для тестовых данных
        self.test_dir = Path('test_data')
        self.test_dir.mkdir(exist_ok=True)

        # Устанавливаем пути к тестовым файлам
        self.balance_file = self.test_dir / 'balance.txt'
        self.transactions_file = self.test_dir / 'transactions.csv'
        self.settings_file = self.test_dir / 'settings.json'

        # Перенаправляем пути в main.py на тестовые файлы
        import main
        main.BALANCE_FILE = self.balance_file
        main.TRANSACTIONS_FILE = self.transactions_file
        import settings
        settings.SETTINGS_FILE = self.settings_file

    def tearDown(self):
        # Удаляем временные файлы после тестов
        for file in [self.balance_file, self.transactions_file, self.settings_file]:
            if file.exists():
                file.unlink()
        self.test_dir.rmdir()

    def test_balance_operations(self):
        # Тест операций с балансом
        write_balance(Decimal('100.50'))
        self.assertEqual(read_balance(), Decimal('100.50'))

        new_balance = update_balance(read_balance(), Decimal('50.25'))
        write_balance(new_balance)
        self.assertEqual(read_balance(), Decimal('150.75'))

    def test_transactions(self):
        # Тест операций с транзакциями
        add_transaction(Decimal('100'), 'Зарплата', 'Доход')
        add_transaction(Decimal('-50'), 'Продукты', 'Расходы')

        transactions = read_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(Decimal(transactions[0]['amount']), Decimal('100'))
        self.assertEqual(Decimal(transactions[1]['amount']), Decimal('-50'))

    def test_validation(self):
        # Тест функций валидации
        self.assertEqual(validate_amount('100.50'), Decimal('100.50'))
        with self.assertRaises(ValueError):
            validate_amount('not a number')

        self.assertEqual(validate_category(' Food '), 'Food')
        with self.assertRaises(ValueError):
            validate_category('')

    def test_report_and_analysis(self):
        # Тест генерации отчета и анализа расходов
        add_transaction(Decimal('1000'), 'Зарплата', 'Доход')
        add_transaction(Decimal('-300'), 'Продукты', 'Еда')
        add_transaction(Decimal('-200'), 'Бензин', 'Транспорт')

        # Тест генерации отчета
        report_output = []

        def mock_print(*args):
            report_output.append(' '.join(map(str, args)))

        import builtins
        original_print = builtins.print
        builtins.print = mock_print

        generate_report(read_transactions())

        builtins.print = original_print

        self.assertIn('Еда: -300.00', report_output)
        self.assertIn('Транспорт: -200.00', report_output)
        self.assertIn('Доход: 1000.00', report_output)

        # Тест анализа расходов
        settings = DEFAULT_SETTINGS.copy()
        settings['budget_limit'] = Decimal('600')

        analysis_output = []
        builtins.print = lambda *args: analysis_output.append(' '.join(map(str, args)))

        analyze_expenses(read_transactions(), settings)

        builtins.print = original_print

        self.assertIn('Еда: 300.00 USD (60.0%)', analysis_output)
        self.assertIn('Транспорт: 200.00 USD (40.0%)', analysis_output)
        self.assertTrue(any('Общие расходы: 500.00 USD' in line for line in analysis_output))
        self.assertTrue(any('Вы сэкономили 100.00 USD' in line for line in analysis_output))

    def test_settings(self):
        # Тест работы с настройками
        settings = load_settings()
        self.assertEqual(settings, DEFAULT_SETTINGS)

        new_settings = settings.copy()
        new_settings['currency'] = 'EUR'
        new_settings['budget_limit'] = Decimal('2000')
        new_settings['categories'].append('Развлечения')

        save_settings(new_settings)

        loaded_settings = load_settings()
        self.assertEqual(loaded_settings['currency'], 'EUR')
        self.assertEqual(loaded_settings['budget_limit'], Decimal('2000'))
        self.assertIn('Развлечения', loaded_settings['categories'])


if __name__ == '__main__':
    unittest.main()