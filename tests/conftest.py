"""Test configuration and fixtures for Family Tree application."""

import pytest
import tempfile
import os
from app import app, db
from models.user import User
from models.family import FamilyMember
from datetime import date


@pytest.fixture
def client():
    """Create a test client for the application."""
    # Create a temporary database
    db_fd, db_path = tempfile.mkstemp()
    
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Create app context
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
    
    # Clean up
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def test_user(client):
    """Create a test user."""
    user = User(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
    user.set_password('password123')
    
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    
    return user


@pytest.fixture
def test_family_member(test_user):
    """Create a test family member."""
    member = FamilyMember(
        user_id=test_user.id,
        first_name='John',
        last_name='Doe',
        gender='Male',
        dob=date(1980, 1, 15),
        email='john@example.com',
        phone='+1234567890',
        address='123 Main Street',
        biography='A test family member'
    )
    
    with app.app_context():
        db.session.add(member)
        db.session.commit()
    
    return member


@pytest.fixture
def authenticated_client(client, test_user):
    """Create an authenticated test client."""
    # Login user
    client.post('/auth/login', data={
        'username': test_user.username,
        'password': 'password123'
    })
    
    return client


@pytest.fixture
def app_context():
    """Create application context."""
    with app.app_context():
        yield


# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "auth: mark test as testing authentication"
    )
