from datetime import datetime
from flask import Flask, render_template  # Import render_template
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
from models import db, User, CampaignGroup, Campaign  # Import User, CampaignGroup, and Campaign
from sqlalchemy.orm import joinedload  # Import joinedload
from routes.auth import auth_bp
from routes.campaign import campaign_bp
from routes.group import group_bp
from routes.journey import journey_bp
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///campaigns.db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here')  # Change this to a random secret key
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(campaign_bp)
app.register_blueprint(group_bp)
app.register_blueprint(journey_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('password')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True, port=5001)  # Set the port to 5001
