from campaign_group import CampaignGroup
from campaign import Campaign
from conversion import Conversion
from product import Product

def main():
    # Create products
    product1 = Product(1, "Laptop")
    product2 = Product(2, "Smartphone")

    # Create campaign group
    group = CampaignGroup(1, "Tech Gadgets")

    # Create campaigns
    campaign1 = Campaign(1, "Summer Laptop Sale", product1, "Students")
    campaign2 = Campaign(2, "Smartphone Launch", product2, "Tech Enthusiasts")

    # Add campaigns to the group
    group.add_campaign(campaign1)
    group.add_campaign(campaign2)

    # Create conversions
    conversion1 = Conversion(1, product1, "Purchase")
    conversion2 = Conversion(2, product2, "Sign-up")

    # Add conversions to campaigns
    campaign1.add_conversion(conversion1)
    campaign2.add_conversion(conversion2)

    # Print information
    print(group)
    for campaign in group.campaigns:
        print(campaign)
        for conversion in campaign.conversions:
            print(f"  {conversion}")

if __name__ == "__main__":
    main()