from models import db
from datetime import datetime


class Relationship(db.Model):
    __tablename__ = 'relationships'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=False)
    related_member_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=False)
    
    relationship_type = db.Column(db.String(50), nullable=False)  # sibling, uncle, aunt, cousin, etc.
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    member = db.relationship('FamilyMember', foreign_keys=[member_id], backref='relationships')
    related_member = db.relationship('FamilyMember', foreign_keys=[related_member_id])
    
    def __repr__(self):
        return f'<Relationship {self.relationship_type}>'
