from extensions import db

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cattle_breed = db.Column(db.String(100), nullable=False)
    age_limit = db.Column(db.String(50), nullable=False)
    premium = db.Column(db.Float, nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Policy {self.name}>'

class UserPolicy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'), nullable=False)
    applied_on = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(20), default='Pending')

    def __repr__(self):
        return f'<UserPolicy user_id={self.user_id} policy_id={self.policy_id}>'
