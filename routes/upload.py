from flask import Blueprint, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from models import db
from models.family import FamilyMember
from werkzeug.utils import secure_filename
import os
from PIL import Image

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def resize_image(image_path, size=(300, 300)):
    """Resize image to specified size"""
    try:
        img = Image.open(image_path)
        img.thumbnail(size, Image.Resampling.LANCZOS)
        img.save(image_path, quality=85, optimize=True)
    except Exception as e:
        print(f"Error resizing image: {e}")


@upload_bp.route('/photo/<int:member_id>', methods=['POST'])
@login_required
def upload_photo(member_id):
    member = FamilyMember.query.get_or_404(member_id)
    
    if member.user_id != current_user.id:
        flash('You do not have permission to upload photos for this member', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    if 'photo' not in request.files:
        flash('No file selected', 'danger')
        return redirect(url_for('family.view_member', member_id=member_id))
    
    file = request.files['photo']
    
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('family.view_member', member_id=member_id))
    
    if not allowed_file(file.filename):
        flash('Only PNG, JPG, JPEG, and GIF files are allowed', 'danger')
        return redirect(url_for('family.view_member', member_id=member_id))
    
    try:
        # Create uploads folder if it doesn't exist
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        # Delete old photo if exists
        if member.photo:
            old_photo_path = os.path.join(upload_folder, member.photo)
            if os.path.exists(old_photo_path):
                os.remove(old_photo_path)
        
        # Generate new filename
        filename = secure_filename(f"{member_id}_{member.first_name.lower()}_{file.filename}")
        filepath = os.path.join(upload_folder, filename)
        
        # Save file
        file.save(filepath)
        
        # Resize image
        resize_image(filepath)
        
        # Update database
        member.photo = filename
        db.session.commit()
        
        flash('Photo uploaded successfully!', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error uploading photo: {str(e)}', 'danger')
    
    return redirect(url_for('family.view_member', member_id=member_id))


@upload_bp.route('/photo/<int:member_id>/delete', methods=['POST'])
@login_required
def delete_photo(member_id):
    member = FamilyMember.query.get_or_404(member_id)
    
    if member.user_id != current_user.id:
        flash('You do not have permission to delete photos for this member', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    if member.photo:
        try:
            photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], member.photo)
            if os.path.exists(photo_path):
                os.remove(photo_path)
            
            member.photo = None
            db.session.commit()
            flash('Photo deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting photo: {str(e)}', 'danger')
    
    return redirect(url_for('family.view_member', member_id=member_id))
