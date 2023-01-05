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
    # Reset database
    curs.execute('DELETE FROM products')
    conn.commit()
    
    for idx, product in enumerate(products):
        print('\nNTUC:')
        get_price_ntuc(idx, product)
        print('\nCOLD STORAGE:')
        get_price_cold_storage(idx,product)
        print('\nIsetan:')
        get_price_isetan(idx,product)
        
        
# Get price for products from NTUC
def get_price_ntuc(idx, item):
    # Get html text from website
    html_text = requests.get(ntuc + item).text
    soup = BeautifulSoup(html_text, 'lxml')
    matches = [4, 0, 0, 0, 0, 0]
    
    # Get product name, price and weight
    try:
        products = soup.find_all('div', class_='sc-1plwklf-0 iknXK product-container')
        for index, product in enumerate(products):
            name = product.find('span', class_ = 'sc-1bsd7ul-1 eJoyLL').text
            
            # Check if product name contains the item
            if item.split()[0].lower() in name.lower().replace(' ', ''): 
                price = product.find('span', class_ = 'sc-1bsd7ul-1 sc-1svix5t-1 gJhHzP biBzHY').text.replace('$', '')
                weight = product.find('span', class_ = 'sc-1bsd7ul-1 eeyOqy').text
                
                print(f'{index}: {name} costs {price} for {weight}')

                if matches[idx] == index:
                    print('Match found')
                    insert_database(name, 'NTUC', price, idx)
    except:
        print('No products found')


# Get price for products from Cold Storage
def get_price_cold_storage(idx, item):
    # Get html text from website
    html_text = requests.get(cold_storage + item).text
    soup = BeautifulSoup(html_text, 'lxml')
    matches = [3, 1, 0, 0, 1, 0]
    
    # Get product name, price and weight
    try:
        products = soup.find_all('div', class_='product_box')
        for index, product in enumerate(products):
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
                    
                price = price.replace('$', '')
                weight = product.find('span', class_ = 'size').text
                
                print(f'{index}: {cat} - {name} costs {price} for {weight}')
                
                if matches[idx] == index:
                    print('Match found')
                    insert_database(name, 'Cold Storage', price, idx)
    except:
        print('No products found')
    
  
        
def get_price_isetan(idx, item):
    pass
    # product-price
    # Get html text from website
    html_text = requests.get(isetan + item).text
    soup = BeautifulSoup(html_text, 'lxml')
    # matches = [0, 0, 0, 0, 0, 0]
    
    # Get product name, price and weight
    try:
        products = soup.find_all('li', class_='item product product-item')
        for index, product in enumerate(products):
            name = product.find('a', class_ = 'product-item-link').text.replace(' ', '')
            
            # Check if product name contains the item
            if item.split()[0].lower() in name.lower(): 
                price = product.find('span', class_ = 'price').text.replace('SG$', '')
                
                print(f'{index}: {name} costs {price}')
                
                if index == 0:
                    print('Match found')
                    insert_database(name, 'Isetan', price, idx)
                
                
    except:
        print('No products found')

     
def insert_database(productName, store, price, productID):
    # Insert into database
    print("Writing to database")
    curs.execute('INSERT INTO products(productName, store, price, productID) VALUES (?, ?, ?, ?)', (productName, store, price, productID))
    conn.commit()
                                                    
if __name__ == '__main__':
    main()