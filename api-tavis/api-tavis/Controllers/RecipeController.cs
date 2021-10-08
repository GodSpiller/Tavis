using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace api_tavis.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class RecipeController : ControllerBase
    {
        private static readonly string[] recipes = new[]
        {
            "Majsdeller", "Guacamole", "Kyllingelår med Marinade", "Chili Con Carne", 
            "Hotwings", "Kylling Kiev", "Fajitas", "Madpandekager", "Krydrede kyllingelår", 
            "Minestronesuppe", "Forloren Hare", "Frikadeller", "Boller i Karry"
        };

        private readonly ILogger<RecipeController> _logger;

        public RecipeController(ILogger<RecipeController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public string Get()
        {
            Random rnd = new Random();
            return recipes[rnd.Next(0, recipes.Length - 1)];
        }
    }
}
