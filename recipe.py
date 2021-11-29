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

    def convert_to_minutes(input):
        arr = input.split(' ')
        arr = list(filter(None, arr))

        if (len(arr) == 2):
            return int(arr[0])
        else:
            return int(arr[0]) * 60 + int(arr[3])

    def set_time(self, time):
        time = time.split('\t')
        time = time[len(time) - 1]
        self.time = self.convert_to_minutes(time)

    def set_amount_unit(self, amount_unit):
        amount_unit = amount_unit.replace('\t', '').split(' ')
        amount_unit = list(filter(None, amount_unit))
        self.amount_unit = amount_unit[len(amount_unit) - 1]

    def set_meal_type(self, meal_type):
        meal_type = meal_type.split(' / ')
        self.meal_type = meal_type[2]

    

