from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Journey, JourneyStep, Task

journey_bp = Blueprint('journey', __name__)

@journey_bp.route('/create_journey', methods=['POST'])
@login_required
def create_journey():
    if not request.is_json:
        return jsonify({'error': 'Content type must be application/json'}), 400
    
    data = request.get_json()
    
    new_journey = Journey(
        name=f"Journey {data['steps'][0]} to {data['steps'][-1]}",
        user_id=current_user.id
    )
    db.session.add(new_journey)
    db.session.commit()

    for step_data in data['steps']:
        journey_step = JourneyStep(
            journey_id=new_journey.id,
            name=step_data['stepName'],
            step_number=step_data['stepNumber'],
            details=f"pageName: ({step_data['pageName']}, required: {step_data['required']})",
            created_at=datetime.utcnow()
        )
        db.session.add(journey_step)

    db.session.commit()
    return jsonify({'success': True, 'journey_id': new_journey.id})

@journey_bp.route('/list_journeys', methods=['GET'])
@login_required
def list_journeys():
    journeys = Journey.query.filter_by(user_id=current_user.id).all()
    return render_template('list_journeys.html', journeys=journeys)

@journey_bp.route('/journey/<int:journey_id>', methods=['GET'])
@login_required
def view_journey(journey_id):
    journey = Journey.query.get_or_404(journey_id)
    if journey.user_id != current_user.id:
        flash('You do not have permission to view this journey.', 'danger')
        return redirect(url_for('index'))
    
    steps = journey.steps.order_by(JourneyStep.step_number).all()
    return render_template('view_journey.html', journey=journey, steps=steps)

@journey_bp.route('/journey/edit/<int:journey_id>', methods=['GET', 'POST'])
def edit_journey(journey_id):
    journey = Journey.query.get_or_404(journey_id)
    if journey.user_id != current_user.id:
        flash('You do not have permission to edit this journey.', 'danger')
        return redirect(url_for('list_journeys'))

    if request.method == 'POST':
        journey.name = request.form['name']
        db.session.commit()
        flash('Journey updated successfully!', 'success')
        return redirect(url_for('journey.view_journey', journey_id=journey.id))

    return render_template('edit_journey.html', journey=journey)

@journey_bp.route('/journey/delete/<int:journey_id>', methods=['POST'])
@login_required
def delete_journey(journey_id):
    journey = Journey.query.get_or_404(journey_id)
    if journey.user_id != current_user.id:
        flash('You do not have permission to delete this journey.', 'danger')
        return redirect(url_for('list_journeys'))

    db.session.delete(journey)
    db.session.commit()
    flash('Journey deleted successfully!', 'success')
    return redirect(url_for('list_journeys'))
