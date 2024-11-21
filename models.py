from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    # journeys = db.relationship('Journey', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    campaigns = db.relationship('Campaign', backref='product', lazy=True)

class Conversion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    product = db.relationship('Product', backref='conversions', lazy=True)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    target_audience = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('campaign_group.id'), nullable=False)
    conversions = db.relationship('Conversion', backref='campaign', lazy=True)
    tasks = db.relationship('Task', backref='campaign', lazy=True)
    campaign_docs = db.Column(db.String(500), nullable=True)
    campaign_description = db.Column(db.Text, nullable=True)
    TnC = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)
    division = db.Column(db.String(100), nullable=True)
    nature = db.Column(db.String(100), nullable=True)
    adobe_camp_id = db.Column(db.String(100), nullable=True)
    crm_camp_id = db.Column(db.String(100), nullable=True)

class CampaignGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    powerbi_link = db.Column(db.String(500), nullable=True)
    campaigns = db.relationship('Campaign', backref='group', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(100), nullable=False)
    jira_ticket = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    status = db.Column(db.String(50), nullable=True, default='Pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    steps = db.relationship('JourneyStep', backref='journey', lazy='dynamic', cascade='all, delete-orphan')

class JourneyStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    journey_id = db.Column(db.Integer, db.ForeignKey('journey.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
