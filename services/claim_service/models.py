# models.py
from extensions import db

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    policy_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    submitted_on = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(20), default='Pending')

    def __repr__(self):
        return f'<Claim {self.id} for user {self.user_id}>'
