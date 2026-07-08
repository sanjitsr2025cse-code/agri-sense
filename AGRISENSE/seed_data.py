import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrisense.settings')
django.setup()

from marketplace.models import PriceHistory

# Data
states = {
    'Punjab': {'districts': ['Amritsar', 'Ludhiana', 'Jalandhar'], 'markets': ['Amritsar Mandi', 'Ludhiana Mandi', 'Jalandhar Mandi']},
    'Tamil Nadu': {'districts': ['Chennai', 'Coimbatore', 'Madurai'], 'markets': ['Chennai Market', 'Coimbatore Market', 'Madurai Market']},
    'Maharashtra': {'districts': ['Mumbai', 'Pune', 'Nagpur'], 'markets': ['Mumbai Mandi', 'Pune Mandi', 'Nagpur Mandi']},
    'West Bengal': {'districts': ['Kolkata', 'Howrah', 'Bardhaman'], 'markets': ['Kolkata Market', 'Howrah Market', 'Bardhaman Market']},
}

crops = {
    'Rice': {'varieties': ['Basmati', 'IR64', 'Sona Masoori'], 'price_range': (2000, 4000)},
    'Wheat': {'varieties': ['HD2967', 'PBW343', 'Lok1'], 'price_range': (1800, 2500)},
    'Onion': {'varieties': ['Red', 'White', 'Hybrid'], 'price_range': (500, 2000)},
    'Tomato': {'varieties': ['Hybrid', 'Local', 'Cherry'], 'price_range': (800, 3000)},
    'Cotton': {'varieties': ['Bt', 'Non-Bt', 'American'], 'price_range': (4000, 6000)},
}

def generate_data():
    start_date = datetime.now().date() - timedelta(days=30)
    end_date = datetime.now().date()
    data = []
    for state, info in states.items():
        districts = info['districts']
        markets = info['markets']
        for crop, crop_info in crops.items():
            varieties = crop_info['varieties']
            min_price, max_price = crop_info['price_range']
            for i in range(50):  # 50 entries per crop per state
                date = start_date + timedelta(days=random.randint(0, 30))
                district = random.choice(districts)
                market = random.choice(markets)
                variety = random.choice(varieties)
                price = round(random.uniform(min_price, max_price), 2)
                data.append(PriceHistory(
                    state=state,
                    district=district,
                    market=market,
                    commodity=crop,
                    variety=variety,
                    price=price,
                    date=date
                ))
    return data

if __name__ == '__main__':
    data = generate_data()
    PriceHistory.objects.bulk_create(data)
    print(f"Inserted {len(data)} records into PriceHistory.")