import json
from pathlib import Path
from typing import Dict, Union, List
from decimal import Decimal

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
SETTINGS_FILE = Path(__file__).parent.parent / "data" / "settings.json"

DEFAULT_SETTINGS = {
    "currency": "USD",
    "budget_limit": Decimal('1000'),
    "categories": ["Продукты", "Транспорт", "Развлечения", "Счета", "Прочее"]
}

def load_settings() -> Dict[str, Union[str, int, Decimal, List[str]]]:
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
        # Convert string representation of Decimal back to Decimal
        if 'budget_limit' in settings:
            settings['budget_limit'] = Decimal(settings['budget_limit'])
        return settings
    except json.JSONDecodeError:
        print("Ошибка в файле настроек. Используем настройки по умолчанию.")
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError

def save_settings(settings: Dict[str, Union[str, int, Decimal, List[str]]]) -> None:
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2, default=decimal_default)