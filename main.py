import discountscraper, database, spacy
from . import unittests
from discount import Discount, Catalogue
from utility import compute_similarity_discount

def main():
    unittests()
    '''catalogues = discountscraper.get_all_catalogs('https://etilbudsavis.dk/discover/groceries')
    catalogue_ids = database.fetch_catalogue_id()
    discounts = []
    new_catalogues = []
    categories = {}

    for catalogue in catalogues: 
        if catalogue.catalogue_id not in catalogue_ids:
            new_catalogues.append(catalogue)
    
    if new_catalogues != []:
        nlp = spacy.load('da_core_news_lg')
        for category in database.fetch_ingredients():
            categories[category] = nlp(category)
        for catalogue in new_catalogues:
            database.insert_catalogue(catalogue)
            discounts += discountscraper.scraper(catalogue)
        for discount in discounts:
            product_count = len(discount.title.replace(" eller ", ",").replace(" el. ", ",").split(","))
            discount.matches = compute_similarity_discount(discount.title, categories, product_count)
        
        database.insert_discount_product(discounts)

        database.batch_insert_matches(discounts) '''





if __name__ == "__main__":
    main()








