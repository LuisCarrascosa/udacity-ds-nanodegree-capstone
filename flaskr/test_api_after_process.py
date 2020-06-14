import api_factory
import json
from datetime import datetime

with open('flaskr/backend/test_data.json', newline='') as file_json:
    test_data = json.load(file_json)

output = api_factory.get_api('alphavantage_daily').parser(
    'BRDT3.SA', test_data, limits=[
        datetime.strptime('2020-06-09', '%Y-%m-%d'), 
        datetime.strptime('2020-06-12', '%Y-%m-%d')])

for data in output:
    print(f'{data.ticker_name}')
    print(f'{data.fecha}')
    print(f'{data.maximo}')
    print(f'{data.cierre}')
