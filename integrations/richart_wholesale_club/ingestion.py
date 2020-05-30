import os, re, io
import numpy as np
import pandas as pd

# from database_setup import engine
from sqlalchemy.orm import sessionmaker
from models import BranchProduct, Product
from database_setup import engine

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
PRODUCTS_PATH = os.path.join(ASSETS_DIR, "PRODUCTS.csv")
PRICES_STOCK_PATH = os.path.join(ASSETS_DIR, "PRICES-STOCK.csv")

def process_csv_files():
    products_df = pd.read_csv(filepath_or_buffer=PRODUCTS_PATH, sep="|",)
    prices_stock_df = pd.read_csv(filepath_or_buffer=PRICES_STOCK_PATH, sep="|",)
    allowed_branches = ['MM', 'RHSM']
    # removing html tags
    products_df['DESCRIPTION'] = products_df['DESCRIPTION'].str.replace('<[^<]+?>', '')

    # merging catetory and sub category. Category should in be lowercase
    products_df['CATEGORY'] = products_df['CATEGORY'].str.lower() + '|' + products_df['SUB_CATEGORY']
    del products_df['SUB_CATEGORY']
    del products_df['SUB_SUB_CATEGORY']

    def get_package(row):
        temp_list = row['DESCRIPTION'].split()
        if len(temp_list) == 1:
            return np.nan
        word1 = temp_list[-1]
        word2 = temp_list[-2]
        try: 
            int(word1)
            return np.nan
        except:
            if bool(re.search(r'\d', word1)):
                return word1
            else:
                try:
                    int(word2)
                    return word2 + ' ' + word1
                except:
                    return np.nan

    def extract_description(row):
        temp_list = row['DESCRIPTION'].split()
        if len(temp_list) == 1:
            return row['DESCRIPTION']
        word1 = temp_list[-1]
        word2 = temp_list[-2]
        try: 
            int(word1)
            return row['DESCRIPTION']
        except:
            if bool(re.search(r'\d', word1)):
                return row['DESCRIPTION'].replace(' ' + word1, '')
            else:
                try:
                    int(word2)
                    return row['DESCRIPTION'].replace(' ' + word2 + ' ' + word1, '')
                except:
                    return row['DESCRIPTION']   

    products_df['package'] = products_df.apply(get_package, axis=1)
    products_df['DESCRIPTION'] = products_df.apply(extract_description, axis=1)
    products_df['store'] = "Richart's"
    products_df = products_df[products_df['NAME'].notna()]

    prices_stock_df = prices_stock_df[(prices_stock_df['BRANCH'].isin(allowed_branches)) & (prices_stock_df['STOCK'] > 0)]

    # write data to database
    products_df.rename(columns={
        'SKU': 'sku',
        'BARCODES': 'barcodes',
        'BRAND': 'brand',
        'NAME': 'name',
        'DESCRIPTION': 'description',
        'IMAGE_URL': 'image_url',
        'CATEGORY': 'category'
    }, inplace=True)

    prices_stock_df.rename(columns={
        'SKU': 'sku',
        'BRANCH': 'branch',
        'PRICE': 'price',
        'STOCK': 'stock',
    }, inplace=True)
    
    #Create the session
    Session = sessionmaker(bind=engine)
    s = Session()

    id_list =[]
    # product
    try:
        for i,row in products_df.iterrows():
            # check if product exists
            product = (
                s.query(Product)
                .filter_by(store=row['store'], sku=row["sku"])
                .first()
            )

            if product is None:
                record = Product(**{
                    'store' : row['store'],
                    'sku' : row['sku'],
                    'barcodes' : row['barcodes'],
                    'name' : row['name'],
                    'description' : row['description'],
                    'package' : row['package'],
                    'image_url' : row['image_url'],
                    'category' : row['category']
                })
                s.add(record)
            else:
                id_list.append(row['sku'])
        print('[START] Product bulk save')
        s.commit() #Attempt to commit all the records
        print('[DONE] Product bulk done')
    except Exception as e:
        print('[ERROR] Product bulk error', e)
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection

    # branch product
    try:
        for i,row in prices_stock_df.iterrows():
            # check if product exists
            branch_product = (
                s.query(BranchProduct)
                .filter_by(product=row['sku'], branch=row["branch"])
                .first()
            )

            if branch_product is None and row['sku'] in id_list:
                record = BranchProduct(**{
                    'product_id' : row['sku'],
                    'branch' : row['branch'],
                    'stock' : row['stock'],
                    'price' : row['price'],
                })
                s.add(record)
        print('[START] BranchProduct bulk save')
        s.commit() #Attempt to commit all the records
        print('[DONE] BranchProduct bulk done')
    except Exception as e:
        print('[ERROR] BranchProduct bulk error', e)
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection



if __name__ == "__main__":
    process_csv_files()
