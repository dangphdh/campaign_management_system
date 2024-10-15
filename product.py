class Product:
    def __init__(self, id, name, description=""):
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        return f"Product(id={self.id}, name={self.name}, description={self.description})"