from models import db
from datetime import datetime


class FamilyMember(db.Model):
    __tablename__ = 'family_members'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # Male, Female, Other
    dob = db.Column(db.Date)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    biography = db.Column(db.Text)
    photo = db.Column(db.String(255))  # Store filename
    
    # Family relationships
    father_id = db.Column(db.Integer, db.ForeignKey('family_members.id'))
    mother_id = db.Column(db.Integer, db.ForeignKey('family_members.id'))
    spouse_id = db.Column(db.Integer, db.ForeignKey('family_members.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships for navigation
    father = db.relationship('FamilyMember', remote_side=[id], foreign_keys=[father_id], backref='children_as_father')
    mother = db.relationship('FamilyMember', remote_side=[id], foreign_keys=[mother_id], backref='children_as_mother')
    spouse = db.relationship('FamilyMember', remote_side=[id], foreign_keys=[spouse_id], 
                            backref='spouses', uselist=False)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        if self.dob:
            from datetime import date
            today = date.today()
            age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            return age
        return None
    
    def get_children(self):
        """Get all children of this member"""
        return FamilyMember.query.filter(
            (FamilyMember.father_id == self.id) | (FamilyMember.mother_id == self.id)
        ).all()
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'dob': self.dob.isoformat() if self.dob else None,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'biography': self.biography,
            'photo': self.photo,
            'father_id': self.father_id,
            'mother_id': self.mother_id,
            'spouse_id': self.spouse_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<FamilyMember {self.get_full_name()}>'
