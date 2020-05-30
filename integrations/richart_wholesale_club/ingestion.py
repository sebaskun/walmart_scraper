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

    allowed_branches = ['MM', 'RHSM']
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

    del products_df['BUY_UNIT']
    del products_df['DESCRIPTION_STATUS']
    del products_df['ORGANIC_ITEM']
    del products_df['KIRLAND_ITEM']
    del products_df['FINELINE_NUMBER']

    # output = io.StringIO()
    # products_df.to_csv(output, sep=',', header=False, index=False)

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:
        for i,row in products_df.iterrows():
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

        s.commit() #Attempt to commit all the records
    except Exception as e:
        print('1', e)
        s.rollback() #Rollback the changes on error
    finally:
        print('2')
        s.close() #Close the connection


if __name__ == "__main__":
    process_csv_files()
