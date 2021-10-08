using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using api_tavis.Food;
using api_tavis.Utility;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace api_tavis.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class RecipeController : ControllerBase
    {
        private readonly ILogger<RecipeController> _logger;

        public RecipeController(ILogger<RecipeController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public string Get()
        {
            List<Recipe> recipes = Util.GetRecipes();
            return JsonConvert.SerializeObject(recipes);
        }
    }
}
