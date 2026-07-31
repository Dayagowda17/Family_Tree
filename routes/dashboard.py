from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.family import FamilyMember
from auth_decorators import admin_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('index.html')


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


@dashboard_bp.route('/share')
@login_required
@admin_required
def share():
    """Show the public, no-login link for external users - Admin only"""
    current_user.ensure_share_token()
    db.session.commit()
    public_url = url_for('public.public_tree', share_token=current_user.share_token, _external=True)
    return render_template('share.html', public_url=public_url)


@dashboard_bp.route('/share/regenerate', methods=['POST'])
@login_required
@admin_required
def regenerate_share():
    """Invalidate the old public link and create a new one - Admin only"""
    import secrets
    current_user.share_token = secrets.token_urlsafe(16)
    db.session.commit()
    flash('Your public link has been regenerated. The old link no longer works.', 'success')
    return redirect(url_for('dashboard.share'))


@dashboard_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@dashboard_bp.route('/profile/family-name', methods=['POST'])
@login_required
def update_family_name():
    """Set or change the family name shown at the top of the family tree."""
    family_name = request.form.get('family_name', '').strip()

    if not family_name:
        flash('Family name cannot be empty', 'danger')
        return redirect(url_for('dashboard.profile'))

    current_user.family_name = family_name
    db.session.commit()
    flash('Family name updated successfully', 'success')
    return redirect(url_for('dashboard.profile'))


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
