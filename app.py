import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from config import config
from models import db
from models.user import User
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.family import family_bp
from routes.upload import upload_bp

# Create Flask application
app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config.get(config_name, config['development']))

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(family_bp)
app.register_blueprint(upload_bp)


# Context processors
@app.context_processor
def inject_user():
    return {'current_user': current_user}


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403


# Shell context for flask shell
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
    }


# Create application context and tables
with app.app_context():
    db.create_all()
    print("✓ Database initialized successfully")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
