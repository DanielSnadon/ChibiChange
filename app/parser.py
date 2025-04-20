from datetime import datetime
from app import db
from app.models import CurrencyPrice

current_prices = {
    "dollar": 75.43,
    "euro": 89.12,
    "yuan": 11.67,
    "bitcoin": 2450000,
    "linganguliguli": 0.0042,
    "TUNG TUNG SAHUR": 3.1415
}

def update_prices():
    try:
        print("Обновление цен...")
        
        # Имитация изменения цен
        for currency in current_prices:
            current_prices[currency] *= 1.01
        
        # Сохранение в базу
        for currency_name, price in current_prices.items():
            price_record = CurrencyPrice(
                currency_name=currency_name,
                price=price,
                timestamp=datetime.utcnow()
            )
            db.session.add(price_record)
        
        db.session.commit()
        print("Цены обновлены")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        db.session.rollback()