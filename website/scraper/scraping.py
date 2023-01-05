from bs4 import BeautifulSoup
import requests

# Website to scrape 
ntuc = 'https://www.fairprice.com.sg/search?query='
cold_storage = 'https://coldstorage.com.sg/search?q='
# Products to scrape
products = ['oreo+original', 'lays+classic', 'camel+roasted+peanuts', 'lindor+cornet+milk']
    

def main():
    for product in products:
        print('\nNTUC:')
        get_price_ntuc(product)
        print('\nCOLD STORAGE:')
        get_price_cold_storage(product)
        
# Get price for products from NTUC
def get_price_ntuc(product):
    # Get html text from website
    html_text = requests.get(ntuc + product).text
    soup = BeautifulSoup(html_text, 'lxml')
    
    # Get product name, price and weight
    products = soup.find_all('div', class_='sc-1plwklf-0 iknXK product-container')
    for product in products:
        name = product.find('span', class_ = 'sc-1bsd7ul-1 eJoyLL').text
        price = product.find('span', class_ = 'sc-1bsd7ul-1 sc-1svix5t-1 gJhHzP biBzHY').text.replace('$', '')
        weight = product.find('span', class_ = 'sc-1bsd7ul-1 eeyOqy').text
        print(f'{name} costs ${price} for {weight}')

# Get price for products from Cold Storage
def get_price_cold_storage(product):
    # Get html text from website
    html_text = requests.get(cold_storage + product).text
    soup = BeautifulSoup(html_text, 'lxml')
    
    # Get product name, price and weight
    products = soup.find_all('div', class_='product_box')
    for product in products:
        cat = product.find('b').text
        name = product.find('div', class_ = 'product_name').text.replace(' ', '')
        
        try:
            price = product.find('div', class_ = 'price_now f-green price_normal').text
        except:
            price = product.find('div', class_ = 'price_now price_normal f-green disc').text
            
        weight = product.find('span', class_ = 'size').text
        print(f'{cat} - {name} costs {price} for {weight}')
                             
                             
                             
if __name__ == '__main__':
    main()