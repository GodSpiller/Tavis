import utility

class Catalogue(object):

    def __init__(self):
        self.store_name = ""
        self.catalogue_id = ""
        self.valid_from = ""
        self.valid_to = ""
        #liste = 

class Discount(object):

    def __init__(self):
        self.catalogue_id = ""
        self.title = ""
        self.price = 0.0
        self.valid_from = ""
        self.valid_to = ""
        self.amount = ""
        self.unit = ""
        self.matches = []

    def __iter__(self):
        yield self.catalogue_id
        yield self.title
        yield self.price
        yield self.valid_from
        yield self.valid_to
        yield self.unit
        yield self.amount
        



    
