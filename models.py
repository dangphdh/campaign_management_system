from bson import ObjectId

class Product:
    def __init__(self, name, _id=None):
        self._id = _id or ObjectId()
        self.name = name

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            _id=data.get('_id')
        )

class Conversion:
    def __init__(self, product_id, action, campaign_id, _id=None):
        self._id = _id or ObjectId()
        self.product_id = product_id
        self.action = action
        self.campaign_id = campaign_id

    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id=data['product_id'],
            action=data['action'],
            campaign_id=data['campaign_id'],
            _id=data.get('_id')
        )

class Campaign:
    def __init__(self, name, product_id, target_audience, group_id, _id=None):
        self._id = _id or ObjectId()
        self.name = name
        self.product_id = product_id
        self.target_audience = target_audience
        self.group_id = group_id

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            product_id=data['product_id'],
            target_audience=data['target_audience'],
            group_id=data['group_id'],
            _id=data.get('_id')
        )

class CampaignGroup:
    def __init__(self, name, powerbi_link=None, _id=None):
        self._id = _id or ObjectId()
        self.name = name
        self.powerbi_link = powerbi_link

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            powerbi_link=data.get('powerbi_link'),
            _id=data.get('_id')
        )