class CampaignGroup:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.campaigns = []

    def add_campaign(self, campaign):
        self.campaigns.append(campaign)

    def __str__(self):
        return f"CampaignGroup(id={self.id}, name={self.name}, campaigns={len(self.campaigns)})"