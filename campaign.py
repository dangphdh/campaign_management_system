class Campaign:
    def __init__(self, id, name, product, target_audience):
        self.id = id
        self.name = name
        self.product = product
        self.target_audience = target_audience
        self.conversions = []

    def add_conversion(self, conversion):
        self.conversions.append(conversion)

    def __str__(self):
        return f"Campaign(id={self.id}, name={self.name}, product={self.product.name}, target_audience={self.target_audience}, conversions={len(self.conversions)})"