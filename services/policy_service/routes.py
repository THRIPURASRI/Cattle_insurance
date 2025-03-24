from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Policy, UserPolicy
from extensions import db
import requests

policy_routes = Blueprint('policy_routes', __name__)

@policy_routes.route('/policies')
def view_policies():
    user_id = request.args.get('user_id')
    if not user_id:
        return "User ID missing", 400

    policies = Policy.query.all()
    user_policies = UserPolicy.query.filter_by(user_id=user_id).all()
    user_policy_ids = [up.policy_id for up in user_policies]
    return render_template('policies.html', policies=policies, user_id=user_id, user_policy_ids=user_policy_ids)


@policy_routes.route('/apply/<int:policy_id>', methods=['POST'])
def apply_policy(policy_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return "User ID missing", 400

    existing = UserPolicy.query.filter_by(user_id=user_id, policy_id=policy_id).first()
    if existing:
        flash("You have already applied for this policy.", "warning")
    else:
        new_application = UserPolicy(user_id=user_id, policy_id=policy_id)
        db.session.add(new_application)
        db.session.commit()
        flash("Policy applied successfully!", "success")

    return redirect(url_for('policy_routes.view_policies', user_id=user_id))


@policy_routes.route('/add_policy', methods=['GET', 'POST'])
def add_policy():
    user_id = request.args.get('user_id')
    if request.method == 'POST':
        name = request.form['name']
        breed = request.form['breed']
        age_limit = request.form['age_limit']
        premium = request.form['premium']
        duration = request.form['duration']

        new_policy = Policy(
            name=name,
            cattle_breed=breed,
            age_limit=age_limit,
            premium=float(premium),
            duration_months=int(duration)
        )
        db.session.add(new_policy)
        db.session.commit()
        flash('New policy added!', 'success')
        return redirect(url_for('policy_routes.view_policies', user_id=user_id))
    
    return render_template('add_policy.html', user_id=user_id)


@policy_routes.route('/applications')
def admin_view_applications():
    user_id = request.args.get('user_id')
    if not user_id:
        return "User ID missing", 400

    try:
        user_response = requests.get(f'http://localhost:5001/api/user/{user_id}')
        if user_response.status_code != 200:
            return "Unable to verify user", 403
        user_data = user_response.json()
        if user_data['role'] != 'admin':
            return "Access Denied: Admins only", 403
    except Exception as e:
        return f"Error verifying user: {e}", 500

    applications = UserPolicy.query.all()
    return render_template('applications.html', applications=applications, user_id=user_id)


@policy_routes.route('/update_status/<int:application_id>/<string:new_status>')
@policy_routes.route('/update_status/<int:application_id>/<string:new_status>')
def update_status(application_id, new_status):
    application = UserPolicy.query.get(application_id)
    if application:
        application.status = new_status.capitalize()
        db.session.commit()
        return '', 204  # ✅ success with no content (used by fetch)
    return 'Application not found', 404
