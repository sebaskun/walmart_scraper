# Cornershop's backend integrations test

## Before you begin

Read this README completely before starting. There whole content of this document is relevant for the test and there are some important tips and notes in every section.

Before you begin, create a new private repository. Once you have finished the test, invite @jeffersonlizar @lbenitez000 as collaborators and send the link to the repository to your recruiter telling them you have finished.

## Introduction

This is the technical test for backend integration engineers. It's focused on connecting to remote services, gathering and processing data, finally storing it in the project's models.

A common task at Cornershop is collecting product information from external sources like websites and files. This test covers both tasks with simple cases:

- **Case 1**: Scraping a product department at Walmart Canada's website
- **Case 2**: Processing CSV files to extract clean information

The data models have already been defined for you. The ORM for this project is SQLAlchemy.

The product information is defined by two models (or tables):

### Product
The Product model contains basic product information:

*Product*

- Store
- Barcodes (a list of UPC/EAN barcodes)
- SKU (the product identifier in the store)
- Brand
- Name
- Description
- Package
- Image URL
- Category
- URL

### BranchProduct
The BranchProduct model contains the attributes of a product that are specific for a store's branch. The same product can be available/unavailable or have different prices at different branches.

*BranchProduct*

- Branch
- Product
- Stock
- Price

## Case 1

Cornershop is expanding to Canada and we want to provide our customers with the very best stores available in their city. One of them is [Walmart](https://www.walmart.ca/). They offer a very broad selection of products, from breakfast cereals to gym equipment. We need to ingest their product information and store it in our database before we can offer them to our customers.

The product information we need is:

*Product*

- Store `Walmart`
- Barcodes `60538887928`
- SKU `10295446`
- Brand `Great Value`
- Name `Spring Water`
- Description `Convenient and refreshing, Great Value Spring Water is a healthy option...`
- Package `24 x 500ml`
- Image URL `["https://i5.walmartimages.ca/images/Large/887/928/999999-60538887928.jpg", "https://i5.walmartimages.ca/images/Large/089/6_1/400896_1.jpg", "https://i5.walmartimages.ca/images/Large/88_/nft/605388879288_NFT.jpg"]`
- Category `Grocery|Pantry, Household & Pets|Drinks›Water|Bottled Water`
- URL `https://www.walmart.ca/en/ip/great-value-24pk-spring-water/6000143709667`

*BranchProduct*
 - Product `<product_id>`
 - Branch `3124`
 - Stock `426`
 - Price `2.27`

For now, we are only interested in the [Fruits](https://www.walmart.ca/en/grocery/fruits-vegetables/fruits/N-3852) category.

This repository has a *[Scrapy](https://scrapy.org/)* project with a dummy `CaWalmartSpider` that you have to finish implementing for this case. The Spider is already configured with the relevant `start_urls`, just make sure no products outside that category are being scraped. Also, the Item `ProductItem` and the Pipeline `StoragePipeline` are provided. You can run the Spider with `scrapy crawl ca_walmart`.

### Constraints

The following constraints apply:
1. The web crawler **must be implemented using [Scrapy](https://scrapy.org/)** only. [Selenium](https://www.selenium.dev/), [Splash](https://github.com/scrapinghub/splash) and similar libraries are not allowed. This test can be completed without using any other library or any kind of JS renderer.
2. We only need (and only want) product information from the "Groceries" website. Particularly from the `Grocery > Fruits & Vegetables > Fruits` category.
3. We only need (and only want) information from the following branches: `3124` and `3106`. These branches are located at Thunder Bay and Toronto respectively.

### Considerations

In Walmart's website, **pricing and availability information are available per branch**.

There is **no need** to create an account or sign-in.

The web crawler **must be implemented using [Scrapy](https://scrapy.org/)**. A ready-to-go project template is provided.

## Case 2
We have just signed a very important deal with one of the main retailers in Toronto: *Richart's Wholesale Club*. To improve the store's customer experience at Cornershop, our new partner has decided to send us periodical updates of their products, prices, and status. To accomplish this, they'll share multiple CSV files containing all the information.

You can find the latest version of these files in the `assets/` directory:
- **PRODUCTS.csv**: Contains the product's basic information.
- **PRICES-STOCK.csv**: Contains information about the prices and stock.

We need to write a script that puts together all the data, processes it, and stores it in our database. The data we need is the same as in case 1, so you can use the same ORM and database.

There is a script template at `integrations/richart_wholesale_club/ingestion.py`, extend it with your own logic.

### Constraints

The following constraints apply:

1. The only external libraries allowed in this case are [Pandas](https://pandas.pydata.org/) and [Numpy](https://numpy.org/).
2. We're only gonna work with branches `MM` and `RHSM` so we don't need (and don't want) other branches' information in the database.
3. You can use `Richart's` as the store name in the database.

### Considerations

#### PRODUCTS.csv
1. The **SKU must be unique** within the store. This is restricted by the data model.
2. All **texts must be cleaned** before inserting them into the database. For example, some product descriptions in the files may contain HTML tags, they must be removed.
3. Categories and sub-categories in the file must be joined together into a **single value** containing all categories **in lower case** and **separated by a pipe symbol** (`|`).
4. Some products might have the **package** information in the **description** column. *Extract the package* and store it in its corresponding field in the database.

#### PRICES-STOCK.csv
1. We only want products that are currently in stock, this means their **stock** is greater than 0.


## General considerations

The example data provided is just referential. **You are completely free to transform the information collected they way you want** (capitalize, replace text, transform symbols, etc.), but data stored must meet the data types and semantics of the data model. i.e: there must be a brand in the `Brand` field and a URL in the `Image URL` field, etc. The ORM is SQLAlchemy and it must be used as the only interface with the DB. If there is any piece of information that you think can be improved with some extra processing, please do it, we want high-quality information!

Feel free to **use the Python environment manager of your preference**. We provide a `Pipfile` in case you want to use `Pipenv` and a `requirements.txt` if you prefer to use Python's `pip`. Just remember to commit a file with the list of dependencies.

**Create and initialize the database** running `python database_setup.py`. It will create an SQLite3 database in the root directory of the project. You can delete and re-create the database as many times as you want.

When working on this test, consider we may want to add more scrapers and integrations in the future or use the same scraper and integration to process more branches of the same store. Please **write your code in a way it's easy to extend and maintain**.

# Aspects to be evaluated
- Software design
- Programing style
- Appropriate use of the framework (Scrapy)
- Crawling strategy
- Data processing strategy
- Quality of the collected data
- GIT repository history
