import random

def get_audience_data():
    """
    Fake API function to fetch audience data for bank guarantee campaigns.
    Returns a list of audience segments with potential values.
    """
    audience_segments = [
        {"name": "High Net Worth Individuals", "potential": random.randint(500, 2000)},
        {"name": "Small Business Owners", "potential": random.randint(300, 1500)},
        {"name": "Corporate Executives", "potential": random.randint(400, 1800)},
        {"name": "Retirees with Investments", "potential": random.randint(400, 1600)},
        {"name": "Real Estate Investors", "potential": random.randint(600, 2200)}
    ]
    return audience_segments
