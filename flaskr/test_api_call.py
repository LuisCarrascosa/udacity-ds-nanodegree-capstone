import api_controller as api_controller

output = api_controller.call_api(
    'BRDT3.SA',
    '2020-06-09',
    '2020-06-12')

for data in output:
    print(f'{data.ticker_name}')
    print(f'{data.fecha}')
    print(f'{data.maximo}')
    print(f'{data.cierre}')
