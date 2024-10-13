class Product:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"Product(id={self.id}, name={self.name})"