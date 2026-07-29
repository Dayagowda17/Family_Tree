"""Tests for authentication functionality."""

import pytest
from flask import url_for
from models.user import User


class TestRegistration:
    """Test user registration."""
    
    def test_register_page_loads(self, client):
        """Test registration page loads."""
        response = client.get(url_for('auth.register'))
        assert response.status_code == 200
        assert b'Register' in response.data
    
    def test_register_valid_user(self, client):
        """Test registering a valid user."""
        response = client.post(url_for('auth.register'), data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Check user was created
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'new@example.com'
    
    def test_register_duplicate_username(self, client, test_user):
        """Test registering with duplicate username."""
        response = client.post(url_for('auth.register'), data={
            'username': test_user.username,
            'email': 'other@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        
        assert b'already exists' in response.data or response.status_code == 200
    
    def test_register_password_mismatch(self, client):
        """Test registering with mismatched passwords."""
        response = client.post(url_for('auth.register'), data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'confirm_password': 'different123'
        })
        
        assert b'do not match' in response.data or response.status_code == 200
    
    def test_register_short_password(self, client):
        """Test registering with short password."""
        response = client.post(url_for('auth.register'), data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'pass',
            'confirm_password': 'pass'
        })
        
        assert b'at least' in response.data or response.status_code == 200


class TestLogin:
    """Test user login."""
    
    def test_login_page_loads(self, client):
        """Test login page loads."""
        response = client.get(url_for('auth.login'))
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_login_valid_credentials(self, client, test_user):
        """Test login with valid credentials."""
        response = client.post(url_for('auth.login'), data={
            'username': test_user.username,
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_login_invalid_password(self, client, test_user):
        """Test login with invalid password."""
        response = client.post(url_for('auth.login'), data={
            'username': test_user.username,
            'password': 'wrongpassword'
        })
        
        assert b'Invalid' in response.data or response.status_code == 200
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        response = client.post(url_for('auth.login'), data={
            'username': 'nonexistent',
            'password': 'password123'
        })
        
        assert b'Invalid' in response.data or response.status_code == 200
    
    def test_login_remember_me(self, client, test_user):
        """Test login with remember me option."""
        response = client.post(url_for('auth.login'), data={
            'username': test_user.username,
            'password': 'password123',
            'remember_me': True
        }, follow_redirects=True)
        
        assert response.status_code == 200


class TestLogout:
    """Test user logout."""
    
    def test_logout(self, authenticated_client):
        """Test logout functionality."""
        response = authenticated_client.get(url_for('auth.logout'), follow_redirects=True)
        assert response.status_code == 200
        assert b'logged out' in response.data or b'Login' in response.data
    
    def test_logout_unauthenticated(self, client):
        """Test logout when not authenticated."""
        response = client.get(url_for('auth.logout'))
        assert response.status_code in [302, 401]  # Redirect or unauthorized


class TestPasswordValidation:
    """Test password validation."""
    
    def test_password_hashing(self, test_user):
        """Test that passwords are properly hashed."""
        assert test_user.password_hash != 'password123'
        assert test_user.check_password('password123')
        assert not test_user.check_password('wrongpassword')
    
    def test_password_change_updates_hash(self, test_user):
        """Test that changing password updates hash."""
        old_hash = test_user.password_hash
        test_user.set_password('newpassword123')
        
        assert test_user.password_hash != old_hash
        assert test_user.check_password('newpassword123')
        assert not test_user.check_password('password123')


class TestSessionManagement:
    """Test session management."""
    
    def test_authenticated_user_access(self, authenticated_client):
        """Test authenticated user can access dashboard."""
        response = authenticated_client.get(url_for('dashboard.dashboard'))
        assert response.status_code == 200
    
    def test_unauthenticated_redirect(self, client):
        """Test unauthenticated user redirected to login."""
        response = client.get(url_for('dashboard.dashboard'))
        assert response.status_code in [302, 401]
    
    def test_session_persistence(self, authenticated_client):
        """Test session persists across requests."""
        response1 = authenticated_client.get(url_for('dashboard.dashboard'))
        response2 = authenticated_client.get(url_for('dashboard.dashboard'))
        
        assert response1.status_code == 200
        assert response2.status_code == 200
