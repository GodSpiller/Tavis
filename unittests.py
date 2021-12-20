
import unittest
from recipescraper import get_all_recipes, recipe_scraper
import requests
from recipe import Recipe
from bs4 import BeautifulSoup
from time import sleep
from urllib.robotparser import RobotFileParser

class TestRecipeScraperMethods(unittest.TestCase):

    def test_get_all_recipes(self):
        recipes = get_all_recipes(['https://mummum.dk/budapestrulle-med-baerskum/'])
        self.assertTrue(recipes is list)

      

if __name__ == '__main__':
    unittest.main()