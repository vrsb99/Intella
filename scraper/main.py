from bs4 import BeautifulSoup
import requests

ntuc = 'https://www.fairprice.com.sg/search?query='
cold_storage = 'https://coldstorage.com.sg/search?q='
products = ['oreo', 'lays+classic']

html_text = requests.get('https://www.fairprice.com.sg/search?query=oreo').text
soup = BeautifulSoup(html_text, 'lxml')
products = soup.find_all('div', class_='sc-1plwklf-0 iknXK product-container')
for product in products:
    name = product.find('span', class_ = 'sc-1bsd7ul-1 eJoyLL').text
    price = product.find('span', class_ = 'sc-1bsd7ul-1 sc-1svix5t-1 gJhHzP biBzHY').text.replace('$', '')
    print(f'{name} costs ${price}')