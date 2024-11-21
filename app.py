from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Product, Conversion, Campaign, CampaignGroup, Task, Journey, JourneyStep
from sqlalchemy.orm import joinedload
from sqlalchemy import distinct
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campaigns.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a random secret key
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different username.')
            return redirect(url_for('register'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    groups = CampaignGroup.query.options(
        joinedload(CampaignGroup.campaigns).joinedload(Campaign.product)
    ).all()
    return render_template('index.html', groups=groups)

@app.route('/test_dashboard')
def test_dashboard():
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

@app.route('/campaign/edit/<int:campaign_id>', methods=['GET', 'POST'])
def edit_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    groups = CampaignGroup.query.all()
    products = Product.query.all()
    
    # New task creation section
    if request.method == 'POST' and request.form.get('form_type') == 'task_creation':
        task_id = request.form.get('task_id')
        jira_ticket = request.form.get('jira_ticket', '')
        description = request.form.get('description', '')
        status = request.form.get('status', 'Pending')
        
        new_task = Task(
            task_id=task_id,
            jira_ticket=jira_ticket,
            description=description,
            campaign_id=campaign_id,
            status=status
        )
        
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('edit_campaign', campaign_id=campaign_id))
    
    # Existing campaign edit logic
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
    
    # Fetch existing tasks for this campaign
    tasks = Task.query.filter_by(campaign_id=campaign_id).all()
    
    return render_template('edit_campaign.html', 
                           campaign=campaign, 
                           groups=groups, 
                           products=products,
                           tasks=tasks)

@app.route('/group/dashboard/<group_id>')
def group_dashboard(group_id):
    group = CampaignGroup.query.get_or_404(group_id)
    return render_template('group_dashboard.html', group=group)

@app.route('/conversion/add', methods=['GET', 'POST'])
def add_conversion():
    if request.method == 'POST':
        product_id = request.form['product_id']
        action = request.form['action']
        campaign_id = request.form['campaign_id']
        
        product = Product.query.get(product_id)
        conversion = Conversion(product_id=product.id, action=action, campaign_id=campaign_id)
        db.session.add(conversion)
        db.session.commit()
        return redirect(url_for('index'))
    
    campaigns = Campaign.query.all()
    return render_template('add_conversion.html', campaigns=campaigns, products=Product.query.all())

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

@app.route('/audience_list')
@login_required
def audience_list():
    audiences = db.session.query(distinct(Campaign.target_audience)).all()
    return render_template('audience_list.html', audiences=audiences)

@app.route('/create_journey', methods=['POST'])
@login_required
def create_journey():
    if not request.is_json:
        return jsonify({'error': 'Content type must be application/json'}), 400
    
    data = request.get_json()
    
    # Create new journey with a default name
    new_journey = Journey(
        name=f"Journey {data['steps'][0]} to {data['steps'][-1]}",
        user_id=current_user.id
    )
    db.session.add(new_journey)
    db.session.commit()

    # Create steps
    step_map = {}  # Map step IDs to database objects
    for step_data in data['steps']:
        journey_step = JourneyStep(
            journey_id=new_journey.id,
            name=f"{step_data['stepNang']} Step",
            details=json.dumps(step_data['details'])
        )
        db.session.add(journey_step)
        step_map[step_data['id']] = journey_step

    # Create connections
    for conn in data['connections']:
        from_step = step_map[conn['from']]
        to_step = step_map[conn['to']]
        from_step.next_step_id = to_step.id

    db.session.commit()
    return jsonify({'success': True, 'journey_id': new_journey.id})

@app.route('/journeys', methods=['GET'])
@login_required
def list_journeys():
    journeys = Journey.query.filter_by(user_id=current_user.id).all()
    return render_template('list_journeys.html', journeys=journeys)

@app.route('/journey/<int:journey_id>', methods=['GET'])
@login_required
def view_journey(journey_id):
    journey = Journey.query.get_or_404(journey_id)
    # Ensure the journey belongs to the current user
    if journey.user_id != current_user.id:
        flash('You do not have permission to view this journey.', 'danger')
        return redirect(url_for('index'))
    
    # Fetch steps in order
    steps = journey.steps.order_by(JourneyStep.step_number).all()
    return render_template('view_journey.html', journey=journey, steps=steps)

@app.route('/journey_design', methods=['GET'])
@login_required
def journey_design():
    return render_template('journey_design.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('password')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
