import discountscraper, database, spacy
from discount import Discount, Catalogue
from utility import compute_similarity_discount

def main():
    catalogues = discountscraper.get_all_catalogs('https://etilbudsavis.dk/discover/groceries')
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
            discount.matches = compute_similarity_discount(discount, categories)

        database.insert_discount_product(discounts)
        
    






if __name__ == "__main__":
    main()








