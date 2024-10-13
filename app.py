from flask import Flask, render_template, request, redirect, url_for
from models import db, Product, Conversion, Campaign, CampaignGroup
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campaigns.db'
db.init_app(app)

@app.route('/')
def index():
    groups = CampaignGroup.query.options(
        joinedload(CampaignGroup.campaigns).joinedload(Campaign.product)
    ).all()
    return render_template('index.html', groups=groups)

@app.route('/group/add', methods=['GET', 'POST'])
def add_group():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_group':
            name = request.form['name']
            powerbi_link = request.form['powerbi_link']
            group = CampaignGroup(name=name, powerbi_link=powerbi_link)
            db.session.add(group)
            db.session.commit()
        return redirect(url_for('index'))
    groups = CampaignGroup.query.all()
    return render_template('add_group.html', groups=groups)

@app.route('/group/edit/<int:group_id>', methods=['GET', 'POST'])
def edit_group(group_id):
    group = CampaignGroup.query.get_or_404(group_id)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_group':
            group.name = request.form['name']
            group.powerbi_link = request.form['powerbi_link']
            db.session.commit()
        elif action == 'add_campaign':
            campaign_name = request.form['campaign_name']
            product_name = request.form['product_name']
            target_audience = request.form['target_audience']
            product = Product.query.filter_by(name=product_name).first()
            if not product:
                product = Product(name=product_name)
                db.session.add(product)
                db.session.commit()
            campaign = Campaign(name=campaign_name, product_id=product.id, group_id=group.id, target_audience=target_audience)
            db.session.add(campaign)
            db.session.commit()
        return redirect(url_for('edit_group', group_id=group.id))
    return render_template('add_group.html', group=group)

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
            db.session.commit()
        
        campaign = Campaign(name=name, product_id=product.id, target_audience=target_audience, group_id=group_id)
        db.session.add(campaign)
        db.session.commit()
        return redirect(url_for('index'))
    
    groups = CampaignGroup.query.all()
    return render_template('add_campaign.html', groups=groups)

@app.route('/group/dashboard/<int:group_id>')
def group_dashboard(group_id):
    group = CampaignGroup.query.get_or_404(group_id)
    return render_template('group_dashboard.html', group=group)

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
            db.session.commit()
        
        conversion = Conversion(product_id=product.id, action=action, campaign_id=campaign_id)
        db.session.add(conversion)
        db.session.commit()
        return redirect(url_for('index'))
    
    campaigns = Campaign.query.all()
    return render_template('add_conversion.html', campaigns=campaigns)

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        product = Product(name=name)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('add_product'))
    products = Product.query.all()
    return render_template('add_edit_product.html', products=products)

@app.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        db.session.commit()
        return redirect(url_for('add_product'))
    return render_template('add_edit_product.html', product=product)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)