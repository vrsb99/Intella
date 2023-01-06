from bs4 import BeautifulSoup
import requests
import sqlite3

# Website to scrape
ntuc = 'https://www.fairprice.com.sg/search?query='
cold_storage = 'https://coldstorage.com.sg/search?q='
isetan = 'https://www.isetan.com.sg/catalogsearch/result/?q='
stores = ['NTUC', 'COLD STORAGE', 'ISETAN']
# Products to scrape
products = ['oreo original', "lay's classic", 'camel roasted peanuts', 'lindor cornet milk', 'ruffles original', 'anchor strong beer']
# Connect to database
conn = sqlite3.connect('../instance/products.db')
curs = conn.cursor()

def main():
    # Reset database
    curs.execute('DROP TABLE IF EXISTS products')
    curs.execute('DROP TABLE IF EXISTS stores')
    curs.execute('DROP TABLE IF EXISTS prices')
    conn.commit()
    curs.execute('CREATE TABLE products (id INTEGER NOT NULL PRIMARY KEY, product_name TEXT NOT NULL)')
    curs.execute('CREATE TABLE stores (id INTEGER NOT NULL PRIMARY KEY, store_name TEXT NOT NULL)')
    curs.execute('CREATE TABLE prices (id INTEGER NOT NULL PRIMARY KEY, product_id INTEGER NOT NULL, store_id INTEGER NOT NULL, price NUMERIC NOT NULL, FOREIGN KEY(product_id) REFERENCES products(id), FOREIGN KEY(store_id) REFERENCES stores(id))')
    conn.commit()
    
    for store in stores:
        # Insert stores into database
        curs.execute('INSERT INTO stores (store_name) VALUES (?)', (store,))
        conn.commit()
    
    for idx, product in enumerate(products):
        # Insert product into database
        curs.execute('INSERT INTO products (product_name) VALUES (?)', (product.capitalize(),))
        conn.commit()
        
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
    matches = [0, 2, 0, 0, 0, 0]
    
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
                    insert_database(idx, 0, price)
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
                    insert_database(idx, 1, price)
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
                    insert_database(idx, 2, price)
                
                
    except:
        print('No products found')

     
def insert_database(product_id, store, price):
    # Insert into database
    print("Writing to database")
    curs.execute('INSERT INTO prices(product_id, store_id, price) VALUES (?, ?, ?)', (product_id, store, price))
    conn.commit()
                                                    
if __name__ == '__main__':
    main()