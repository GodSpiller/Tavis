using api_tavis.Food;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace api_tavis.Utility
{
    public static class Util
    {
        public static List<Recipe> GetRecipes()
        {
            List<Recipe> recipes = new List<Recipe>()
            {
                new Recipe()
                {
                    Name = "Madpandekager",
                    Image = "https://mambeno.dk/wp-content/uploads/2015/12/Madpandekager.jpg",
                    Guide = "Placeholder",
                    Ingredients = new List<Ingredient>()
                    {
                        new Ingredient() { Name = "Mel" },
                        new Ingredient() { Name = "Mælk" },
                        new Ingredient() { Name = "Æg" }
                    }
                },

                new Recipe()
                {
                    Name = "Omelet",
                    Image = "https://mariavestergaard.dk/wp-content/uploads/2020/04/Omelet.jpg",
                    Guide = "Placeholder",
                    Ingredients = new List<Ingredient>()
                    {
                        new Ingredient() { Name = "Æg" },
                        new Ingredient() { Name = "Paprika" },
                        new Ingredient() { Name = "Peber" },
                        new Ingredient() { Name = "Olie" }
                    }
                },

                new Recipe()
                {
                    Name = "Rødspætte",
                    Image = "https://asset.dr.dk/imagescaler01/http://mad-recipe-pictures-dr-dk.s3.amazonaws.com/prod/recipe/rodspaetter-1518863468.jpg&w=1140&h=641&scaleAfter=crop&quality=75&ratio=16-9",
                    Guide = "Placeholder",
                    Ingredients = new List<Ingredient>()
                    {
                        new Ingredient() { Name = "Rødspætte" },
                        new Ingredient() { Name = "Rugmel " },
                        new Ingredient() { Name = "Smør " },
                        new Ingredient() { Name = "Olie" },
                        new Ingredient() { Name = "Peper" },
                        new Ingredient() { Name = "Salt" },
                    }
                },
            };

            return recipes;
        }
    }
}
