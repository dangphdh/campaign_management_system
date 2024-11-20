from flask import Blueprint, render_template, request, redirect, url_for
from models import db, CampaignGroup, Product

group_bp = Blueprint('group', __name__)

@group_bp.route('/group/add', methods=['GET', 'POST'])
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

@group_bp.route('/group/edit/<int:group_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('group.edit_group', group_id=group.id))
    return render_template('add_group.html', group=group)
