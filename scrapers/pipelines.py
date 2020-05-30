from sqlalchemy.orm import sessionmaker

from database_setup import engine
from models import BranchProduct, Product

# class TestPipeline:
#     def process_item(self, item, spider):
#         print('===============================================================', item)
#         return item

class StoragePipeline:
    def __init__(self, db_engine=engine) -> None:
        self.engine = db_engine

    def open_spider(self, spider):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):

        # Check if the Product already exists
        product = (
            self.session.query(Product)
            .filter_by(store=item["store"], sku=item["sku"])
            .first()
        )

        if product is None:
            product = Product(store=item["store"], sku=item["sku"])

        product.barcodes = item["barcodes"]
        product.brand = item["brand"]
        product.name = item["name"]
        product.package = item["package"]
        product.description = item["description"]
        product.image_url = item["image_url"]
        product.url = item['url']
        product.category = item['category']

        self.session.add(product)
        self.session.commit()

        # Check if the BranchProduct already exists
        branch_product = (
            self.session.query(BranchProduct)
            .filter_by(product=product, branch=item["branch"])
            .first()
        )

        if branch_product is None:
            branch_product = BranchProduct(product=product, branch=item["branch"])

        branch_product.stock = item["stock"]
        branch_product.price = item["price"]

        self.session.add(branch_product)
        self.session.commit()

        return item
