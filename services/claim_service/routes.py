from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Claim
from forms import ClaimForm
import requests

claim_routes = Blueprint('claim_routes', __name__)

@claim_routes.route('/claims')
def view_claims():
    user_id = request.args.get('user_id')
    if not user_id:
        return "User ID missing", 400

    claims = Claim.query.filter_by(user_id=user_id).all()
    return render_template('claims.html', claims=claims, user_id=user_id)


@claim_routes.route('/submit_claim', methods=['GET', 'POST'])
def submit_claim():
    user_id = request.args.get('user_id')
    if not user_id:
        return "User ID missing", 400

    form = ClaimForm()
    if form.validate_on_submit():
        new_claim = Claim(
            user_id=user_id,
            policy_id=form.policy_id.data,
            description=form.description.data
        )
        db.session.add(new_claim)
        db.session.commit()
        flash('Claim submitted successfully!', 'success')
        return redirect(url_for('claim_routes.view_claims', user_id=user_id))

    return render_template('submit_claim.html', form=form, user_id=user_id)

@claim_routes.route('/review_claims')
def review_claims():
    user_id = request.args.get('user_id')
    if not user_id:
        return "User ID missing", 400

    try:
        res = requests.get(f'http://localhost:5001/api/user/{user_id}')
        user_data = res.json()
        if user_data['role'] != 'admin':
            return "Access denied", 403
    except:
        return "Error verifying user", 500

    all_claims = Claim.query.all()
    return render_template('review_claims.html', claims=all_claims, user_id=user_id)

@claim_routes.route('/update_claim_status/<int:claim_id>/<string:new_status>')
def update_claim_status(claim_id, new_status):
    claim = Claim.query.get(claim_id)
    if claim:
        claim.status = new_status.capitalize()
        db.session.commit()
        return '', 204
    return 'Claim not found', 404
