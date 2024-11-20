from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Campaign, CampaignGroup, Product

campaign_bp = Blueprint('campaign', __name__)

@campaign_bp.route('/campaign/add', methods=['GET', 'POST'])
def add_campaign():
    if request.method == 'POST':
        name = request.form['name']
        product_id = request.form['product_id']
        target_audience = request.form['target_audience']
        group_id = request.form['group_id']
        campaign_docs = request.form['campaign_docs']
        campaign_description = request.form['campaign_description']
        TnC = request.form['TnC']
        content = request.form['content']
        division = request.form['division']
        nature = request.form['nature']
        adobe_camp_id = request.form['adobe_camp_id']
        crm_camp_id = request.form['crm_camp_id']
        
        product = Product.query.get(product_id)
        campaign = Campaign(
            name=name, 
            product_id=product.id, 
            target_audience=target_audience, 
            group_id=group_id,
            campaign_docs=campaign_docs,
            campaign_description=campaign_description,
            TnC=TnC,
            content=content,
            division=division,
            nature=nature,
            adobe_camp_id=adobe_camp_id,
            crm_camp_id=crm_camp_id
        )
        db.session.add(campaign)
        db.session.commit()
        flash('New campaign added successfully.')
        return redirect(url_for('index'))
    
    groups = CampaignGroup.query.all()
    products = Product.query.all()
    return render_template('add_campaign.html', groups=groups, products=products)

@campaign_bp.route('/campaign/edit/<int:campaign_id>', methods=['GET', 'POST'])
def edit_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    groups = CampaignGroup.query.all()
    products = Product.query.all()
    
    if request.method == 'POST':
        campaign.name = request.form['name']
        product_id = request.form['product_id']
        campaign.target_audience = request.form['target_audience']
        campaign.group_id = request.form['group_id']
        campaign.campaign_docs = request.form['campaign_docs']
        campaign.campaign_description = request.form['campaign_description']
        campaign.TnC = request.form['TnC']
        campaign.content = request.form['content']
        campaign.division = request.form['division']
        campaign.nature = request.form['nature']
        campaign.adobe_camp_id = request.form['adobe_camp_id']
        campaign.crm_camp_id = request.form['crm_camp_id']
        
        product = Product.query.get(product_id)
        campaign.product_id = product.id
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_campaign.html', 
                           campaign=campaign, 
                           groups=groups, 
                           products=products)
