from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def admin_required(f):
    """
    Decorator to require admin role for a route.
    Redirects non-admin users to the dashboard with an error message.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin():
            flash('You do not have permission to access this page. Admin access is required.', 'danger')
            return redirect(url_for('dashboard.dashboard'))
        
        return f(*args, **kwargs)
    
    return decorated_function
