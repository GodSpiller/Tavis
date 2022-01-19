import unittest
from discountscraper import get_all_catalogs, scraper
from discount import Discount, Catalogue
from recipescraper import get_all_recipes, recipe_scraper
from recipe import Recipe
import utility, spacy
from utility import compute_similarity, compute_similarity_discount, highest_values

class TestDiscountScraper(unittest.TestCase):

    def test_get_all_catalogs(self):
        #arrange
        test_list = []
        #act
        test_list = get_all_catalogs('https://etilbudsavis.dk/discover/groceries')
        #assert
        for catalogue in test_list:
            self.assertIsNotNone(catalogue)

    def test_scraper(self):
        #arrange
        test_list = []
        #act
        test_list = scraper(get_all_catalogs('https://etilbudsavis.dk/discover/groceries')[0])
        #assert
        for discount in test_list:
            self.assertIsNotNone(discount)

    
    def test_recipe_crawler(self):
        #arrange
        test_list = []
        #act
        test_list = get_all_recipes(['https://mummum.dk/opskrifter/'])
        #assert
        for url in test_list:
            self.assertTrue('https://mummum.dk/' in url)

    def test_recipe_scraper(self):
        #arrange
        test_list = []
        #act
        test_list = recipe_scraper(['https://mummum.dk/hasselnoeddekurve/'])
        #assert
        self.assertIsNotNone(test_list[0])
    
    def test_compute_similarity(self):
        #arrange
        nlp = spacy.load('da_core_news_lg')
        categories = {}
        categories['test'] = nlp('test')
        #act
        test = compute_similarity('test', categories)
        #assert
        self.assertTrue(test == 'test')


if __name__ == '__main__':
    unittest.main()