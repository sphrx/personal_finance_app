import unittest
import sys
import os
from decimal import Decimal
from typing import NoReturn

# Добавляем путь к директории src в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import update_balance, validate_amount, validate_category
from settings import DEFAULT_SETTINGS

class TestFinanceApp(unittest.TestCase):
    """
    Тестовый класс для проверки основных функций приложения персонального финансового учета.
    """

    def test_update_balance(self) -> NoReturn:
        """
        Тестирует функцию обновления баланса.
        """
        self.assertEqual(update_balance(Decimal('100'), Decimal('50')), Decimal('150'))
        self.assertEqual(update_balance(Decimal('100'), Decimal('-30')), Decimal('70'))

    def test_validate_amount(self) -> NoReturn:
        """
        Тестирует функцию валидации суммы транзакции.
        """
        self.assertEqual(validate_amount('100'), Decimal('100'))
        self.assertEqual(validate_amount('-50.5'), Decimal('-50.5'))
        with self.assertRaises(ValueError):
            validate_amount('not a number')

    def test_validate_category(self) -> NoReturn:
        """
        Тестирует функцию валидации категории транзакции.
        """
        self.assertEqual(validate_category('Food'), 'Food')
        self.assertEqual(validate_category(' Transport '), 'Transport')
        with self.assertRaises(ValueError):
            validate_category('')

    def test_default_settings(self) -> NoReturn:
        """
        Тестирует значения по умолчанию в настройках приложения.
        """
        self.assertEqual(DEFAULT_SETTINGS['currency'], 'USD')
        self.assertEqual(DEFAULT_SETTINGS['budget_limit'], 1000)
        self.assertIn('Продукты', DEFAULT_SETTINGS['categories'])

if __name__ == '__main__':
    unittest.main()