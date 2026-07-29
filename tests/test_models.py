"""
Unit tests for database models
"""

import pytest
from datetime import date, datetime
from app import app, db
from models.user import User
from models.family import FamilyMember


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def app_context():
    """Create application context"""
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


class TestUserModel:
    """Test User model"""
    
    def test_user_creation(self, app_context):
        """Test creating a user"""
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('password123')
        
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
    
    def test_password_hashing(self, app_context):
        """Test password is hashed correctly"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        
        assert user.password_hash != 'password123'
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')


class TestFamilyMemberModel:
    """Test FamilyMember model"""
    
    def test_family_member_creation(self, app_context):
        """Test creating a family member"""
        # Create user first
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # Create family member
        member = FamilyMember(
            user_id=user.id,
            first_name='John',
            last_name='Doe',
            gender='Male',
            dob=date(1990, 1, 15)
        )
        db.session.add(member)
        db.session.commit()
        
        assert member.id is not None
        assert member.user_id == user.id
        assert member.get_full_name() == 'John Doe'
    
    def test_get_full_name(self, app_context):
        """Test getting full name"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        member = FamilyMember(
            user_id=user.id,
            first_name='Jane',
            last_name='Smith',
            gender='Female'
        )
        
        assert member.get_full_name() == 'Jane Smith'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
