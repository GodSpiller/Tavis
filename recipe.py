import utility

class Recipe(object):

    def __init__(self):
        self.title = ''
        self.amounts = []
        self.units = []
        self.ingredients = []
        self.instructions = ''
        self.meal_type = ''
        self.quantity = 1
        self.image = ''
        self.amount_unit = ''
        self.time = 0

    def set_time(self, time):
        time = time.split('\t')
        time = time[len(time) - 1]
        self.time = utility.convertToMinutes(time)

    def set_amount_unit(self, amount_unit):
        amount_unit = amount_unit.replace('\t', '').split(' ')
        amount_unit = list(filter(None, amount_unit))
        self.amount_unit = amount_unit[len(amount_unit) - 1]

    def set_meal_type(self, meal_type):
        meal_type = meal_type.split(' / ')
        self.meal_type = meal_type[2]
