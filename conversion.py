class Conversion:
    def __init__(self, id, product, action):
        self.id = id
        self.product = product
        self.action = action

    def __str__(self):
        return f"Conversion(id={self.id}, product={self.product.name}, action={self.action})"