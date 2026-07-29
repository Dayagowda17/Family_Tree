from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.family import FamilyMember

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    members = FamilyMember.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=10)
    stats = {
        'total_members': FamilyMember.query.filter_by(user_id=current_user.id).count(),
        'male_count': FamilyMember.query.filter_by(user_id=current_user.id, gender='Male').count(),
        'female_count': FamilyMember.query.filter_by(user_id=current_user.id, gender='Female').count(),
    }
    return render_template('dashboard.html', members=members, stats=stats)


@dashboard_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@dashboard_bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip()
    results = []
    
    if query:
        results = FamilyMember.query.filter_by(user_id=current_user.id).filter(
            (FamilyMember.first_name.ilike(f'%{query}%')) |
            (FamilyMember.last_name.ilike(f'%{query}%')) |
            (FamilyMember.email.ilike(f'%{query}%'))
        ).all()
    
    return render_template('search_results.html', results=results, query=query)
