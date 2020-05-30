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

    prices_stock_df = prices_stock_df[prices_stock_df['SKU'].isin(list(products_df.SKU.unique()))]
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
    del products_df['BUY_UNIT']
    del products_df['DESCRIPTION_STATUS']
    del products_df['ORGANIC_ITEM']
    del products_df['FINELINE_NUMBER']
    del products_df['KIRLAND_ITEM']

    print('[START] Product bulk insert started')
    s.bulk_insert_mappings(Product, products_df.to_dict(orient="records"))
    s.commit()
    print('[FINISH] Product bulk insert finished')
    a = pd.read_sql_table('products', engine)
    prices_stock_df['sku']=prices_stock_df['sku'].astype(str)

    merge = pd.merge(prices_stock_df, a, left_on='sku', right_on='sku', how='left')
    del merge['sku']
    del merge['barcodes']
    del merge['name']
    del merge['description']
    del merge['image_url']
    del merge['category']
    del merge['brand']
    del merge['package']
    del merge['store']
    merge.rename(columns={'id':'product_id'}, inplace=True)
    merge = merge[merge['product_id'].notna()]

    s.bulk_insert_mappings(BranchProduct, merge.to_dict(orient="records"))
    print('[START] BranchProduct bulk insert started')
    s.commit()
    print('[FINISH] BranchProduct bulk insert finished')
    s.close()




if __name__ == "__main__":
    process_csv_files()
