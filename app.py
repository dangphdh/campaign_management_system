from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson import ObjectId
from models import Product, Conversion, Campaign, CampaignGroup

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/campaign_management'
app.secret_key = 'your_secret_key_here'  # Add this line for flash messages
mongo = PyMongo(app)

@app.route('/')
def index():
    groups = list(mongo.db.campaign_groups.find())
    for group in groups:
        group['campaigns'] = list(mongo.db.campaigns.find({'group_id': group['_id']}))
        for campaign in group['campaigns']:
            campaign['product'] = mongo.db.products.find_one({'_id': campaign['product_id']})
    return render_template('index.html', groups=groups)

@app.route('/group/add', methods=['GET', 'POST'])
def add_group():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_group':
            name = request.form['name']
            powerbi_link = request.form['powerbi_link']
            group = CampaignGroup(name=name, powerbi_link=powerbi_link)
            mongo.db.campaign_groups.insert_one(group.__dict__)
        return redirect(url_for('index'))
    groups = list(mongo.db.campaign_groups.find())
    return render_template('add_group.html', groups=groups)

@app.route('/group/edit/<group_id>', methods=['GET', 'POST'])
def edit_group(group_id):
    group = mongo.db.campaign_groups.find_one({'_id': ObjectId(group_id)})
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_group':
            mongo.db.campaign_groups.update_one(
                {'_id': ObjectId(group_id)},
                {'$set': {
                    'name': request.form['name'],
                    'powerbi_link': request.form['powerbi_link']
                }}
            )
        elif action == 'add_campaign':
            campaign_name = request.form['campaign_name']
            product_name = request.form['product_name']
            target_audience = request.form['target_audience']
            product = mongo.db.products.find_one({'name': product_name})
            if not product:
                product = Product(name=product_name)
                product_id = mongo.db.products.insert_one(product.__dict__).inserted_id
            else:
                product_id = product['_id']
            campaign = Campaign(name=campaign_name, product_id=product_id, group_id=ObjectId(group_id), target_audience=target_audience)
            mongo.db.campaigns.insert_one(campaign.__dict__)
        return redirect(url_for('edit_group', group_id=group_id))
    return render_template('add_group.html', group=group)

@app.route('/campaign/add', methods=['GET', 'POST'])
def add_campaign():
    if request.method == 'POST':
        name = request.form['name']
        product_name = request.form['product']
        target_audience = request.form['target_audience']
        group_id = request.form.get('group_id', '')
        
        if not group_id:
            flash('Please select a valid group for the campaign.', 'error')
            groups = list(mongo.db.campaign_groups.find())
            return render_template('add_campaign.html', groups=groups)
        
        try:
            group_id = ObjectId(group_id)
        except:
            flash('Invalid group selected. Please try again.', 'error')
            groups = list(mongo.db.campaign_groups.find())
            return render_template('add_campaign.html', groups=groups)
        
        product = mongo.db.products.find_one({'name': product_name})
        if not product:
            product = Product(name=product_name)
            product_id = mongo.db.products.insert_one(product.__dict__).inserted_id
        else:
            product_id = product['_id']
        
        try:
            campaign = Campaign(name=name, product_id=product_id, target_audience=target_audience, group_id=group_id)
            mongo.db.campaigns.insert_one(campaign.__dict__)
            flash('Campaign added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding campaign: {str(e)}', 'error')
            groups = list(mongo.db.campaign_groups.find())
            return render_template('add_campaign.html', groups=groups)
        
        return redirect(url_for('index'))
    
    groups = list(mongo.db.campaign_groups.find())
    return render_template('add_campaign.html', groups=groups)

@app.route('/campaign/edit/<campaign_id>', methods=['GET', 'POST'])
def edit_campaign(campaign_id):
    campaign = mongo.db.campaigns.find_one({'_id': ObjectId(campaign_id)})
    if request.method == 'POST':
        name = request.form['name']
        product_name = request.form['product']
        target_audience = request.form['target_audience']
        group_id = request.form.get('group_id', '')
        
        if not group_id:
            flash('Please select a valid group for the campaign.', 'error')
            groups = list(mongo.db.campaign_groups.find())
            return render_template('edit_campaign.html', campaign=campaign, groups=groups)
        
        try:
            group_id = ObjectId(group_id)
        except:
            flash('Invalid group selected. Please try again.', 'error')
            groups = list(mongo.db.campaign_groups.find())
            return render_template('edit_campaign.html', campaign=campaign, groups=groups)
        
        product = mongo.db.products.find_one({'name': product_name})
        if not product:
            product = Product(name=product_name)
            product_id = mongo.db.products.insert_one(product.__dict__).inserted_id
        else:
            product_id = product['_id']
        
        try:
            mongo.db.campaigns.update_one(
                {'_id': ObjectId(campaign_id)},
                {'$set': {
                    'name': name,
                    'product_id': product_id,
                    'target_audience': target_audience,
                    'group_id': group_id
                }}
            )
            flash('Campaign updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating campaign: {str(e)}', 'error')
            groups = list(mongo.db.campaign_groups.find())
            return render_template('edit_campaign.html', campaign=campaign, groups=groups)
        
        return redirect(url_for('index'))
    
    groups = list(mongo.db.campaign_groups.find())
    return render_template('edit_campaign.html', campaign=campaign, groups=groups)

@app.route('/group/dashboard/<group_id>')
def group_dashboard(group_id):
    group = mongo.db.campaign_groups.find_one({'_id': ObjectId(group_id)})
    return render_template('group_dashboard.html', group=group)

@app.route('/conversion/add', methods=['GET', 'POST'])
def add_conversion():
    if request.method == 'POST':
        product_name = request.form['product']
        action = request.form['action']
        campaign_id = request.form.get('campaign_id', '')
        
        if not campaign_id:
            flash('Please select a valid campaign for the conversion.', 'error')
            campaigns = list(mongo.db.campaigns.find())
            return render_template('add_conversion.html', campaigns=campaigns)
        
        try:
            campaign_id = ObjectId(campaign_id)
        except:
            flash('Invalid campaign selected. Please try again.', 'error')
            campaigns = list(mongo.db.campaigns.find())
            return render_template('add_conversion.html', campaigns=campaigns)
        
        product = mongo.db.products.find_one({'name': product_name})
        if not product:
            product = Product(name=product_name)
            product_id = mongo.db.products.insert_one(product.__dict__).inserted_id
        else:
            product_id = product['_id']
        
        try:
            conversion = Conversion(product_id=product_id, action=action, campaign_id=campaign_id)
            mongo.db.conversions.insert_one(conversion.__dict__)
            flash('Conversion added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding conversion: {str(e)}', 'error')
            campaigns = list(mongo.db.campaigns.find())
            return render_template('add_conversion.html', campaigns=campaigns)
        
        return redirect(url_for('index'))
    
    campaigns = list(mongo.db.campaigns.find())
    return render_template('add_conversion.html', campaigns=campaigns)

@app.route('/conversion/edit/<conversion_id>', methods=['GET', 'POST'])
def edit_conversion(conversion_id):
    conversion = mongo.db.conversions.find_one({'_id': ObjectId(conversion_id)})
    if request.method == 'POST':
        product_name = request.form['product']
        action = request.form['action']
        campaign_id = request.form.get('campaign_id', '')
        
        if not campaign_id:
            flash('Please select a valid campaign for the conversion.', 'error')
            campaigns = list(mongo.db.campaigns.find())
            return render_template('edit_conversion.html', conversion=conversion, campaigns=campaigns)
        
        try:
            campaign_id = ObjectId(campaign_id)
        except:
            flash('Invalid campaign selected. Please try again.', 'error')
            campaigns = list(mongo.db.campaigns.find())
            return render_template('edit_conversion.html', conversion=conversion, campaigns=campaigns)
        
        product = mongo.db.products.find_one({'name': product_name})
        if not product:
            product = Product(name=product_name)
            product_id = mongo.db.products.insert_one(product.__dict__).inserted_id
        else:
            product_id = product['_id']
        
        try:
            mongo.db.conversions.update_one(
                {'_id': ObjectId(conversion_id)},
                {'$set': {
                    'product_id': product_id,
                    'action': action,
                    'campaign_id': campaign_id
                }}
            )
            flash('Conversion updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating conversion: {str(e)}', 'error')
            campaigns = list(mongo.db.campaigns.find())
            return render_template('edit_conversion.html', conversion=conversion, campaigns=campaigns)
        
        return redirect(url_for('index'))
    
    campaigns = list(mongo.db.campaigns.find())
    return render_template('edit_conversion.html', conversion=conversion, campaigns=campaigns)

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        product = Product(name=name)
        mongo.db.products.insert_one(product.__dict__)
        return redirect(url_for('add_product'))
    products = list(mongo.db.products.find())
    return render_template('add_edit_product.html', products=products)

@app.route('/product/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if request.method == 'POST':
        mongo.db.products.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': {'name': request.form['name']}}
        )
        return redirect(url_for('add_product'))
    return render_template('add_edit_product.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)