from bs4 import BeautifulSoup
import requests
import sqlite3

# Website to scrape
ntuc = 'https://www.fairprice.com.sg/search?query='
cold_storage = 'https://coldstorage.com.sg/search?q='
isetan = 'https://www.isetan.com.sg/catalogsearch/result/?q='
# Products to scrape
products = ['oreo original', "lay's classic", 'camel roasted peanuts', 'lindor cornet milk', 'ruffles original', 'anchor strong beer']
# Connect to database
conn = sqlite3.connect('../../instance/products.db')
curs = conn.cursor()

def main():
    for product in products:
        print('\nNTUC:')
        get_price_ntuc(product)
        print('\nCOLD STORAGE:')
        get_price_cold_storage(product)
        print('\nIsetan:', end='')
        get_price_isetan(product)
        
# Get price for products from NTUC
def get_price_ntuc(item):
    # Get html text from website
    html_text = requests.get(ntuc + item).text
    soup = BeautifulSoup(html_text, 'lxml')
    
    # Get product name, price and weight
    try:
        products = soup.find_all('div', class_='sc-1plwklf-0 iknXK product-container')
        for product in products:
            name = product.find('span', class_ = 'sc-1bsd7ul-1 eJoyLL').text
            
            # Check if product name contains the item
            if item.split()[0].lower() in name.lower().replace(' ', ''): 
                price = product.find('span', class_ = 'sc-1bsd7ul-1 sc-1svix5t-1 gJhHzP biBzHY').text
                weight = product.find('span', class_ = 'sc-1bsd7ul-1 eeyOqy').text
                print(f'{name} costs {price} for {weight}')
    except:
        print('No products found')


# Get price for products from Cold Storage
def get_price_cold_storage(item):
    # Get html text from website
    html_text = requests.get(cold_storage + item).text
    soup = BeautifulSoup(html_text, 'lxml')
    
    # Get product name, price and weight
    try:
        products = soup.find_all('div', class_='product_box')
        for product in products:
            cat = product.find('b').text
            name = product.find('div', class_ = 'product_name').text.replace(' ', '')
            
            # Check if product name contains the item
            if item.split()[0].lower() in name.lower() or item.split()[0].lower() in cat.lower(): 
                # Will try for original price first, if not found, will try for discounted price
                try:
                    price = product.find('div', class_ = 'price_now f-green price_normal').text
                except:
                    
                    try:
                        price = product.find('div', class_ = 'price_now price_normal f-green disc').text
                    except:
                        price = product.find('div', class_ = 'price_now price-buy price_normal').text
                    
                weight = product.find('span', class_ = 'size').text
                print(f'{cat} - {name} costs {price} for {weight}')
    except:
        print('No products found')
    
  
        
def get_price_isetan(item):
    pass
    # product-price
    # Get html text from website
    html_text = requests.get(isetan + item).text
    soup = BeautifulSoup(html_text, 'lxml')
    
    # Get product name, price and weight
    try:
        products = soup.find_all('li', class_='item product product-item')
        for product in products:
            name = product.find('a', class_ = 'product-item-link').text.replace(' ', '')
            
            # Check if product name contains the item
            if item.split()[0].lower() in name.lower(): 
                price = product.find('span', class_ = 'price').text.replace('SG$', '$')
                print(f'{name} costs {price}', end=' ')
    except:
        print('No products found')
    print('')
        
                                                    
if __name__ == '__main__':
    main()