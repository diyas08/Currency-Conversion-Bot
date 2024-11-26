import requests

url = "https://nbu.uz/en/exchange-rates/json/"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    for item in data:
        country = item.get('title', 'N/A')
        code_curr = item.get('code', 'N/A')
        kurs = item.get('cb_price', 'N/A')
        nbu_buy_price = item.get('nbu_buy_price') or "Nomalum"
        nbu_cell_price = item.get('nbu_cell_price') or "Nomalum"
        date = item.get('date', 'N/A')

        result = []
        result.append("Давлат:", country)
        print(result)
#         print("Код валюты:", code_curr)
#         print("Курс:", kurs)
#         print("Цена покупки (NBU):", nbu_buy_price)
#         print("Цена продажи (NBU):", nbu_cell_price)
#         print("Дата:", date)
#         print("-" * 30)
# else:
    print("Ошибка при выполнении запроса:", response.status_code)
