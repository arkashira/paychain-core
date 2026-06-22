class Product:
    def __init__(self, name, demand):
        self.name = name
        self.demand = demand

    def __str__(self):
        return f"Product '{self.name}' with demand {self.demand}"
