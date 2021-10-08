using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace api_tavis.Food
{
    public class Recipe
    {
        public string Name { get; set; }

        public string Image { get; set; }

        public string Guide { get; set; }

        public List<Ingredient> Ingredients { get; set; }
    }
}
