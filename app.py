from flask import Flask, render_template, request, redirect, url_for
from models import db, Product, Conversion, Campaign, CampaignGroup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campaigns.db'
db.init_app(app)

@app.route('/')
def index():
    groups = CampaignGroup.query.all()
    return render_template('index.html', groups=groups)

@app.route('/group/add', methods=['GET', 'POST'])
def add_group():
    if request.method == 'POST':
        name = request.form['name']
        group = CampaignGroup(name=name)
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_group.html')

@app.route('/campaign/add', methods=['GET', 'POST'])
def add_campaign():
    if request.method == 'POST':
        name = request.form['name']
        product_name = request.form['product']
        target_audience = request.form['target_audience']
        group_id = request.form['group_id']
        
        product = Product.query.filter_by(name=product_name).first()
        if not product:
            product = Product(name=product_name)
            db.session.add(product)
        
        campaign = Campaign(name=name, product=product, target_audience=target_audience, group_id=group_id)
        db.session.add(campaign)
        db.session.commit()
        return redirect(url_for('index'))
    
    groups = CampaignGroup.query.all()
    return render_template('add_campaign.html', groups=groups)

@app.route('/conversion/add', methods=['GET', 'POST'])
def add_conversion():
    if request.method == 'POST':
        product_name = request.form['product']
        action = request.form['action']
        campaign_id = request.form['campaign_id']
        
        product = Product.query.filter_by(name=product_name).first()
        if not product:
            product = Product(name=product_name)
            db.session.add(product)
        
        conversion = Conversion(product=product, action=action, campaign_id=campaign_id)
        db.session.add(conversion)
        db.session.commit()
        return redirect(url_for('index'))
    
    campaigns = Campaign.query.all()
    return render_template('add_conversion.html', campaigns=campaigns)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)