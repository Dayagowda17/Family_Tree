"""Utility functions for Family Tree application."""

import os
import secrets
from datetime import datetime, date
from functools import wraps
from flask import abort, current_app
from flask_login import current_user


def generate_secret_key(length=32):
    """Generate a secure random secret key.
    
    Args:
        length: Length of the generated key
        
    Returns:
        A secure random string
    """
    return secrets.token_urlsafe(length)


def allowed_file(filename, allowed_extensions=None):
    """Check if file extension is allowed.
    
    Args:
        filename: The filename to check
        allowed_extensions: Set of allowed extensions
        
    Returns:
        Boolean indicating if file is allowed
    """
    if allowed_extensions is None:
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def secure_filename_custom(filename, prefix=''):
    """Create a secure filename with optional prefix.
    
    Args:
        filename: Original filename
        prefix: Optional prefix for the filename
        
    Returns:
        A secure filename
    """
    import re
    from werkzeug.utils import secure_filename as werkzeug_secure_filename
    
    secure_name = werkzeug_secure_filename(filename)
    
    if prefix:
        name, ext = os.path.splitext(secure_name)
        secure_name = f"{prefix}_{name}{ext}"
    
    # Add timestamp to ensure uniqueness
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(secure_name)
    return f"{name}_{timestamp}{ext}"


def calculate_age(birth_date):
    """Calculate age from birth date.
    
    Args:
        birth_date: datetime.date object
        
    Returns:
        Age in years as integer
    """
    if not birth_date:
        return None
    
    today = date.today()
    age = today.year - birth_date.year
    
    # Adjust if birthday hasn't occurred this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age if age >= 0 else None


def format_date(date_obj, format_str='%B %d, %Y'):
    """Format date object to string.
    
    Args:
        date_obj: datetime.date or datetime.datetime object
        format_str: strftime format string
        
    Returns:
        Formatted date string
    """
    if not date_obj:
        return None
    
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()
    
    return date_obj.strftime(format_str)


def require_permission(permission):
    """Decorator to check user permissions.
    
    Args:
        permission: Required permission string
        
    Returns:
        Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            # Add permission check logic here
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def check_user_owns_member(member_id):
    """Check if current user owns a family member.
    
    Args:
        member_id: Family member ID
        
    Returns:
        Boolean indicating ownership
    """
    from models.family import FamilyMember
    
    if not current_user.is_authenticated:
        return False
    
    member = FamilyMember.query.get(member_id)
    return member and member.user_id == current_user.id


def get_file_size(file_path):
    """Get file size in bytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in bytes
    """
    try:
        return os.path.getsize(file_path)
    except OSError:
        return None


def get_file_size_mb(file_path):
    """Get file size in megabytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in MB
    """
    size_bytes = get_file_size(file_path)
    if size_bytes is None:
        return None
    return size_bytes / (1024 * 1024)


def delete_file(file_path):
    """Safely delete a file.
    
    Args:
        file_path: Path to file
        
    Returns:
        Boolean indicating success
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        current_app.logger.error(f"Error deleting file {file_path}: {str(e)}")
        return False


def sanitize_html(text):
    """Remove potentially dangerous HTML from text.
    
    Args:
        text: Text containing HTML
        
    Returns:
        Sanitized text
    """
    if not text:
        return text
    
    import html
    return html.escape(text)


def truncate_text(text, length=100, suffix='...'):
    """Truncate text to specified length.
    
    Args:
        text: Text to truncate
        length: Maximum length
        suffix: Suffix to add when truncated
        
    Returns:
        Truncated text
    """
    if not text:
        return text
    
    if len(text) <= length:
        return text
    
    return text[:length - len(suffix)] + suffix


def get_initials(first_name, last_name=''):
    """Get initials from names.
    
    Args:
        first_name: First name
        last_name: Last name (optional)
        
    Returns:
        Initials as uppercase string
    """
    initials = first_name[0].upper() if first_name else ''
    
    if last_name:
        initials += last_name[0].upper()
    
    return initials


def is_valid_email(email):
    """Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        Boolean indicating valid email
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone):
    """Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        Boolean indicating valid phone
    """
    import re
    # Simple validation - allows digits, spaces, dashes, parentheses, +
    pattern = r'^[\d\s\-\(\)\+]{7,}$'
    return bool(re.match(pattern, phone))


def paginate_results(items, page, per_page=10):
    """Paginate a list of items.
    
    Args:
        items: List of items to paginate
        page: Current page number
        per_page: Items per page
        
    Returns:
        Tuple of (items for page, total pages)
    """
    total = len(items)
    total_pages = (total + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = start + per_page
    
    return items[start:end], total_pages


def get_relationship_label(member1, member2):
    """Get relationship label between two family members.
    
    Args:
        member1: First family member
        member2: Second family member
        
    Returns:
        Relationship label string
    """
    if member1.father_id == member2.id:
        return "Father"
    elif member1.mother_id == member2.id:
        return "Mother"
    elif member1.spouse_id == member2.id:
        return "Spouse"
    elif member2.father_id == member1.id or member2.mother_id == member1.id:
        return "Child"
    else:
        return "Family Member"


def get_common_ancestors(member1, member2):
    """Find common ancestors between two family members.
    
    Args:
        member1: First family member
        member2: Second family member
        
    Returns:
        List of common ancestors
    """
    def get_ancestors(member):
        ancestors = set()
        if member.father_id:
            ancestors.add(member.father_id)
        if member.mother_id:
            ancestors.add(member.mother_id)
        return ancestors
    
    ancestors1 = get_ancestors(member1)
    ancestors2 = get_ancestors(member2)
    
    return list(ancestors1 & ancestors2)


def log_user_action(action, details=''):
    """Log user action for audit trail.
    
    Args:
        action: Action description
        details: Additional details
    """
    if current_user.is_authenticated:
        log_message = f"User {current_user.username}: {action}"
        if details:
            log_message += f" - {details}"
        current_app.logger.info(log_message)


def send_email_notification(recipient, subject, body):
    """Send email notification.
    
    Args:
        recipient: Recipient email
        subject: Email subject
        body: Email body
        
    Returns:
        Boolean indicating success
    """
    # TODO: Implement email sending
    current_app.logger.info(f"Would send email to {recipient}: {subject}")
    return True


def create_backup(database_path, backup_dir='backups'):
    """Create database backup.
    
    Args:
        database_path: Path to database file
        backup_dir: Backup directory
        
    Returns:
        Path to backup file
    """
    import shutil
    
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"family_tree_backup_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_name)
    
    try:
        shutil.copy2(database_path, backup_path)
        current_app.logger.info(f"Database backup created: {backup_path}")
        return backup_path
    except Exception as e:
        current_app.logger.error(f"Backup failed: {str(e)}")
        return None


def get_storage_usage():
    """Get total storage usage of uploads directory.
    
    Returns:
        Dictionary with storage information
    """
    upload_dir = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
    
    if not os.path.exists(upload_dir):
        return {'total_bytes': 0, 'total_mb': 0, 'file_count': 0}
    
    total_bytes = 0
    file_count = 0
    
    for root, dirs, files in os.walk(upload_dir):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                total_bytes += os.path.getsize(filepath)
                file_count += 1
            except OSError:
                pass
    
    return {
        'total_bytes': total_bytes,
        'total_mb': round(total_bytes / (1024 * 1024), 2),
        'file_count': file_count
    }
